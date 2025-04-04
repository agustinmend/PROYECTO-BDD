--TRIGER PARA AGREGAR LA FECHA DE DEVOLUCION DE FORMA AUTOMATICAMNTE

CREATE TRIGGER fecha_limite_devolucion
ON prestamo
AFTER INSERT
AS
BEGIN
    UPDATE prestamo
	SET estado = 'Activo',
    fecha_limite_devolucion = 
        CASE 
            WHEN MONTH(DATEADD(DAY, 14, p.fecha_prestamo)) = MONTH(p.fecha_prestamo)
            THEN DATEADD(DAY, 14, p.fecha_prestamo) 
            ELSE 
                DATEADD(DAY, 14, EOMONTH(p.fecha_prestamo, 0)) 
        END
    FROM prestamo p
    INNER JOIN INSERTED i ON p.prestamo_id = i.prestamo_id;
END;

SELECT * FROM PRESTAMO
insert into prestamo(usuario_id, fecha_prestamo,bibliotecario_id)VALUES(1,'2025-03-28',1)
SELECT * FROM prestamo
