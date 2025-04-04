import pyodbc
from dataclasses import dataclass
from tkinter import messagebox

@dataclass
class Conexiones:
    serverdb: pyodbc.Connection = None
    current_user: str = None
    current_role: str = None

    def conectar_sqlserver(self, username: str, password: str, rol: str):
        server = 'LENOVO1023'
        database = 'BibliotecaUniversitaria'
        
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password};"
            )
            self.serverdb = pyodbc.connect(conn_str)
            self.current_user = username
            self.current_role = rol 
            
            if not self._verificar_permisos_reales():
                messagebox.showerror("Error", "Los permisos reales no coinciden con el rol asignado")
                return None
                
            return self.serverdb
            
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {e}")
            self.serverdb = None
            return None

    def _verificar_permisos_reales(self):
        try:
            cursor = self.serverdb.cursor()
            
            if self.current_role == 'DBA':
                cursor.execute("SELECT IS_ROLEMEMBER('db_owner', USER_NAME())")
                return cursor.fetchone()[0] == 1
                
            elif self.current_role == 'VENDEDOR':
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.TABLE_PRIVILEGES 
                    WHERE GRANTEE = USER_NAME()
                    AND PRIVILEGE_TYPE IN ('INSERT', 'UPDATE')
                    AND TABLE_NAME IN ('prestamo', 'detalle_prestamo', 'libro', 'usuario')
                """)
                return cursor.fetchone()[0] >= 4
                
            elif self.current_role == 'GERENTE':
                cursor.execute("SELECT IS_ROLEMEMBER('db_datareader', USER_NAME())")
                return cursor.fetchone()[0] == 1
                
            return False
            
        except:
            return False
    def cerrar_conexiones(self):
        if self.serverdb:
            self.serverdb.close()
            self.serverdb = None