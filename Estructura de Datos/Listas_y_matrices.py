# Creacion de una lista.

x_list = []

y = [1, 2, 3, 4, 5]

z= [1, "Hola", 3.4, True]

# Métodos de las listas.
x = [9, 10, 24, 22, 10, 30]

# agregar elemento
x.append(99)
print(x)

# ordenar lista
x.sort()
print(x)

# ----------------------------------------------
# Crear algoritmos
my_array = [7, 12, 9, 4, 11, 8, 15]
minVal = my_array[0]

for i in my_array:
    if i < minVal:
        minVal = i

print("El valor minimo es:", minVal)

