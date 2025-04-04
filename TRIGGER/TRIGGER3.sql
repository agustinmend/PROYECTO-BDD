--TRIGGER MODIFICAR EL STOCK SEGUN LA NECESIDAD
create TRIGGER actualizar_stock
ON detalle_prestamo
AFTER INSERT
AS
BEGIN

    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN libro l ON i.libro_id = l.libro_id
        WHERE i.cantidad > l.copias_totales
    )
    BEGIN
        RAISERROR('La cantidad solicitada excede el stock disponible.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    UPDATE libro
    SET copias_totales = copias_totales - i.cantidad
    FROM libro l
    INNER JOIN inserted i ON l.libro_id = i.libro_id;
END;
