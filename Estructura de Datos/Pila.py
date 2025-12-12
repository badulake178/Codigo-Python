stack = []

# Push
stack.append('A')
stack.append('B')
stack.append('C')
print("Pila después de push:", stack)

#Peek
topElement = stack[-1]
print("Elemento en la cima (peek):", topElement)

# Pop
poppedElement = stack.pop()
print("Elemento removido (pop):", poppedElement)

#Stack after Pop
print("Stack después de pop:", stack)

# isEmpty
isEmpty = not bool(stack)
print("isEmpty:", isEmpty)

# Size
print("Tamaño de la pila:", len(stack))