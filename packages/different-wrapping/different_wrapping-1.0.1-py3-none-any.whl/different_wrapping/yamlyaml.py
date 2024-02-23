# Responsible for converting the docker-compose style manifests to a k8s kustomize project
import tempfile
import shutil
import subprocess
from pathlib import Path

import yaml

import logging

logger = logging.getLogger(__name__)


def tempdir():
    """Debugging purposes"""
    import uuid

    directory = Path("/tmp") / str(uuid.uuid4())
    directory.mkdir(parents=True)
    return directory


def build_challenge_kustomize(files, out_file):
    """Builds the kustomize manifest for a challenge"""
    logger.info("Building for %s" % files)
    manifest = {
        "apiVersion": "kustomize.config.k8s.io/v1beta1",
        "kind": "Kustomization",
        "resources": [f.name for f in files],
    }

    with out_file.open("w") as f:
        yaml.dump(manifest, f)


def bulid_kustomize_manifest(challenges, folder, filter):
    """Builds the topmost kustomize manifest which includes all challenges"""
    manifest = {
        "apiVersion": "kustomize.config.k8s.io/v1beta1",
        "kind": "Kustomization",
        "resources": ["./%s" % challenge.key() for challenge in challenges],
    }

    out_file = folder / Path("kustomization.yml")

    with out_file.open("w") as f:
        yaml.dump(manifest, f)


def build_k8s_manifests(challenge, output, filter_lambda, args):
    """Builds k8s manifests to a given base directory(organized by challenge type).
    selector_lambda allows filtering of what containers to use"""
    logger.info("Processing %s" % challenge.key())

    # with tempfile.TemporaryFile() as compose_file:
    # with tempfile.TemporaryDirectory() as workdir:
    workdir = Path(tempdir())

    service_dict = {
        key: value.container_dict
        for key, value in filter(filter_lambda, challenge.containers.items())
    }
    if len(service_dict.keys()) == 0:
        logger.info(
            "Challenge %s has no services valid for %s - skipping"
            % (challenge.key(), str(output))
        )
        return

    compose_file = workdir / "docker-compose.yml"

    logger.info("Writing to %s" % compose_file)
    compose_data = {"version": "3", "services": service_dict}
    with compose_file.open("w") as f:
        yaml.dump(compose_data, f)

    kompose_args = ["kompose", "-f", "docker-compose.yml", "convert"]

    result = subprocess.run(kompose_args, cwd=workdir, capture_output=True)

    if result.returncode != 0:
        logger.error("Failed to run kompose! stderr: \n%s" % result.stderr)

    logger.info(
        "Kompose returned %d\nstdout %s\nstderr %s"
        % (result.returncode, result.stdout, result.stderr)
    )

    # Generate ingress
    generate_challenge_ingresses(challenge, workdir, args.dns_host)

    # Manifest files to be copied
    files = list(
        filter(lambda file: not ("docker-compose" in file.name), workdir.iterdir())
    )
    logger.info("Files: %s" % len(files))
    if not args.dry:
        # Create the output folder
        output_dir = output / Path(challenge.key())
        output_dir.mkdir(parents=True, exist_ok=True)

        # Build kustomize file
        kustomize_file = output_dir / Path("kustomization.yml")
        build_challenge_kustomize(files, kustomize_file)

        # Copy over files
        for file in files:
            dest = output_dir / Path(file.name)
            logger.debug("%s -> %s" % (file, dest))
            shutil.copyfile(file, dest)

        logger.debug("Done copying files")


def get_external_port(port):
    # Extracts external ports from a docker port string
    # See https://docs.docker.com/compose/compose-file/compose-file-v3/#ports
    if isinstance(port, int):
        return port
    components = port.split(":")
    if len(components) == 1:
        return components[0]
    elif len(components) == 2:
        return components[0]
    elif len(components) == 3:
        return components[1]
    else:
        raise RuntimeError("Unable to parse external port")


def generate_ingress(service_name, service, challenge, dns_host):
    # First we need to determine the port that the ingress is supposed to be pointed towards
    if "ports" not in service.container_dict:
        raise RuntimeError(
            f"Tried to create ingress for {service_name} but it has no ports exposed(and therefore no k8s service to point to)"
        )

    external_ports = [
        get_external_port(port) for port in service.container_dict["ports"]
    ]

    if len(external_ports) == 0:
        raise RuntimeError(
            f"Unable to create ingress for {service_name} as there are no ports"
        )
    elif len(external_ports) > 1:
        raise RuntimeError(
            f"Unable to determine external port for {service_name} as there are more than one ports exposed"
        )

    # Determine DNS name
    host = service.get_dns_name(dns_host)

    return {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": f"ingress-{challenge.name()}-{service_name}",
        },
        "spec": {
            "ingressClassName": "TODO",
            "rules": [
                {
                    "host": host,
                    "http": {
                        "paths": [
                            {
                                "path": "/",
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {
                                        "name": service_name,
                                        "port": {"number": int(external_ports[0])},
                                    }
                                },
                            }
                        ]
                    },
                }
            ],
        },
    }


def generate_challenge_ingresses(challenge, outdir, dns_host):
    outfile = outdir / "different-wrapping-ingress.yaml"

    ingresses = []

    for service_name, service in challenge.containers.items():
        logger.debug(service_name)
        if service.has_label("no.cyberlandslaget.http"):
            logger.info("Container has http label, creating ingress")
            ingresses.append(
                generate_ingress(service_name, service, challenge, dns_host)
            )
        else:
            logger.info("Container has no ingress requirement")

    if len(ingresses) > 0:
        with outfile.open("w") as f:
            f.write("\n---\n".join([yaml.dump(ingress) for ingress in ingresses]))
