from tkinter import messagebox
from datetime import datetime

def fetch_data(db_connection, tree, table_name):
    conn = db_connection.serverdb
    if not conn:
        messagebox.showerror("Error", "No hay conexión a la base de datos")
        return
        
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        tree.delete(*tree.get_children())
        
        for row in rows:
            formatted_row = []
            for value in row:
                if value is None:
                    formatted_row.append("")
                elif hasattr(value, 'strftime'):  # Para objetos de fecha
                    formatted_row.append(value.strftime("%Y-%m-%d"))
                else:
                    formatted_row.append(str(value))
            tree.insert("", "end", values=formatted_row)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo recuperar datos de {table_name}: {e}")

def add_data(db_connection, tree, table_name, columns, values):
    conn = db_connection.serverdb
    if not conn:
        return
    
    if table_name == "prestamo":
        try:
            fecha_prestamo_index = columns.index("fecha_prestamo")
            fecha_devolucion_index = columns.index("fecha_devolucion")
            fecha_limite_devolucion_index = columns.index("fecha_limite_devolucion")

            fecha_prestamo = datetime.strptime(values[fecha_prestamo_index], "%Y-%m-%d")
            fecha_devolucion = datetime.strptime(values[fecha_devolucion_index], "%Y-%m-%d")
            fecha_limite_devolucion = datetime.strptime(values[fecha_limite_devolucion_index], "%Y-%m-%d")

            if fecha_prestamo > fecha_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                return
            if fecha_prestamo > fecha_limite_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
            return
    
    values = [value if value and str(value).strip() else None for value in values]
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ? 
            AND COLUMN_NAME = 'fecha_modificacion'
        """, (table_name,))
        fecha_mod_exists = cursor.fetchone() is not None

        if fecha_mod_exists:
            columns.append('fecha_modificacion')
            values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        placeholders = ", ".join(["?"] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro agregado a {table_name}.")
        fetch_data(db_connection, tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el registro a {table_name}: {e}")

def delete_data(db_connection, tree, table_name, id_column):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona un registro para eliminar.")
        return
        
    confirm = messagebox.askquestion("Confirmación", "¿Estás seguro que deseas eliminar el registro?", icon='warning')
    if confirm != 'yes':
        return
        
    conn = db_connection.serverdb
    if not conn:
        return
        
    cursor = conn.cursor()
    try:
        record_id = tree.item(selected_item)["values"][0]
        query = f"DELETE FROM {table_name} WHERE {id_column} = ?"
        cursor.execute(query, (record_id,))
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro eliminado de {table_name}.")
        fetch_data(db_connection, tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el registro de {table_name}: {e}")

def update_data(db_connection, tree, table_name, columns, values, record_id):
    conn = db_connection.serverdb
    if not conn:
        return
    
    try:
        primary_key = f"{table_name}_id"

        if table_name == "prestamo":
            try:
                def validar_fecha(col_name):
                    if col_name in columns:
                        fecha_str = values[columns.index(col_name)]
                        return datetime.strptime(fecha_str, "%Y-%m-%d") if fecha_str and fecha_str.strip() else None
                    return None

                fecha_prestamo = validar_fecha("fecha_prestamo")
                fecha_devolucion = validar_fecha("fecha_devolucion")
                fecha_limite_devolucion = validar_fecha("fecha_limite_devolucion")

                if fecha_prestamo and fecha_devolucion and fecha_prestamo > fecha_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                    return

                if fecha_prestamo and fecha_limite_devolucion and fecha_prestamo > fecha_limite_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                    return

                if "estado" in columns and values[columns.index("estado")] == "Devuelto":
                    if not fecha_devolucion:
                        messagebox.showerror("Error", "La fecha de devolución no puede estar vacía si el estado es 'Devuelto'.")
                        return

            except ValueError as e:
                messagebox.showerror("Error", f"Formato de fecha inválido. Use AAAA-MM-DD. Detalle: {e}")
                return

        excluded_columns = [primary_key, 'fecha_modificacion']
        modifiable_columns = [col for col in columns if col not in excluded_columns]
        processed_values = [values[columns.index(col)] for col in modifiable_columns]

        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ? 
            AND COLUMN_NAME = 'fecha_modificacion'
        """, (table_name,))
        fecha_mod_exists = cursor.fetchone() is not None

        if fecha_mod_exists:
            modifiable_columns.append('fecha_modificacion')
            processed_values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        set_clause = ", ".join([f"{col} = ?" for col in modifiable_columns])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = ?"

        cursor.execute(query, processed_values + [record_id])
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro actualizado en {table_name}.")
        fetch_data(db_connection, tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el registro de {table_name}: {e}")