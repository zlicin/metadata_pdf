from flask import Flask, request, render_template, jsonify
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
import uuid
from io import StringIO
from PyPDF2 import PdfReader
import json
import sqlite3
import unittest
import os


my_app = Flask(__name__)
conn = sqlite3.connect('pdf_metadata.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS pdf_metadata(id TEXT PRIMARY KEY, metadata TEXT, text TEXT)')


@my_app.route('/')
def home():
    return render_template("homepage.html")


@my_app.route('/documents/', methods=['GET', 'POST'])
def pdf_processing():
    if request.method == 'POST':
        file = request.files['myfile']
        file_name = file.filename
        file_size = file.content_length
        file_type = file.content_type
        extension = file_name.split(".")[-1]

        if file_type != 'application/pdf' or extension != 'pdf':
            return f'Error: The file must be a PDF<br>' \
                   f'File type: {file_type.split("/")[-1]}<br>'
        if file_size > 5 * 1024 * 1024:
            return f'Error: The file size must be less than 5MB<br>' \
                   f'File size: {file_size}<br>'

        uid = str(uuid.uuid4())
        uid_ext = uid + '.' + extension

        file_path_dir = './uploaded_pdf/'
        file_path = file_path_dir + uid_ext
        isExist = os.path.exists(file_path_dir)
        if not isExist:
            os.makedirs(file_path_dir)
        file.save(file_path)

        pdf_reader = PdfReader(file)
        metadata = str(pdf_reader.metadata)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        cursor.execute('INSERT INTO pdf_metadata (id, metadata, text) '
                       'VALUES (?, ?, ?)', (uid, metadata, text))
        conn.commit()
        #conn.close()

        return render_template("upload_ok.html",
                               metadata = metadata, uid = uid, file_name = file_name,
                               file_size = file_size, file_type = file_type,
                               extension = extension, text = text)
    return render_template('pdf_processing.html')


@my_app.route('/documents/<document_id>')
def return_documents(document_id):
    cursor.execute('SELECT * FROM pdf_metadata WHERE id=?', (document_id,))
    metadata = cursor.fetchone()
    if metadata is None:
        return render_template('return_doc_nok.html')
    else:
        return render_template('return_doc_ok.html', metadata=metadata)


@my_app.route('/text/<document_id>.txt')
def extract_text(document_id):
    cursor.execute('SELECT * FROM pdf_metadata WHERE id=?', (document_id,))
    metadata = cursor.fetchone()
    if metadata is None:
        return render_template('ext_text_nok.html')
    else:
        return render_template('ext_text_ok.html', metadata=metadata)


if __name__ == '__main__':
    my_app.run(debug=True)