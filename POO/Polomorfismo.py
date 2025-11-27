# funcion len() en strings
x = "Hello World"

print(len(x))  # Salida: 11

# funcion len() en Tuplas
mytuple = ("apple", "banana", "cherry")
print(len(mytuple))  # Salida: 3

# funcion len() en Listas
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

print(len(thisdict))

# Ejemplo para las clases
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Drive!")

class Boat:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Sail!")
    
class Plane:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Fly!")

car1 = Car("Ford", "Mustang")
boat1 = Boat("Yamaha", "212X")
plane1 = Plane("Boeing", "747")

for x in (car1, boat1, plane1):
    x.move()  # Llama al método move() correspondiente a cada clase