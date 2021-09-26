CREATE OR REPLACE FUNCTION public.getPKName(p_schemaName varchar, p_tableName varchar) 
returns varchar 
as 
$$
DECLARE
       v_keyColumnName varchar  ;
       v_ConstraintName varchar ;
BEGIN
     --selecciona el nombre de la restricción d ela llave primaria de la tabla indicada
     SELECT constraint_name
     FROM information_schema.table_constraints
     WHERE table_schema = p_schemaName AND table_name = p_tableName AND constraint_type='PRIMARY KEY'
     INTO v_ConstraintName ;

     --Si no lo encuentra: lanza una excepción 
     IF NOT FOUND THEN
        RAISE EXCEPTION 'No es posible determinar una llave primaria para esta tabla en este esquema.';
     ELSE
          --Captura el nombre de la columna con el nombre de la restricción obtenida anteriormente para la tabla buscada 
          SELECT column_name
          FROM information_schema.key_column_usage
          WHERE table_schema = p_schemaName AND table_name = p_tableName AND constraint_name = v_ConstraintName
          INTO v_keyColumnName ;
     END IF ;
     RETURN v_keyColumnName ;
END ;
$$ LANGUAGE PLPGSQL ;
--Procedimiento que busca la llave primaria de una tabla
CREATE OR REPLACE FUNCTION public.getPKType(p_schemaName varchar, p_tableName varchar) 
returns varchar 
as 
$$
DECLARE
       v_keyColumnName varchar  ;
       v_ConstraintName varchar ;
	   typeName varchar ;
BEGIN
     --selecciona el nombre de la restricción d ela llave primaria de la tabla indicada
     SELECT constraint_name
     FROM information_schema.table_constraints
     WHERE table_schema = p_schemaName AND table_name = p_tableName AND constraint_type='PRIMARY KEY'
     INTO v_ConstraintName ;

     --Si no lo encuentra: lanza una excepción 
     IF NOT FOUND THEN
        RAISE EXCEPTION 'No es posible determinar una llave primaria para esta tabla en este esquema.';
     ELSE
          --Captura el nombre de la columna con el nombre de la restricción obtenida anteriormente para la tabla buscada 
          SELECT column_name
          FROM information_schema.key_column_usage
          WHERE table_schema = p_schemaName AND table_name = p_tableName AND constraint_name = v_ConstraintName
          INTO v_keyColumnName ;
		 SELECT format_type(a.atttypid, a.atttypmod) AS data_type
		FROM pg_attribute a JOIN pg_class b ON a.attrelid = b.relfilenode
		WHERE a.attnum > 0 -- hide internal columns
		AND NOT a.attisdropped -- hide deleted columns
		AND b.oid =p_tableName ::regclass::oid and a.attname =v_keyColumnName  into typeName;
     END IF ;
     RETURN typeName ;
END ;
$$ LANGUAGE PLPGSQL ;

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




/*
Procedimiento almacenado que genera el código para la creación de 
procedimientos de inserción para todas la tabla recibida de parámetro
*/
CREATE OR REPLACE FUNCTION public.genInsProc(p_schemaName VARCHAR,pNomTable varchar) 
RETURNS varchar 
AS 
$$
DECLARE
  vTablas	REFCURSOR;
  vColumnas 	REFCURSOR;
  vSQL		varchar;
  vLParamTipos 	varchar;

  vLParam 	varchar;
  vLColum 	varchar;
  vNomTabla 	varchar;
  vNomColumna 	varchar;
  vTipoDatos 	varchar;
BEGIN
  vSQL:= '/*' || E'\n'|| 'Procedimientos de inserción' || E'\n' || 'Creado por: Msc Leonardo Víquez Acuña' || E'\n' || 'Instituo Tecnológico de Costa Rica, Unidad de Computación' || E'\n' || '*/' || E'\n\n\n';
  OPEN vTablas FOR 
    SELECT table_name 
    from information_schema.tables
    where table_type='BASE TABLE' 
          and table_schema='public' and table_name=pNomTable;;
    FETCH vTablas INTO vNomTabla;
    LOOP
      IF FOUND THEN
        vSQL:= vSQL || '--Procedimiento de inserción para la tabla: ' || vNomTabla || E'\n';
        vSQL:= vSQL || 'CREATE OR REPLACE FUNCTION '|| p_schemaName ||'.ins_' || vNomTabla ||'(';
	OPEN vColumnas FOR 	
	  select column_name,data_type 
	  from information_Schema.columns
	  where table_schema=p_schemaName
	        and table_name=vNomTabla;
	  vLParamtipos='';
	  vLParam='';
	  vLColum='';
	  FETCH vColumnas INTO vNomColumna,vTipoDatos;
	  LOOP
	    IF FOUND THEN
	      IF (vLParamtipos!='') THEN
	        vLParamTipos=vLParamTipos || ', ';
	        vLParam=vLParam || ', ';
	        vLColum=vLcolum || ', ';
	      END IF;
	      vLParamTipos = vLParamTipos ||  'p_' || vNomColumna|| ' ' || vTipoDatos;
	      vLParam = vLParam ||  'p_' || vNomColumna;
	      vLColum = vLColum || vNomColumna;
	    ELSE
	      EXIT;
	    END IF;
	    FETCH vColumnas INTO vNomColumna,vTipoDatos;
	END LOOP ;
	CLOSE vcolumnas;
	
	vSQL:= vSQL || vLParamTipos || ')' || E'\n';
	vSQL:= vSQL || 'RETURNS VOID' || E'\n' || 'AS' || E'\n' || E'\$\$' || E'\n' || 'BEGIN' || E'\n';
	vSQL:= vSQL || E'\t' || 'INSERT INTO ' || p_schemaName|| '.' || vNomTabla || '(' || vLColum || ')' || E'\n';
	vSQL:= vSQL || E'\t' || 'VALUES (' || vLParam || ');' ||  E'\n' || 'END' || E'\n' || E'\$\$' || E'\n' || 'LANGUAGE PLPGSQL;' || E'\n\n\n';
	
      ELSE
	EXIT;
      END IF ;
      FETCH vTablas INTO vNomTabla;
    END LOOP ;
    CLOSE vTablas;
  return vSQL;
END;
$$ 
LANGUAGE PLPGSQL ;


-- generacion para update

CREATE OR REPLACE FUNCTION public.genUpdate(p_schemaName VARCHAR,pNomTable varchar) 
RETURNS varchar 
AS 
$$
DECLARE
  vTablas	REFCURSOR;
  vColumnas 	REFCURSOR;
  vSQL		varchar;
  vLParamTipos 	varchar;

  vLParam 	varchar;
  vLColum 	varchar;
  vNomTabla 	varchar;
  vNomColumna 	varchar;
  vTipoDatos 	varchar;
  nombreCampo varchar;
  tipoCampo varchar;
BEGIN
  vSQL:= '/*' || E'\n'|| '' || E'\n' || 'Creado por: ' || E'\n' || 'Instituo Tecnológico de Costa Rica, Unidad de Computación' || E'\n' || '*/' || E'\n\n\n';
  OPEN vTablas FOR 
    SELECT table_name 
    from information_schema.tables
    where table_type='BASE TABLE' 
          and table_schema=p_schemaName and table_name=pNomTable;
    FETCH vTablas INTO vNomTabla;
    LOOP
      IF FOUND THEN
        vSQL:= vSQL || '--Procedimiento de update  para la tabla: ' || vNomTabla || E'\n';
        vSQL:= vSQL || 'CREATE OR REPLACE FUNCTION '|| p_schemaName ||'.ins_' || vNomTabla ||'(';
	OPEN vColumnas FOR 	
	  select column_name,data_type 
	  from information_Schema.columns
	  where table_schema=p_schemaName
	        and table_name=vNomTabla;
	  vLParamtipos='';
	  vLParam='';
	  vLColum='';
	  FETCH vColumnas INTO vNomColumna,vTipoDatos;
	  LOOP
	    IF FOUND THEN
	      IF (vLParamtipos!='') THEN
	        vLParamTipos=vLParamTipos || ', ';
	        vLParam=vLParam || ', ';
	        vLColum=vLcolum || ', ';
	      END IF;
	      vLParamTipos = vLParamTipos ||  'p_' || vNomColumna|| ' ' || vTipoDatos;
	      vLParam = vLParam ||  'p_' || vNomColumna;
	      vLColum = vLColum || vNomColumna;
	    ELSE
	      EXIT;
	    END IF;
	    FETCH vColumnas INTO vNomColumna,vTipoDatos;
	END LOOP ;
	CLOSE vcolumnas;
 	nombreCampo= public.getPKName(p_schemaName,vNomTabla);
	tipoCampo =public.getPKType(p_schemaName,vNomTabla);

	vSQL:= vSQL || vLParamTipos || ' '||'p_'||nombreCampo||' '||tipoCampo|| ')' || E'\n';
	vSQL:= vSQL || 'RETURNS VOID' || E'\n' || 'AS' || E'\n' || E'\$\$' || E'\n' || 'BEGIN' || E'\n';
	vSQL:= vSQL || E'\t' || 'update ' || p_schemaName|| '.' || vNomTabla || ' set '||' ' || vLColum || ' ' || E'\n';
	vSQL:= vSQL || E'\t' || '= ' || vLParam||' where '||nombreCampo||'='||'p_'||nombreCampo || ' ;' ||  E'\n' || 'END' || E'\n' || E'\$\$' || E'\n' || 'LANGUAGE PLPGSQL;' || E'\n\n\n';
	
      ELSE
	EXIT;
      END IF ;
      FETCH vTablas INTO vNomTabla;
    END LOOP ;
    CLOSE vTablas;
  return vSQL;
END;
$$ 
LANGUAGE PLPGSQL ;
CREATE OR REPLACE FUNCTION public.genDelete(p_schemaName VARCHAR,pNomTable varchar) 
RETURNS varchar 
AS 
$$
DECLARE
  vTablas	REFCURSOR;
  vColumnas 	REFCURSOR;
  vSQL		varchar;
  vLParamTipos 	varchar;

  vLParam 	varchar;
  vLColum 	varchar;
  vNomTabla 	varchar;
  vNomColumna 	varchar;
  vTipoDatos 	varchar;
  nombreCampo varchar;
  tipoCampo varchar;
BEGIN
  vSQL:= '/*' || E'\n'|| 'Procedimientos de delete' || E'\n' || 'Creado por: Msc Leonardo Víquez Acuña' || E'\n' || 'Instituo Tecnológico de Costa Rica, Unidad de Computación' || E'\n' || '*/' || E'\n\n\n';
  OPEN vTablas FOR 
    SELECT table_name 
    from information_schema.tables
    where table_type='BASE TABLE' 
          and table_schema=p_schemaName and table_name=pNomTable;
    FETCH vTablas INTO vNomTabla;
    LOOP
      IF FOUND THEN
        vSQL:= vSQL || '--Procedimiento de delete para la tabla: ' || vNomTabla || E'\n';
        vSQL:= vSQL || 'CREATE OR REPLACE FUNCTION '|| p_schemaName ||'.ins_' || vNomTabla ||'(';
	OPEN vColumnas FOR 	
	  select column_name,data_type 
	  from information_Schema.columns
	  where table_schema=p_schemaName
	        and table_name=vNomTabla;
	  vLParamtipos='';
	  vLParam='';
	  vLColum='';
	  FETCH vColumnas INTO vNomColumna,vTipoDatos;
	  LOOP
	    IF FOUND THEN
	      IF (vLParamtipos!='') THEN
	        vLParamTipos=vLParamTipos || ', ';
	        vLParam=vLParam || ', ';
	        vLColum=vLcolum || ', ';
	      END IF;
	      vLParamTipos = vLParamTipos ||  'p_' || vNomColumna|| ' ' || vTipoDatos;
	      vLParam = vLParam ||  'p_' || vNomColumna;
	      vLColum = vLColum || vNomColumna;
	    ELSE
	      EXIT;
	    END IF;
	    FETCH vColumnas INTO vNomColumna,vTipoDatos;
	END LOOP ;
	CLOSE vcolumnas;
 	nombreCampo= public.getPKName(p_schemaName,vNomTabla);
	tipoCampo =public.getPKType(p_schemaName,vNomTabla);

	vSQL:= vSQL || vLParamTipos || ' '||'p_'||nombreCampo||' '||tipoCampo|| ')' || E'\n';
	vSQL:= vSQL || 'RETURNS VOID' || E'\n' || 'AS' || E'\n' || E'\$\$' || E'\n' || 'BEGIN' || E'\n';
	vSQL:= vSQL || E'\t' || 'delete from ' || p_schemaName|| '.' || vNomTabla || E'\n';
	vSQL:= vSQL || E'\t' || ' where '||nombreCampo||'='||'p_'||nombreCampo || ' ;' ||  E'\n' || 'END' || E'\n' || E'\$\$' || E'\n' || 'LANGUAGE PLPGSQL;' || E'\n\n\n';
	
      ELSE
	EXIT;
      END IF ;
      FETCH vTablas INTO vNomTabla;
    END LOOP ;
    CLOSE vTablas;
  return vSQL;
END;
$$ 
LANGUAGE PLPGSQL ;

CREATE OR REPLACE FUNCTION public.genSelect(p_schemaName VARCHAR,pNomTable varchar) 
RETURNS varchar 
AS 
$$
DECLARE
  vTablas	REFCURSOR;
  vColumnas 	REFCURSOR;
  vSQL		varchar;
  vLParamTipos 	varchar;

  vLParam 	varchar;
  vLColum 	varchar;
  vNomTabla 	varchar;
  vNomColumna 	varchar;
  vTipoDatos 	varchar;
  nombreCampo varchar;
  tipoCampo varchar;
BEGIN
  vSQL:= '/*' || E'\n'|| 'Procedimientos de select' || E'\n' || 'Creado por: Msc Leonardo Víquez Acuña' || E'\n' || 'Instituo Tecnológico de Costa Rica, Unidad de Computación' || E'\n' || '*/' || E'\n\n\n';
  OPEN vTablas FOR 
    SELECT table_name 
    from information_schema.tables
    where table_type='BASE TABLE' 
          and table_schema=p_schemaName and table_name=pNomTable;
    FETCH vTablas INTO vNomTabla;
    LOOP
      IF FOUND THEN
        vSQL:= vSQL || '--Procedimiento de select para la tabla: ' || vNomTabla || E'\n';
        vSQL:= vSQL || 'CREATE OR REPLACE FUNCTION '|| p_schemaName ||'.ins_' || vNomTabla ||'(';
	OPEN vColumnas FOR 	
	  select column_name,data_type 
	  from information_Schema.columns
	  where table_schema=p_schemaName
	        and table_name=vNomTabla;
	  vLParamtipos='';
	  vLParam='';
	  vLColum='';
	  FETCH vColumnas INTO vNomColumna,vTipoDatos;
	  LOOP
	    IF FOUND THEN
	      IF (vLParamtipos!='') THEN
	        vLParamTipos=vLParamTipos || ', ';
	        vLParam=vLParam || ', ';
	        vLColum=vLcolum || ', ';
	      END IF;
	      vLParamTipos = vLParamTipos ||  'p_' || vNomColumna|| ' ' || vTipoDatos;
	      vLParam = vLParam ||  'p_' || vNomColumna;
	      vLColum = vLColum || vNomColumna;
	    ELSE
	      EXIT;
	    END IF;
	    FETCH vColumnas INTO vNomColumna,vTipoDatos;
	END LOOP ;
	CLOSE vcolumnas;
 	nombreCampo= public.getPKName(p_schemaName,vNomTabla);
	tipoCampo =public.getPKType(p_schemaName,vNomTabla);

	vSQL:= vSQL || vLParamTipos || ' '||'p_'||nombreCampo||' '||tipoCampo|| ')' || E'\n';
	vSQL:= vSQL || 'RETURNS VOID' || E'\n' || 'AS' || E'\n' || E'\$\$' || E'\n' || 'BEGIN' || E'\n';
	vSQL:= vSQL || E'\t' || 'select ' ||vLColum||' from '|| p_schemaName|| '.' || vNomTabla || E'\n';
	vSQL:= vSQL || E'\t' || ' where '||nombreCampo||'='||'p_'||nombreCampo || ' ;' ||  E'\n' || 'END' || E'\n' || E'\$\$' || E'\n' || 'LANGUAGE PLPGSQL;' || E'\n\n\n';
	
      ELSE
	EXIT;
      END IF ;
      FETCH vTablas INTO vNomTabla;
    END LOOP ;
    CLOSE vTablas;
  return vSQL;
END;
$$ 
LANGUAGE PLPGSQL ;


select  public.getPKName('public','aplicadores');
select public.genUpdate('public','aplicadores');
select public.genDelete('public','aplicadores');
select public.genSelect('public','aplicadores');