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
        time.sleep(2)
        try:
            populations = []
            for key, value in request.form.items():
                if key == 'populations[]':
                    populations.append(value)
            if len(populations) == 0:
                raise Exception('Error: Please choose at least one population')

            selected_radio = request.form['selectedRadio']
            if selected_radio == 'position':
                position = request.form['position']
                if position == '':
                    raise Exception('Error: Please specify chromosome region')
            elif selected_radio == 'geneName':
                gene_name = request.form['geneName']
                if gene_name == '':
                    raise Exception('Error: Please specify gene name')
            else:
                rsid = request.form['rsid']
                if rsid == '':
                    raise Exception('Error: Please specify rsid')

            if request.form['regionSize'] == '' or not request.form['regionSize'].isdigit():
                raise Exception('Error: Please specify region size')
            region_size = int(request.form['regionSize'])

            use_random_samples = False
            number_of_random_samples = 0
            random_sample_population = None
            if request.form['useRandomSample'] == 'true':
                use_random_samples = True
                if not request.form['numberOfRandomSamples'].isdigit():
                    raise Exception('Error: Please specify the number of random samples')
                number_of_random_samples = int(request.form['numberOfRandomSamples'])
                random_sample_population = request.form['randomSamplePopulations']

            return jsonify(img_url_1='something.jpg', img_url_2='something2.jpg', has_errors=False)
        except Exception as exp:
            return jsonify(errors=exp.args, has_errors=True)
    else:
        return render_template('main.html')
