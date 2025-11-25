#En este ejemplo usamos metodos dentro de una clase

class Person:
    def __init__(self, name, age, altura, peso):
        self.name = name
        self.age = age
        self.altura = altura
        self.peso = peso

    def get_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Altura: {self.altura}, Peso: {self.peso}")

    def imc(self):
        print(f"El IMC de {self.name} es {self.peso / (self.altura ** 2)}")
    
person1 = Person("Eduardo", 24, 1.70, 75)

person1.get_info()
person1.imc()
        

class Person:
    def __init__(self, name, age, altura, peso):
        self.name = name
        self.age = age
        self.altura = altura
        self.peso = peso
    
    def __str__(self):
        return f"{self.name}, {self.age} años, Altura: {self.altura}m, Peso: {self.peso}kg"

    def get_info(self):
        return f"Name: {self.name}, Age: {self.age}, Altura: {self.altura}, Peso: {self.peso}"

    def imc(self):
        return self.peso / (self.altura ** 2)
    
person2 = Person("Ana", 30, 1.60, 60)
print(person2)