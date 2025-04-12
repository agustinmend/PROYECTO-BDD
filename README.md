# Sistema de Gestión de Biblioteca Universitaria
Documentacion del Proyecto: https://docs.google.com/document/d/1badtp8cm4XjZkvnguIqoesS3zT_rXq2XExLZC_pL1Z8/edit?usp=sharing
## Credenciales de los Roles:

### Rol Vendedor: 
*Usuario*: login_vendedor
*Contraseña*: vendedor123
### Rol Gerente: 
*Usuario*: login_gerente
*Contraseña*: gerente123
### Rol DBA: 
*Usuario*: login_dba
*Contraseña*: dba123

## Descripción
Sistema completo para la gestión de bibliotecas universitarias con:

- Autenticación por roles (DBA, Gerente, Vendedor)
- Operaciones CRUD para libros, préstamos y usuarios
- Reportes gerenciales automatizados
- Interfaz gráfica intuitiva con Tkinter
- Triggers
- Stored Procedures
- Indices
- Vistas

## Componentes

| Carpeta              | Contenido                                        |
|----------------------|--------------------------------------------------|
| indices/             | Indices para optimizar consultas                 |
| roles/               | Scripts de creacion roles y permisos             |
| stored_procedure/    | Procedimientos Almacenados                       |
| triggers/            | Triggers para integridad de datos                |
| vistas/              | Vistas para reportes                             |

## Estructura del Proyecto

biblioteca-universitaria/

├── interfaz/

│   ├── conexion_sqlserver/

│   │   └── conexion.py

│   ├── interfaz/

│   │   ├── autenticacion.py

│   │   └── biblioteca_app.py

│   └── main.py

├── indices/

│   ├── indices.sql/

├── roles/

│   ├── RolesAsignados.sql/

├── stored_procedure/

│   └── Historial_pedidos_clientes.sql/

│   └── Llamadas_sp.sql/

│   └── Registrar_Libros.sql/

│   └── Reporte_Mes.sql/

├── trigger/

│   └── trigger1.sql/

│   └── trigger2.sql/

│   └── trigger3.sql/

│   └── trigger4.sql/

├── views/

│   └── vista.sql/


## Roles y Permisos:

El sistema implementa tres roles con distintos niveles de acceso:

1. DBA (Administrador):

- Acceso completo a todas las tablas

- Permisos de CRUD completos

- Acceso a reportes

2. Gerente:

- Solo visualización de datos

- Acceso a reportes gerenciales:

  * Libros más prestados

  *Detalle de préstamos

3. Vendedor:

- Operaciones CRUD (sin eliminar)

- Acceso limitado a tablas específicas
