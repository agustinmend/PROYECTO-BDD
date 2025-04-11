import pyodbc
from tkinter import messagebox

class Autenticacion:
    def __init__(self):
        self.server = 'AGUSTIN'
        self.database = 'BibliotecaUniversitaria'
        
    def verificar_credenciales(self, username, password):
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={username};"
                f"PWD={password};"
            )
            
            with pyodbc.connect(conn_str, timeout=10) as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT USER_NAME()")
                db_username = cursor.fetchone()[0]
                print(f"DEBUG - Usuario en BD: {db_username}")
                
                cursor.execute("SELECT IS_ROLEMEMBER('db_owner', ?)", db_username)
                dba_result = cursor.fetchone()[0]
                print(f"DEBUG - Resultado DBA: {dba_result}")
                
                if dba_result == 1:
                    return 'DBA'
                
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM (
                        SELECT p.permission_name, o.name AS table_name
                        FROM sys.database_permissions p
                        JOIN sys.objects o ON p.major_id = o.object_id
                        JOIN sys.database_principals dp ON p.grantee_principal_id = dp.principal_id
                        WHERE dp.name = ?
                        AND p.permission_name IN ('INSERT', 'UPDATE')
                        AND o.name IN ('prestamo', 'detalle_prestamo', 'libro', 'usuario')
                    ) AS permisos
                """, db_username)
                vendedor_count = cursor.fetchone()[0]
                print(f"DEBUG - Conteo VENDEDOR: {vendedor_count}")
                
                if vendedor_count >= 4:
                    return 'VENDEDOR'
                
                cursor.execute("SELECT IS_ROLEMEMBER('db_datareader', ?)", db_username)
                gerente_result = cursor.fetchone()[0]
                print(f"DEBUG - Resultado GERENTE: {gerente_result}")
                
                if gerente_result == 1:
                    return 'GERENTE'
                
                cursor.execute("""
                    SELECT r.name 
                    FROM sys.database_role_members rm
                    JOIN sys.database_principals r ON rm.role_principal_id = r.principal_id
                    JOIN sys.database_principals m ON rm.member_principal_id = m.principal_id
                    WHERE m.name = ?
                """, db_username)
                roles = [row[0] for row in cursor.fetchall()]
                print(f"DEBUG - Todos los roles asignados: {roles}")
                
                return None
                
        except Exception as e:
            print(f"DEBUG - Error completo: {str(e)}")
            messagebox.showerror("Error", f"Error de autenticación: {str(e)}")
            return None