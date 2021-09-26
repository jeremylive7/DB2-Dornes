

-- select public.getPKName('public','aplicadores');
-- select public.genUpdate('public','aplicadores');
-- select public.genDelete('public','aplicadores');
-- select public.genSelect('public','aplicadores');




select public.getPKName('public','supercarros');
select public.genUpdate('public','supercarros');
select public.genDelete('public','supercarros');
select public.genSelect('public','supercarros');














--busqueda de la llave primaria para la tabla solicitantes
select public.getPKType('public', 'aplicadores')


 select  @v_KeyType = data_type from information_schema.columns  
	 WHERE table_schema = @p_schemaName 
	 AND table_name = @p_tableName and column_name = @v_keyColumnName;

--Procedimiento que devuelve los nombres de las columnas de una tabla determinada
CREATE OR REPLACE FUNCTION pruebas.getColumnNames(p_schemaName varchar, p_tableName varchar) 
returns REFCURSOR 
AS $$
DECLARE
	vColumnas REFCURSOR;
BEGIN
	OPEN vColumnas FOR
		SELECT column_name,data_type
		FROM information_schema.columns
		WHERE table_schema=p_schemaName and table_name = p_tableName;
	return vColumnas;
END;
$$ LANGUAGE PLPGSQL;
--
select pruebas.getColumnNames('pruebas', 'personas') ;

--lista las columnas de una tabla y las retorna en un string
CREATE OR REPLACE FUNCTION pruebas.listarColumnas(p_schemaName VARCHAR, p_tableName VARCHAR) 
RETURNS varchar 
AS 
$$
DECLARE
	vRegistro	RECORD;
	vColumnas	REFCURSOR;
	vLista 		varchar;
BEGIN
	vLista:= 'Select ';

	OPEN vColumnas FOR SELECT pruebas.getColumnNames(p_schemaName,p_tableName);
	FETCH vColumnas INTO vColumnas;
	LOOP
	    FETCH vColumnas INTO vRegistro;
		IF FOUND THEN
			vLista := vLista || vRegistro.column_name || ',';
		ELSE
			EXIT;
		END IF ;
	END LOOP ;
	CLOSE vColumnas;
	vLista := substring(vLista from 1 for length(vLista)-1);
	vLista := vLista || 'from ' || p_schemaName || '.' || p_tableName||';';
	return vLista;
END;
$$ 
LANGUAGE PLPGSQL ;
