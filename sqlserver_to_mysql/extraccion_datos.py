#OBTIENES LOS NOMBRES DE LAS TABLAS
def obtener_tablas(cursor,base_datos):
        tablas = []
        try:
            if base_datos == "mysql":
                cursor.execute("SHOW TABLES;")
            else:
                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME !='sysdiagrams';")
            
            resultados = cursor.fetchall()
            for tabla in resultados:
                tablas.append(tabla[0])
            return tablas
        except Exception as e:
            print(f"error in obtener_tablas, {str(e)}")
            return 
#EXTRAES LA CANTIDAD DE LINEAS TOTALES DE UNA TABLA
def extraer_numero_registros(cursor,tabla):
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla};")
            numero_registros=cursor.fetchone()[0]

            return numero_registros
        except Exception as e:
            print(f"error in extraer_numero_registros, {str(e)}")
            return
#EXTRAES LOS NOMBRES DE LAS COLUMNAS DE UNA TABLA
def extraer_columnas(cursor,tabla,base_datos):
    try:
        if base_datos=="mysql":
            cursor.execute(f"SELECT * FROM {tabla} LIMIT 1;") #PARA TRAER SOLO LAS COLUMNAS
        else:
            cursor.execute(f"SELECT TOP 1 * FROM {tabla};")
        columnas = []
        for columna in cursor.description:
            columnas.append(columna[0])
        cursor.fetchall()
        return columnas

    except Exception as e:
        print("Error in extraction of columns")
        return
#EXTRAES EL CONTENIDO DE UNA TABLA
def extraer_info(cursor,tabla,base_datos):
    try:
        columnas=extraer_columnas(cursor,tabla,base_datos)
        if "fecha_modificacion" in columnas:
            columnas.remove("fecha_modificacion")
        columnas_query = ", ".join(columnas)
        cursor.execute(f"SELECT {columnas_query} FROM {tabla};")
        info = cursor.fetchall()
        return info        
            
    except Exception as e:
        print(f"error in extraer_info, {str(e)}")
        return
#EXTRAES LOS TIPOS DE DATO DE LAS COLUMNAS DE UNA TABLA CONCATENADO CON EL NOMBRE DE LAS COLUMNAS
def extraer_tipo_datos(cursor,tabla,base_datos):
    try:
        columnas=extraer_columnas(cursor,tabla,base_datos)
        tipo_datos=[]
        i=1
        for columna in cursor.description:
            if int == (columna[1]):
                tipo ="INT"
            elif str == (columna[1]):
                tipo="VARCHAR(255)"
            else:
                tipo="DATE"
            if i==1:
                tipo +=" AUTO_INCREMENT PRIMARY KEY"
                
            tipo_datos.append(f"{columna[0]} {tipo}")
            i +=1
        tipo_datos.append("fecha_modificacion DATETIME")
        return tipo_datos
    except Exception as e:
        print(f"Data type error, {str(e)}")
        return
