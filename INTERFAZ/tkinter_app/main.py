from tkinter import Tk
from biblioteca_app import BibliotecaApp
from autenticacion import Autenticacion
import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'conexion_sqlserver')))

from conexion import Conexiones

def main():
    try:
        auth = Autenticacion()
        root_login = Tk()
        
        
        def intentar_login():
            username = entry_user.get()
            password = entry_pass.get()
            
            rol = auth.verificar_credenciales(username, password)
            if rol:
                root_login.destroy()
                iniciar_aplicacion(username, password, rol)
            else:
                messagebox.showerror("Error", "Credenciales inválidas o sin permisos")
        
        tk.Label(root_login, text="Usuario:", font=("Arial", 12)).pack(pady=5)
        entry_user = tk.Entry(root_login, font=("Arial", 12))
        entry_user.pack(pady=5)
        
        tk.Label(root_login, text="Contraseña:", font=("Arial", 12)).pack(pady=5)
        entry_pass = tk.Entry(root_login, show="*", font=("Arial", 12))
        entry_pass.pack(pady=5)
        
        tk.Button(root_login, text="Ingresar", command=intentar_login, 
                 bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=20)
        
        root_login.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error inicial: {str(e)}")

def iniciar_aplicacion(username: str, password: str, rol: str):
    try:
        print(f"DEBUG - Rol autenticado: {rol}")
        
        conexion_db = Conexiones()

        if rol not in ['DBA', 'VENDEDOR', 'GERENTE']:
            messagebox.showerror("Error", f"Rol no válido: {rol}")
            return
            
        conexion_db.conectar_sqlserver(username, password, rol)
        
        if not conexion_db.serverdb:
            messagebox.showerror("Error", "Conexión fallida")
            return
            
        if conexion_db.current_role != rol:
            messagebox.showerror("Error", 
                f"Conflicto de roles: Autenticación={rol} vs Conexión={conexion_db.current_role}")
            return
            
        root = Tk()
        app = BibliotecaApp(root, conexion_db)
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error en la aplicación: {str(e)}")

if __name__ == "__main__":
    main()