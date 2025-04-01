#CREAS LAS TABLAS CON LAS COLUMNAS A MYSQL, PERO VACIAS
def insertar_tabla(cursor,tabla,tipo_datos):
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {tabla} ({', '.join(tipo_datos)});")
    except Exception as e:
        print(f"Error in document insertar_datos, with creation of table, {str(e)}")
        return
#INSERTAS EL CONTENIDO DE SQLSERVER A LA TABLA CREADA DE MYSQL
def insertar_info(cursor,tabla,columnas,info):
    try:
        for row in info:
            placeholders = ", ".join(["%s"] * (len(row)+1))
            insert_query = f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES ({placeholders})"
            cursor.execute("SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s')")
            fecha_actual=cursor.fetchone()[0]
            cursor.execute(insert_query, tuple(row)+(fecha_actual,))
    except Exception as e:
        print(f"Error in document insertar_datos, with insertion of information, {str(e)}")
        return
    