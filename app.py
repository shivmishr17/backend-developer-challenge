from flask import Flask, request, render_template, send_file
from service.give_service import process_data
import pathlib
import os
import pandas as pd

app = Flask(__name__)


@app.route('/get_donations/', methods=['POST'])
def process_csv():
    file = request.files.get('input_file')
    base_currency = request.values.get('base_currency', 'USD')
    if file is None or 'csv' != file.filename.split('.')[-1]:
        return "<h2>Please upload file with correct format</h2>"
    filename = file.filename
    pathlib.Path('uploads').mkdir(exist_ok=True)
    path = os.path.join('uploads', filename)
    file.save(path)
    try:
        data = pd.read_csv(path, names=['Date', 'Order Id', 'Nonprofit', 'Donation Currency', 'Donation Amount', 'Fee'])
        process_data(data, base_currency)
    except Exception as e:
        print(f"Exception occurred: {e}")
        return "<h1>Something went wrong!<h1>"
    finally:
        os.remove(path)
    return render_template('result_page.html')


@app.route('/upload/')
def frontend():
    return render_template('upload.html')


@app.route("/get_csv")
def get_result():
    return send_file(os.path.join('uploads', 'response.csv'), mimetype='text/csv',
                     attachment_filename='Result.csv',
                     as_attachment=True)


if __name__ == '__main__':
    app.run()
