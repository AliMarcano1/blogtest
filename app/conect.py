#coneccion con la base de datos
import pymysql
def obtener_conexion():
    return pymysql.connect(host='localhost',user='root',password='hirano6951015',db='testblog',use_unicode=True,charset='utf8')