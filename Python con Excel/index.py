import pandas as pd

file_path = r'C:\Users\ASUS UX325DEA-KG325T\Documents\GitHub\C-digo-Python\Python con Excel\cartola_22052026.xls'
# Cargar el archivo Excel
df_cartola = pd.read_excel(file_path, sheet_name='Hoja1', skiprows=24, index_col=0)

# Crear indices
df_cartola = df_cartola.reset_index(drop=True)

# limpiar filas y columnas que no son necesarias
df_cartola = df_cartola.drop('Saldo (PESOS)', axis=1)

df_cartola = df_cartola.drop(df_cartola.index[0])

df_cartola.columns = ["Fecha", "Descripcion", "Origen", "Cargos", "Abonos"]

print(df_cartola[0:10])





"""for indice, fila in cartola.iterrows():
    print(f"Índice: {indice}")
    print(f"Fila: {fila}")
    print("-" * 40)"""
