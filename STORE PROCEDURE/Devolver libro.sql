--AUTOR: AGUSTIN MENDOZA
--FECHA: 11-04-2025
--DESCRIPCION: DEVUELVE UN LIBRO PRESTADO

--AUTOR: ARIANY LOPEZ
--FECHA: 11-04-2025
--DESCRIPCION: MODIFICACION CON FECHA DEVOLUCION 

ALTER PROCEDURE DevolverLibro
    @prestamo_id INT
AS
BEGIN
    UPDATE prestamo
    SET estado = 'Devuelto',
        fecha_devolucion = GETDATE()
    WHERE prestamo_id = @prestamo_id
END;


select *
from prestamo