from app.file import file
from flask import send_from_directory, current_app, request, jsonify
from app.model.response import OK
import os
import uuid
from app.setting import HOST
from datetime import datetime



def random_filename(filename):
    extension = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + extension
    return new_filename


@file.route("/upload", methods=["POST"])
def fileUpload():
    file = request.files.get("file")
    if file is not None:
        file.filename = random_filename(str(datetime.now().timestamp()) + os.path.splitext(file.filename)[1])
        file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
    return jsonify(OK(
        url="http://" + HOST + "/file/download/" + file.filename,
        filename=file.filename
    ))


@file.route("/download/<path:filename>")
def fileDownload(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename, as_attachment=True)