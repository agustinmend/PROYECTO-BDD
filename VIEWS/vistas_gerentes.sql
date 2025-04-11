CREATE VIEW mostrar_usuarios_con_prestamo_activo AS
SELECT 
    u.nombre + ' ' + u.apellido as nombre,
    u.correo,
    u.tipo_usuario,
    u.carrera,
    p.fecha_prestamo,
	p.fecha_limite_devolucion,
	SUM(d.cantidad) AS cant_libros
FROM Usuario u
JOIN Prestamo p ON u.usuario_id = p.usuario_id
JOIN detalle_prestamo d ON d.prestamo_id = p.prestamo_id
WHERE p.estado = 'Activo'
GROUP BY
    u.nombre + ' ' + u.apellido,
    u.correo,
    u.tipo_usuario,
    u.carrera,
    p.fecha_prestamo,
	p.fecha_limite_devolucion;

CREATE VIEW usuarios_con_mas_prestamos AS
SELECT 
    u.usuario_id, 
    CONCAT(u.nombre, ' ', u.apellido) AS nombre, 
    COUNT(DISTINCT p.prestamo_id) AS cantidad_prestamos, 
    SUM(dp.cantidad) AS cantidad_libros
FROM Usuario u
LEFT JOIN prestamo p ON u.usuario_id = p.usuario_id
LEFT JOIN detalle_prestamo dp ON dp.prestamo_id = p.prestamo_id
GROUP BY u.usuario_id, CONCAT(u.nombre, ' ', u.apellido)
HAVING SUM(dp.cantidad) IS NOT NULL;

CREATE VIEW libros_por_categoria AS
SELECT 
    c.nombre_categoria,
    COUNT(l.libro_id) AS cantidad_de_titulos,
    SUM(l.copias_totales) AS total_stock
FROM libro l
LEFT JOIN categoria c ON c.categoria_id = l.categoria_id
GROUP BY c.nombre_categoria;


SELECT * 
                FROM libros_por_categoria
                ORDER BY total_stock DESC;