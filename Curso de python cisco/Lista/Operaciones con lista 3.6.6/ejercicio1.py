my_list = [1, 2, 4, 4, 1, 4, 2, 6, 2, 9, 10, 11, 32, 22, 90, 22]
#
# Escribe tu código aquí.
#
for i in range(len(my_list)):
    # Si la pisicion es mayor que la posicion admitible de la lista, se termina el proceso
    if i > len(my_list) - 1:
        break
    copy_lista = my_list[:]
    elemento_buscar = my_list[i]
    del copy_lista[i]
    # Verifico si existe otro elemento igual
    if elemento_buscar in copy_lista:
        for i in range(len(copy_lista)):
            if elemento_buscar == copy_lista[i]:
                del my_list[i+1]

print("La lista con elementos únicos:")
print(my_list)
