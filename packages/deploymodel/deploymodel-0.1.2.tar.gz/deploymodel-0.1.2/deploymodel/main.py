import json
from pathlib import Path
import os
import urllib.parse
import tempfile
from typing import Annotated
import requests
from tqdm import tqdm
from loguru import logger
import diskcache
import docker
import typer
from deploymodel.settings import API_HOST
from deploymodel.serverless.register import get_module_and_handler, get_remote_env_var

app = typer.Typer()
assert API_HOST is not None, "API_HOST environment variable is not set"

CACHE = diskcache.Cache("/tmp/deploymodel", timeout=3600 * 24)


def get_uploaded_size(session_uri):
    """Check how much has been uploaded to resume correctly."""
    headers = {"Content-Range": "bytes */*"}  # Asking for the current status
    response = requests.put(session_uri, headers=headers)
    if response.status_code == 308:  # Resume Incomplete
        range_header = response.headers.get("Range")
        if range_header:
            bytes_uploaded = int(range_header.split("-")[1]) + 1
            return bytes_uploaded
    return 0


def upload_chunk(session_uri, file_path, start_position, chunk_size, total_size):
    """Upload a single chunk."""
    end_position = start_position + chunk_size - 1
    headers = {"Content-Range": f"bytes {start_position}-{end_position}/{total_size}"}

    with open(file_path, "rb") as f:
        f.seek(start_position)
        data = f.read(chunk_size)
        response = requests.put(session_uri, headers=headers, data=data)
        return response


def upload_file_in_chunks(session_uri, file_path, chunk_size=26214400):
    """Upload a file in chunks and resume if interrupted."""
    file_size = os.path.getsize(file_path)
    start_position = get_uploaded_size(session_uri)

    # Calculate the number of chunks
    total_chunks = (file_size - start_position + chunk_size - 1) // chunk_size
    logger.debug(f"Resuming at {start_position} bytes for {total_chunks} chunks")
    # Iterate over the file in chunks with a for loop
    for i in tqdm(range(total_chunks), desc="Uploading"):
        current_position = start_position + i * chunk_size
        current_chunk_size = min(chunk_size, file_size - current_position)

        response = upload_chunk(
            session_uri, file_path, current_position, current_chunk_size, file_size
        )
        response.raise_for_status()

        if response.status_code in (200, 201):
            logger.info(f"Upload complete after {total_chunks} chunks.")
            break
        elif response.status_code == 308:
            continue


def get_openapi_specs(image: docker.models.images.Image):
    client = docker.from_env()
    logger.debug("Image loaded successfully")
    out = client.containers.run(
        image.tags[0],
        command="python openapi.py",
        remove=True,
        stdout=True,
        stderr=True,
    )
    openapi = out.decode().strip()
    logger.debug("Generated API specs")
    openapi = json.loads(openapi)
    logger.debug("API specs parsed successfully")
    return openapi


def get_session_uri(url):
    headers = {"x-goog-resumable": "start", "Content-Type": "application/octet-stream"}
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    session_uri = response.headers["Location"]
    return session_uri


@app.command()
def build():
    # should check that modelRequest / ModelRequest is in the expected deploymodel.py
    raise NotImplementedError("Not implemented yet")


def build_docker_image(
    dockerfile: Path, token: str, nocache: bool = False
) -> docker.models.images.Image:
    client = docker.from_env()
    context = Path(dockerfile).parent

    logger.info(f"Building Docker image from {context}")
    image, build_logs = client.images.build(
        path=str(context),
        tag=token,
        rm=True,
        quiet=False,
        nocache=nocache,
    )
    for line in build_logs:
        stream = line.pop("stream", "").strip()
        if stream:
            logger.info(stream)
        if line:
            logger.debug(line)

    logger.debug("Docker image built successfully")
    module, handler = get_module_and_handler(client, image)
    pythonpath_env = get_remote_env_var(client, image, "PYTHONPATH")
    if not pythonpath_env:
        raise ValueError(
            "PYTHONPATH environment variable not found in the image, please set it in the Dockerfile, using\nPYTHONPATH='<some-path>"
        )
    logger.info(f"Handler {module}:{handler} registered successfully")
    return image


@app.command()
def push(
    token: str,
    dockerfile: Annotated[Path, typer.Option("--input", "-i")],
    nocache: bool = typer.Option(False, "--no-cache", "-nc"),
):
    url = urllib.parse.urljoin(API_HOST, "/api/v1/version/signed-url")

    if url in CACHE:
        logger.info("Resuming upload.")
        session_uri, image_path = CACHE[url]
    else:
        logger.info("Starting new upload.")
        logger.info("Building Docker image.")
        image = build_docker_image(dockerfile, token, nocache)

        with tempfile.NamedTemporaryFile(delete=False, prefix="dm-build-") as f:
            for chunk in image.save():
                f.write(chunk)
            f.flush()
            image_path = f.name

        logger.debug(f"Image TAR saved locally to {image_path}")
        logger.info("Docker image built successfully.")
        signed_urls_res = requests.get(url, params={"token": token})
        signed_urls_res.raise_for_status()
        signed_urls = signed_urls_res.json()

        url_openapi = signed_urls["openapi"]
        logger.info("Signed URLs fetched.")

        logger.info("Generating API specs.")
        openapi = get_openapi_specs(image)
        logger.info("API specs generated successfully.")

        with tempfile.NamedTemporaryFile(mode="w") as f:
            json.dump(openapi, f)
            f.flush()
            openapi_path = f.name
            session_openapi_uri = get_session_uri(url_openapi)
            upload_file_in_chunks(session_openapi_uri, openapi_path)
        logger.info("API specs uploaded.")

        url_image = signed_urls["image"]
        session_uri = get_session_uri(url_image)

        CACHE[url] = (session_uri, image_path)
    upload_file_in_chunks(session_uri, image_path)
    logger.info("Upload complete.")
    logger.debug(f"Cleaning up {image_path}.")
    os.remove(image_path)
    logger.debug("Cleaning up complete.")


if __name__ == "__main__":
    app()
