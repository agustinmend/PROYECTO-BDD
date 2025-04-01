from tkinter import Tk
from biblioteca_app import BibliotecaApp
import sys
import os

# Configurar el acceso al módulo de migración
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sqlserver_to_mysql')))
from conexion import Conexiones
from DEFENSA_EXAMEN import add_registro_defensa
def main():
    try:
        print("Iniciando migración de datos...")

        # Crear conexión a bases de datos
        conexion_db=Conexiones()
        conexion_db.conectar_mysql()  # Conexión a MySQL
        conexion_db.conectar_sqlserver()
        
        print("Conexion a MySQL")
    except Exception as e:
        print(f"Error durante la conexión: {str(e)}")
    # Iniciando la app Tkinter
    try:
        root=Tk()
        app = BibliotecaApp(root, conexion_db)  # Pasar la conexión a la aplicación
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación Tkinter: {str(e)}")
    finally:
        # Cerrar conexiones al finalizar
        conexion_db.cerrar_conexiones()
        print("Conexiones cerradas correctamente.")

if __name__=="__main__":
    main()