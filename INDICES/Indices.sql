-- INDICES
CREATE INDEX idx_prestamo_usuario ON prestamo(usuario_id);

SELECT p.prestamo_id, p.fecha_prestamo, p.estado, u.nombre, u.apellido
FROM prestamo p
INNER JOIN usuario u ON p.usuario_id = u.usuario_id
WHERE u.usuario_id = 10;

CREATE INDEX idx_libro_categoria ON libro(categoria_id);

SELECT l.libro_id, l.titulo, c.nombre_categoria, l.copias_totales
FROM libro l
JOIN categoria c ON l.categoria_id = c.categoria_id
ORDER BY l.copias_totales DESC;

CREATE INDEX idx_detalle_libro ON detalle_prestamo(libro_id);

SELECT l.titulo, COUNT(dp.detalle_id) AS total_prestamos
FROM detalle_prestamo dp
JOIN libro l ON dp.libro_id = l.libro_id
GROUP BY l.titulo
ORDER BY total_prestamos DESC
