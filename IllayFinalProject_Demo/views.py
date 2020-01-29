
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from IllayFinalProject_Demo import app
from IllayFinalProject_Demo.models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from IllayFinalProject_Demo.models.QueryFormStructure import QueryFormStructure 
from IllayFinalProject_Demo.models.QueryFormStructure import LoginFormStructure 
from IllayFinalProject_Demo.models.QueryFormStructure import UserRegistrationFormStructure 

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/photoalbum')
def photoalbum():
    """Renders the about page."""
    return render_template(
        'photoalbum.html',
        title='Photo Album',
        year=datetime.now().year,
        message='Welcome to my Photo Album'
    )


@app.route('/query', methods=['GET', 'POST'])
def query():

    Name = None
    Country = ''
    capital = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\capitals.csv'))
    df = df.set_index('Country')

    form = QueryFormStructure(request.form)
     
    if (request.method == 'POST' ):
        name = form.name.data
        Country = name
        if (name in df.index):
            capital = df.loc[name,'Capital']
        else:
            capital = name + ', no such country'
        form.name.data = ''

   ## df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\users.csv'))

    raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template('query.html', 
            form = form, 
            name = capital, 
            Country = Country,
            raw_data_table = raw_data_table,
            title='Query by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input'
        )

# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('photoalbum')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )


