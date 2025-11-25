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