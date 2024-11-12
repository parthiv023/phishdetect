import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
import joblib
import numpy as np
import urllib.request
import pandas as pd
import features_extraction
import requests

app = Flask(__name__, template_folder="Extension")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXCEL_FILE'] = 'contact_data.xlsx'
VIRUSTOTAL_API_KEY = '30b89558bec1e76cbc19ddca6d5537316d72c9bd00ec73b823e9b7c8d2592ec9'  

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_prediction_from_url(test_url):
    try:
        features_test = features_extraction.main(test_url)
        features_test = np.array(features_test).reshape((1, -1))

        rf = joblib.load(r"C:\classifierrandom_forest1.pkl")#change path to your requirement

        pred = rf.predict(features_test)
        return int(pred[0])
    except Exception as e:
        print(f"Error in feature extraction: {e}")
        return None

def check_with_virustotal(url):
    try:
        params = {
            'apikey': VIRUSTOTAL_API_KEY,
            'resource': url
        }
        response = requests.get('https://www.virustotal.com/vtapi/v2/url/report', params=params)
        json_response = response.json()

        if json_response['response_code'] == 1:
            if json_response['positives'] == 0:
                return 1  # Safe
            else:
                return -1  # Malicious
        else:
            return None
    except Exception as e:
        print(f"Error in VirusTotal API request: {e}")
        return None

def main(url):
    prediction = get_prediction_from_url(url)
    vt_prediction = check_with_virustotal(url)
    if vt_prediction == 1:
        print("The website is safe to browse")
        return '<body style="background-color:green;"><center style="margin-top:300px; margin-bottom:50px; font-size:36px; color:white; font-weight:bold;">SAFE WEBSITE</center>' \
               '<div><center><a href="' + url + '"><button>Proceed to Website</button></a></div></center></body>'
    elif prediction == -1:
        print("The website has phishing features. DO NOT VISIT!")
        return '<body style="background-color:RED;"><center style="margin-top:300px; margin-bottom:50px; font-size:36px; color:white; font-weight:bold;">PHISHING WEBSITE</center>' \
               '<div><center><button onclick="window.history.back();">Check Again</button></div></center></body>'
    else:
        print("Using VirusTotal API as fallback...")
        vt_prediction = check_with_virustotal(url)
        if vt_prediction == 1:
            return '<body style="background-color:green;"><center style="margin-top:300px; margin-bottom:50px; font-size:36px; color:white; font-weight:bold;">SAFE WEBSITE</center>' \
               '<div><center><a href="' + url + '"><button>Proceed to Website</button></a></div></center></body>'
        elif vt_prediction == -1:
            return '<body style="background-color:RED;"><center style="margin-top:300px; margin-bottom:50px; font-size:36px; color:white; font-weight:bold;">PHISHING WEBSITE</center>' \
               '<div><center><button onclick="window.history.back();">Check Again</button></div></center></body>'
        else:
            return '<body style="background-color: ORANGE;">' \
               '<center style="margin-top: 300px; margin-bottom: 50px; font-size: 36px; color: white; font-weight: bold;">' \
               'LIKELY TO BE PHISHING WEBSITE' \
               '<div style="font-size: 20px; color: white; font-weight: bold; margin-bottom: 20px;">' \
               'Caution: This website shows characteristics similar to phishing sites. ' \
               'Proceed with care and verify its authenticity before entering any personal information.' \
               '</div>' \
               '<center><a href="' + url + '"><button>Proceed to Website</button></a></center>' \
               '</center></body>'
@app.route("/")
def home():
    return render_template("popup.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/check/", methods=['POST'])
def check_url():
    url = request.form.get("url")
    try:
        urllib.request.urlretrieve(url, "markup.txt")
    except Exception as e:
        check_with_virustotal(url)
        

    return main(url)

@app.route("/submit", methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    file = request.files['file']

    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    else:
        filename = None

    # Store data in Excel file
    data = {'Name': [name], 'Email': [email], 'Message': [message], 'File': [filename]}
    df = pd.DataFrame(data)

    if os.path.exists(app.config['EXCEL_FILE']):
        existing_df = pd.read_excel(app.config['EXCEL_FILE'])
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_excel(app.config['EXCEL_FILE'], index=False)

    return redirect(url_for('contact'))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
