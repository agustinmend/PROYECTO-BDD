--AUTOR: AGUSTIN MENDOZA
--FECHA: 11-04-25
--DESCRIPCION: OBTENER PRESTAMOS ACTIVOS POR NOMBRE
CREATE PROCEDURE [dbo].[ObtenerPrestamosActivosPorNombre]
    @Nombre NVARCHAR(100)
AS
BEGIN
    SELECT p.prestamo_id, u.nombre + ' ' + u.apellido AS usuario, p.fecha_prestamo, p.estado
    FROM prestamo p
    INNER JOIN usuario u 
	ON p.usuario_id = u.usuario_id
    WHERE p.estado = 'Activo'
      AND (u.nombre LIKE '%' + @Nombre + '%' OR u.apellido LIKE '%' + @Nombre + '%')
END