import tkinter as tk
from tkinter import ttk 
import psycopg2
import pyodbc

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
        logSql()
        banderaMotor = 1
    elif valor_combox1 == "POSTGRESQL":
        # Postgres
        banderaMotor = 0
        logPosgtre()


"""
Metodo de postgresql para obtener de la base que se va trabajar las tablas existentes.
Las muestra en el comboBox.
"""
def logPosgtre():

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
    combobox1 = c1.get()
    if var1.get() == 1:
        if combobox1 == 'POSTGRESQL':
            command1 = "select public.genInsProc('public','"
            command1 += valor_combox2
            command1 += "');"
            comandos.append(command1)
        elif combobox1 == 'SQL SERVER':
            command1 = "select dbo.insertCrud ('customer_services','"
            command1 += valor_combox2
            command1 += "');"
            comandos.append(command1) 
     
    
    if var2.get() == 1:
        if combobox1 == 'POSTGRESQL':
            command2 = "select public.genSelect('public','"
            command2 += valor_combox2
            command2 += "');"
            comandos.append(command2)
        elif combobox1 == 'SQL SERVER':
            command1 = "select dbo.selectCrud ('customer_services','"
            command1 += valor_combox2
            command1 += "');"
            comandos.append(command1)

    if var3.get() == 1:
        if combobox1 == 'POSTGRESQL':
            command3 = "select public.genUpdate('public','"
            command3 += valor_combox2
            command3 += "');"
            comandos.append(command3)
        elif combobox1 == 'SQL SERVER':
            command1 = "select dbo.updateCrud ('customer_services','"
            command1 += valor_combox2
            command1 += "');"
            comandos.append(command1)

    if var4.get() == 1:
        if combobox1 == 'POSTGRESQL':
            command4 = "select public.genDelete('public','"
            command4 += valor_combox2
            command4 += "');"
            comandos.append(command4)
        elif combobox1 == 'SQL SERVER':
            command1 = "select dbo.deleteCrud ('customer_services','"
            command1 += valor_combox2
            command1 += "');"
            comandos.append(command1)


    # Boton para procesar mostrar comandos y los ejecuta
    submitbtn = tk.Button(root, text ="Run",
                        bg ='green', command = getComandos)
    submitbtn.place(x = 280, y = 170, width = 55)

    # Boton para procesar mostrar comandos
    submitbtn = tk.Button(root, text ="Gen",
                        bg ='orange', command = commandGenShow)
    submitbtn.place(x = 345, y = 170, width = 55)

"""
Muestra los comandos que son generados y los ejecuta
"""
def getComandos():

    T = tk.Text(root, height = 40, width = 120)
    T.place(x = 10, y = 200)
    
    combobox1 = c1.get()
    if combobox1 == "POSTGRESQL":
        for comando in comandos:
        
            T.insert(tk.END,comando)
            T.insert(tk.END,"\n")

            conn = psycopg2.connect(dbname =name, user = user, password = pas, host = host )
            cur = conn.cursor()
            
            cur.execute(comando)
            
            result = cur.fetchall()[0][0]
            
            T.insert(tk.END,result)
            T.insert(tk.END,"\n")

            cur.execute(result)
            print("Se ejecuto el commando en la base de datos de dicho motor.")

    elif combobox1 == "SQL SERVER":

        for comando in comandos:
            T.insert(tk.END,comando)
            T.insert(tk.END,"\n")

            conexion = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                                    "SERVER="+direccion_servidor+
                                    ";DATABASE="+nombre_bd+
                                    ";Trusted_Connection=yes;")

            cursor = conexion.cursor()
            cursor.execute(comando)
            print("Se ejecuto el comando")

            result = cursor.fetchall()[0][0]

            T.insert(tk.END,result)
            T.insert(tk.END,"\n")

"""
Muestra los comandos que son generados
"""
def commandGenShow():

    T = tk.Text(root, height = 40, width = 120)
    T.place(x = 10, y = 200)
    
    combobox1 = c1.get()
    if combobox1 == "POSTGRESQL":
        for comando in comandos:
        
            T.insert(tk.END,comando)
            T.insert(tk.END,"\n")

            conn = psycopg2.connect(dbname =name, user = user, password = pas, host = host )
            cur = conn.cursor()
            
            cur.execute(comando)
            
            result = cur.fetchall()[0][0]
            
            T.insert(tk.END,result)
            T.insert(tk.END,"\n")

    elif combobox1 == "SQL SERVER":

        for comando in comandos:
            T.insert(tk.END,comando)
            T.insert(tk.END,"\n")

            conexion = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                                    "SERVER="+direccion_servidor+
                                    ";DATABASE="+nombre_bd+
                                    ";Trusted_Connection=yes;")

            cursor = conexion.cursor()
            cursor.execute(comando)
            print("Se ejecuto el comando")

            result = cursor.fetchall()[0][0]

            T.insert(tk.END,result)
            T.insert(tk.END,"\n")

"""
Connexion de sql 
"""
def connectionSQL():                                    #
    try:
        conexion = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                                "SERVER="+direccion_servidor+
                                ";DATABASE="+nombre_bd+
                                ";Trusted_Connection=yes;")
        # OK! conexión exitosa
        cursor = conexion.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='customer_services';")
        
        row = cursor.fetchone() 

        tables = []

        while row: 
            tables.append(row[0])
            row = cursor.fetchone()

        # Combobox
        c2['values'] = tables   
        c2['state'] = 'readonly' 
        c2.pack(fill='x', padx=5, pady=5)

        # CheckBox
        showCheckBoxs()

        # Boton para procesar consultas
        submitbtn = tk.Button(root, text ="Tables",
                            bg ='red', command = submitact2)
        submitbtn.place(x = 215, y = 170, width = 55)


    except Exception as e:
        # Atrapar error
        print("Ocurrió un error al conectar a SQL Server: ", e) 

"""
Metodo de postgresql para obtener de la base que se va trabajar las tablas existentes.
Las muestra en el comboBox.
"""
def logSql():
    connectionSQL() #Se hace la connection con sql server.




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
resultado = []
comandos = []
cursor = []
banderaMotor = 0
#SQL
direccion_servidor = 'DESKTOP-UK4T5SJ\SQLEXPRESS'
nombre_bd = 'db'    

#Postgresql
user = "postgres"
pas = "1234"
name = "postgres"
host = "localhost"


# Boton para procesar consultas
submitbtn = tk.Button(root, text ="Login",
                      bg ='lightblue', command = submitact)
submitbtn.place(x = 150, y = 170, width = 55)



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