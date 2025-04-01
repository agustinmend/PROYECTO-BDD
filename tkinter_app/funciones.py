from tkinter import messagebox
from datetime import datetime

# Visualizar Datos: Recupera y muestra todos los registros de una tabla específica
def fetch_data(db_connection, tree, table_name):
    conn=db_connection.mydb
    if not conn:
        return
    cursor=conn.cursor()
    try:
        # Ejecución de consulta para seleccionar todos los registros de la tabla especificada.
        cursor.execute(f"SELECT * FROM {table_name}")
        rows=cursor.fetchall()
        # Limpia el árbol de datos para evitar duplicados
        tree.delete(*tree.get_children())
        # Inserta los registros recuperados 
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo recuperar datos de {table_name}: {e}")
    finally:
        pass

# Añadir datos: Agrega un nuevo registro a la tabla especificada en la base de datos.
def add_data(db_connection, tree, table_name, columns, values):
    conn=db_connection.mydb
    if not conn:
        return
    
    # Validación para la tabla Prestamo
    if table_name=="prestamo":
        try:
            # Obtiene los índices de las columnas relacionadas con fechas
            fecha_prestamo_index=columns.index("fecha_prestamo")
            fecha_devolucion_index=columns.index("fecha_devolucion")
            fecha_limite_devolucion_index=columns.index("fecha_limite_devolucion")

            # Conversión de fechas: string a datetime para validar
            fecha_prestamo=datetime.strptime(values[fecha_prestamo_index], "%Y-%m-%d")
            fecha_devolucion=datetime.strptime(values[fecha_devolucion_index], "%Y-%m-%d")
            fecha_limite_devolucion=datetime.strptime(values[fecha_limite_devolucion_index], "%Y-%m-%d")

            # Reglas de validación de fechas
            if fecha_prestamo>fecha_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                return
            if fecha_prestamo>fecha_limite_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
            return
    
    # Remplaza valores vacíos por None-NULL
    values=[value if value.strip() else None for value in values]
    cursor=conn.cursor()
    try:
        # Verificar si la tabla tiene columna fecha_modificacion
        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'fecha_modificacion'")
        fecha_mod_exists=cursor.fetchone() is not None

        if fecha_mod_exists:
            # Agregar fecha_modificacion automáticamente
            columns.append('fecha_modificacion')
            values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        placeholders=", ".join(["%s"] * len(values))
        query=f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro agregado a {table_name}.")
        fetch_data(db_connection, tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el registro a {table_name}: {e}")
    finally:
        pass

# Eliminar datos: Elimina un registro específico de la tabla en función del ID proporcionado
def delete_data(db_connection, tree, table_name, id_column):
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona un registro para eliminar.")
        return
    # Mensaje de Confirmación eliminar registro
    confirm=messagebox.askquestion("Confirmación", "¿Estás seguro que deseas eliminar el registro?", icon='warning')
    if confirm != 'yes':
        return
    conn=db_connection.mydb
    if not conn:
        return
    cursor=conn.cursor()
    try:
        record_id=tree.item(selected_item)["values"][0]
        query=f"DELETE FROM {table_name} WHERE {id_column} = %s"
        cursor.execute(query, (record_id,))
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro eliminado de {table_name}.")
        fetch_data(db_connection, tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el registro de {table_name}: {e}")
    finally:
        pass

# Modificar datos: Actualiza un registro existente en la base de datos.
def update_data(db_connection, tree, table_name, columns, values, record_id):
    conn = db_connection.mydb
    if not conn:
        return

    try:
        # Generar el nombre de la clave primaria basado en el patrón [table_name]_id
        primary_key=f"{table_name}_id"

        # Validación específica para la tabla "prestamo"
        if table_name=="prestamo":
            try:
                # Validar formato de fecha solo si las columnas están presentes y tienen valores
                def validar_fecha(col_name):
                    if col_name in columns:
                        fecha_str=values[columns.index(col_name)]
                        return datetime.strptime(fecha_str, "%Y-%m-%d") if fecha_str.strip() else None
                    return None

                fecha_prestamo=validar_fecha("fecha_prestamo")
                fecha_devolucion=validar_fecha("fecha_devolucion")
                fecha_limite_devolucion=validar_fecha("fecha_limite_devolucion")

                # Validar lógica de fechas solo si las fechas están presentes
                if fecha_prestamo and fecha_devolucion and fecha_prestamo>fecha_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                    return

                if fecha_prestamo and fecha_limite_devolucion and fecha_prestamo>fecha_limite_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                    return

                # Validar estado: si "Devuelto", la fecha de devolución es obligatoria
                if "estado" in columns and values[columns.index("estado")]=="Devuelto":
                    if not fecha_devolucion:
                        messagebox.showerror("Error", "La fecha de devolución no puede estar vacía si el estado es 'Devuelto'.")
                        return

            except ValueError as e:
                messagebox.showerror("Error", f"Formato de fecha inválido. Use AAAA-MM-DD. Detalle: {e}")
                return

        # Excluir las columnas que no se deben modificar
        excluded_columns=[primary_key, 'fecha_modificacion']
        modifiable_columns=[col for col in columns if col not in excluded_columns]
        processed_values=[values[columns.index(col)] for col in modifiable_columns]

        cursor=conn.cursor()

        # Verificar si la tabla tiene columna fecha_modificacion
        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'fecha_modificacion'")
        fecha_mod_exists=cursor.fetchone() is not None

        if fecha_mod_exists:
            # Agregar fecha_modificacion automáticamente
            modifiable_columns.append('fecha_modificacion')
            processed_values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Construir consulta SQL dinámicamente
        set_clause=", ".join([f"{col} = %s" for col in modifiable_columns])
        query=f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = %s"

        # Ejecutar la consulta con los valores procesados y el ID
        cursor.execute(query, processed_values+[record_id])
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro actualizado en {table_name}.")
        fetch_data(db_connection, tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el registro de {table_name}: {e}")
    finally:
        pass