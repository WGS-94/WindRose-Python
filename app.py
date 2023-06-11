# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, session, jsonify, flash, url_for
from decouple import config
import pandas as pd
import time

app = Flask(__name__)

app.secret_key = config('SECRET_KEY')

@app.route('/')
def home():
  # Home Page
  return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate():
  # Your Python script code here
  file = request.files['file']
  if file.filename.endswith('.xlsx'):
    df = pd.read_excel(file)
    # Realize aqui a formatação dos dados conforme necessário
    # Por exemplo, você pode imprimir as colunas e os valores:
    print(df)
    # print(df.columns)
    # print(df.values)
    flash("Upload e formatação concluídos com sucesso!")
    return render_template('success.html')
  else:
    return 'Por favor, faça o upload de um arquivo XLSX.'
  # flash("Data Inserted Successfully")
  # time.sleep(5)

if __name__ == '__main__':
  app.run(debug=True, threaded=True)