--===========================================
--Author:       AGUSTIN MENDOZA
--Create date:  03-04-25
--Description:  REGISTRAR LIBRO
--===========================================
ALTER PROCEDURE Registrar_Libro
    @titulo VARCHAR(255),
    @anio_publicacion INT,
    @editorial VARCHAR(255),
    @tipo_texto_id INT,
    @categoria_id INT,
    @copias_totales INT,
    @nombre_autor VARCHAR(255),
    @apellido_autor VARCHAR(255)
AS
BEGIN
    DECLARE @libro_existente INT
    DECLARE @autor_existente INT
    DECLARE @libro_id INT
    DECLARE @autor_id INT

    BEGIN TRANSACTION
    BEGIN TRY
        IF @titulo IS NULL OR @titulo = ''
        BEGIN
            PRINT 'Error: Título vacío'
            ROLLBACK
            RETURN
        END
        
        IF @copias_totales <= 0
        BEGIN
            PRINT 'Error: El número de copias debe ser mayor a 0'
            ROLLBACK
            RETURN
        END

        SELECT @libro_existente = l.libro_id
        FROM libro AS l
        WHERE titulo = @titulo
            AND anio_publicacion = @anio_publicacion
            AND editorial = @editorial

        IF @libro_existente IS NOT NULL
        BEGIN
            UPDATE libro
            SET copias_totales = copias_totales + @copias_totales
            WHERE libro_id = @libro_existente
            COMMIT
            PRINT 'Libro actualizado con éxito.'
            RETURN
        END
        
        SELECT @autor_existente = a.autor_id
        FROM autor AS a
        WHERE nombre = @nombre_autor
            AND apellido = @apellido_autor

        IF @autor_existente IS NULL
        BEGIN
            INSERT INTO autor (nombre, apellido)
            VALUES (@nombre_autor, @apellido_autor)

            SET @autor_id = SCOPE_IDENTITY()
        END
        ELSE
        BEGIN
            SET @autor_id = @autor_existente
        END

        INSERT INTO libro (titulo, anio_publicacion, editorial, tipo_texto_id, categoria_id, copias_totales)
        VALUES (@titulo, @anio_publicacion, @editorial, @tipo_texto_id, @categoria_id, @copias_totales)
       
	    SET @libro_id = SCOPE_IDENTITY()

        INSERT INTO libro_autor (libro_id, autor_id)
        VALUES (@libro_id, @autor_id)
        
        COMMIT
        PRINT 'Libro registrado con éxito.'
    END TRY
    BEGIN CATCH
        ROLLBACK
        PRINT 'Error'
        RETURN
    END CATCH
END

select *
from libro

select *
from autor