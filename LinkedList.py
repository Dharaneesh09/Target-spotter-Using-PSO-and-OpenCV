class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LList:
    def __init__(self):
        self.head = None
        self.no = 0

    def insertBeg(self, data):
        node = Node(data, self.head)
        self.head = node
        self.no += 1

    def insert(self,data,n=None):
        if n is None:
            self.insertLast(data)
        elif n == 0:
            self.insertBeg(data)
        i = 0
        node = self.head
        newNode = Node(data)
        if i + 1 is not n:
            node = node.next
            i += 1
        newNode.next = node.next
        node.next = newNode

    def insertLast(self, data):
        if self.head is None:
            self.insertBeg(data)
            return
        node = self.head
        newNode = Node(data)
        while node.next is not None:
            node = node.next
        node.next = newNode

    def get(self, a):
        i = 0
        node = self.head
        while i != a:
            node = node.next
            i += 1
        return node

    def printAll(self):
        node = self.head
        while node is not None:
            print(node.data)
            node = node.next


l1 = LList()
l1.insertBeg(10)
l1.insertBeg("HelloWorld")
l1.insertLast("This is last")
l1.insertLast("No this one")
l1.insert("This is an insertion", 2)
l1.printAll()
