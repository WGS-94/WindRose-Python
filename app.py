# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, session, jsonify, flash, url_for
from decouple import config
import os
import time
import datetime
import logging

app = Flask(__name__)

app.secret_key = config('SECRET_KEY')

@app.route('/')
def home():
  # logging.debug('INÍCIO DO PROGRAMA')
  # Home Page
  return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate():
  # Your Python script code here

  flash("Data Inserted Successfully")
  time.sleep(5)

  return render_template('success.html')

if __name__ == '__main__':
  app.run(debug=True, threaded=True)