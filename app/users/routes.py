import os
from flask import Flask, redirect,session
from flask import render_template
from flask import request
from pathlib import Path
from . import users
from . import querys
from app.conect import obtener_conexion
import json
import uuid

#los endpoint para los usuarios, todos los endpoint que reciben data la reciben por form data decidi mantener esto 
#por el tema de que se necesita enviar imagenes o archivos para unos

#cerrar session
@users.route('/users/logout')
def logOut():
	#limpia la cache de la session
	session.clear()
	return json.dumps({"status":True,"message":"logout","status":200})

#inciiar session
@users.route('/users/auth/',methods=["POST"])
def auth():
	try:
		email = request.form['email']
		password = request.form['password']
	except:
		return json.dumps({"error":True,"message":"error read data","status":401})
	user = querys.obtener_usuario_email(email)
	#vericica la password
	if str(user["password"]) == password:
		session['email'] = user["email"]
		session['userid'] = user["id"]
		return json.dumps({"error":True,"email":session['email'],"userid":session['userid'],"status":200})
	return json.dumps({"status":False,"message":"error email or paswword incorrect","status":401})

#metodo de creacion de usuarios
@users.route('/users/create/',methods=["POST"])
def create():
	try:
		email = request.form['email']
		password = request.form['password']
		fullname= request.form['fullname']
	except:
		return json.dumps({"error":True,"message":"error read data","status":401})
	try:
		#get de la photo
		file1 = request.files['photo']
	except:
		return json.dumps({"error":True,"message":"error get file","status":401})
	try:
		#genera un uuid para el nombre de la photo
		imgname=str(uuid.uuid4())
		file1.filename = "img/users/"+str(email)+"/"+imgname+".png"
		if not os.path.exists(users.static_folder+"/img/users/"+str(email)):
			os.makedirs(users.static_folder+"/img/users/"+str(email))
		path = os.path.join(users.static_folder , file1.filename)
		img = file1.filename
	except:
		return json.dumps({"error":True,"message":"error ocurred in save img","status":401})
		
	user = querys.create_user(password,email,fullname,img)

	if not user:
		return json.dumps({"error":True,"message":"error creating user","status":401})
	#guarda el archivo una vez que ya se creo el usuario
	file1.save(path)
	return json.dumps({"status":200,"error":"False"})


#end point de update usuario
@users.route('/users/update/',methods=["POST"])
def update():
	try:
		userid = request.form['id']
		email = request.form['email']
		password = request.form['password']
		fullname= request.form['fullname']
	except:
		return json.dumps({"error":True,"message":"error read data","status":401})
	try:
		file1=request.files['photo']
	except:
		return json.dumps({"error":True,"message":"error get file","status":401})
	
	#busca al usuario para saber si existe antes de pasar a hacer el resto del procedimiento 
	user= querys.obtener_usuariobyid(userid)
	if not user:	
		return json.dumps({"error":True,"message":"error get user","status":401})
	try:
		#toma el nombre de la photo en la db lo asigna para reemplazar por la nueva photo
		file1.filename = user["photo"]
		if not os.path.exists(users.static_folder+"/img/users/"+str(email)):
			#crea el directorio en caso de que no exista
			os.makedirs(users.static_folder+"/img/users/"+str(email))
		path = os.path.join(users.static_folder , file1.filename)
		img = file1.filename
	except:
		return json.dumps({"error":True,"message":"error ocurred in save img","status":401})
	
	#llama a la query de update user
	u_user= querys.edit_usuario(userid,password,email,fullname,img)
	if not u_user:
		return json.dumps({"error":True,"message":"error ocurred saving changes","status":401})
	#guarda el archivo una vez que se verifico que el usuario fue modificado
	file1.save(path)
	return json.dumps({"status":"True","userdata":user,"status":200})

#endpoint delete user segun su id
@users.route('/users/delete/<id>',methods=["GET"])
def delete(id):
	#llama a la query que borra al usuario
	user = querys.delete_user(id)
	if user:
		return json.dumps({"error":"False","message":"user deleted","status":200})
	else:
		return json.dumps({"error":"True","message":"error deleted user","status":401})

#endpoint para buscar 1 usuario en espesifico segun su id
@users.route('/users/search/<id>',methods=["GET"])
def search(id):
	#llama la query que busca al usuario segun la id
	user = querys.obtener_usuariobyid(id)
	if user:
		return json.dumps({"error":"False","user":user,"status":200})
	else:
		return json.dumps({"error":"True","message":"error user not exist"})

#endpoint para obtener todos los usuarios
@users.route('/users/all/',methods=["GET"])
def alluser():
	#llama a la query que devuelve todos los usuarios
	users = querys.allusers()
	return json.dumps({"error":False,"list":users})