from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime

class Pol:
    def __init__(self):
        pass

    def generar_reporte_libros_mas_prestados(self, db_connection):
        try:
            cursor = db_connection.serverdb.cursor()
            cursor.execute("""
                SELECT * from libros_mas_prestados
            """)
            
            return cursor
            
        except Exception as e:
            error_msg = f"No se pudo generar el reporte. Error detallado:\n{str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"Error completo: {repr(e)}")
            return None
    
    def generar_reporte_usuarios_estado_activo(self, db_connection):
        try:
            cursor = db_connection.serverdb.cursor()
            cursor.execute("""
                SELECT * from mostrar_usuarios_con_prestamo_activo
            """)
            
            return cursor
            
        except Exception as e:
            error_msg = f"No se pudo generar el reporte. Error detallado:\n{str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"Error completo: {repr(e)}")
            return None
        
    def generar_reporte_usuarios_con_mas_prestamos(self, db_connection):
        try:
            cursor = db_connection.serverdb.cursor()
            cursor.execute("""
                SELECT * 
                FROM usuarios_con_mas_prestamos
                ORDER BY cantidad_prestamos DESC;
            """)
            
            return cursor
            
        except Exception as e:
            error_msg = f"No se pudo generar el reporte. Error detallado:\n{str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"Error completo: {repr(e)}")
            return None
        
    def generar_reporte_categorias(self, db_connection):
        try:
            cursor = db_connection.serverdb.cursor()
            cursor.execute("""
                SELECT * 
                FROM libros_por_categoria
                ORDER BY total_stock DESC;
            """)
            
            return cursor
            
        except Exception as e:
            error_msg = f"No se pudo generar el reporte. Error detallado:\n{str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"Error completo: {repr(e)}")
            return None

    def mostrar_resultados_reporte(self, root, cursor, titulo, create_main_menu_callback):

        for widget in root.winfo_children():
            widget.destroy()
        
        tk.Label(root, text=titulo, font=("Arial", 16)).pack(pady=10)
        
        columns = [column[0] for column in cursor.description]
        
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=('Arial', 10))
        style.configure("mystyle.Treeview.Heading", font=('Arial', 11, 'bold'))
        
        tree = ttk.Treeview(root, columns=columns, show="headings", style="mystyle.Treeview")
        
        scrolly = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        scrollx = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        tree.pack(fill="both", expand=True, pady=10)
        scrolly.pack(side="right", fill="y")
        scrollx.pack(side="bottom", fill="x")
        
        for row in cursor.fetchall():
            formatted_row = []
            for value in row:
                if isinstance(value, datetime):
                    formatted_value = value.strftime("%Y-%m-%d")
                elif isinstance(value, str):
                    formatted_value = value.replace("'", "").replace('"', '')
                else:
                    formatted_value = str(value)
                formatted_row.append(formatted_value)
            
            tree.insert("", "end", values=formatted_row)
        
        tk.Button(
            root, 
            text="Volver", 
            command=create_main_menu_callback,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10)
        ).pack(pady=10)