class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
    
class Stack:
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, value):
        new_node = Node(value)
        if self.head:
            new_node.next = self.head
        self.head = new_node
        self.size += 1

    def pop(self):
        if self.isEmpty():
            return "Stack is empty"
        popped_node = self.head
        self.head = self.head.next
        self.size -= 1
        return popped_node.value
    
    def peek(self):
        if self.isEmpty():
            return "Stack is empty"
        return self.head.value

    def isEmpty(self):
        return self.size == 0
    
    def stackSize(self):
        return self.size
    
    def traverseAndPrint(self):
        currentNode = self.head
        while currentNode:
            print(currentNode.value, end=" --> ")
            currentNode = currentNode.next
        print()

# Create a stack
stack = Stack()
stack.push(10)
stack.push(20)
stack.push(30)

print("LinkedList: ", end="")
stack.traverseAndPrint()
print("Peek: ", stack.peek())
print("Pop: ", stack.pop())
print("LinkedList after Pop: ", end="")
stack.traverseAndPrint()
print("isEmpty: ", stack.isEmpty())
print("Size: ", stack.stackSize())