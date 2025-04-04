--===========================================
--Author:       AGUSTIN MENDOZA
--Create date:  03-04-25
--Description:  Historial pedidos cliente
--===========================================
create procedure Historial_pedidos_cliente
	@clienteid int
as
begin
	select u.usuario_id , u.nombre , u.apellido , 
			u.correo , p.prestamo_id , p.fecha_prestamo , 
			p.fecha_devolucion , p.fecha_limite_devolucion , p.estado
	from usuario as u
	inner join prestamo as p
	on p.usuario_id = u.usuario_id
	where u.usuario_id = @clienteid
end