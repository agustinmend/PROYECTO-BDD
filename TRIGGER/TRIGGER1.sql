--TRIGGER PARA VERIFICAR QUE EL CLIENTE NO DEBA LIBROS ANTES DE PEDIR OTRO

CREATE TRIGGER antes_de_insertar_pedido
ON prestamo
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1 
        FROM prestamo p
        INNER JOIN inserted i ON p.usuario_id = i.usuario_id
        WHERE p.estado = 'Activo'
    )
    BEGIN
		RAISERROR('El usuario tiene préstamos activos y no puede solicitar un nuevo préstamo',16,1)
	END
    ELSE
    BEGIN

        INSERT INTO prestamo (usuario_id, fecha_prestamo, fecha_devolucion, estado, fecha_limite_devolucion, bibliotecario_id)
        SELECT usuario_id, fecha_prestamo, fecha_devolucion, estado, fecha_limite_devolucion, bibliotecario_id
        FROM inserted;
    END
END;

SELECT * FROM PRESTAMO
insert into prestamo(usuario_id, fecha_prestamo,bibliotecario_id)VALUES(7,'2025-03-04',1)
SELECT * FROM prestamo
