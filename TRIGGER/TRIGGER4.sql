--TRIGGER PARA ACTUALIZAR EL STOCK LUEGO DE DEVOLVER

CREATE TRIGGER actualizar_stock2
ON prestamo
AFTER UPDATE
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM inserted i
        JOIN detalle_prestamo d ON i.prestamo_id = d.prestamo_id
        WHERE i.estado = 'devuelto'
    )
    BEGIN
        UPDATE l
        SET l.copias_totales = l.copias_totales + dp.cantidad
        FROM libro l
        INNER JOIN detalle_prestamo dp ON dp.libro_id = l.libro_id
        INNER JOIN inserted i ON i.prestamo_id = dp.prestamo_id
        WHERE i.estado = 'devuelto';
    END
END;

select * from prestamo
SELECT * FROM detalle_prestamo
select * from libro
update prestamo
set estado = 'Devuelto',
fecha_devolucion = GETDATE()
where prestamo_id = 13

select * from libro
