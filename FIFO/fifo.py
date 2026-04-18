from tkinter import *
import tkinter as tk
import time
import os
print("Cargando Librerias")
import pandas as pd
import datetime
from pandas import ExcelWriter
from tqdm.auto import tqdm
from time import sleep
from functools import reduce
import numpy as np
import math


ruta_archivo = ""

print("Parametros para la ejecucion del FIFO")

print("Seleccionar fecha de ejecucion del FIFO")
hoy = input("Ingrese la fecha de ejecucion del FIFO (formato dd-mm-yyyy): ")

if hoy is None or hoy == "":
	print("No se ingresó una fecha válida. Se utilizará la fecha actual.")
	hoy = datetime.datetime.now().strftime("%d-%m-%Y")


hoy_datetime = datetime.datetime.strptime(hoy, "%d-%m-%Y")
fechahoy = hoy_datetime.strftime("%d") + "." + hoy_datetime.strftime("%m") + "." + hoy_datetime.strftime("%Y")

opcion = int(input("Seleccione una opcion: \n 1. Ejecutar FIFO usando Databricks \n 2. Ejecutar FIFO usando Excel \n"))

if opcion == 1:
	print("Ejecutando FIFO usando Databricks")
	ruta_archivo = f"C:/Users/ASUS UX325DEA-KG325T/OneDrive - Universidad San Sebastian/Proyectos/Proyecto Agrosuper/01. Area comercial/04. Construccion/Test/FIFO/Databricks/FIFO {fechahoy} Databricks.xlsx"
elif opcion == 2:
	print("Ejecutando FIFO usando Excel")
	ruta_archivo = f"C:/Users/ASUS UX325DEA-KG325T/OneDrive - Universidad San Sebastian/Proyectos/Proyecto Agrosuper/01. Area comercial/04. Construccion/Test/FIFO/Excel/FIFO {fechahoy}.xlsx"


porcentaje_fresco = [["T161",0.2020],["T162",0.3110],["T163",0.3030],["T164",0.1840]]
kilos_por_pallet_cecina = 750

print("Se inicia Proceso de FIFO CDA")
#archivo 		= "FIFO/FIFO " + fechahoy + ".xlsx"	
	
archivo = ruta_archivo

# [0] Material (vdisp_cod_material), [1] Cad./FPC (vdisp_fecaduc_feprefercons), [2] CLAS (vdisp_clasificacion), [3] lugar (vdisp_lugar), [4] Total (vdisp_total)
dispo 			= pd.read_excel(archivo,sheet_name='DISPONIBLE') 

# [0] deno traspa, [1] Centro, [2] DENO, [3] Cod, [4] Total
pedido 			= pd.read_excel(archivo,sheet_name='PEDIDO')

# [0] Cod
codtras 		= pd.read_excel(archivo,sheet_name='CODTRAS')
paletizado		= pd.read_excel(archivo,sheet_name='PALETIZADO') # cod_material, cant_paletizado
bd_mat			= pd.read_excel(archivo,sheet_name='BD MATERIALES')
dda_48			= pd.read_excel(archivo,sheet_name='DDA 48')
codtras 		= codtras.to_numpy().tolist()
pedido 			= pedido.to_numpy().tolist()
dispo 			= dispo.to_numpy().tolist()
paletizado 		= paletizado.to_numpy().tolist()
bd_mat			= bd_mat.to_numpy().tolist()
dda_48			= dda_48.to_numpy().tolist()
clas 	= ["COB","SPMK B","SPMK A"]
orden	= ["T161","T162","T164","T163"]
nuevopedido = 0
cont = 0

# ======================= RESULTADO FIFO CDA ===========================================================
# depende del orden de disponible (codigo y fecha caducidad)
resultado_FIFO_CD = pd.DataFrame(columns=["Deno","Centro","Codigo","Cantidad","Fecha","Lugar","Clas"])
for x in codtras:
	#Disponibilidad del material/ probar con Comprehensions
	#Usando Filter
	dispo1 = [t for t in dispo if t[0] == x[0]]
	
	# Sucursales = z
	for z in orden:
		# y = SPMK A, SPMK B, COB
		for y in clas:
			for i in pedido:
				if i[1] == z and i[2] == y and i[3] == x[0]:
					
					pedido1 = [i[0],i[1],i[2],i[3],i[4]]
					if pedido1[4] > 0:
						ped 	= pedido1[4]
						if len(dispo1) == 0:
							continue
						d = 0

						# di = [0] Material (vdisp_cod_material), [1] Cad./FPC (vdisp_fecaduc_feprefercons), [2] CLAS (vdisp_clasificacion), [3] lugar (vdisp_lugar), [4] Total (vdisp_total)
						for di in dispo1:
							# Revisar la claisificacion del DISPONIBLE Y PEDIDO
							if pedido1[2] == "SPMK B" and di[2] == "COB":
								d = d + 1
								continue
							if pedido1[2] == "SPMK A" and di[2] == "COB":
								d = d + 1
								continue
							if pedido1[2] == "SPMK A" and di[2] == "SPMK B":
								d = d + 1
								continue	
							dis 	= dispo1[d][4]
							while ped > 0:
								
								if ped < dis:
									cont = cont + 1 
									resul1 = pd.DataFrame({'Deno': str(i[0]), 'Centro':str(z), 'Codigo':x[0], 'Cantidad':ped, 'Fecha':dispo1[d][1], 'Lugar':str(dispo1[d][3]),'Clas':str(y) }, index= [cont])
									resultado_FIFO_CD = pd.concat([resultado_FIFO_CD, resul1], ignore_index=True)
									#print (str(i[0]) + ";" + str(z) + ";" + str(x[0]) + ";" + str(ped) + ";" + str(dispo1[0][1]) + ";" + str(dispo1[0][3]))
									dis = dis - ped
									dispo1[d][4] = dis
									ped = 0
									break						
								elif ped >= dis:
									cont = cont + 1 
									resul1 = pd.DataFrame({'Deno': str(i[0]), 'Centro':str(z), 'Codigo':x[0], 'Cantidad':dis, 'Fecha':dispo1[d][1], 'Lugar':str(dispo1[d][3]), 'Clas':str(y)}, index= [cont])
									resultado_FIFO_CD = pd.concat([resultado_FIFO_CD, resul1], ignore_index=True)
									#print (str(i[0]) + ";" + str(z) + ";" + str(x[0]) + ";" + str(dis) + ";" + str(dispo1[0][1]) + ";" + str(dispo1[0][3]))
									ped = ped - dis
									dispo1.pop(d)
									if not dispo1:
										break
									if len(dispo1) < d +1:
										break
									if len(dispo1) == 1:
										dis 	= dispo1[0][4]
										d = 0 
									else:
										dis 	= dispo1[d][4]
							break

# ================ Calculo palet congelado REFRIGERADO y CONGELADO =========================
print("Se inicia proceso de calculo pallet Regrigerado y Congelado")
resultado_FIFO_CD 				= resultado_FIFO_CD.to_numpy().tolist()
estado 							= ["REFRIGERADO","CONGELADO"]
cant_total_palet_REFRIGERADO 	= []
cant_total_palet_CONGELADO 		= []
cant_total_palet 				= []
cantidad = 0

# order contiene las sucursales T161|T162|T164|T163
for s in tqdm(orden):
	cant_pallet_REFRIGERADO = 0 
	cant_pallet_CONGELADO = 0
	kilos_pallet_REFRIGERADO = 0 
	kilos_pallet_CONGELADO = 0  
	# recorre los resultados del FIFO CDA [0] deno, [1] centro, [2] codigo, [3] cantidad, [4] fecha, [5] lugar, [6] clasificacion
	for y in resultado_FIFO_CD:
		# recorre los estados CONGELADO Y REFRIGERADO
		for h in estado:
			# recorre tabla material
			for g in bd_mat:
				# comparamos el estado (congelado o refrigerado), codigo, y sucursal 
				if g[5] == h and y[2] == g[0] and s == y[1]:
					tihi = 0
					# q = cod_material, cant_paletizado
					for q in paletizado:
						if q[0] == y[2]:
							tihi = q[1]

					# Validar que tihi no sea 0 para evitar division por cero
					if tihi == 0:
						palet_mat = 0
						kilos_mat = round(y[3] * g[9],2)
					else:
						palet_mat = round(y[3] / tihi,2)
						kilos_mat = round(y[3] * g[9],2)
					
					pallet_por_estado = f"cant_pallet_{h}"
					kilos_por_estado = f"kilos_pallet_{h}"
					vars()[pallet_por_estado]= round(vars()[pallet_por_estado] + palet_mat,2)
					vars()[kilos_por_estado]= round(vars()[kilos_por_estado] + kilos_mat,2)
	cant_total_palet.append([s,[cant_pallet_CONGELADO,kilos_pallet_CONGELADO],[cant_pallet_REFRIGERADO,kilos_pallet_REFRIGERADO]])

# ========= calculo pallet Cecina =================================================================================================
print("Se inicia proceso de calculo pallet Cecina")
#print(cant_total_palet)
#suma_cantidad = 0
#suma_kilo = 0
# recorre las sucursales en el orden T161|T162|T164|T163
for s in cant_total_palet:
	
	pallet_total_cecina = 0 
	kilos_cecina_total = 0

	for y in resultado_FIFO_CD:
		for g in bd_mat:
			# Se busca por sector Cecina, codigo y sucursal
			if g[8] == "Cecina" and y[2] == g[0] and s[0] == y[1]:
				#print(f"{y[2]} : {g[9]}")
				kilos_cecina = round(y[3]*g[9], 2)
				kilos_cecina_total =+ round(kilos_cecina_total + kilos_cecina, 2 )
				#suma_kilo += g[9]
				#suma_cantidad += y[3]
            	
	pallet_total_cecina = round(kilos_cecina_total / kilos_por_pallet_cecina,2)			
	s.insert(4,[pallet_total_cecina,kilos_cecina_total])

#print(suma_cantidad)
#print(suma_kilo)


#Cantidad de pallet y kilos por sucursal
# ============================= Calculo nuevo stock descontando traspasos =========================
nuevostock = []
dispo 			= pd.read_excel(archivo,sheet_name='DISPONIBLE')
dispo 			= dispo.to_numpy().tolist()
fecha_actual = hoy_datetime.date()

print("Nuevo Stock descontanto Traspasos")
for j in tqdm(dispo):
	
	if j[3] =="STOCK":
			
		cod_descuento = list(filter(lambda y: str(y[2]) == str(j[0]) and y[4] == j[1] and str(y[5]) =="STOCK" ,resultado_FIFO_CD))
		sumadescuento = 0
		for y in cod_descuento:
			sumadescuento = sumadescuento + y[3]

		nuevodisponible = j[4] - sumadescuento
		if nuevodisponible > 0:
			nuevostock.append(["deno",j[0],j[1],nuevodisponible])

print("Nuevo Stock descontanto DDA 48hrs")
descuento_DDA48 = []

#==========================  Descuento DDA 48  ======================================================================================
print(f"Tamaño de la demanda 48: {len(dda_48)}")
for h in tqdm(dda_48):
	#print(h)
	cont_nuevostock = 0
	pedido_dda_48 = h[2] 
	for j in nuevostock:
		dis = j[3]
		if h[0] == j[1] and h[1] <= j[2] and dis > 0:
			#print(j)
			if pedido_dda_48 < dis:
				nuevostock[cont_nuevostock][3] = dis - pedido_dda_48
				descuento_DDA48.append([j[1],pedido_dda_48,j[2]])
				#print(nuevostock[cont_nuevostock])
				cont_nuevostock += 1 
				break
			elif pedido_dda_48 >= dis:
				descuento_DDA48.append([j[1],dis,j[2]])
				nuevostock[cont_nuevostock][3] = 0
				#print(nuevostock[cont_nuevostock])
				pedido_dda_48 = pedido_dda_48 - dis 

				cont_nuevostock += 1 
		else:
			cont_nuevostock += 1 
	#print("\n")

descuento_DDA48_df = pd.DataFrame(descuento_DDA48)
print("FIFO CDA terminado")

# ========== Inicio de empujes a sucursales ============================================================
print("Empujes Sucursales")
opcion_empujes = []
suc_empujes = ["T161","T162","T164"]

#obetener la sumas de cajas por dias
def obtener_suma_para_fecha(fecha, stock):
    suma = 0
    for q in stock:
        if fecha == q[2]:
            suma += q[3]
    return suma

fechas = [datetime.datetime(fecha_actual.year, fecha_actual.month, fecha_actual.day, 0, 0) + datetime.timedelta(days=i)  for i in range(5, 9)]
sumas = [obtener_suma_para_fecha(fecha, nuevostock) for fecha in fechas]
fechas_col = [5,6,7,8]
cant_empuje = []

for i in fechas:
    cant_empuje.append(['T163',i])

# Pantalla desplegable
# Función para manejar el cambio de estado de un checkbox
def checkbox_changed(row, col):
    global cant_empuje
    variable_name = f"checkbox{row}{col}"
    clave = [suc_empujes[row], fechas[col]]
    if clave not in cant_empuje:
        cant_empuje.append(clave)
    else:
        cant_empuje.remove(clave)
    #print(f"Checkbox {variable_name} cambió ")
    #print (cant_empuje)
# Crear la etiqueta principal
root = tk.Tk()
root.title("Creación de casillas de verificación en una matriz")
label1 = tk.Label(root, text="Selecciona una o varias opciones:")
label1.grid(row=0, column=0, columnspan=1)
# Definir las dimensiones de la matriz
# Crear un diccionario para almacenar las casillas de verificación
checkboxes = {}
# Crear las etiquetas de los días de la semana y agregarlas a la matriz
for col, dia in enumerate(fechas_col):
    label = tk.Label(root, text=f"{dia}")
    label.grid(row=1, column=col+1, columnspan=1)
    label = tk.Label(root, text=f"{sumas[col]}")
    label.grid(row=2, column=col+1, columnspan=1)
# Crear las casillas de verificación y agregarlas a la matriz
for row, suc in enumerate(suc_empujes):
    # Crear la etiqueta de la sucursal
    label = tk.Label(root, text=suc)
    label.grid(row=row+3, column=0, columnspan=1)
    label2 = tk.Label(root, text="Duracion restante")
    label2.grid(row=1, column=0, columnspan=1)
    label3 = tk.Label(root, text="Cantidad")
    label3.grid(row=2, column=0, columnspan=1)
    for col, dia in enumerate(fechas_col):
        # Crear el nombre de la variable dinámicamente
        variable_name = f"checkbox{row}{col}"
        # Crear la casilla de verificación y asignarla a la variable correspondiente
        checkboxes[variable_name] = tk.Checkbutton(root)
        checkboxes[variable_name].var = tk.BooleanVar()  # Crear una variable asociada al checkbox
        checkboxes[variable_name]["variable"] = checkboxes[variable_name].var  # Vincular la variable al checkbox
        checkboxes[variable_name]["command"] = lambda r=row, c=col: checkbox_changed(r, c)  # Vincular función
        # Ubicar la casilla de verificación en la cuadrícula
        checkboxes[variable_name].grid(row=row+3, column=col+1, columnspan=1)
#print(checkboxes)
root.mainloop()

#====================== FIFO part. 2 Empujes a sucursales ============================================================
#calculo de cuanto empujar por material a cada sucursal 
empuje_total = []
cod_empujes = list(set(codigo_empuje[1] for codigo_empuje in nuevostock))
#print(cod_empujes)
def obtener_suma_para_fecha_por_codigo(fecha,codigo, stock):
    suma_fecha = 0
    for q in stock:
        if codigo == q[1] and fecha == q[2]:
        	suma_fecha = suma_fecha + q[3]
    return [q[0],codigo,fecha,suma_fecha]

cod_fecha_cant = []
emp_centro_nuevos_porce = []
emp_final = []

# =================== CREAR LISTA DE EMPUJE ===============================
print(f"lista de fechas: {len(fechas)}")
for l in fechas:
	#obtener la Cantidad por la fecha l de las lista "fechas" por codigo
	cod_fecha_cant = [obtener_suma_para_fecha_por_codigo(l,cod, nuevostock)for cod in cod_empujes]
	#eliminar todos los elementos que la suma para esta fecha sean 0
	cod_fecha_cant_filtrada = [elem for elem in cod_fecha_cant if elem[3] != 0]
	#esta es la lita que contiene los centros que se van a empujar con la fecha l de fechas
	centro_fecha_emp = [elem for elem in cant_empuje if elem[1] == l ]
	#se crea una nueva lista que almacene el porcentaje original de envio a las surusales 
	centro_fecha_porcentaje_emp = []
	for elemento_original in centro_fecha_emp:
	    for elemento_porcentaje in porcentaje_fresco:
	        if elemento_original[0] == elemento_porcentaje[0]:
	            elemento_original.append(elemento_porcentaje[1])
	            centro_fecha_porcentaje_emp.append(elemento_original)
	suma2 = 0
	for elemento in centro_fecha_porcentaje_emp:
	    suma2 += elemento[2]
	for i in range(len(centro_fecha_porcentaje_emp)):
		centro_fecha_porcentaje_emp[i][2] = round(centro_fecha_porcentaje_emp[i][2] / suma2, 3)
	#print(centro_fecha_porcentaje_emp)
	#recorrer los centros con sus porcentaje por cada fecha
	for r in centro_fecha_porcentaje_emp:
		#recorrer por la fecha los codigos y sus cantidad disponibles para empujar
		for k in cod_fecha_cant_filtrada:
			#calcular la cantidad a empujar 
			cant_empuje_fecha_suc = round(r[2] * k[3],0)
			#agregarlo a las lista de empuje final
			emp_final.append([k[0],r[0],k[1],cant_empuje_fecha_suc,r[1],"STOCK"])
#agregrar etiqueta agrupacion sector y estado deno HT_@
for l in emp_final:
	for k in bd_mat:
		if l[2] == k[0]:
			l[0] = str(k[11] + "_" + l[1])
			#print("entra")

emp_final_df = pd.DataFrame(emp_final)
print("Se inicia Proceso de FIFO Sucursales Satelites")
resultado_suc_sat = pd.DataFrame(columns=["Centro","Codigo","Cantidad","Fecha"])
dispo 			= pd.read_excel(archivo,sheet_name='DISPONIBLE SUC SAT')
pedido 			= pd.read_excel(archivo,sheet_name='PEDIDO SUC SAT')
codtras 		= pd.read_excel(archivo,sheet_name='COD SUC SAT')
codtras 		= codtras.to_numpy().tolist()
pedido 			= pedido.to_numpy().tolist()
dispo 			= dispo.to_numpy().tolist()
clas 	= ["COB","SPMK B","SPMK A"]
orden	= ["T161","T162","T164"]
nuevopedido = 0
cont = 0
for x in tqdm(codtras):
	for z in orden:
		dispo1 = [t for t in dispo if t[0] == z and t[1] == x[0]]
		for y in clas:
			for i in pedido:
				if i[0] == z and i[1] == y and i[2] == x[0]:
					pedido1 = [i[0],i[1],i[2],i[3]]
					if pedido1[3] > 0:
						ped 	= pedido1[3]
						if len(dispo1) == 0:
							continue
						d = 0
						for di in dispo1:
							if pedido1[1] == "SPMK B" and di[3] == "COB":
								d = d + 1
								continue
							if pedido1[1] == "SPMK A" and di[3] == "COB":
								d = d + 1
								continue
							if pedido1[1] == "SPMK A" and di[3] == "SPMK B":
								d = d + 1
								continue	
							dis 	= dispo1[d][4]
							while ped > 0:	
								if ped < dis:
									cont = cont + 1 
									resul1 = pd.DataFrame({'Centro':str(z), 'Centro':str(z), 'Codigo':x[0], 'Cantidad':ped, 'Fecha':dispo1[d][2]}, index= [cont])
									resultado_suc_sat = pd.concat([resultado_suc_sat, resul1], ignore_index=True)
									#print (str(i[0]) + ";" + str(z) + ";" + str(x[0]) + ";" + str(ped) + ";" + str(dispo1[0][1]) + ";" + str(dispo1[0][3]))
									dis = dis - ped
									dispo1[d][4] = dis
									ped = 0
									break						
								elif ped >= dis:
									cont = cont + 1 
									resul1 = pd.DataFrame({'Centro':str(z), 'Centro':str(z), 'Codigo':x[0], 'Cantidad':dis, 'Fecha':dispo1[d][2]}, index= [cont])
									resultado_suc_sat = pd.concat([resultado_suc_sat, resul1], ignore_index=True)
									#print (str(i[0]) + ";" + str(z) + ";" + str(x[0]) + ";" + str(dis) + ";" + str(dispo1[0][1]) + ";" + str(dispo1[0][3]))
									ped = ped - dis
									dispo1.pop(d)
									if not dispo1:
										break
									if len(dispo1) < d +1:
										break
									if len(dispo1) == 1:
										dis 	= dispo1[0][4]
										d = 0 
									else:
										dis 	= dispo1[d][4]
							break
print("FIFO SUC SAT Terminado")
cant_total_palet = pd.DataFrame(cant_total_palet, columns=["Centro","Congelado","Fresco","Cecina"])
resultado_FIFO_CD = pd.DataFrame(resultado_FIFO_CD , columns=["Deno","Centro","Codigo","Cantidad","Fecha","Lugar","Clas"])
descuento_DDA48_df.columns = ['Codigo', 'Cantidad', 'Fecha']
emp_final_df.columns = ["Deno","Centro","Codigo","Cantidad","Fecha","Lugar"]

print("Se crea Archivo Excel")
#nombrearchivo_final = "Archivo Final " + fechahoy + ".xlsx"

nombrearchivo_final = os.path.join("FIFO", "Archivo Final " + fechahoy + ".xlsx")

# Crear la carpeta FIFO si no existe
if not os.path.exists("FIFO"):
    os.makedirs("FIFO")



writer_final = pd.ExcelWriter(nombrearchivo_final, engine='openpyxl')
resultado_FIFO_CD.to_excel(writer_final, sheet_name='FIFO CDA', index=False)
descuento_DDA48_df.to_excel(writer_final,sheet_name='DESCUENTO DD48', index=False)
emp_final_df.to_excel(writer_final, sheet_name='EMPUJES', index=False)
resultado_suc_sat.to_excel(writer_final,sheet_name='FIFO SUC SAT', index=False)
cant_total_palet.to_excel(writer_final,sheet_name='CANT PALLET', index=False)
writer_final.book.save(nombrearchivo_final)

root = Tk()
frameCnt = 24

frames = [PhotoImage(file="C:/Users/ASUS UX325DEA-KG325T/Documents/GitHub/C-digo-Python/FIFO/Utils/cargando.gif",format = 'gif -index %i' %(i)) for i in range(frameCnt)]
def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)
label = Label(root)
label.pack()
root.after(0, update, 0)
root.after(5000,lambda:root.destroy())
root.mainloop()