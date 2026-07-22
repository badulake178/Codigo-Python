numero_lista = []
start = True
cantidad = int(input("¿Cuántos elementos deseas ordenar?: "))

for contador in range(cantidad):
    valor = float(input("Ingresa un elemento de la lista: "))
    numero_lista.append(valor)

print('\nLista original')
print(numero_lista)

while start:
    start = False
    for i in range(len(numero_lista) - 1):
        if numero_lista[i] > numero_lista[i + 1]:
            start = True
            numero_lista[i], numero_lista[i+1] = numero_lista[i+1], numero_lista[i]

print("\nOrdenada: ")
print(numero_lista)