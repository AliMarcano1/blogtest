import os
from flask import Flask
from app.conect import obtener_conexion
from urlparse import urlparse
import json

#aqui estan todos las query a la base de datos para la tabla de usuarios

def serializeruser(user):
	return {"id":user[0],"password":user[1],"email":user[2],"fullname":user[3],"photo":user[4]}

#metodo para crear los usuarios
def create_user(password,email,fullname,photo):
	conexion = obtener_conexion()#obtiene la conexion con la db
	with conexion.cursor() as cursor:
		try:
			cursor.execute("INSERT INTO users(password,email,fullname,photo) VALUES (%s,%s,%s,%s)",(password,email,fullname,photo))
			publicacion = cursor.fetchall()
			conexion.commit()
		except:
			return False
		return True
	return False

#para obtener los usuarios segun su email sirve para el login
def obtener_usuario_email(email):
	conexion = obtener_conexion()
	user = []
	with conexion.cursor() as cursor:
		cursor.execute("SELECT * FROM users WHERE email='"+email+"'")
		user = cursor.fetchall()
		conexion.close()
		print(user)
		if not user:
			return False
	return serializeruser(user[0])

#busca el usuario por su id
def obtener_usuariobyid(id):
	conexion = obtener_conexion()
	user = []
	with conexion.cursor() as cursor:
		cursor.execute("SELECT * FROM users WHERE id="+str(id))
		user = cursor.fetchall()
		conexion.close()
		if not user:
			return False
	return serializeruser(user[0])

#update del usuario segun su id
def edit_usuario(id,password,email,fullname,photo):
	conexion = obtener_conexion()
	with conexion.cursor() as cursor:
		cursor.execute("UPDATE users SET photo='"+str(photo)+"',email='"+email+"',fullname='"+fullname+"',password='"+password+"' WHERE id="+str(id))
		conexion.commit()
		conexion.close()
		if cursor.rowcount > 0:
			return True
	return False
#delete del usuario segun su id
def delete_user(id):
	conexion = obtener_conexion()
	with conexion.cursor() as cursor:
		cursor.execute("DELETE FROM users WHERE id="+str(id))
		conexion.commit()
		conexion.close()
		if cursor.rowcount > 0:
			return True
	return False

#todos los usuario
def allusers():
	conexion = obtener_conexion()
	users = []
	lista =[]
	with conexion.cursor() as cursor:
		cursor.execute("SELECT * FROM users")
		users = cursor.fetchall()
		conexion.close()
		for user in users:
			lista.append(serializeruser(user)) 
	return lista
