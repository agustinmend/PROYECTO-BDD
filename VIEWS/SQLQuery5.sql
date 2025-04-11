use[BibliotecaUniversitaria]
alter view Libros_disponibles as
select l.libro_id , l.titulo , c.nombre_categoria ,tp.nombre_tipo , l.editorial , l.copias_totales
from libro as l
inner join tipo_texto as tp
on l.tipo_texto_id = tp.tipo_texto_id
inner join categoria as c
on l.categoria_id = c.categoria_id
where l.copias_totales > 0

alter view Libros_mas_prestados as
select top 10 l.libro_id , l.titulo , c.nombre_categoria , tp.nombre_tipo ,l.editorial , sum(dp.cantidad) as prestamos
from libro as l
inner join detalle_prestamo as dp
on dp.libro_id = l.libro_id
inner join categoria as c
on c.categoria_id = l.categoria_id
inner join tipo_texto as tp
on l.tipo_texto_id = tp.tipo_texto_id
group by l.libro_id, l.titulo , c.nombre_categoria , tp.nombre_tipo ,l.editorial
order by prestamos desc


select titulo
from Libros_disponibles

select *
from Libros_mas_prestados

--otro
create view prestamos_activos as
select u.nombre + ' ' + u.apellido as Nombre , l.titulo, l.editorial , p.fecha_prestamo , p.fecha_limite_devolucion, p.estado
from prestamo as p
inner join usuario as u
on p.usuario_id = u.usuario_id
left join detalle_prestamo as dp
on p.prestamo_id = dp.prestamo_id
inner join libro as l
on dp.libro_id = l.libro_id
where p.estado = 'Activo'


select *
from prestamos_activos

select u.nombre + ' ' + u.apellido as Nombre 
from prestamo as p
inner join usuario as u
on p.usuario_id = u.usuario_id
where p.estado = 'Activo'
