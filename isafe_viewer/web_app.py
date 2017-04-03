from populations import get_superpopulations, get_subpopulations

from flask import Flask, render_template, request, jsonify
import os
import time

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
RESULT_FOLDER = os.path.join(APP_ROOT, 'static/results')
app.config['RESULT_FOLDER'] = RESULT_FOLDER


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

            # call a function with the above variable as parameters
            img_url_1 = 'static/results/' + 'freq.png'
            img_url_2 = 'static/results/' + 'iSAFE.png'
            return jsonify(img_url_1=img_url_1, img_url_2=img_url_2, has_errors=False)
        except Exception as exp:
            return jsonify(errors=exp.args, has_errors=True)
    else:
        subpopulations = get_subpopulations()
        superpopulations = get_superpopulations()
        return render_template('main.html', subpopulations=subpopulations, superpopulations=superpopulations)
