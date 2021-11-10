from flask import Flask, render_template,request,redirect,url_for, Blueprint # For flask implementation
from bs4 import BeautifulSoup
import requests
import pandas as pd

scraping = Blueprint('scraping', __name__,
                        template_folder='templates')

@scraping.route('/', defaults={'page': 'index'})
@scraping.route('/scraping')
def listscraping():
   url='https://mexico.as.com/resultados/futbol/mexico_apertura/clasificacion/'
   page = requests.get(url)
   soup = BeautifulSoup(page.content, 'html.parser')
   
   #Equipos
   #equipos = soup.findall('span', class_='nombre-equipo')
   equipos = soup.findAll("span", attrs={"class": "nombre-equipo"})
   list_equipos = list()
    
   count = 0
   for i in equipos:
       if count < 18:
          list_equipos.append(i.text)
       else:
          break
       count +=1
   #Puntuación
   #puntos = soup.findall('td', class_='destacado')
   puntos = soup.findAll("td", attrs={"class": "destacado"})
   list_puntos = list()

   count = 0
   for i in puntos:
      if count < 18:
          list_puntos.append(i.text)
      else:
          break
      count +=1

   escudos = soup.findAll("span", attrs={"class": "cont-img-escudo"})
   list_escudos = list()
   list_posicion = list()
   count = 0
   for i in escudos:
      if count < 18:
          escudo = i.find('img')['data-src']
          list_escudos.append('https:'+ escudo )
      else:
          break
      count +=1   
      list_posicion.append(count)
   df = pd.DataFrame({'Posición': list_posicion,'Escudo': list_escudos, 'Equipo': list_equipos, 'Puntos': list_puntos}, index=list(range(1,19)))

   #df.to_csv('Clasificación.csv', index=False)
   #df.to_html('listaScraping.html', index=False)
   #lista_json = df.to_json(orient="values")
   temp = df.to_dict('records') 
   columnNames = df.columns.values

   return render_template("scraping.html", records=temp, colnames=columnNames) 
