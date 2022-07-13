# coding=utf-8
"""
TODO
"""
import json
from os import listdir
import os.path as pathlib

import click
import requests


@click.group()
def main():
    """
    Load information on Dorothy Server
    """
    pass


@main.command(
    help="Load the dataset to the server from a directory. The directory should contain a metadata file following Dorothy's "
         "model and a sub directory named 'images' containing all the images from the dataset."
)
@click.option("-d", "--dataset", type=str, help="Dataset name", required=True)
@click.option("-f", "--folder", type=click.Path(exists=True), help="Dataset folder path", required=True)
@click.option("-t", "--token", type=str, help="Dorothy server auth token", required=True)
@click.option("-h", "--host", show_default=True, type=str, default="http://localhost:80", help="Dorothy server host")
@click.option("-c", "--condition", show_default=False, type=bool, default=False,
              help="Create images first and after register their metadata. (Lazy option)")
def database(dataset, folder, token, host, condition):
    dorothy_host = host
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Token {token}"
        }
    )
    if dorothy_host.endswith("/"):
        dorothy_host = dorothy_host[:-1]
    images_path = pathlib.join(folder, "images")
    metadata_file_path = pathlib.join(folder, "metadata.json")

    image_formats = list(set(
        [file.split(".")[-1] for file in listdir(images_path) if file.split(".")[-1] in ["png", "jpg", "jpeg", "svg"]]
    ))

    print("Image formats found: %s" % image_formats)
    response = session.post(
        url=pathlib.join(dorothy_host, "post_dataset") + "/",
        data={
            "name": dataset,
            "image_formats": image_formats
        }
    )
    print("Create dataset: %s" % response.status_code)
    response.raise_for_status()

    with open(metadata_file_path, mode="r") as metadata:
        content = json.load(metadata)

    print("Finding images..")
    images = [file for file in listdir(images_path) if file.split(".")[-1] in ["png", "jpg", "jpeg", "svg"]]
    for image in images:
        print("Creating image %s" % image)
        image_metadata = {}
        for metadata in content:
            if metadata.get("image_name") == image.split(".")[0]:
                image_metadata = metadata

        response = session.post(
            url=pathlib.join(dorothy_host, "post_image") + "/",
            data={
                "dataset_name": dataset,
                "project_id": "temp"
            },
            files={"image": open(pathlib.join(images_path, image), "rb")}
        )
        print("Create image response: %s" % response.status_code)
        response.raise_for_status()

        project_id = None
        if condition:
            response = session.get(
                url=pathlib.join(dorothy_host, "images"),
                params={"search": dataset}
            )
            response.raise_for_status()
            dataset_images = response.json()
            for element in dataset_images:
                if element.get("project_id", "").find(image.split(".")[0]) >= 0:
                    project_id = element.get("project_id")
        else:
            project_id = response.json().get("project_id")

        image_metadata.update({
            "image": project_id
        })
        image_metadata.pop("image_name")
        print("Creating image metadata")
        response = session.post(
            url=pathlib.join(dorothy_host, "post_metadata") + "/",
            data=image_metadata
        )
        print("Create image metadata response: %s" % response.status_code)
        response.raise_for_status()
