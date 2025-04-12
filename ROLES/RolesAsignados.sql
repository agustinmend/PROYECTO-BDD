use[BibliotecaUniversitaria]
CREATE LOGIN login_dba WITH PASSWORD = 'dba123';
CREATE LOGIN login_gerente WITH PASSWORD = 'gerente123';
CREATE LOGIN login_vendedor WITH PASSWORD = 'vendedor123';

-- Usuario DBA 
CREATE USER usuario_dba FOR LOGIN login_dba;
EXEC sp_addrolemember 'db_owner', 'usuario_dba';

-- Usuario Gerente
CREATE USER usuario_gerente FOR LOGIN login_gerente;
EXEC sp_addrolemember 'db_datareader', 'usuario_gerente';

-- Usuario Vendedor 
CREATE USER usuario_vendedor FOR LOGIN login_vendedor;
EXEC sp_addrolemember 'db_datareader', 'usuario_vendedor'

GRANT SELECT, INSERT, UPDATE ON libro TO usuario_vendedor;
GRANT SELECT, INSERT, UPDATE ON autor TO usuario_vendedor;
GRANT SELECT, INSERT, UPDATE ON categoria TO usuario_vendedor;
GRANT SELECT, INSERT, UPDATE ON tipo_texto TO usuario_vendedor;
GRANT SELECT, INSERT, UPDATE ON prestamo TO usuario_vendedor;
GRANT SELECT, INSERT, UPDATE ON detalle_prestamo TO usuario_vendedor;
GRANT SELECT, INSERT, UPDATE ON libro_autor TO usuario_vendedor;
GRANT SELECT, INSERT, UPDATE ON usuario TO usuario_vendedor;
--dar permiso a vendedor para que ejecute sp
GRANT EXECUTE ON dbo.ObtenerLibrosPorAutor TO usuario_vendedor;
GRANT EXECUTE ON dbo.Registrar_Libro TO usuario_vendedor;
GRANT EXECUTE ON dbo.ObtenerPrestamosActivosPorNombre TO usuario_vendedor;
GRANT EXECUTE ON dbo.DevolverLibro TO usuario_vendedor;

SELECT name FROM sys.server_principals WHERE type = 'S';	

create view libros_mas_prestados as
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
