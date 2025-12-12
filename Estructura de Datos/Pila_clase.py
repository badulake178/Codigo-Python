class Stack:
    def __init__(self):
        self.stack =  []

    def push(self, element):
        self.stack.append(element)
    
    def pop(self):
        if self.isEmpty():
            return "Stack is empty"
        return self.stack.pop()

    def peek(self):
        if self.isEmpty():
            return "Stack is empty"
        return self.stack[-1]

    def isEmpty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)
    

# Create a stack
new_stack = Stack()

new_stack.push('Eduardo F.')
new_stack.push('Matias G.')
new_stack.push('Sofia L.')
print("Pila después de push:", new_stack.stack)

print("Stack: ", new_stack.stack)
print("Pop: ", new_stack.pop())
print("Stack after Pop: ", new_stack.stack)
print("Peek: ", new_stack.peek())
print("isEmpty: ", new_stack.isEmpty())
print("Size: ", new_stack.size())