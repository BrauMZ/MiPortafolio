from flask import Flask, render_template, request, redirect, Blueprint
import requests
import bson
import json
import pandas as pd
from bs4 import BeautifulSoup
from forms.forms import ContactForm
from forms.crud import crud
from forms.scraping import scraping


app = Flask(__name__)
app.register_blueprint(crud)
app.register_blueprint(scraping)
app.secret_key = 'secretKey'

@app.route('/')

def template():
    return render_template("index.html")

@app.route('/download')
def download():
    return render_template("cv_pdf.html")

@app.route('/api_request')
def api_request():
    dataRequest = requests.get('https://api.dailymotion.com/videos?channel=sport&limit=12')
    dataInJSON = dataRequest.json()
    #print(dataInJSON)
    return render_template("api_request.html", datos=dataInJSON['list'])

@app.route('/scraping')
def scraping():
    return render_template("scraping.html")

@app.route('/portfolio1')
def portfolio1():
    return render_template("portfolio1.html") 
@app.route('/portfolio2')
def portfolio2():
    return render_template("portfolio2.html") 
@app.route('/portfolio3')
def portfolio3():
    return render_template("portfolio3.html") 
@app.route('/portfolio4')
def portfolio4():
    return render_template("portfolio4.html") 
@app.route('/portfolio5')
def portfolio5():
    return render_template("portfolio5.html") 
@app.route('/portfolio6')
def portfolio6():
    return render_template("portfolio6.html")                     

@app.route('/underconstruction')
def underconstruction():
    return render_template("underconstruction.html")       

@app.route('/crud')
def crud():
    return render_template("crud.html")
    
@app.route('/contact', methods=["GET","POST"])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        name =  request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        subject = request.form["subject"]
        message = request.form["message"]
        res = pd.DataFrame({'name':name, 'email':email, 'phone':phone ,'subject':subject ,'message':message}, index=[0])
        res.to_csv('./contactos.csv')
        print("Registro Guardado !")
    else:
        return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)