from flask import Flask, render_template, request, redirect, url_for, Response
import json
from models import storage
from models.book import Books
from models.tags import Tags

available_classes = {
    "Books": Books,
    "tags": Tags,
}

app = Flask(__name__)


from flask import request, Response, jsonify


@app.route("/add/<item>", methods=["POST"])
def add(item):
    if item not in available_classes:
        return Response("Item not found", status=404)

    cls = available_classes[item]
    data = request.get_json()
    attr_data, att_tags = process_data(data)

    try:
        instance = create_instance(cls, attr_data, att_tags)
        instance.save()
    except Exception as e:
        return Response(str(e), status=500)

    return Response("Posted successfully", status=200)


def process_data(data):
    attr_data = data.get("attr")
    att_tags = data.get("tags")
    return attr_data, att_tags


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


app.run(debug=True, port=5600, host="0.0.0.0")
