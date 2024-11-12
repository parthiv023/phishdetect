# phishdetect
Welcome to the Phishing Website Detection Web Application! This application helps you identify whether a website is safe to visit or potentially a phishing attempt. Using a combination of machine learning and VirusTotal's API, we provide real-time predictions for URLs you submit.

## Features
- **Phishing Detection**: Uses a trained Random Forest Classifier to identify phishing websites based on various extracted features from URLs.
- **VirusTotal Integration**: Leverages the VirusTotal API to cross-check the safety of URLs.
- **File Upload**: Allows users to submit files alongside their contact information.
- **Contact Form**: Collects user contact details and feedback.

## Technologies Used
- **Flask**: A lightweight Python web framework used to build the application.
- **Machine Learning**: Random Forest Classifier for phishing detection based on URL features.
- **Pandas**: For handling data and saving the contact information in Excel files.
- **Requests**: Used to make HTTP requests to the VirusTotal API for URL safety checks.
- **HTML/CSS**: For creating interactive and attractive frontend pages.
- **Joblib**: For loading the pre-trained machine learning model.

## Setup Instructions

### Prerequisites
To run this project, you need:
- Python 3.x
- Flask
- Pandas
- Scikit-learn
- Requests

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/phishing-website-detection.git
   cd phishing-website-detection
Install the required dependencies:
pip install -r requirements.txt

Set up your VirusTotal API Key in the VIRUSTOTAL_API_KEY variable. You can obtain an API key by signing up for free on the VirusTotal website.
Ensure the machine learning model classifierrandom_forest1.pkl is saved on your local system, or train a new model if necessary.

Usage
Homepage: Users can enter a URL to check its safety.
About Page: Learn more about the application and how it works.
Contact Page: Submit contact details and feedback, with an option to upload files.
Flow of URL Check
User Input: User submits a URL on the homepage.
Phishing Detection: The system first checks the URL using a pre-trained machine learning model.
VirusTotal Check: If the model is unsure, it falls back to VirusTotal API to verify if the URL is safe.
Result: Users receive a result page that indicates whether the URL is safe, malicious, or suspicious.

Acknowledgments
Flask: A web framework that makes building web applications easy.
Scikit-learn: For providing the machine learning tools.
VirusTotal API: For providing an additional layer of security checks.
