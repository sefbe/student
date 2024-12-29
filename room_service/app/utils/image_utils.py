import os
from werkzeug.utils import secure_filename

def save_images(files, upload_folder):
    saved_files = []
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            saved_files.append(filepath)
    return saved_files

