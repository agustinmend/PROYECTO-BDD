import pyodbc
from dataclasses import dataclass
from conexion import Conexiones

conexion_db=Conexiones()
conexion_db.conectar_sqlserver()
cursor_server=conexion_db.serverdb.cursor()
@dataclass
class Pruebas:
    mycursor:any
    cursor_server:any
    #TRANSFORMA UNA LISTA DE TUPLAS A UNA LISTA DE STRING PARA LA COMPARACION DEL ASSERT
    def lista_tuplas_a_string(self,info):
        try:
            informacion = []
            for fila in info:
                informacion.append(str(fila))
            return informacion
        except Exception as e:
            print(f"Error in document Pruebas, with the lista_tuplas_a_string,{str(e)}")
            return 
    #COMPRUEBA QUE LA CANTIDAD DE LINEAS EN SQLSERVER SEA LA MISMA QUE EN MYSQL
    def comprobar_registros(self, tabla):
        try:
            registros_mysql = extraer_numero_registros(self.mycursor,tabla)
            registros_sqlserver = extraer_numero_registros(self.cursor_server,tabla)
            assert registros_mysql == registros_sqlserver, f"Error en la tabla {tabla} en cantidad de registros"
            
        except Exception as e:
            print(f"Pruebas error in comprobar_numero_registros, {str(e)}")
            return
    #COMPRUEBA QUE LA INFORMACION DE UNA TABLA SEA IGUAL ENTRE SQLSERVER Y MYSQL
    def comprobar_contenido(self, tabla):
        try:
            # Extraer la información de ambas bases de datos
            info_mysql = extraer_info(self.mycursor, tabla,"mysql")
            info_mysql_transformada= self.lista_tuplas_a_string(info_mysql)
            info_sqlserver = extraer_info(self.cursor_server, tabla,"sqlserver")
            info_sqlserver_transformada= self.lista_tuplas_a_string(info_sqlserver)

            assert sorted(info_mysql_transformada) == sorted(info_sqlserver_transformada), f"Diferencia de contenido en tabla {tabla}"
        except Exception as e:
            print(f"Pruebas error in comprobar_contenido, {str(e)}")
            return 
    def comprobar_querys(self,query):
        try:
            self.mycursor.execute(query)
            resultado1=self.mycursor.fetchall()
            query1_resultado1=self.lista_tuplas_a_string(resultado1)

            self.cursor_server.execute(query)
            resultado2=self.cursor_server.fetchall()
            query1_resultado2=self.lista_tuplas_a_string(resultado2)

            assert sorted(query1_resultado1)==sorted(query1_resultado2), "Error en el caso de prueba 1"
        except Exception as e:
            print(f"Error in comprobar_query, {str(e)}")
    def casos_prueba(self):
        try:
            #LIBRO PRESTADO POR CADA USUARIO
            query1=""" 
            SELECT u.usuario_id, u.nombre, COUNT(dp.libro_id) AS total_libros_prestados
            FROM usuario u
            JOIN prestamo p ON u.usuario_id = p.usuario_id
            JOIN detalle_prestamo dp ON p.prestamo_id = dp.prestamo_id
            GROUP BY u.usuario_id, u.nombre
            ORDER BY total_libros_prestados DESC;
            """
            """
            Resultado:
            ["(1, 'Fernando', 5)", "(2, 'Carlos', 5)", "(3, 'Laura', 5)", "(4, 'José', 5)", "(5, 'María', 5)", "(6, 'Alfredo', 5)", "(7, 'Sofía', 5)", "(8, 'Andrés', 5)", 
            "(9, 'Paula', 5)", "(10, 'Luis', 5)"]
            """
            self.comprobar_querys(query1)
            #Prestamos realizados por biblitecarios
            query2="""
            SELECT b.bibliotecario_id, b.nombre, COUNT(p.prestamo_id) AS total_prestamos
            FROM bibliotecario b
            JOIN prestamo p ON b.bibliotecario_id = p.bibliotecario_id
            GROUP BY b.bibliotecario_id, b.nombre
            ORDER BY total_prestamos DESC;
            """
            """
            Resultado:
            ["(2, 'María', 16)", "(3, 'Carlos', 15)", "(1, 'Juan', 13)", "(4, 'Ana', 6)"]
            """
            self.comprobar_querys(query2)
            #LIBRO POR CATEGORIA Y AUTOR
            query3="""
            SELECT c.nombre_categoria AS categoria, a.nombre AS autor, COUNT(l.libro_id) AS total_libros
            FROM categoria c
            JOIN libro l ON c.categoria_id = l.categoria_id
            JOIN libro_autor la ON l.libro_id = la.libro_id
            JOIN autor a ON la.autor_id = a.autor_id
            GROUP BY c.nombre_categoria, a.nombre
            ORDER BY total_libros DESC;
            """
            """
            Resultado:
            ["('Arte', 'Albert', 1)", "('Cultura', 'Alice', 1)", "('Clasica', 'Carlos', 1)", 
            "('Tecnología', 'Charles', 1)", "('Geografía', 'Chuck', 1)",', 1)", "('Psicología', 'David', 1)", 
            "('Tecnología', 'Doris', 1)", "('Política', 'Edgar', 1)", "('Ficción', 'Eduardo', 1)", 
            "('Antropología'('Clasica', 'F. Scott', 1)", "('Clasica', 'Fernando', 1)", "('Ficción', 'Franz', 1)", 
            "('Realistico', 'Fyodor', 1)", "('Clasica', 'Gabriel', 1)", "('Clasica', 'Isabel', 1)", 
            "('Historia', 'J.K.', 1)", "('Salud', 'J.R.R.', 1)", "('Derecho', 'James', 1)", "('Salud', 'Jean-Paul', 1)", 
            "('Clasica'Isabel', 1)", "('Historia', 'J.K.', 1)", "('Salud', 'J.R.R.', 1)", "('Derecho', 'James', 1)", 
            "('Salud', 'Jean-Paul', 1)", "('Clas, 'John', 1)", "('Deportes', 'John', 1)", "('Realistico', 'John', 1)", 
            "('Ficción', 'Jorge', 1)", "('Derecho', 'Kurt', 1)", "('Investigacion', 'Kurt', 1'Economía', 'Margaret', 1)",
            "('Realistico', 'Mario', 1)", "('Ciencia', 'Mark', 1)", "('Arte', 'Octavio', 1)", "('Derecho', 'Pablo)", 
            "('Medicina', 'Leo', 1)", "('Economía', 'Margaret', 1)", "('Realistico', 'Mario', 1)", 
            "('Ciencia', 'Mark', 1)", "('Arte', 'Octavio', 1)"'Margaret', 1)", "('Realistico', 'Mario', 1)", 
            "('Ciencia', 'Mark', 1)", "('Arte', 'Octavio', 1)", "('Derecho', 'Pablo', 1)", "('Derecho', 'Rainer', 1)", 
            "('Clasica', 'Ray', 1)", "('Arte', 'Raymond', 1)", "('Matemáticas', 'Salman', 1)", 
            "('Filosofía', 'Stephen', 1)", "('Clasica', 'Toni', 1)", "('Derecho', 'Victor', 1)", 
            "('Educación', 'Virginia', 1)", "('Biología', 'William', 1)", "('Historia', 'William', 1)", 
            "('Infantil', 'Zadie', 1)"]
            """
            self.comprobar_querys(query3)
        except Exception as e:
            print(f"Error in casos_prueba, {str(e)}")

    #EJECUTA TODAS LAS PRUEBAS, COMPROBANDO CADA TABLA
    def ejecutar_pruebas(self):
        try:
            tablas_mysql = obtener_tablas(self.mycursor,"mysql")
            tablas_sqlserver = obtener_tablas(self.cursor_server,"sqlserver")
            if sorted(tablas_mysql)==sorted(tablas_sqlserver):
                for tabla in tablas_mysql:
                    self.comprobar_registros(tabla)
                    self.comprobar_contenido(tabla)
                    print(f"Tabla {tabla} realizado")
                self.casos_prueba()
                print("Casos de Prueba realizados")
            else:
                print("Number of tables test error")
        except Exception as e:
            print(f"Pruebas error in ejecutar_pruebas, {str(e)}")
            return

try:
    pruebas=Pruebas(mycursor,cursor_server)
    pruebas.ejecutar_pruebas()

except Exception as e:
    print(f"Pruebas Error, {str(e)}")
