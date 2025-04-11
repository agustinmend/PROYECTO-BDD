import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from funciones import fetch_data, add_data, delete_data, update_data

class BibliotecaApp:
    def __init__(self, root, db_connection):
        self.root = root
        self.root.title("Gestión de Biblioteca Universitaria")
        self.root.geometry("1000x700")
        self.db_connection = db_connection
        self.create_main_menu()

    def create_action_interface(self, action, table_name, columns, id_column):
        if self.db_connection.current_role == 'GERENTE' and action != 'visualizar':
            messagebox.showerror("Acceso denegado", "Su rol solo permite visualización")
            return
            
        if self.db_connection.current_role == 'VENDEDOR' and action == 'eliminar':
            messagebox.showerror("Acceso denegado", "Vendedores no pueden eliminar registros")
            return
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text=f"{action.capitalize()} en {table_name}", font=("Arial", 16)).pack(pady=10)
        
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, pady=10)
        
        fetch_data(self.db_connection, tree, table_name)
        
        # Configurar acciones según rol
        if self.db_connection.current_role == 'VENDEDOR' and action == 'eliminar':
            messagebox.showwarning("Restricción", "Su rol no permite eliminar registros")
            self.create_table_menu(action)
            return
            
        if self.db_connection.current_role == 'GERENTE' and action != 'visualizar':
            messagebox.showwarning("Restricción", "Su rol solo permite visualizar información")
            self.create_table_menu(action)
            return

        if action in ["agregar", "modificar"]:
            if table_name == "prestamo":
                self.create_prestamo_form(action, tree, table_name, columns[1:], id_column)
            else:
                self.create_form(action, tree, table_name, columns[1:], id_column)
        elif action == "eliminar":
            delete_button = tk.Button(
                self.root, text="Eliminar",
                command=lambda: delete_data(self.db_connection, tree, table_name, id_column),
                bg="#ff6666", fg="white"
            )
            delete_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Volver", command=lambda: self.create_table_menu(action))
        back_button.pack(pady=10)

    def create_table_menu(self, action):
        for widget in self.root.winfo_children():
            widget.destroy()

        tablas_disponibles = self.get_tablas_por_rol()
        
        acciones_permitidas = self.get_acciones_por_rol()
        if action not in acciones_permitidas:
            messagebox.showerror("Error", "Acción no permitida para su rol")
            self.create_main_menu()
            return

        tk.Label(self.root, text=f"Seleccione tabla para {action}", font=("Arial", 14)).pack(pady=20)
        
        for table_name, columns in tablas_disponibles.items():
            tk.Button(
                self.root,
                text=table_name.capitalize(),
                width=25,
                command=lambda t=table_name, c=columns: self.create_action_interface(action, t, c, c[0])
            ).pack(pady=5)

        back_button = tk.Button(self.root, text="Volver", command=self.create_main_menu)
        back_button.pack(pady=10)

    def get_tablas_por_rol(self):
        tablas_completas = self.obtener_tablas_y_columnas()
        
        if self.db_connection.current_role == 'VENDEDOR':
            tablas_permitidas = ['usuario', 'libro', 'libro_autor', 'autor', 'categoria', 
                                'tipo_texto', 'prestamo', 'detalle_prestamo']
            return {k: v for k, v in tablas_completas.items() if k in tablas_permitidas}
        
        elif self.db_connection.current_role == 'GERENTE':
            return {'detalle_prestamo': tablas_completas['detalle_prestamo']}
            
        return tablas_completas 

    def get_acciones_por_rol(self):
        if self.db_connection.current_role == 'VENDEDOR':
            return ['visualizar', 'agregar', 'modificar']
        elif self.db_connection.current_role == 'GERENTE':
            return ['visualizar']
        return ['visualizar', 'agregar', 'modificar', 'eliminar'] 

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        print(f"DEBUG - Rol actual: {self.db_connection.current_role}")
        
        header = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        header.pack(fill="x")
        
        tk.Label(header, 
                text=f"Usuario: {self.db_connection.current_user} | Rol: {self.db_connection.current_role}",
                font=("Arial", 12, "bold"),
                bg="#f0f0f0").pack()

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack()

        if self.db_connection.current_role == 'GERENTE':
            self._create_gerente_interface(main_frame)
        elif self.db_connection.current_role == 'VENDEDOR':
            self._create_vendedor_interface(main_frame)
        elif self.db_connection.current_role == 'DBA':
            self._create_dba_interface(main_frame)
        else:
            messagebox.showerror("Error", f"Rol no reconocido: {self.db_connection.current_role}")
            self.root.destroy()

    def _create_vendedor_interface(self, parent_frame):
        tk.Label(parent_frame, 
                text="OPCIONES DE VENDEDOR",
                font=("Arial", 14, "bold"),
                fg="#2E7D32").pack(pady=(0, 20))

        actions = [
            ("📋 Visualizar Datos", 'visualizar'),
            ("✏️ Editar Registros", 'modificar')
        ]

        for text, action in actions:
            btn = tk.Button(parent_frame,
                        text=text,
                        width=25,
                        bg="#4CAF50",
                        fg="white",
                        font=("Arial", 11),
                        command=lambda a=action: self.create_table_menu(a))
            btn.pack(pady=5)

        ##bloque para anadir boton ver libros disponibles
        tk.Button(
            self.root,
            text="📚 Ver Libros Disponibles",
            width=30,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11),
            command=self.mostrar_libros_disponibles
        ).pack(pady=10)
        ##bloque para ver prestamos activos
        tk.Button(
            self.root,
            text="📄 Ver Préstamos Activos",
            width=30,
            bg="#009688",
            fg="white",
            font=("Arial", 11),
            command=self.mostrar_prestamos_activos
        ).pack(pady=10)
        ##bloque para libros por autor
        tk.Button(
            self.root,
            text="🔎 Buscar libros por autor",
            width=30,
            bg="#673AB7",
            fg="white",
            font=("Arial", 11),
            command=self.buscar_libros_por_autor
        ).pack(pady=10)
        ##bloque para devolver
        tk.Button(
            self.root,
            text="🔁 Devolver libro por nombre",
            width=30,
            bg="#009688",
            fg="white",
            font=("Arial", 11),
            command=self.buscar_y_devolver_por_nombre
        ).pack(pady=10)


        tk.Button(parent_frame,
                text="🔒 Cerrar Sesión",
                command=self.volver_al_login,
                bg="#FF5722",
                fg="white",
                font=("Arial", 11),
                width=25).pack(pady=10)

    def _create_gerente_interface(self, parent_frame):
        tk.Label(parent_frame, 
                text="REPORTES GERENCIALES",
                font=("Arial", 14, "bold"),
                fg="#1565C0").pack(pady=(0, 20))

        options = [
            ("📊 Libros más prestados", self.generar_reporte_libros_mas_prestados),
            ("📋 Tabla de Préstamos", lambda: self.mostrar_tabla_gerente('prestamo')),
            ("📑 Detalle de Préstamos", lambda: self.mostrar_tabla_gerente('detalle_prestamo'))
        ]

        for text, cmd in options:
            btn = tk.Button(parent_frame,
                        text=text,
                        width=25,
                        bg="#2196F3",
                        fg="white",
                        font=("Arial", 11),
                        command=cmd)
            btn.pack(pady=5)
        
        tk.Button(parent_frame,
                text="🔒 Cerrar Sesión",
                command=self.volver_al_login,
                bg="#FF5722",
                fg="white",
                font=("Arial", 11),
                width=25).pack(pady=10)

    def mostrar_tabla_gerente(self, table_name):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, 
                text=f"Visualizando: {table_name}",
                font=("Arial", 16)).pack(pady=10)
        
        cursor = self.db_connection.serverdb.cursor()
        cursor.execute(f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
        """, table_name)
        columns = [row[0] for row in cursor.fetchall()]
        
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, pady=10)
        
        fetch_data(self.db_connection, tree, table_name)
        
        tk.Button(self.root, 
                text="Volver",
                command=self.create_main_menu,
                bg="#2196F3",
                fg="white").pack(pady=10)
# Obtener libros_disponibles by Agustin
    def obtener_libros_disponibles(self):
        cursor = self.db_connection.serverdb.cursor()
        
        cursor.execute("SELECT titulo, nombre_categoria , nombre_tipo, editorial, copias_totales FROM Libros_disponibles")
        columnas = [column[0] for column in cursor.description]
        resultados = cursor.fetchall()

        libros = []
        for fila in resultados:
            libro = dict(zip(columnas, fila))
            libros.append(libro)
        
        cursor.close()
        return libros
    
    def mostrar_libros_disponibles(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        libros = self.obtener_libros_disponibles()
        tk.Label(self.root, text="📚 Libros Disponibles", font=("Arial", 14, "bold")).pack(pady=20)
        if not libros:
            tk.Label(self.root, text="No hay libros disponibles.", font=("Arial", 11)).pack(pady=10)
        else:
            columnas = ["titulo", "nombre_categoria", "nombre_tipo", "editorial", "copias_totales"]
            tree = ttk.Treeview(self.root, columns=columnas, show='headings', height=15)
            tree.pack(pady=10, padx=10)
            tree.heading("titulo", text="Título")
            tree.heading("nombre_categoria", text="Categoría")
            tree.heading("nombre_tipo", text="Tipo")
            tree.heading("editorial", text="Editorial")
            tree.heading("copias_totales", text="Copias Totales")
            for col in columnas:
                tree.column(col, width=150)
            for libro in libros:
                tree.insert("", "end", values=(
                    libro["titulo"],
                    libro["nombre_categoria"],
                    libro["nombre_tipo"],
                    libro["editorial"],
                    libro["copias_totales"]
                ))
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=20)
# hasta aca
#ver prestamos activos
    def obtener_prestamos_activos(self):
        cursor = self.db_connection.serverdb.cursor()
        
        cursor.execute("SELECT * FROM prestamos_activos")
        columnas = [col[0] for col in cursor.description]
        resultados = cursor.fetchall()

        prestamos = []
        for fila in resultados:
            prestamos.append(dict(zip(columnas, fila)))

        cursor.close()
        return prestamos
    
    def mostrar_prestamos_activos(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="📄 Préstamos Activos", font=("Arial", 14, "bold")).pack(pady=20)
        prestamos = self.obtener_prestamos_activos()
        if not prestamos:
            tk.Label(self.root, text="No hay préstamos activos.", font=("Arial", 11)).pack(pady=10)
            tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=20)
            return
        columnas = list(prestamos[0].keys())
        tree = ttk.Treeview(self.root, columns=columnas, show='headings', height=15)
        tree.pack(pady=10)
        for col in columnas:
            tree.heading(col, text=col.replace("_", " ").capitalize())
            tree.column(col, width=130)
        for prestamo in prestamos:
            valores = [prestamo[col] for col in columnas]
            tree.insert("", "end", values=valores)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=20)
# hasta aca
#libros por autor
    def obtener_libros_por_autor(self, nombre_autor):
        cursor = self.db_connection.serverdb.cursor()

        cursor.execute("exec ObtenerLibrosPorAutor ?", (nombre_autor,))
        
        columnas = [col[0] for col in cursor.description]
        resultados = cursor.fetchall()

        libros = []
        for fila in resultados:
            libros.append(dict(zip(columnas, fila)))

        cursor.close()
        return libros
        

    def buscar_libros_por_autor(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="🔍 Buscar libros por autor", font=("Arial", 14, "bold")).pack(pady=20)
        entry_var = tk.StringVar()
        tk.Entry(self.root, textvariable=entry_var, font=("Arial", 12), width=40).pack(pady=10)
        def realizar_busqueda():
            autor = entry_var.get()
            if not autor:
                messagebox.showwarning("Campo vacío", "Por favor ingrese un nombre de autor.")
                return
            libros = self.obtener_libros_por_autor(autor)
            for widget in self.root.pack_slaves():
                if isinstance(widget, ttk.Treeview):
                    widget.destroy()
            if not libros:
                tk.Label(self.root, text="No se encontraron libros para ese autor.", font=("Arial", 11)).pack(pady=10)
                return
            columnas = list(libros[0].keys())
            tree = ttk.Treeview(self.root, columns=columnas, show='headings', height=15)
            tree.pack(pady=10)
            for col in columnas:
                tree.heading(col, text=col.replace("_", " ").capitalize())
                tree.column(col, width=140)
            for libro in libros:
                tree.insert("", "end", values=[libro[col] for col in columnas])
        tk.Button(
            self.root,
            text="Buscar",
            command=realizar_busqueda,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11)
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Volver",
            command=self.create_main_menu,
            font=("Arial", 11)
        ).pack(pady=20)
#hasta aca
#hacer devolucion
    def obtener_prestamos_por_nombre(self, nombre):
        cursor = self.db_connection.serverdb.cursor()
        cursor.execute("EXEC ObtenerPrestamosActivosPorNombre ?", (nombre,))
        columnas = [col[0] for col in cursor.description]
        prestamos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        cursor.close()
        return prestamos
    def buscar_y_devolver_por_nombre(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="🔍 Buscar préstamos activos por nombre", font=("Arial", 14, "bold")).pack(pady=20)

        entry_var = tk.StringVar()
        tk.Entry(self.root, textvariable=entry_var, font=("Arial", 12), width=40).pack(pady=10)

        def realizar_busqueda():
            nombre = entry_var.get()
            if not nombre:
                messagebox.showwarning("Campo vacío", "Por favor ingrese un nombre.")
                return

            prestamos = self.obtener_prestamos_por_nombre(nombre)

            # Eliminar Treeview anterior si existe
            if hasattr(self, 'treeview') and self.treeview:
                self.treeview.destroy()

            # Eliminar botón de devolución anterior si existe
            if hasattr(self, 'devolver_btn') and self.devolver_btn:
                self.devolver_btn.destroy()

            if not prestamos:
                tk.Label(self.root, text="No se encontraron préstamos activos para ese nombre.", font=("Arial", 11)).pack(pady=10)
                self.treeview = None
                self.devolver_btn = None
                return

            columnas = list(prestamos[0].keys())

            self.treeview = ttk.Treeview(self.root, columns=columnas, show='headings', height=15)
            self.treeview.pack(pady=10)

            for col in columnas:
                self.treeview.heading(col, text=col.replace("_", " ").capitalize())
                self.treeview.column(col, width=140)

            for p in prestamos:
                self.treeview.insert("", "end", values=[p[col] for col in columnas])

            def seleccionar_y_devolver():
                selected_item = self.treeview.focus()
                if not selected_item:
                    messagebox.showwarning("Atención", "Seleccioná un préstamo para devolver.")
                    return

                datos = self.treeview.item(selected_item)['values']
                id_prestamo = datos[0]

                confirmar = messagebox.askyesno("Confirmar devolución", f"¿Devolver préstamo ID {id_prestamo}?")
                if confirmar:
                    self.devolver_libro(id_prestamo)
                    realizar_busqueda()

            self.devolver_btn = tk.Button(
                self.root,
                text="Devolver préstamo seleccionado",
                command=seleccionar_y_devolver,
                bg="#FF5722",
                fg="white",
                font=("Arial", 11)
            )
            self.devolver_btn.pack(pady=10)

        tk.Button(self.root, text="Buscar", command=realizar_busqueda, bg="#4CAF50", fg="white", font=("Arial", 11)).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=20)
        
    def devolver_libro(self, id_prestamo):
        cursor = self.db_connection.serverdb.cursor()
        try:
            cursor.execute("EXEC DevolverLibro ?", (id_prestamo,))
            self.db_connection.serverdb.commit()
            messagebox.showinfo("Éxito", "Libro devuelto correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo devolver el libro:\n{str(e)}")
        finally:
            cursor.close()

#hasta aca
    def volver_al_login(self):
        """Cierra la sesión actual y vuelve al login"""
        self.root.destroy()
        from main import main
        main()

    def _create_dba_interface(self, parent_frame):
        """Interfaz COMPLETA para DBAs"""
        tk.Label(parent_frame, 
                text="ADMINISTRACIÓN COMPLETA",
                font=("Arial", 14, "bold"),
                fg="#BF360C").pack(pady=(0, 20))

        actions = [
            ("👁️ Visualizar", 'visualizar'),
            ("➕ Agregar", 'agregar'),
            ("✏️ Modificar", 'modificar'),
            ("🗑️ Eliminar", 'eliminar')
        ]

        for text, action in actions:
            color = "#D32F2F" if "Eliminar" in text else "#4CAF50"
            btn = tk.Button(parent_frame,
                        text=text,
                        width=20,
                        bg=color,
                        fg="white",
                        font=("Arial", 11),
                        command=lambda a=action: self.create_table_menu(a))
            btn.pack(pady=5)
        
        # Añadido: Botón para cerrar sesión
        tk.Button(parent_frame,
                text="🔒 Cerrar Sesión",
                command=self.volver_al_login,
                bg="#FF5722",
                fg="white",
                font=("Arial", 11),
                width=25).pack(pady=10)

    def generar_reporte_libros_mas_prestados(self):
        try:
            cursor = self.db_connection.serverdb.cursor()
            
            cursor.execute("""
                SELECT TOP 10 
                    l.libro_id, 
                    l.titulo, 
                    c.nombre_categoria,
                    COUNT(*) as total_prestamos
                FROM libro l
                JOIN detalle_prestamo dp ON l.libro_id = dp.libro_id
                JOIN categoria c ON l.categoria_id = c.categoria_id
                GROUP BY l.libro_id, l.titulo, c.nombre_categoria
                ORDER BY total_prestamos DESC
            """)
            self.mostrar_resultados_reporte(cursor, "Libros más prestados")
            
        except Exception as e:
            error_msg = f"No se pudo generar el reporte. Error detallado:\n{str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"Error completo: {repr(e)}")

    def generar_reporte_libros_no_prestados(self):
        try:
            cursor = self.db_connection.serverdb.cursor()
            cursor.execute("""
                SELECT l.libro_id, l.titulo, a.nombre_autor
                FROM libro l
                JOIN autor a ON l.autor_id = a.autor_id
                LEFT JOIN detalle_prestamo dp ON l.libro_id = dp.libro_id
                WHERE dp.detalle_prestamo_id IS NULL
            """)
            self.mostrar_resultados_reporte(cursor, "Libros nunca prestados")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {str(e)}")

    def mostrar_resultados_reporte(self, cursor, titulo):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text=titulo, font=("Arial", 16)).pack(pady=10)
        
        # Obtener nombres de columnas
        columns = [column[0] for column in cursor.description]
        
        # Crear Treeview con estilo mejorado
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=('Arial', 10))
        style.configure("mystyle.Treeview.Heading", font=('Arial', 11, 'bold'))
        
        tree = ttk.Treeview(self.root, columns=columns, show="headings", style="mystyle.Treeview")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        tree.pack(fill="both", expand=True, pady=10)
        
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
            self.root, 
            text="Volver", 
            command=self.create_main_menu,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10)
        ).pack(pady=10)

    def create_prestamo_form(self, action, tree, table_name, form_columns, id_column):
        frame=tk.Frame(self.root)
        frame.pack(pady=10)
        form_columns=[col for col in form_columns if col!='fecha_modificacion']

        entry_widgets={}
        for i, col in enumerate(form_columns):
            if col=="estado": 
                tk.Label(frame, text=col).grid(row=i, column=0, padx=5, pady=2)
                estado_var=tk.StringVar()
                estado_frame=tk.Frame(frame)
                estado_frame.grid(row=i, column=1, padx=5, pady=2)

                def update_estado_fields(*args):
                    estado=estado_var.get()
                    if estado=="Activo":
                        entry_widgets["fecha_devolucion"].delete(0, tk.END)
                        entry_widgets["fecha_devolucion"].config(state="disabled")
                    else:
                        entry_widgets["fecha_devolucion"].config(state="normal")

                tk.Radiobutton(estado_frame, text="Activo", variable=estado_var, value="Activo", command=update_estado_fields).pack(side="left")
                tk.Radiobutton(estado_frame, text="Devuelto", variable=estado_var, value="Devuelto", command=update_estado_fields).pack(side="left")
                estado_var.trace_add("write", update_estado_fields)
                entry_widgets[col]=estado_var
            else:
                tk.Label(frame, text=col).grid(row=i, column=0, padx=5, pady=2)
                entry=tk.Entry(frame)
                entry.grid(row=i, column=1, padx=5, pady=2)
                entry_widgets[col] = entry

                if "fecha" in col.lower():
                    tk.Label(frame, text="AAAA-MM-DD", fg="gray").grid(row=i, column=2, padx=5, pady=2)

        def handle_add():
            values = []
            for col in form_columns:
                if col == "estado":
                    values.append(entry_widgets[col].get())
                else:
                    values.append(entry_widgets[col].get())

            try:
                # Validación de fechas
                fecha_prestamo = datetime.strptime(entry_widgets['fecha_prestamo'].get(), "%Y-%m-%d")
                # Validamos solo si el campo no está vacío
                fecha_devolucion_str = entry_widgets['fecha_devolucion'].get().strip()
                if fecha_devolucion_str:
                    fecha_devolucion = datetime.strptime(fecha_devolucion_str, "%Y-%m-%d")
                    if fecha_prestamo > fecha_devolucion:
                        messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                        return
                
                fecha_limite_devolucion = datetime.strptime(entry_widgets['fecha_limite_devolucion'].get(), "%Y-%m-%d")
                if fecha_prestamo > fecha_limite_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
                return

            add_data(self.db_connection, tree, table_name, form_columns, values)

        def handle_update():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Selecciona un registro para modificar.")
                return

            record_id = tree.item(selected_item)["values"][0]
            values = []
            for col in form_columns:
                if col in entry_widgets:
                    values.append(entry_widgets[col].get())
                else:
                    values.append(None)

            try:
                # Validación de fechas
                fecha_prestamo = datetime.strptime(entry_widgets['fecha_prestamo'].get(), "%Y-%m-%d")
                
                # Validamos solo si el campo no está vacío
                fecha_devolucion_str = entry_widgets['fecha_devolucion'].get().strip()
                if fecha_devolucion_str:
                    fecha_devolucion = datetime.strptime(fecha_devolucion_str, "%Y-%m-%d")
                    if fecha_prestamo > fecha_devolucion:
                        messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                        return
                
                fecha_limite_devolucion = datetime.strptime(entry_widgets['fecha_limite_devolucion'].get(), "%Y-%m-%d")
                if fecha_prestamo > fecha_limite_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
                return
            
            update_data(self.db_connection, tree, table_name, form_columns, values, record_id)

        if action=="agregar":
            tk.Button(frame, text="Agregar", command=handle_add).grid(row=len(form_columns), column=0, pady=10)
        elif action=="modificar":
            def load_selected(event):
                selected_item=tree.selection()
                if not selected_item:
                    return
                values=tree.item(selected_item)["values"]
                for i, col in enumerate(form_columns):
                    if col=="estado":
                        entry_widgets[col].set(values[i+1])
                    else:
                        entry_widgets[col].delete(0, tk.END)
                        entry_widgets[col].insert(0, values[i+1])

            tree.bind("<ButtonRelease-1>", load_selected)
            tk.Button(frame, text="Modificar", command=handle_update).grid(row=len(form_columns), column=0, pady=10)

    def create_form(self, action, tree, table_name, columns, id_column):
        form_columns=[col for col in columns if col!='fecha_modificacion']
        frame=tk.Frame(self.root)
        frame.pack(pady=10)

        entry_widgets={}
        for i, col in enumerate(form_columns):
            tk.Label(frame, text=col).grid(row=i, column=0, padx=5, pady=2)
            entry=tk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entry_widgets[col]=entry

            if "fecha" in col.lower():
                tk.Label(frame, text="AAAA-MM-DD", fg="gray").grid(row=i, column=2, padx=5, pady=2)

        if action=="agregar":
            def handle_add():
                values=[entry_widgets[col].get() for col in form_columns]
                add_data(self.db_connection, tree, table_name, form_columns, values)
            tk.Button(frame, text="Agregar", command=handle_add).grid(row=len(form_columns), column=0, pady=10)

        elif action=="modificar":
            def load_selected(event):
                selected_item=tree.selection()
                if not selected_item:
                    return
                values=tree.item(selected_item)["values"]
                for i, col in enumerate(form_columns):
                    entry_widgets[col].delete(0, tk.END)
                    entry_widgets[col].insert(0, values[i+1])

            def handle_update():
                selected_item=tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Selecciona un registro para modificar.")
                    return
                record_id=tree.item(selected_item)["values"][0]
                values=[]
                for col in form_columns:
                    if col in entry_widgets:
                        values.append(entry_widgets[col].get())
                    else:
                        values.append(None)
                update_data(self.db_connection, tree, table_name, form_columns, values, record_id)
            tree.bind("<ButtonRelease-1>", load_selected)
            tk.Button(frame, text="Modificar", command=handle_update).grid(row=len(form_columns), column=0, pady=10)

    def obtener_tablas_y_columnas(self):
        try:
            if not self.db_connection.serverdb:
                print("Reconectando a SQL Server...")
                self.db_connection.conectar_sqlserver()

            conn = self.db_connection.serverdb
            cursor = conn.cursor()

            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE' 
                AND TABLE_CATALOG = 'BibliotecaUniversitaria'
                AND TABLE_NAME <> 'sysdiagrams'
            """)
            tablas = [fila[0] for fila in cursor.fetchall()]

            tablas_columnas = {}

            for tabla_nombre in tablas:
                cursor.execute("""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = ? 
                    ORDER BY ORDINAL_POSITION
                """, (tabla_nombre,))
                
                columnas = [col[0] for col in cursor.fetchall()]
                tablas_columnas[tabla_nombre] = columnas

            return tablas_columnas

        except Exception as e:
            print(f"Error al obtener tablas y columnas: {e}")
            return {}