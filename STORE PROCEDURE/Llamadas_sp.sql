use[BibliotecaUniversitaria]
EXEC Registrar_Libro 
    @titulo = 'Probando',
    @anio_publicacion = 2023,
    @editorial = 'Editorial ABC',
    @tipo_texto_id = 1,
    @categoria_id = 2, 
    @copias_totales = 10,
    @nombre_autor = 'Juan',
    @apellido_autor = 'Pérez';

EXEC Reporte_Mes @fecha = '2024-05-15';
exec Historial_pedidos_cliente @clienteid = 7

select *
from prestamo

select *
from libro

select * 
from libro_autor

select *
from autor

select *
from categoria

select *
from tipo_texto