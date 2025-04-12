--AUTOR: AGUSTIN MENDOZA
--FECHA: 11-04-2025
--DESCRIPCION: DEVUELVE UN LIBRO PRESTADO

alter procedure DevolverLibro
	@prestamo_id INT
as
begin
	update prestamo
	set estado = 'Devuelto'
	where prestamo_id = @prestamo_id
end

select *
from prestamo