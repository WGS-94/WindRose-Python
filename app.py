# -*- coding: utf-8 -*-
# %matplotlib inline
from flask import Flask, render_template, redirect, request, session, jsonify, flash, url_for
from decouple import config
from matplotlib import pyplot as plt
from math import pi
from io import BytesIO
from windrose import WindroseAxes
import urllib.parse
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import base64
import time
import os
matplotlib.use('agg')

# UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)

app.secret_key = config('SECRET_KEY')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    # print(df)

    # Obtendo o caminho absoluto do diretório atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Imagem 01
    df['velocidad_x'] = df['VelVento'] * np.sin(df['DirVento(°)'] * np.pi / 180.0)
    df['velocidad_y'] = df['VelVento'] * np.cos(df['DirVento(°)'] * np.pi / 180.0)
    fig, ax = plt.subplots(figsize=(8, 8), dpi=80)
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    ax.set_aspect('equal')
    _ = df.plot(kind='scatter', x='velocidad_x', y='velocidad_y', alpha=0.35, ax=ax)
    imagem_01 = 'upload/windrose_01.png'
    plt.savefig(imagem_01)
    caminho_absoluto_01 = os.path.join(diretorio_atual, imagem_01)
    # Convertendo o caminho de diretório para a notação de URL
    url_01 = urllib.parse.quote(imagem_01.replace("\\", "/"))

    # Imagem 02
    fig, ax = plt.subplots()
    ax = WindroseAxes.from_ax()
    ax.bar(df['DirVento(°)'], df['VelVento'], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    imagem_02 = 'upload/windrose_02.png'  
    plt.savefig(imagem_02)
    caminho_absoluto_02 = os.path.join(diretorio_atual, imagem_02)
    # Convertendo o caminho de diretório para a notação de URL
    url_02 = urllib.parse.quote(imagem_02.replace("\\", "/"))

    imagens = [caminho_absoluto_01, caminho_absoluto_02]

    print(imagens)

    # # Imagem 03
    # figure, ax = plt.subplots()
    # ax = WindroseAxes.from_ax()
    # ax.bar(df['DirVento(°)'], df['VelVento'], normed=True, opening=0.8, edgecolor='white', cmap=cm.hot)
    # ax.set_legend()
    # imagem_03 = 'windrose_03.png'

    # # Imagem 04
    # figure, ax = plt.subplots()
    # ax = WindroseAxes.from_ax()
    # ax.box(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1))
    # ax.set_legend()
    # imagem_04 = 'windrose_04.png'

    # # Imagem 05
    # figure, ax = plt.subplots()
    # ax = WindroseAxes.from_ax()
    # ax.contourf(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1), cmap=cm.hot)
    # ax.set_legend()
    # imagem_05 = 'windrose_05.png'

    # # Imagem 06
    # figure, ax = plt.subplots()
    # ax = WindroseAxes.from_ax()
    # ax.contourf(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1), cmap=cm.hot)
    # ax.contour(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1), colors='black')
    # ax.set_legend()
    # imagem_06 = 'windrose_06.png'

    # # Imagem 07
    # figure, ax = plt.subplots()
    # ax = WindroseAxes.from_ax()
    # ax.contour(df['DirVento(°)'], df['VelVento'], bins=np.arange(0, 8, 1), cmap=cm.hot, lw=3)
    # ax.set_legend()
    # imagem_07 = 'windrose_07.png'

    # # Salvar as imagens em um array
    # imagens = [imagem_01, imagem_02, imagem_03, imagem_04, imagem_05, imagem_06, imagem_07]

    flash("Upload e formatação concluídos com sucesso!")

    # Exibir o array de imagens no cliente da aplicação
    return render_template('success.html', imagens=imagens)
  else:
    return 'Por favor, faça o upload de um arquivo XLSX.'

# Exibir o array de imagens no cliente da aplicação
# @app.route('/sucess')
# def sucess():
#     return render_template('sucess.html', imagens=imagens)
# time.sleep(5)

if __name__ == '__main__':
  app.run(debug=True, threaded=True)