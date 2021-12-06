# -*- coding: utf-8 -*-
import os
from flask import Flask, redirect,send_from_directory,session 
from app.conect import obtener_conexion
import json
from datetime import datetime
from app.users.querys import obtener_usuariobyid

#estas son todas las querys para las publicaciones

def serializerpost(post):
	#metodo que reallizo para que los post tengan un formato mas comodo para obtener la info de estos	
	posts = []
	for p in post:
		user= obtener_usuariobyid(p[5])
		actual = datetime.now()
		time =   actual - p[7]
		years = int(time.days/365)
		mont = int((time.days % 365)/30)
		day = int((time.days % 365)%30)
		hours =time.seconds/3600
		minutes = (time.seconds % 3600)/60
		secons = ((time.seconds % 3600)%60)
		time= {"years":years,"month":mont,"days":day,"hours":hours,"minutes":minutes,"seconds":secons}
		#times2 = "Y:"+str(years)+"/M:"+str(mont)+"/D:"+str(day)+"/h:"+str(hours)+"/m:"+str(minutes)+"/s:"+str(secons)
		posts.append({"tittle":p[1],"description":p[2],"priority":p[3],"status":p[4],"user":user,"time":time,"create_at":str(p[7]),"update_at":str(p[8])})
		#siempre que se pase por el serializer de la data se actualizara el dato que se tiene del time en la db
		#el json dumps es para que se guarde correctamente en la base de datos
		updateTime(p[0],json.dumps(time))
	return posts

#update time actualiza el json de del tiempo desde que se creo el post
def updateTime(id,time):
	conexion = obtener_conexion()
	with conexion.cursor() as cursor:
		cursor.execute("UPDATE post SET time='"+time.encode('utf-8')+"' WHERE id="+str(id))
		publicacion = cursor.fetchall()
		conexion.commit()
		return True
	return False

#obtiene todas las publicaciones desde la mas nueva a la mas antigua
def obtener_publicaciones():
	conexion = obtener_conexion()
	with conexion.cursor() as cursor:
		cursor.execute("SELECT * FROM post ORDER BY create_at DESC" )
		publicacion = cursor.fetchall()
	conexion.close()
	return serializerpost(publicacion)

#obtiene las que son de un usuario en espesifico
def obtener_publicaciones_usuario(user_id):
	conexion = obtener_conexion()
	publicacion = []
	with conexion.cursor() as cursor:
		cursor.execute("SELECT * FROM post WHERE user='"+str(user_id)+"' ORDER BY date DESC")
		publicacion = cursor.fetchall()
	conexion.close()
	return serializerpost(publicacion)


#obtiene una publicacion en espesifico
def obtener_publicacion(post_id):
	conexion = obtener_conexion()
	publicacion = []
	with conexion.cursor() as cursor:
		cursor.execute("SELECT * FROM post WHERE id='"+str(post_id)+"'")
		publicacion = cursor.fetchall()
	conexion.close()
	print(publicacion)
	return serializerpost(publicacion)

#para buscar segun multiples parametros recibe una query que se arma en el metodo de route
def multisearch(query):
	conexion = obtener_conexion()
	publicacion = []
	with conexion.cursor() as cursor:
		cursor.execute(query)
		publicacion = cursor.fetchall()
	conexion.close()
	return serializerpost(publicacion)

#crea las publicaciones
def crear_publicaciones_usuario(tittle, description, priority, status, user):
	create_at = datetime.now().strftime("%y-%m-%d %H:%M:%S")
	conexion = obtener_conexion()
	with conexion.cursor() as cursor:
		cursor.execute("INSERT INTO post(tittle, description, priority, status, user,create_at) VALUES ( %s, %s, %s,%s, %s, %s)",(tittle, description, priority, status, user,create_at))
		publicacion = cursor.fetchall()
		conexion.commit()
		if cursor.rowcount > 0:
			return True
	return False

#borra las publicaciones segun su id
def delete_publicaciones_usuario(id):
	conexion = obtener_conexion()
	with conexion.cursor() as cursor:
		cursor.execute("DELETE FROM post WHERE id="+str(id))
		publicacion = cursor.fetchall()
		conexion.commit()
		if cursor.rowcount > 0:
			return True
	return False

#update de las publicaciones
def update_post(id,tittle, description, priority, status):	
	conexion = obtener_conexion()
	update_at = datetime.now().strftime("%y-%m-%d %H:%M:%S")
	with conexion.cursor() as cursor:
		cursor.execute("UPDATE post SET tittle='"+tittle+"',description='"+description+"',priority="+str(priority)+",status="+str(status)+",update_at='"+update_at+"' WHERE id="+str(id))
		publicacion = cursor.fetchall()
		conexion.commit()
		if cursor.rowcount > 0:
			return True
	return False

