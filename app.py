import os
from flask import Flask, request, url_for, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST', 'PUT'])
def upload_file():
    if request.method in ('POST', 'PUT'):
        if len(request.files) != 0:
            f = request.files['file']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            return url_for('uploaded_file',
                           filename=f.filename)
        else:
            f = open(os.path.join(app.config['UPLOAD_FOLDER'], 'file'), 'wb')
            f.write(request.data)
            f.close()
            return url_for('uploaded_file',
                           filename='file')


@app.route('/files/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def create_upload_folder():
    try:
        os.makedirs(UPLOAD_FOLDER)
    except:
        pass


if __name__ == '__main__':
    create_upload_folder()
    app.run(host='0.0.0.0', port=8881)
