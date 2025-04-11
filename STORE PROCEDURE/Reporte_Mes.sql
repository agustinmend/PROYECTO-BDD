--===========================================
--Author:       AGUSTIN MENDOZA
--Create date:  03-04-25
--Description:  OBTENER REPORTE MES
--===========================================
CREATE PROCEDURE Reporte_Mes
    @fecha DATE 
AS
BEGIN
	declare @ultimo_dia_mes date
	declare @primer_dia_mes date
	set @ultimo_dia_mes = EOMONTH(@fecha)
	set @primer_dia_mes = DATEADD(DAY, 1, EOMONTH(@fecha, -1))
	select p.prestamo_id ,dp.libro_id , u.usuario_id , u.nombre , u.apellido , p.fecha_prestamo , p.fecha_devolucion , p.estado, p.bibliotecario_id , dp.cantidad
	from detalle_prestamo as dp
	right join prestamo as p
	on p.prestamo_id = dp.prestamo_id
	inner join usuario as u
	on u.usuario_id = p.usuario_id
	where p.fecha_prestamo >= @primer_dia_mes
		and p.fecha_prestamo <= @ultimo_dia_mes
END

select *
from detalle_prestamo

select *
from prestamo

select *
from bibliotecario

select *
from usuario

