import ctypes 


#######################################################
class Node(object):

    def __init__(self, data):
        self.data = data
        self.id = None
        self.next = None
        self.prev = None
        self.edges = LinkedList()

    def _get_neighbors(self):
        neighbors = set()
        for neighbor in self.edges:
            neighbors.update([neighbor.target])
        return neighbors

    neighbors = property(_get_neighbors)

    def _valid_neighbors(self, visited):
        for neighbor in self.neighbors:
            if not visited[neighbor]:
                return True
        return False

########################################

class Edge(object):

    def __init__(self, data, source, target):
        self.data = data
        self.next = None
        self.prev = None
        self.source = source
        self.target = target      

#############################################

class NodeArray(object):

    def __init__(self, size):
        self._size = size
        PyArray = ctypes.py_object * size
        self._items = PyArray()
        self._count = 0
        self.clear(None)

    def __len__(self):
        return self._count

    def __getitem__(self, ndx):
        return self._items[ndx]

    def __setitem__(self, ndx, data):
        self._items[ndx] = data

    def __iter__(self):
        return ArrayIterator(self._items)

    def clear(self, value):
        for ndx in range(self._size):
            self._items[ndx] = value

    def add_node(self, data, ndx=None):
        n_node = Node(data)
        if ndx:
            n_node.id = ndx
            self._items[ndx] = n_node
            self._count += 1
        elif self._count < self._size:
            n_node.id = self._count
            self._items[self._count] = n_node
            self._count += 1
        else:
            print "Array Resized"
            resize = self._size * 2
            n_arr = NodeArray(resize)
            n_arr.copy(self._items)
            self._items = n_arr
            self._items[self._count] = n_node
            self._size = resize
            self._count += 1

    def full(self):
        return self._count == self._size

    def copy(self, arr):
        for ndx, item in enumerate(arr):
            self._items[ndx] = item

########################################################
class ArrayIterator(object):
    
    def __init__(self, arr):
        self.array = arr
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current < len(self.array):
            output = self.array[self.current]
            self.current += 1
            return output
        else:
            raise StopIteration

########################################################
class LinkedList(object):

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __iter__(self):
        return LinkedListIterator(self.head)

    def __len__(self):
        return self.length

    def __contains__(self, target):
        return self.search(target)

    def search(self, target):
        current = self.head
        while current != None and current.data != target:
            current = current.next
        return current is not None

    def add_node(self, data):
        n_node = Node(data)
        if self.head == None:
            self.head = n_node
            self.tail = n_node
            self.length += 1
        else:
            n_node.prev = self.tail
            self.tail.next = n_node
            self.tail = n_node

    def add_edge(self, data, source, target):
        n_edge = Edge(data, source, target)
        if self.head == None:
            self.head = n_edge
            self.tail = n_edge
            self.length += 1
        else:
            n_edge.prev = self.tail
            self.tail.next = n_edge
            self.tail = n_edge
            self.length += 1

    def remove(self, target):
        item = self.find(target)
        if item:
            if item is self.head:
                self.head = item.next
            elif item is self.tail:
                self.tail = item.prev
            else:
                item.prev.next = item.next
                item.next.prev = item.prev
        
    def find(self, target): # maybe find nodes tuple here
        current = self.head
        while current.target != target and current != None:
            current = current.next
        if current == None:
            return False
        else:
            return current

#################################################
class LinkedListIterator(object):

    def __init__(self, head):
        self.current = head

    def __iter__(self):
        return self

    def next(self):
        if self.current == None:
            raise StopIteration
        else:
            node = self.current
            self.current = self.current.next
            return node 



######################################
class Stack(object):

    def __init__(self):
        self.top = None
        self.length = 0

    def __len__(self):
        return self.length

    def push(self,data):
        node = StackNode(data)
        if self.top == None:
            self.top = node
            self.length += 1
        else:
            node.prev = self.top
            self.top = node
            self.length += 1

    def pop(self):
        pop = self.top
        self.top = self.top.prev
        self.length -= 1
        return pop

    def peek(self):
        return self.top.data

########################################
class StackNode(object):

    def __init__(self,data):
        self.data = data
        self.prev = None
