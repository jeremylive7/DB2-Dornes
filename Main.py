import tkinter as tk
from tkinter import ttk 
import psycopg2

"""
Accion del boton para decidir que motor de db va usar y 
    que tabla va usar junto con cuales acciones va hacerse del CRUD.
"""
def submitact():
    #Primera dicision.
    #Que va db usar.
    valor_combox1 = c1.get()
    if valor_combox1 == "SQL SERVER":
        # SQL
        print('SQL SERVER')
    elif valor_combox1 == "POSTGRESQL":
        # Postgres
        user = "postgres"
        passw = "1234"
        name = "postgres"
        host1 = "localhost"
        logPosgtre(user,passw,name,host1)


"""
Metodo para obtener de la base que se va trabajar las tablas existentes.
Las muestra en el comboBox.
"""
def logPosgtre(user, pas, name, host):

    conn = psycopg2.connect(dbname =name, user = user, password = pas, host = host )
    cur = conn.cursor()
        
    cur.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")

    for table in cur.fetchall():
        tables.append(table)

    c2['values'] = tables
    c2['state'] = 'readonly' 
    c2.pack(fill='x', padx=5, pady=5)

    showCheckBoxs()

    # Boton para procesar consultas
    submitbtn = tk.Button(root, text ="Tables",
                        bg ='red', command = submitact2)
    submitbtn.place(x = 215, y = 170, width = 55)


"""
Accion para mostrar los checkboxs.
"""
def showCheckBoxs():
    #Segunda accion.
    #Que acciones del CRUD van hacerse.
    p1 = tk.Checkbutton(root, text='Create',variable=var1, onvalue=1, offvalue=0)
    p1.pack()
    p2 = tk.Checkbutton(root, text='Read',variable=var2, onvalue=1, offvalue=0)
    p2.pack()
    p3 = tk.Checkbutton(root, text='Update',variable=var3, onvalue=1, offvalue=0)
    p3.pack()
    p4 = tk.Checkbutton(root, text='Delete',variable=var4, onvalue=1, offvalue=0)
    p4.pack()

"""
Accion del segundo boton para obtener que eligio el usaurio exactamente del CRUD y tabla.
"""
def submitact2():
    valor_combox2 = c2.get()

    if var1.get() == 1:
        command1 = "select public.genInsProc('public','"
        command1 += valor_combox2
        command1 += "');"

        #cur.execute(command1)

        comandos.append(command1)

        resultado.append(create)
    
    if var2.get() == 1:
        command2 = "select public.genSelect('public','"
        command2 += valor_combox2
        command2 += "');"

        #cur.execute(command2)

        comandos.append(command2)

        resultado.append(read)
    
    if var3.get() == 1:
        command3 = "select public.genUpdate('public','"
        command3 += valor_combox2
        command3 += "');"

        #cur.execute(command3)

        comandos.append(command3)

        resultado.append(update)

    if var4.get() == 1:
        command4 = "select public.genDelete('public','"
        command4 += valor_combox2
        command4 += "');"

        #cur.execute(command4)

        comandos.append(command4)

        resultado.append(delete)

    # Boton para procesar mostrar resultados
    submitbtn = tk.Button(root, text ="Results",
                        bg ='purple', command = getResultados)
    submitbtn.place(x = 280, y = 170, width = 55)

    # Boton para procesar mostrar comandos
    submitbtn = tk.Button(root, text ="Run",
                        bg ='green', command = getComandos)
    submitbtn.place(x = 345, y = 170, width = 55)

def getResultados():
    T = tk.Text(root, height = 40, width = 120)
    T.place(x = 10, y = 200)
    for result in resultado:
        T.insert(tk.END,result)

def getComandos():
    T = tk.Text(root, height = 40, width = 120)
    T.place(x = 10, y = 200)
    for result in comandos:
        T.insert(tk.END,result)
        T.insert(tk.END,"\n")

        #Ejecuta el comando!!!!!
        #cur.execute(result)
    


#-------------------------------------------------------------
# Start
root = tk.Tk()
root.geometry("1000x1800")
root.title("DBMS Login Page")
tables = [] #Arreglo de nombre de las tablas
bases = ['SQL SERVER','POSTGRESQL'] #Arreglos de los motores de db
nivel_abstracion = 0
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
var4 = tk.IntVar()
s = tk.StringVar()
c1 = ttk.Combobox(root, textvariable=s) #dbs
c1['values'] = bases
c1['state'] = 'readonly' 
c1.pack(fill='x', padx=5, pady=5)
combobox1 = ""
combobox2 = ""
s2 = tk.StringVar()
c2 = ttk.Combobox(root, textvariable=s2)
cur = []
resultado = []
comandos = []
# create = []
# read = []
# update = []
# delete = []
#


# Boton para procesar consultas
submitbtn = tk.Button(root, text ="Login",
                      bg ='blue', command = submitact)
submitbtn.place(x = 150, y = 170, width = 55)

create = """

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


"""


read = """


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


"""

update = """


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

"""

delete = """


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

"""


# END
root.mainloop()
#-------------------------------------------------------------




#T = tk.Text(root, height = 40, width = 100)
#T.place(x = 200, y = 150)
#T.insert(tk.END,cur.fetchall()[0][1])





    #print(cleanStr(table))

    #current_value = combobox.get()

    #[row[0] for row in cur]

    #cur.execute("select * from maquinas.carros")
    #cur.execute("select * from maquinas.motos")










# def cleanStr(texto):
#     result =  re.sub(r'[^a-zA-Z]', '', texto)  
#     return result  

# def cleanStr(texto):
#     result =  re.sub(pattern = "[^\w\s]", repl = " ", string = texto)  
#     return result  

# def submitact():
#     user = "postgres"
#     passw = "1234"
#     name = "postgres"
#     host1 = "localhost"
#     logPosgtre(user,passw,name,host1)
     
# submitbtn = tk.Button(root, text ="Login",
#                       bg ='blue', command = submitact)
# submitbtn.place(x = 150, y = 155, width = 55)
 
#root.mainloop()









# def submitact():
#     user = Username.get()
#     passw = password.get()
#     name = nombre.get()
#     host1 = host.get()
#     logPosgtre(user,passw,name,host1)
    
# Defining the first row
# lblfrstrow = tk.Label(root, text ="Usuario -", )
# lblfrstrow.place(x = 50, y = 20)
 
# Username = tk.Entry(root, width = 35)
# Username.place(x = 150, y = 20, width = 100)
  
# lblsecrow = tk.Label(root, text ="Contraseña -")
# lblsecrow.place(x = 50, y = 50)
# password = tk.Entry(root, width = 35)
# password.place(x = 150, y = 50, width = 100)


# lblthird = tk.Label(root, text ="Nombre -")
# lblthird.place(x = 50, y = 80)

# nombre = tk.Entry(root, width = 35)
# nombre.place(x = 150, y = 80, width = 100) 

# lblfth = tk.Label(root, text ="Host -")
# lblfth.place(x = 50, y = 110)

# host = tk.Entry(root, width = 35)
# host.place(x = 150, y = 110, width = 100) 