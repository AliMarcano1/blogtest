import os
from flask import Flask,session 
from flask import request
from . import publicaciones
#import de las querys de los posts
from . import querys
from app.users import routes
import json
import uuid
from datetime import datetime
import pytest
#los endpoint para los post

#todos los post
@publicaciones.route('/publicaciones/all')
def index():
	try:
		post = querys.obtener_publicaciones()
		return json.dumps({"error":"False","post":post,"status":200})
	except:
		return json.dumps({"error":"True","message":"error search"})
	
#devuelve un post en espesifico
@publicaciones.route('/publicaciones/post/<id>')
def search(id):
	try:
		post = querys.obtener_publicacion(id)
	except:
		return json.dumps({"error":"True","message":"error search"})
	if post:
		return json.dumps({"error":"False","post":post,"status":200})
	else:
		return json.dumps({"error":"True","message":"post dont exist"})

#crea los post
@publicaciones.route('/publicaciones/create/',methods=['POST'])
def create_post():
	try:
		tittle = request.form['tittle']
		description = request.form['description']
		priority = request.form['priority']
		status = request.form['status']
		#si el usuario no esta la data enviada toma al usuario que tiene iniciada la session
		if not 'user' in request.form:
			if not 'userid' in session:
				return json.dumps({"error":True,"message":"error not user in data","status":401})
			user = session['userid']
		else:
			user = request.form['user']
	except:
		return json.dumps({"error":True,"message":"error read data","status":401})
	
	#si la query falla no entra y le pasamos el id del usuario que tiene la session iniciada como el creador del post
	if querys.crear_publicaciones_usuario(tittle,description,priority,status,user):
		return json.dumps({"status":200,"error":False,"message":"Post Created"})
	return json.dumps({"error":True,"message":"error creating post","status":401})	

#edit de los post asumo que no se puede cambiar el usuario que creo la publicacion
@publicaciones.route('/publicaciones/edit/<id>',methods=['POST'])
def edit_post(id):
	try:
		tittle = request.form['tittle']
		description = request.form['description']
		priority = request.form['priority']
		status = request.form['status']
	except:
		return json.dumps({"error":True,"message":"error read data","status":401})
	#verifica la existencia del post antes de intentar editarlo
	ex_post = querys.obtener_publicacion(id)	
	if not ex_post:
		return json.dumps({"error":True,"message":"error post not exist","status":401})

	if querys.update_post(id,tittle,description,priority,status):
		return json.dumps({"status":200,"error":False,"message":"Post updated"})

	return json.dumps({"error":True,"message":"error updating post","status":401})	

@publicaciones.route('/publicaciones/delete/<id>',methods=["POST"])
def delete_publicacion(id):
	#verifica la existencia del post
	ex_post = querys.obtener_publicacion(id)	
	if not ex_post:
		return json.dumps({"error":True,"message":"error post not exist","status":401})
	#borra el post
	if querys.delete_publicaciones_usuario(id):
		return json.dumps({"error":"False","message":"post deleted","status":200})
	else:
		return json.dumps({"error":"True","message":"error deleted post","status":401})

@publicaciones.route('/publicaciones/search/',methods=["POST"])
def multisearch():
	#no coloco el id porque si se va a buscar el id para eso que se use el search simple de arriba 
	#igual para el caso de todo los post
	
	#declaro el inicio de la query ya que este no varia
	stringquery = "SELECT * FROM post WHERE"
	anterior = 0 #esta vandera me ayudara a saber si bo agregar AND o no en la query dependiendo
	#de si ya existe en la query un parametro de busqueda
	if 'tittle' in request.form:
		anterior = 1
		stringquery= stringquery+" tittle='"+request.form['tittle']+"'"
		#aqui no hace falta poner un condicional ya que en casod e que este siempre sera el primero en colocarse
	if 'description' in request.form:
		if anterior ==0 :
			stringquery= stringquery+" description='"+request.form['description']+"'"
			anterior=1
		else:
			stringquery= stringquery+" AND description='"+request.form['description']+"'"
	if 'priority' in request.form:
		if anterior==0:
			stringquery= stringquery+" priority="+str(request.form['priority'])
			anterior=1
		else:
			stringquery= stringquery+" AND priority="+str(request.form['priority'])
	if 'status' in request.form:
		if anterior == 0:
			anterior=1
			stringquery= stringquery+" status="+str(request.form['status'])
		else:
			stringquery= stringquery+" AND status="+str(request.form['status'])
	
	if 'user' in request.form:
		if anterior == 0:
			anterior=1
			stringquery= stringquery+" user="+str(request.form['user'])
		else:
			stringquery= stringquery+" AND user="+str(request.form['user'])
	#seria copiar y pegar lo mismo si sequiere para las fechas de update
	if 'fecha' in request.form:
		print(request.form['fecha'])
		#para obtener post por su fecha de creacion un rango
		if 'fecha2' in request.form:
			if anterior== 0:
				stringquery= stringquery+" CAST(create_at AS DATE) BETWEEN  CAST('"+request.form['fecha']+"' AND CAST('"+request.form['fecha2']+"' AS DATE)"
			else:
				stringquery= stringquery+" AND CAST(create_at AS DATE) BETWEEN  CAST('"+request.form['fecha']+"' AS DATE) AND CAST('"+request.form['fecha2']+"' AS DATE)"
		else:
			# qui seria para la fehca exacta
			if anterior == 0:
				stringquery= stringquery+" CAST(create_at AS DATE)=CAST('"+request.form['fecha']+"' AS DATE)"
			else:
				stringquery= stringquery+" AND CAST(create_at AS DATE)=CAST('"+request.form['fecha']+"' AS DATE)"
	try:
	#aqui le paso la consulta ya construida al cursor para que me devuelva el resultado
		post = querys.multisearch(stringquery)
	except:
		return json.dumps({"error":"True","message":"error search"})
	
	if not post:
		return json.dumps({"error":"True","message":"posts dont matching"})
	else:	
		return json.dumps({"error":"False","post":post,"status":200})
