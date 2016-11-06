from django.shortcuts import render #importamos render de django
import requests
import urllib2
import json
import demjson
import time
import os
from django.http import HttpResponse
from lxml import etree
# Create your views here.
 
def generatePath():
	path = int(round(time.time() * 1000))
	path = str(path) +".xml"
	print path
	return path

def deleteXML(path):
	os.remove(path)
	
def getXML(path): 
	url = 'http://www.pamplona.es/xml/parkings.xml'
	response = urllib2.urlopen(url)
	html = response.read()
	file = open(path, 'wb')
	file.write(html)
	file.close()
	
def parsearXML(path):
	tree = etree.parse(path)
	root = tree.getroot()
	parkings_array = root.findall('APARCAMIENTO')
	parkings_json=[]
	for parking in parkings_array:
		parking_json=[]
		parking_json=getJSONFromParking(parking)
		parkings_json.append(parking_json)
	return parkings_json

def getJSONFromParking(parking):
	parking_json= []
	print parking
	estado=''
	codigo = parking.find('CODIGO').text
	latitud = parking.find('LATITUD').text
	longitud = parking.find('LONGITUD').text
	nombre = parking.find('NOMBRE_CORTO').text
	#OBTENEMOS LOS VALORES DE OCUPADO Y TOTAL
	plazas = parking.find('PLAZAS')
	total = plazas.find('TOTAL').text
	libre = plazas.find('LIBRES').text
#COMPROBAMOS QUE SEA NUMERICO, PUEDE ENVIAR DATOS FALSOS	
	if libre.isdigit() is False or total.isdigit() is False: 
		libre=1
		total=1
		
	porc = float(libre)/float(total) *100
	porcentaje_String = str(int(porc)) + "%"
	if porc < 33 :
		estado = 'bajo'
	if porc > 34 and porc < 66:
	   	estado = 'medio'
	if porc > 67 :
		estado = 'alto'
	parking_json.append({'total' : total , 'libres' : libre , 'codigo' : codigo, 'latitud' : latitud, 'longitud' : longitud, 'nombre' : nombre , 'porcentaje':porcentaje_String, 'estado' : estado })	
	return parking_json
	
def webapp(request):
#GENERAMOS EL PATH
	fileName=generatePath()
	return_json = []
#OBTENEMOS EL FICHERO DESDE LA URL
	getXML(fileName)
#TENEMOS EL FICHERO. LO PARSEAMOS
	return_json=parsearXML(fileName)
#CODIFICAMOS EN JSON LOS DATOS A DEVOLVER
	json_return = demjson.encode(return_json)
	print(json_return)
#ELIMINAMOS EL FICHERO XML DEL FILESYSTEM	
	deleteXML(fileName)
	return HttpResponse(json_return, content_type="application/json")

