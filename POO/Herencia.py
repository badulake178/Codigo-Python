class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self):
        print(self.firstname, self.lastname)

x = Person("John", "Doe")
x.printname()


#En este ejemplo se ostrara como heredar una clase a otra clase
class Student(Person):
    pass

y = Student("Mike", "Olsen")
y.printname()


#En este ejemplo se muestra como agregar un __init__() a la clase hija
class Student(Person):
    def __init__(self, fname, lname):
        Person.__init__(self, fname, lname)

# En este ejemplo se muestra como usar la funcion super() para heredar la clase padre
class Student(Person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname)
        self.graduationyear = 2024

x = Student("Mike", "Olsen")
print(x.graduationyear)

# En este ejemplo se muestra como usar la funcion super() para heredar la clase padre
class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationyear = year

    def welcome(self):
        print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)
    

x = Student("Mike", "Olsen", 2016)
print(x.graduationyear)
x.welcome()