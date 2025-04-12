import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from funciones import fetch_data, add_data, delete_data, update_data
from pol import Pol

class BibliotecaApp:
    def __init__(self, root, db_connection):
        self.root = root
        self.root.title("Gestión de Biblioteca Universitaria")
        self.root.geometry("1000x700")
        self.db_connection = db_connection
        self.pol = Pol()
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        header.pack(fill="x")

        tk.Label(header,
                 text=f"Usuario: {self.db_connection.current_user} | Rol: {self.db_connection.current_role}",
                 font=("Arial", 12, "bold"),
                 bg="#f0f0f0").pack()

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack()

        if self.db_connection.current_role == 'VENDEDOR':
            self._create_vendedor_interface(main_frame)
        elif self.db_connection.current_role == 'GERENTE':
            self._create_gerente_interface(main_frame)
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
            ("➕ Agregar Nuevos Usuarios", self.create_agregar_usuario_interface),
            ("➕ Agregar Préstamos", self.create_agregar_prestamo_interface),
            ("➕ Agregar Nuevos Libros", self.create_agregar_libro_interface),
            ("📚 Ver Libros Disponibles", self.mostrar_libros_disponibles),
            ("📄 Ver Préstamos Activos", self.mostrar_prestamos_activos),
            ("🔎 Buscar libros por autor", self.buscar_libros_por_autor),
            ("🔁 Devolver libro por nombre", self.buscar_y_devolver_por_nombre)
        ]

        for text, action in actions:
            btn = tk.Button(parent_frame,
                            text=text,
                            width=25,
                            bg="#4CAF50" if "Agregar" in text else "#673AB7" if "Buscar" in text else "#009688",
                            fg="white",
                            font=("Arial", 11),
                            command=action)
            btn.pack(pady=5)

    ##esto en biblioteca_app dentro de la clase
#BLOQUE MODIFICADO POR DARIANA
    def _create_gerente_interface(self, parent_frame):
        tk.Label(parent_frame, 
                text="REPORTES GERENCIALES",
                font=("Arial", 14, "bold"),
                fg="#1565C0").pack(pady=(0, 20))

        options = [
            ("📊 Libros más prestados", self.mostrar_reporte_libros_mas_prestados),
            ("📋 Usuarios Activos", self.mostrar_reporte_usuarios_activos),
            ("📒 Usuarios Con Mas Prestamos", self.mostrar_reporte_usuarios_mas_prestamos),
            ("🗂️ Stock de Libros por Categoria", self.mostrar_reporte_categoria)
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

    def mostrar_reporte_libros_mas_prestados(self):
        cursor = self.pol.generar_reporte_libros_mas_prestados(self.db_connection)
        if cursor:
            self.pol.mostrar_resultados_reporte(self.root, cursor, "Libros más prestados", self.create_main_menu)

    def mostrar_reporte_usuarios_activos(self):
        cursor = self.pol.generar_reporte_usuarios_estado_activo(self.db_connection)
        if cursor:
            self.pol.mostrar_resultados_reporte(self.root, cursor, "Usuarios con estado activo", self.create_main_menu)

    def mostrar_reporte_usuarios_mas_prestamos(self):
        cursor = self.pol.generar_reporte_usuarios_con_mas_prestamos(self.db_connection)
        if cursor:
            self.pol.mostrar_resultados_reporte(self.root, cursor, "Usuarios con mas prestamos", self.create_main_menu)

    def mostrar_reporte_categoria(self):
        cursor = self.pol.generar_reporte_categorias(self.db_connection)
        if cursor:
            self.pol.mostrar_resultados_reporte(self.root, cursor, "Cantidad de Libros por categoria", self.create_main_menu)
##FIN DE BLOQUE MODIFICADO >;)
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

    def create_agregar_usuario_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Agregar Nuevo Usuario", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        entry_widgets = {}
        fields = ["nombre", "apellido", "correo", "tipo_usuario", "carrera", "fecha_registro"]

        for i, field in enumerate(fields):
            tk.Label(frame, text=field.capitalize()).grid(row=i+1, column=0, padx=5, pady=2)
            entry = tk.Entry(frame)
            entry.grid(row=i+1, column=1, padx=5, pady=2)
            entry_widgets[field] = entry

        def handle_add_user():
            values = [entry_widgets[field].get() for field in fields]
            add_data(self.db_connection, None, "usuario", fields, values)
            messagebox.showinfo("Éxito", "Usuario agregado exitosamente.")
            self.mostrar_tabla_usuarios()

        tk.Button(frame, text="Agregar Usuario", command=handle_add_user, bg="#4CAF50", fg="white", font=("Arial", 11)).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        back_button = tk.Button(self.root, text="Volver", command=self.create_main_menu, bg="#2196F3", fg="white", font=("Arial", 11))
        back_button.pack(pady=10)

    def mostrar_tabla_usuarios(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Tabla de Usuarios", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(self.root, columns=["nombre", "apellido", "correo", "tipo_usuario", "carrera", "fecha_registro"], show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, pady=10)

        fetch_data(self.db_connection, tree, "usuario")

        back_button = tk.Button(self.root, text="Volver", command=self.create_main_menu, bg="#2196F3", fg="white", font=("Arial", 11))
        back_button.pack(pady=10)

    def create_agregar_prestamo_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Registrar Nuevo Préstamo", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Campos del formulario con sus variables
        fields = [
            {"name": "correo", "label": "Correo Usuario*", "type": "entry", "var": tk.StringVar()},
            {"name": "libro", "label": "Libro*", "type": "option", "table": "libro", "display": "titulo", "var": tk.StringVar()},
            {"name": "cantidad", "label": "Cantidad*", "type": "spinbox", "from": 1, "to": 10, "var": tk.StringVar()},
            {"name": "fecha_prestamo", "label": "Fecha Préstamo*", "type": "entry", "default": datetime.now().strftime("%Y-%m-%d"), "var": tk.StringVar()},
            {"name": "bibliotecario", "label": "Bibliotecario*", "type": "option", "table": "bibliotecario", 
            "display": "CONCAT(nombre, ' ', apellido)", "var": tk.StringVar()}
        ]

        # Crear widgets y almacenar las variables
        for row, field in enumerate(fields, start=1):
            tk.Label(frame, text=field["label"]).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            
            if field["type"] == "entry":
                widget = tk.Entry(frame, textvariable=field["var"])
                if "default" in field:
                    field["var"].set(field["default"])
                widget.grid(row=row, column=1, padx=5, pady=2, sticky="w")
                
            elif field["type"] == "spinbox":
                widget = tk.Spinbox(frame, from_=field["from"], to=field["to"], 
                                textvariable=field["var"], width=5)
                widget.grid(row=row, column=1, padx=5, pady=2, sticky="w")
                
            elif field["type"] == "option":
                if field["display"] == "CONCAT(nombre, ' ', apellido)":
                    cursor = self.db_connection.serverdb.cursor()
                    cursor.execute(f"SELECT {field['display']} FROM {field['table']}")
                    options = [row[0] for row in cursor.fetchall()]
                else:
                    options = self.get_options_from_table(field["table"], field["display"])
                
                field["var"].set(options[0] if options else "")
                widget = tk.OptionMenu(frame, field["var"], *options)
                widget.grid(row=row, column=1, padx=5, pady=2, sticky="ew")

        # Función para verificar usuario
        def verificar_usuario():
            correo = fields[0]["var"].get()  # Accedemos al correo a través de la variable
            if not correo:
                messagebox.showwarning("Error", "Ingrese un correo electrónico")
                return
                
            cursor = self.db_connection.serverdb.cursor()
            cursor.execute("SELECT usuario_id FROM usuario WHERE correo = ?", (correo,))
            result = cursor.fetchone()
            
            if result:
                messagebox.showinfo("Éxito", "Usuario verificado correctamente")
                return result[0]
            else:
                messagebox.showerror("Error", "Usuario no encontrado. Regístrelo primero")
                return None

        # Botón verificar usuario
        tk.Button(frame, text="Verificar Usuario", command=verificar_usuario,
                bg="#2196F3", fg="white").grid(row=1, column=2, padx=5, pady=2)

        # Función para agregar préstamo
        def agregar_prestamo():
            try:
                # Verificar usuario primero
                usuario_id = verificar_usuario()
                if usuario_id is None:
                    return

                # Obtener valores de los campos
                libro_titulo = fields[1]["var"].get()
                cantidad = fields[2]["var"].get()
                fecha_prestamo = fields[3]["var"].get()
                biblio_nombre_completo = fields[4]["var"].get()

                # Validaciones básicas
                if not all([libro_titulo, cantidad, fecha_prestamo, biblio_nombre_completo]):
                    raise ValueError("Todos los campos marcados con * son obligatorios")

                # Validar que cantidad sea un número
                try:
                    cantidad_int = int(cantidad)
                    if cantidad_int < 1:
                        raise ValueError("La cantidad debe ser mayor a 0")
                except ValueError:
                    raise ValueError("La cantidad debe ser un número válido")

                # Validar formato de fecha
                try:
                    datetime.strptime(fecha_prestamo, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Use AAAA-MM-DD")

                # Obtener IDs de las relaciones
                cursor = self.db_connection.serverdb.cursor()
                
                # Obtener ID del libro
                cursor.execute("SELECT libro_id FROM libro WHERE titulo = ?", (libro_titulo,))
                libro_result = cursor.fetchone()
                if not libro_result:
                    raise ValueError("Libro no encontrado")
                libro_id = libro_result[0]
                
                # Obtener ID del bibliotecario
                try:
                    biblio_nombre, biblio_apellido = biblio_nombre_completo.split(' ', 1)
                except ValueError:
                    raise ValueError("Formato de nombre de bibliotecario inválido")
                    
                cursor.execute("""
                    SELECT bibliotecario_id FROM bibliotecario 
                    WHERE nombre = ? AND apellido = ?
                """, (biblio_nombre, biblio_apellido))
                biblio_result = cursor.fetchone()
                if not biblio_result:
                    raise ValueError("Bibliotecario no encontrado")
                biblio_id = biblio_result[0]

                # PRIMERO INSERTAR EN PRESTAMO
                cursor.execute("""
                    INSERT INTO prestamo (
                        usuario_id, 
                        bibliotecario_id, 
                        fecha_prestamo, 
                        estado
                    ) 
                    VALUES (?, ?, ?, 'Activo')
                """, (usuario_id, biblio_id, fecha_prestamo))
                
                # OBTENER EL ID DE FORMA CONFIABLE
                cursor.execute("SELECT IDENT_CURRENT('prestamo')")
                prestamo_id = cursor.fetchone()[0]
                
                if not prestamo_id:
                    raise Exception("No se pudo obtener el ID del préstamo creado")

                # LUEGO INSERTAR EN DETALLE_PRESTAMO
                cursor.execute("""
                    INSERT INTO detalle_prestamo (
                        prestamo_id, 
                        libro_id, 
                        cantidad
                    ) VALUES (?, ?, ?)
                """, (prestamo_id, libro_id, cantidad_int))
                
                self.db_connection.serverdb.commit()
                messagebox.showinfo("Éxito", "Préstamo registrado correctamente")
                self.mostrar_tabla_prestamos()
                
            except ValueError as ve:
                messagebox.showerror("Error de validación", str(ve))
            except Exception as e:
                self.db_connection.serverdb.rollback()
                messagebox.showerror("Error", f"No se pudo registrar el préstamo: {str(e)}")
        # Botón agregar préstamo
        tk.Button(frame, text="Registrar Préstamo", command=agregar_prestamo,
                bg="#4CAF50", fg="white", font=("Arial", 11)).grid(
                    row=len(fields)+1, column=0, columnspan=3, pady=10)

        # Botón volver
        tk.Button(self.root, text="Volver", command=self.create_main_menu,
                bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=10)

    def mostrar_tabla_prestamos(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Registro de Préstamos", font=("Arial", 16)).pack(pady=10)

        # Columnas a mostrar
        columns = [
            "correo_usuario", 
            "libro", 
            "cantidad", 
            "fecha_prestamo", 
            "bibliotecario",
            "estado"
        ]
        
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        # Configurar encabezados
        headers = [
            "Usuario", 
            "Libro", 
            "Cantidad", 
            "Fecha Préstamo", 
            "Bibliotecario",
            "Estado"
        ]
        
        for col, header in zip(columns, headers):
            tree.heading(col, text=header)
            tree.column(col, width=120, anchor="center")
        
        tree.pack(fill="both", expand=True, pady=10)

        # Obtener datos de la vista
        try:
            cursor = self.db_connection.serverdb.cursor()
            cursor.execute("""
                SELECT 
                    correo_usuario,
                    libro,
                    cantidad,
                    fecha_prestamo,
                    bibliotecario,
                    estado
                FROM vista_prestamos_completa
                ORDER BY fecha_prestamo DESC
            """)
            
            for row in cursor.fetchall():
                formatted_row = []
                for value in row:
                    if value is None:
                        formatted_row.append("")
                    elif hasattr(value, 'strftime'):
                        formatted_row.append(value.strftime("%Y-%m-%d"))
                    else:
                        formatted_row.append(str(value))
                tree.insert("", "end", values=formatted_row)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los préstamos: {e}")

        # Botón Volver
        tk.Button(self.root, text="Volver", command=self.create_main_menu,
                bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=10)
    def create_agregar_libro_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Agregar Nuevo Libro", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        entry_widgets = {}
        fields = ["titulo", "ano_publicacion", "editorial", "tipo_texto_id", "categoria_id", "copias_totales", "autor_nombre", "apellido_autor"] 

        for i, field in enumerate(fields):
            if field in ["tipo_texto_id", "categoria_id"]:
                tk.Label(frame, text=field.replace("_id", "").replace("_", " ").capitalize()).grid(row=i+1, column=0, padx=5, pady=2)
                values = self.get_options_from_table(field.replace("_id", ""), "nombre_tipo" if field == "tipo_texto_id" else "nombre_categoria")
                var = tk.StringVar(frame)
                var.set(values[0])  # Establecer el primer valor por defecto
                option_menu = tk.OptionMenu(frame, var, *values)
                option_menu.grid(row=i+1, column=1, padx=5, pady=2)
                entry_widgets[field] = var
            elif field in ["autor_nombre", "apellido_autor"]:
                tk.Label(frame, text=field.replace("_", " ").capitalize()).grid(row=i+1, column=0, padx=5, pady=2)
                entry = tk.Entry(frame)
                entry.grid(row=i+1, column=1, padx=5, pady=2)
                entry_widgets[field] = entry
            else:
                tk.Label(frame, text=field.capitalize()).grid(row=i+1, column=0, padx=5, pady=2)
                entry = tk.Entry(frame)
                entry.grid(row=i+1, column=1, padx=5, pady=2)
                entry_widgets[field] = entry

        def handle_add_libro():
            values = []
            for field in fields:
                if field in ["tipo_texto_id", "categoria_id"]:
                    values.append(self.get_id_for_name(field.replace("_id", ""), entry_widgets[field].get()))
                else:
                    values.append(entry_widgets[field].get())

            # Llamar al stored procedure
            self.call_registrar_libro_procedure(values)
            messagebox.showinfo("Éxito", "Libro agregado/actualizado exitosamente.")
            self.mostrar_tabla_libros()

        tk.Button(frame, text="Agregar Libro", command=handle_add_libro, bg="#4CAF50", fg="white", font=("Arial", 11)).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        back_button = tk.Button(self.root, text="Volver", command=self.create_main_menu, bg="#2196F3", fg="white", font=("Arial", 11))
        back_button.pack(pady=10)

    def mostrar_tabla_libros(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Tabla de Libros", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(self.root, columns=["titulo", "ano_publicacion", "editorial", "tipo_texto_id", "categoria_id", "autor_id", "copias_totales"], show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, pady=10)

        fetch_data(self.db_connection, tree, "libro")

        back_button = tk.Button(self.root, text="Volver", command=self.create_main_menu, bg="#2196F3", fg="white", font=("Arial", 11))
        back_button.pack(pady=10)

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
            tk.Button(frame, text="Agregar", command=handle_add, bg="#4CAF50", fg="white", font=("Arial", 11)).grid(row=len(form_columns), column=0, pady=10)
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
            tk.Button(frame, text="Modificar", command=handle_update, bg="#4CAF50", fg="white", font=("Arial", 11)).grid(row=len(form_columns), column=0, pady=10)

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
            tk.Button(frame, text="Agregar", command=handle_add, bg="#4CAF50", fg="white", font=("Arial", 11)).grid(row=len(form_columns), column=0, pady=10)

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
            tk.Button(frame, text="Modificar", command=handle_update, bg="#4CAF50", fg="white", font=("Arial", 11)).grid(row=len(form_columns), column=0, pady=10)

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
    def create_table_menu(self, action):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Seleccionar tabla para {action}", font=("Arial", 14, "bold")).pack(pady=10)

        tablas_columnas = self.obtener_tablas_y_columnas()

        if not tablas_columnas:
            tk.Label(self.root, text="No se encontraron tablas.", font=("Arial", 12)).pack(pady=10)
            return

        for tabla in tablas_columnas:
            btn = tk.Button(
                self.root,
                text=tabla,
                font=("Arial", 11),
                width=25,
                command=lambda t=tabla: self.mostrar_tabla_general(t, action, tablas_columnas[tabla])
            )
            btn.pack(pady=5)

        tk.Button(
            self.root,
            text="Volver",
            command=self.create_main_menu,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11)
        ).pack(pady=20)

    def mostrar_tabla_general(self, tabla, action, columnas):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"📋 {action.capitalize()} en tabla: {tabla}", font=("Arial", 14, "bold")).pack(pady=10)

        tree = ttk.Treeview(self.root, columns=columnas, show="headings")
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, pady=10)

        fetch_data(self.db_connection, tree, tabla)

        if action == "agregar":
            self.create_form("agregar", tree, tabla, columnas, f"{tabla}_id")
        elif action == "modificar":
            self.create_form("modificar", tree, tabla, columnas, f"{tabla}_id")
        elif action == "eliminar":
            delete_button = tk.Button(self.root, text="Eliminar", command=lambda: delete_data(self.db_connection, tree, tabla, f"{tabla}_id"), bg="#D32F2F", fg="white", font=("Arial", 11))
            delete_button.pack(pady=10)

        tk.Button(self.root, text="Volver", command=self._create_dba_interface, bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=20)

    def _create_dba_interface(self, parent_frame=None):
        """Interfaz COMPLETA para DBAs"""
        container = parent_frame if parent_frame else self.root
        for widget in container.winfo_children():
            widget.destroy()

        header = tk.Frame(container, bg="#f0f0f0", padx=10, pady=10)
        header.pack(fill="x")

        tk.Label(header,
                text=f"Usuario: {self.db_connection.current_user} | Rol: {self.db_connection.current_role}",
                font=("Arial", 12, "bold"),
                bg="#f0f0f0").pack()

        main_frame = tk.Frame(container, padx=20, pady=20)
        main_frame.pack()

        tk.Label(main_frame,
                text="ADMINISTRACIÓN COMPLETA - DBA",
                font=("Arial", 14, "bold"),
                fg="#BF360C").pack(pady=(0, 20))

        actions = [
            ("👁️ Visualizar Tablas", self._show_tables),
            ("➕ Agregar Registros", lambda: self._show_tables('agregar')),
            ("✏️ Modificar Registros", lambda: self._show_tables('modificar')),
            ("🗑️ Eliminar Registros", lambda: self._show_tables('eliminar')),
            ("📊 Reportes Gerenciales", self._show_reports)
        ]

        for text, action in actions:
            btn = tk.Button(main_frame,
                          text=text,
                          width=25,
                          bg="#D32F2F" if "Eliminar" in text else 
                             "#4CAF50" if "Agregar" in text else
                             "#2196F3",
                          fg="white",
                          font=("Arial", 11),
                          command=action)
            btn.pack(pady=5)
        tk.Button(parent_frame,
                text="🔒 Cerrar Sesión",
                command=self.volver_al_login,
                bg="#FF5722",
                fg="white",
                font=("Arial", 11),
                width=25).pack(pady=10)

    def _show_tables(self, action='visualizar'):
        """Muestra lista de tablas para seleccionar"""
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            cursor = self.db_connection.serverdb.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE' 
                AND TABLE_NAME != 'sysdiagrams'
            """)
            tables = [row[0] for row in cursor.fetchall()]

            tk.Label(self.root, 
                    text=f"Seleccione una tabla para {action}",
                    font=("Arial", 14)).pack(pady=20)

            for table in tables:
                btn = tk.Button(
                    self.root,
                    text=table,
                    font=("Arial", 11),
                    width=25,
                    command=lambda t=table: self._manage_table(t, action)
                )
                btn.pack(pady=5)

            tk.Button(self.root, 
                    text="Volver", 
                    command=lambda: self._create_dba_interface(self.root),
                    bg="#2196F3", 
                    fg="white").pack(pady=20)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener las tablas: {str(e)}")
            self._create_dba_interface(self.root)

    def _manage_table(self, table_name, action):
        """Gestiona una tabla específica según la acción con manejo de tipos de datos"""
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            cursor = self.db_connection.serverdb.cursor()
            
            # Obtener columnas con sus tipos de datos
            cursor.execute(f"""
                SELECT 
                    COLUMN_NAME, 
                    DATA_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = ?
                ORDER BY ORDINAL_POSITION
            """, (table_name,))
            columns_info = {row[0]: row[1] for row in cursor.fetchall()}
            columns = list(columns_info.keys())

            tk.Label(self.root, 
                    text=f"{action.capitalize()} en tabla: {table_name}",
                    font=("Arial", 14)).pack(pady=10)

            # Treeview con scrollbars
            container = tk.Frame(self.root)
            container.pack(fill="both", expand=True, padx=10, pady=10)
            
            tree_scroll = ttk.Scrollbar(container)
            tree_scroll.pack(side="right", fill="y")

            tree = ttk.Treeview(container, columns=columns, show="headings",
                            yscrollcommand=tree_scroll.set)
            
            for col in columns:
                tree.heading(col, text=col.capitalize().replace('_', ' '))
                # Ajustar ancho según tipo de dato
                width = 100 if columns_info[col] in ['int', 'smallint', 'bigint'] else 150
                tree.column(col, width=width, anchor="w")

            tree.pack(fill="both", expand=True)
            tree_scroll.config(command=tree.yview)

            # Cargar datos con formato adecuado
            cursor.execute(f"SELECT * FROM {table_name}")
            for row in cursor.fetchall():
                formatted_row = []
                for i, value in enumerate(row):
                    col_type = columns_info[columns[i]]
                    if value is None:
                        formatted_row.append("NULL")
                    elif col_type in ['date', 'datetime', 'datetime2']:
                        formatted_row.append(value.strftime("%Y-%m-%d"))
                    elif col_type in ['int', 'smallint', 'bigint']:
                        formatted_row.append(str(value))
                    else:  # varchar, nvarchar, text, etc.
                        formatted_row.append(str(value))
                tree.insert("", "end", values=formatted_row)

            # Acciones específicas
            if action == 'agregar':
                self._create_add_form(tree, table_name, columns, columns_info)
            elif action == 'modificar':
                self._create_edit_form(tree, table_name, columns, columns_info)
            elif action == 'eliminar':
                delete_btn = tk.Button(
                    self.root,
                    text="Eliminar Seleccionado",
                    command=lambda: self._delete_record(tree, table_name, columns[0]),
                    bg="#D32F2F",
                    fg="white"
                )
                delete_btn.pack(pady=10)

            tk.Button(self.root, 
                    text="Volver", 
                    command=lambda: self._show_tables(action),
                    bg="#2196F3", 
                    fg="white").pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo gestionar la tabla: {str(e)}")
            self._show_tables(action)

    def _create_add_form(self, tree, table_name, columns):
        """Crea formulario para agregar registros"""
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        entries = {}
        for i, col in enumerate(columns):
            tk.Label(form_frame, text=col).grid(row=i, column=0, padx=5, pady=2)
            entry = tk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries[col] = entry

        def add_record():
            try:
                values = [entries[col].get() for col in columns]
                cursor = self.db_connection.serverdb.cursor()
                placeholders = ", ".join(["?"] * len(values))
                cursor.execute(f"""
                    INSERT INTO {table_name} ({", ".join(columns)})
                    VALUES ({placeholders})
                """, values)
                self.db_connection.serverdb.commit()
                messagebox.showinfo("Éxito", "Registro agregado correctamente")
                self._manage_table(table_name, 'visualizar')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar: {str(e)}")

        tk.Button(form_frame, 
                 text="Agregar", 
                 command=add_record,
                 bg="#4CAF50",
                 fg="white").grid(row=len(columns), columnspan=2, pady=10)

    def _create_edit_form(self, tree, table_name, columns, columns_info):
        """Crea formulario para editar registros con manejo de tipos de datos"""
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        entries = {}
        for i, col in enumerate(columns):
            tk.Label(form_frame, text=f"{col.capitalize().replace('_', ' ')}:").grid(row=i, column=0, padx=5, pady=2, sticky="e")
            
            col_type = columns_info[col]
            
            if col_type in ['date', 'datetime', 'datetime2']:
                # Campo de fecha con calendario
                entry = tk.Entry(form_frame)
                entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
                tk.Button(form_frame, text="📅", 
                        command=lambda e=entry: self._show_calendar(e)).grid(row=i, column=2)
            elif col_type in ['int', 'smallint', 'bigint']:
                # Spinbox para números enteros
                var = tk.StringVar()
                entry = tk.Spinbox(form_frame, from_=0, to=999999, textvariable=var, width=10)
                entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            elif 'varchar' in col_type or 'text' in col_type:
                # Campo de texto normal
                entry = tk.Entry(form_frame, width=30)
                entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            else:
                # Campo genérico para otros tipos
                entry = tk.Entry(form_frame, width=30)
                entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            
            entries[col] = entry

        def load_selected():
            selected = tree.focus()
            if not selected:
                return
            values = tree.item(selected)['values']
            for col, value in zip(columns, values):
                if value == "NULL":
                    entries[col].delete(0, tk.END)
                else:
                    entries[col].delete(0, tk.END)
                    entries[col].insert(0, value)

        def update_record():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un registro")
                return
            
            id_value = tree.item(selected)['values'][0]
            set_clause = []
            values = []
            
            for col in columns[1:]:  # Excluir la columna ID
                value = entries[col].get()
                col_type = columns_info[col]
                
                if value == "NULL":
                    set_clause.append(f"{col} = NULL")
                elif col_type in ['int', 'smallint', 'bigint']:
                    try:
                        set_clause.append(f"{col} = ?")
                        values.append(int(value))
                    except ValueError:
                        messagebox.showerror("Error", f"{col} debe ser un número entero")
                        return
                elif col_type in ['date', 'datetime', 'datetime2']:
                    try:
                        set_clause.append(f"{col} = ?")
                        values.append(datetime.strptime(value, "%Y-%m-%d").date())
                    except ValueError:
                        messagebox.showerror("Error", f"{col} debe tener formato AAAA-MM-DD")
                        return
                else:
                    set_clause.append(f"{col} = ?")
                    values.append(value)
            
            try:
                cursor = self.db_connection.serverdb.cursor()
                query = f"""
                    UPDATE {table_name}
                    SET {", ".join(set_clause)}
                    WHERE {columns[0]} = ?
                """
                cursor.execute(query, values + [id_value])
                self.db_connection.serverdb.commit()
                messagebox.showinfo("Éxito", "Registro actualizado")
                self._manage_table(table_name, 'visualizar')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {str(e)}")

        tree.bind("<ButtonRelease-1>", lambda e: load_selected())
        tk.Button(form_frame, 
                text="Actualizar", 
                command=update_record,
                bg="#FF9800",
                fg="white").grid(row=len(columns), columnspan=3, pady=10)

    def _delete_record(self, tree, table_name):
        """Elimina un registro seleccionado"""
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un registro")
            return
        
        id_value = tree.item(selected)['values'][0]
        
        if messagebox.askyesno("Confirmar", "¿Eliminar este registro?"):
            try:
                cursor = self.db_connection.serverdb.cursor()
                cursor.execute(f"""
                    DELETE FROM {table_name}
                    WHERE {tree['columns'][0]} = ?
                """, (id_value,))
                self.db_connection.serverdb.commit()
                messagebox.showinfo("Éxito", "Registro eliminado")
                self._manage_table(table_name, 'visualizar')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")

    def _show_reports(self):
        """Muestra menú de reportes gerenciales"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, 
                text="REPORTES GERENCIALES",
                font=("Arial", 14, "bold")).pack(pady=20)

        reports = [
            ("📊 Libros más prestados", self.mostrar_reporte_libros_mas_prestados),
            ("👥 Usuarios más activos", self.mostrar_reporte_usuarios_activos),
            ("📚 Stock por categoría", self.mostrar_reporte_categoria),
            ("⏳ Préstamos vencidos", self._show_overdue_loans)
        ]

        for text, command in reports:
            btn = tk.Button(self.root,
                          text=text,
                          width=25,
                          bg="#673AB7",
                          fg="white",
                          font=("Arial", 11),
                          command=command)
            btn.pack(pady=5)

        tk.Button(self.root, 
                 text="Volver", 
                 command=lambda: self._create_dba_interface(self.root),
                 bg="#2196F3", 
                 fg="white").pack(pady=20)

    def _show_overdue_loans(self):
        """Muestra reporte de préstamos vencidos"""
        cursor = self.pol.generar_reporte_prestamos_vencidos(self.db_connection)
        if cursor:
            self.pol.mostrar_resultados_reporte(self.root, cursor, "Préstamos Vencidos", 
                                               lambda: self._show_reports())

    def get_options_from_table(self, table_name, column_name):
        cursor = self.db_connection.serverdb.cursor()
        cursor.execute(f"SELECT {column_name} FROM {table_name}")
        return [row[0] for row in cursor.fetchall()]

    def get_id_for_name(self, table_name, name):
        cursor = self.db_connection.serverdb.cursor()
        if table_name == "libro":
            cursor.execute(f"SELECT libro_id FROM {table_name} WHERE titulo = ?", (name,))
        elif table_name == "bibliotecario":
            cursor.execute(f"SELECT bibliotecario_id FROM {table_name} WHERE nombre = ?", (name,))
        elif table_name == "tipo_texto":
            cursor.execute(f"SELECT tipo_texto_id FROM {table_name} WHERE nombre_tipo = ?", (name,))
        elif table_name == "categoria":
            cursor.execute(f"SELECT categoria_id FROM {table_name} WHERE nombre_categoria = ?", (name,))
        elif table_name == "autor":
            cursor.execute(f"SELECT autor_id FROM {table_name} WHERE nombre = ? AND apellido = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def call_registrar_libro_procedure(self, values):
        cursor = self.db_connection.serverdb.cursor()
        try:
            cursor.execute("EXEC Registrar_Libro @titulo=?, @anio_publicacion=?, @editorial=?, @tipo_texto_id=?, @categoria_id=?, @copias_totales=?, @nombre_autor=?, @apellido_autor=?", values)
            self.db_connection.serverdb.commit()
        except Exception as e:
            self.db_connection.serverdb.rollback()
            messagebox.showerror("Error", f"No se pudo registrar el libro: {e}")

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
        tk.Button(self.root, text="Volver", command=self.create_main_menu, bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=20)

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
            tk.Button(self.root, text="Volver", command=self.create_main_menu, bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=20)
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
        tk.Button(self.root, text="Volver", command=self.create_main_menu, bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=20)

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
        tk.Button(self.root, text="Volver", command=self.create_main_menu, bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=20)

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

    def volver_al_login(self):
        """Cierra la sesión actual y vuelve al login"""
        self.root.destroy()
        from main import main
        main()
