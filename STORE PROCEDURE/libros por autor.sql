--CREADOR: AGUSTIN MENDOZA
--FECHA: 10-04-25
--DESCRIPCION: OBTIENE LOS LIBROS POR AUTOR
CREATE PROCEDURE ObtenerLibrosPorAutor
    @nombre NVARCHAR(100)
AS
BEGIN
    SELECT a.nombre + ' ' + a.apellido as Nombre_autor, l.titulo, l.anio_publicacion, l.editorial, c.nombre_categoria, t.nombre_tipo
    FROM Libro l
    inner join Libro_Autor as la
	on l.libro_id = la.libro_id
    inner join Autor as a 
	on la.autor_id = a.autor_id
    inner join Categoria as c 
	on l.categoria_id = c.categoria_id
    inner join Tipo_Texto as t
	on l.tipo_texto_id = t.tipo_texto_id
    where a.nombre Like '%' + @nombre + '%'
END;

select *
from autor
