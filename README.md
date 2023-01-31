# metadata_pdf
Flask app for reading, extracting metadata of PDF files


# Installation 
1. Clone the repository:
git clone https://github.com/zlicin/metadata_pdf.git
2. Install the required packages: pip install -r requirements.txt


# Usage
The Flask application can be used through the user-friendly interface provided by the application.<br/>The application will be accessible at http://localhost:5000/ after running the flask run command.<br/><br/>
Availabe API:<br/>
POST&emsp;&emsp;&emsp;&emsp;/documents&emsp;&emsp;&emsp;&emsp;upload a new PDF file, responds a document ID<br/>
GET&emsp;&emsp;&ensp;&emsp;&emsp;/documents/<id>&emsp;&emsp;&emsp;&emsp;return its metadata<br/>
GET&emsp;&emsp;&emsp;&emsp;&ensp;/text/<id>.txt&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;return its raw text
