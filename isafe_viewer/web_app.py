from flask import Flask, render_template, request, jsonify
import os
import time

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        print(request.form)
        time.sleep(5)
        return jsonify(img_url_1='something.jpg', img_url_2='something2.jpg')
    else:
        return render_template('main.html')
