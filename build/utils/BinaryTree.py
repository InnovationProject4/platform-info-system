


'''
  # decide sorting
    tree = TupledBST()
    
    tree.insert((key, unique_key), {"datacontainer": ["data..."]})
    
    # function must return boolean
    x = tree.get_sorted_data(lambda x: (
        True
    ))


'''
class TupledBSTNode():
    '''
       Tuple-key Binary Search Tree
    '''
    def __init__(self, keys : tuple, value):
        self.key = keys
        self.value = value
        self.left = None
        self.right = None
    
    def get_leftmost_node(self):
        node = self
        while node.left is not None:
            node = node.left
        return node
    
    def insert(self, keys, value):
        key, unique_k = self.key
        fkey, funique_k = keys
        
        if unique_k == funique_k:
            self.key[0] = key[0]
         
        if fkey == key:
            self.value[value] = None
        elif fkey < key:
            if self.left is None:
                self.left = TupledBSTNode(keys, [value])
            else:
                self.left.insert(keys, value)
        else:
            if self.right is None:
                self.right = TupledBSTNode(keys, [value])
            else:
                self.right.insert(keys, value)              
    
    def search(self, key):
        if key == self.key:
            return self.value
        elif key < self.key:
            if self.left is not None:
                return self.left.search(key)
            else:
                return None
        else:
            if self.right is not None:
                return self.right.search(key)
            else:
                return None
            


    def get_sorted_data(self, filter_func):
        sorted_data = []
        stack = []
        node = self

        while stack or node:
            while node:
                stack.append(node)
                node = node.left

            node = stack.pop()
            for item in list(node.value):
                if item is not None and filter_func(item):
                    sorted_data.append(item)

            node = node.right

        return sorted_data

    

class TupledBST:
    def __init__(self, compareTo=None):
        self.root = None
        
        if compareTo is not None:
            setattr(TupledBSTNode,"compareTo", compareTo)
        
    def insert(self, keys : tuple, value):
        if self.root is None:
            self.root = TupledBSTNode(keys, [value])
        else:
            self.root.insert(keys, value)
    
    def search(self, key):
        if self.root is not None:
            return self.root.search(key)
        else:
            return None
        
    # funktion pitää palauttaa väite
    def get_sorted_data(self, filter_func):
        if self.root is None: return []
        else:
            return self.root.get_sorted_data(filter_func)



