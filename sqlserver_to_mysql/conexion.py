import mysql.connector
from mysql.connector import Error
import pyodbc
from dataclasses import dataclass

@dataclass
class Conexiones:
    mydb=None
    serverdb=None

    # Crea la base de datos en MySQL si no existe
    def crear_base_datos(self):
        try:
            if self.mydb.is_connected():
                mycursor=self.mydb.cursor()
                mycursor.execute("CREATE DATABASE IF NOT EXISTS BibliotecaUniversidad;")
                mycursor.execute("USE BibliotecaUniversidad;")
                mycursor.close()
                print("Base de datos 'BibliotecaUniversidad' creada o seleccionada exitosamente.")
        except Error as e:
            print(f"Error al crear o seleccionar la base de datos en MySQL: {e}")

    # Establece la conexión con MySQL
    def conectar_mysql(self, usar_base_datos=True):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                port='3306',
                password='Fernando2420',  # Ajusta según sea necesario
                auth_plugin='mysql_native_password'
            )
            print("Conexión a MySQL establecida.")
            if usar_base_datos:
                self.crear_base_datos()
        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self.mydb = None

    # Establece la conexión con SQL Server
    def conectar_sqlserver(self):
        server = 'DESKTOP-T8BJL71'  # Cambia según corresponda
        database = 'BibliotecaUniversitaria'
        username = 'DESKTOP-T8BJL71\\user'  # Cambia según corresponda

        try:
            self.serverdb = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"Trusted_Connection=yes;"
            )
            print("Conexión a SQL Server establecida.")
        except Exception as e:
            print(f"Error al conectar a SQL Server: {e}")
            self.serverdb = None

    # Cierra ambas conexiones si están abiertas
    def cerrar_conexiones(self):
        try:
            if self.mydb:
                self.mydb.close()
                print("Conexión a MySQL cerrada.")
            if self.serverdb:
                self.serverdb.close()
                print("Conexión a SQL Server cerrada.")
        except Exception as e:
            print(f"Error al cerrar las conexiones: {e}")
