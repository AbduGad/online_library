
from flask import Flask, render_template, request, redirect, url_for, Response
import json
from models import storage
from models.book import Books
from models.tags import Tags
import os
import sys
import requests

available_classes = {
    "Books": Books,
    "tags": Tags,
}

PDF_FOLDER_PATH = "./pdf/"

app = Flask(__name__)


from flask import request, Response, jsonify


@app.route("/add/<item>", methods=["POST"])
def add(item):

    if item not in available_classes:
        return Response("Item not found", status=404)

    cls = available_classes[item]
    data = request.form.to_dict(flat=False)

    if 'pdf' in request.files:
        relative_path, status_code = handle_pdf_upload(request)

        if status_code != 200:
            err = relative_path
            return Response(err, status_code)

    attr_data, att_tags = process_data(data)

    set_relative_path(attr_data, relative_path)

    print(attr_data)

    try:
        instance = create_instance(cls, attr_data, att_tags)
        instance.save()

    except Exception as e:
        return Response(str(e), status=502)

    return Response("Posted successfully", status=200)


def process_data(data):
    if isinstance(data, str):
        data = json.loads(data)
    attrs = {}
    tags = {}

    for key, values in data.items():
        if key != "tags":

            if isinstance(values, list):
                attrs[key] = values[0]
            else:
                attrs[key] = values

    if data.get("tags"):
        tags = {"tags,": data["tags"], }

    return attrs, tags


def create_instance(cls, attr_data, att_tags):
    instance = cls(**attr_data)
    storage.new(instance)
    if att_tags and cls.__name__ == "Books":
        add_tags_to_instance(instance, att_tags)
    return instance


def add_tags_to_instance(instance, att_tags):
    for tag_name in att_tags:
        tag = storage.getBy_name(Tags, tag_name)
        if tag:
            instance.tags.append(tag)


def save_pdf_file(pdf_file):
    # Get the current directory of the application
    current_dir = os.path.dirname(__file__)

    # Navigate up one directory to reach the parent directory
    parent_dir = os.path.dirname(current_dir)

    # Specify the directory where you want to save the PDF files
    pdf_dir = os.path.join(parent_dir, "pdf")

    # Check if the directory exists, if not, create it
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Construct the full path to save the file
    Pdf_saving_path = os.path.join(pdf_dir, pdf_file.filename)

    pdf_file.save(Pdf_saving_path)

    if os.path.exists(f"{Pdf_saving_path}"):

        print("pdf saved successfully!")
        return Pdf_saving_path
    else:
        print("failed to save pdf")
        return None


def get_relative_path(path):

    # Example path

    # Split the path based on the directory separator
    parts = path.split(os.sep)

    # Find the index of "online_library" in the parts list
    index = parts.index("pdf")

    # Reconstruct the path starting from "online_library"
    extracted_path = os.path.join(*parts[index:])

    return extracted_path


def handle_pdf_upload(request) -> str:
    """saves the uploaded PDF file, retrieves the relative path of
    the saved file, and returns the path with a success status code or
    an error message with a failure status code.


    Args:
        request (Request): the given request excepted
        to have a pdf file


    Returns:
        str: the relative path of the saved pdf or
        an error massage if something wrong happened

        int: a status code indicating failure or success:
        200 if success or 500 if failed
    """
    try:
        absolute_path = save_pdf_file(request.files['pdf'])

        if absolute_path is None:
            raise FileExistsError("failed to save the pdf file")

        relative_path_pdf = get_relative_path(absolute_path)
        return (relative_path_pdf, 200)

    except Exception as e:
        return (str(e), 500)


def set_relative_path(data: dict, relative_path: str):
    data["path"] = relative_path


app.run(debug=True, port=5600, host="0.0.0.0")
