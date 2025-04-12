CREATE VIEW vista_prestamos_completa AS
SELECT 
    p.prestamo_id,
    u.correo AS correo_usuario,
    l.titulo AS libro,
    dp.cantidad,
    p.fecha_prestamo,
    p.fecha_devolucion,
    p.estado,
    CONCAT(b.nombre, ' ', b.apellido) AS bibliotecario,
    p.fecha_limite_devolucion
FROM prestamo p
JOIN usuario u ON p.usuario_id = u.usuario_id
JOIN detalle_prestamo dp ON p.prestamo_id = dp.prestamo_id
JOIN libro l ON dp.libro_id = l.libro_id
JOIN bibliotecario b ON p.bibliotecario_id = b.bibliotecario_id;

SELECT * FROM vista_prestamos_completa