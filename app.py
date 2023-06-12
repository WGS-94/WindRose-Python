# -*- coding: utf-8 -*-
# %matplotlib inline
from flask import Flask, render_template, redirect, request, session, jsonify, flash, url_for
from decouple import config
from matplotlib import pyplot as plt
from math import pi
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import base64
import time

app = Flask(__name__)

app.secret_key = config('SECRET_KEY')

@app.route('/')
def home():
  # Home Page
  return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate(figure):
  # Your Python script code here
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)
  imagem_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
  return imagem_base64

file = request.files['file']
if file.filename.endswith('.xlsx'):
  df = pd.read_excel(file)
  # Realize aqui a formatação dos dados conforme necessário
  print(df)

  # Imagem 01
  df['velocidad_x'] = df['VelVento'] * np.sin(df['DirVento(°)'] * np.pi / 180.0)
  df['velocidad_y'] = df['VelVento'] * np.cos(df['DirVento(°)'] * np.pi / 180.0)
  fig, ax = plt.subplots(figsize=(8, 8), dpi=80)
  x0, x1 = ax.get_xlim()
  y0, y1 = ax.get_ylim()
  ax.set_aspect('equal')
  _ = df.plot(kind='scatter', x='velocidad_x', y='velocidad_y', alpha=0.35, ax=ax)
  imagem_01 = generate(fig)

  # Imagem 02
  fig, ax = plt.subplots()
  ax = WindroseAxes.from_ax()
  ax.bar(df['DirVento(°)'], df['VelVento'], normed=True, opening=0.8, edgecolor='white')
  ax.set_legend()
  imagem_02 = generate(fig)

  # Imagem 03
  fig, ax = plt.subplots()
  ax = WindroseAxes.from_ax()
  ax.bar(df['DirVento(°)'], df['VelVento'], normed=True, opening=0.8, edgecolor='white', cmap=cm.hot)
  ax.set_legend()
  imagem_03 = generate(fig)

  # Imagem 04
  fig, ax = plt.subplots()
  ax = WindroseAxes.from_ax()
  ax.box(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1))
  ax.set_legend()
  imagem_04 = generate(fig)

  # Imagem 05
  fig, ax = plt.subplots()
  ax = WindroseAxes.from_ax()
  ax.contourf(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1), cmap=cm.hot)
  ax.set_legend()
  imagem_05 = generate(fig)

  # Imagem 06
  fig, ax = plt.subplots()
  ax = WindroseAxes.from_ax()
  ax.contourf(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1), cmap=cm.hot)
  ax.contour(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1), colors='black')
  ax.set_legend()
  imagem_06 = generate(fig)

  # Imagem 07
  fig, ax = plt.subplots()
  ax = WindroseAxes.from_ax()
  ax.contour(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1), cmap=cm.hot, lw=3)
  ax.set_legend()
  imagem_07 = generate(fig)

  # Salvar as imagens em um array
  imagens = [imagem_01, imagem_02, imagem_03, imagem_04, imagem_05, imagem_06, imagem_07]

  # Exibir o array de imagens no cliente da aplicação

  flash("Upload e formatação concluídos com sucesso!")
  return render_template('success.html', imagens=imagens)
else:
  return 'Por favor, faça o upload de um arquivo XLSX.'
# flash("Data Inserted Successfully")
# time.sleep(5)

if __name__ == '__main__':
  app.run(debug=True, threaded=True)