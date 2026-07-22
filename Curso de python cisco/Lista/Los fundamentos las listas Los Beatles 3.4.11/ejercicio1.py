# paso 1
beatles = []
print("Paso 1:", beatles)

# paso 2
beatles.append('John Lennon')
beatles.append('Paul McCartney')
beatles.append('George Harrison')

print("Paso 2:", beatles)

# paso 3
for persona in ['Stu Sutcliffe', 'Pete Best']:
    beatles.append(persona)
print("Paso 3:", beatles)

# paso 4
del beatles[3]
print("Paso 4:", beatles)

# paso 5
beatles.insert(3, 'Ringo Starr')
print("Paso 5:", beatles)


# probando la longitud de la lista
print("Los Fav", len(beatles))

