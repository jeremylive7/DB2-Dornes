
CREATE or alter FUNCTION dbo.update(@p_schemaName VARCHAR(Max),@p_nomTabla varchar(Max))
returns varchar(max)
begin
  declare @vSQL		varchar(max);
  declare @vLParamTipos varchar(max);
  declare @vLParam 	varchar(max);
  declare @vLColum 	varchar(max);
  declare @vNomTabla 	varchar(max) = '';
  declare @vNomColumna 	varchar(max);
  declare @vTipoDatos 	varchar(max);
  declare @procUpdate varchar(max);
  declare @vTipoParamPrimaryKey varchar(max);
  declare @vSetUpdates varchar(max);
  
  set @vSQL = '/*' + char(13)+ 'Procedimientos de inserci�n' + char(13) + 'Creado por: Ricardo soto' + char(13) + 'Instituo Tecnol�gico de Costa Rica, Unidad de Computaci�n' + char(13) + '*/'+ char(13)  
set @procUpdate= '/*' + char(13)+ 'Procedimientos de update' + char(13) + 'Creado por: Ricardo Soto' + char(13) + 'Instituo Tecnol�gico de Costa Rica, Unidad de Computaci�n' + char(13) + '*/' + char(13)

   declare vTablas cursor for   	
   SELECT table_name 
   from information_schema.tables
   where table_type='BASE TABLE' 
   and table_schema=@p_schemaName and table_name = @p_nomTabla;
   open vTablas;
   fetch next from vTablas into @vNomTabla	
   WHILE @@FETCH_STATUS = 0
   begin
    	If exists(SELECT table_name from information_schema.tables where table_type='BASE TABLE'and table_schema=@p_schemaName) 
	begin 
        	set @vSQL= @vSQL + '--Procedimiento de inserci�n para la tabla: ' + @vNomTabla + char(13);
        	set @vSQL= @vSQL + 'CREATE  procedure '+ @p_schemaName +'.ins_' + @vNomTabla +'(';			
		set @procUpdate =  @procUpdate + 'CREATE procedure ' + @p_schemaName +'.updt_'+  @vNomTabla+'(';
		declare vColumnas cursor FOR 
	  	select column_name,data_type 
	  	from information_Schema.columns
	  	where table_schema=@p_schemaName
	     and table_name=@vNomTabla;
		set @vLParamtipos='';
		set @vLParam='';
		set @vLColum='';
		set @vSetUpdates = '';
		open vColumnas;
	  	fetch next from vColumnas into @vNomColumna,@vTipoDatos
		WHILE @@FETCH_STATUS = 0
		begin
	    		IF exists (select column_name,data_type from information_Schema.columns where table_schema=@p_schemaName and table_name=@vNomTabla)
			begin 
	      		IF (@vLParamtipos<>'')
				begin
	        			set @vLParamTipos=@vLParamTipos + ', ';
	        			set @vLParam=@vLParam + ', ';
	        			set @vLColum=@vLcolum + ', ';
					set @vSetUpdates=@vSetUpdates + ', ';
					

	      		end
	      		set @vLParamTipos = @vLParamTipos +  '@p_' + @vNomColumna+ ' ' + @vTipoDatos;
	      		set @vLParam = @vLParam +  '@p_' + @vNomColumna;
	      		set @vLColum = @vLColum + @vNomColumna;
				set @vSetUpdates =@vSetUpdates +  @vNomColumna + '=' + '@p_' + @vNomColumna;

			end
			fetch next from vColumnas into @vNomColumna,@vTipoDatos

		end;
		close vColumnas
		deallocate vColumnas
			       		
	    		

	
		declare @nombreCampo varchar(max) = dbo.getPKName(@p_schemaName,@vNomTabla);
		declare @tipoCampo varchar(max) =dbo.getPKNameType(@p_schemaName,@vNomTabla)

		if not exists (select @nombreCampo)
		begin 
			set @nombreCampo = 'nullid';
			set @tipoCampo = 'varchar(10)'
		end

		set @vTipoParamPrimaryKey= '@p_PK_'+@nombreCampo;							
		
	
		set @procUpdate = @procUpdate + @vLParamTipos + ')' + char(13);
		set @procUpdate = @procUpdate + 'AS' + char(13) + 'BEGIN' + char(13);		
		set @procUpdate = @procUpdate + 'Update ' + @vNomTabla +' set ' + @vSetUpdates+char(13) + 'where '+@nombreCampo+
		'= '+'@p_'+@nombreCampo+';'+char(13)+'END;';			

     end;
	fetch next from vTablas into @vNomTabla	     
   end
   close vTablas
   deallocate vTablas
   set @vSQL= @vSQL +@procSelect +@procDelete + @procUpdate
   return @vSQL;
    
END;


