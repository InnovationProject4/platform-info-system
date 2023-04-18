import bisect 
from typing import Iterable
from math import log

'''
B+ Tree implementation for in-memory db-like data queries.
'''

__all__ = (
    "BPNode",
    "BPTree",
    "query",
)

#Make static class
class query:
    """Perform queries on BPTrees."""
    
    @staticmethod
    def select(iterable : Iterable, *columns : str, **conditions):
        """Database-like key-value row selection query

        Args:
            iterable (Iterable):  A generator/iterable of dictionaries to select data from. 
                    Available generators: 'self.traverse', 'self.point_query', 'self.range_query'
            *columns (str):  Arguments representing the names of columns to select.
            **conditions (any): Keyword args representing conditions to filter rows by.  

        Returns:
            rows (List): A list of rows containing selected values from the specified columns.
            
        Example:
            >>> values = [
                {name: 'Bob', age: 35, tools: ['axe']},
                {name: 'John', age: 20, tools: ['pickaxe', 'axe']},
                {name: 'Alice', age: 21, tools: ['wool']},
            ]
            
            We can select the names of people who have an axe in their tools like this:
            
            >>> query((x for x in values), 'name', tools=['axe'])
            [{'name': 'Bob'}, {'name': 'Alice'}]
            
            
            We can also select the names of people who are at least 40 years old using a lambda condition like this:
            
            >>> select_from_values((x for x in values), 'name', age=lambda val: val >= 40)
            [{'name': 'John'}, {'name': 'Alice'}]
        """

        selected_records = []
        
        for _ , row in iterable:
            if all((key not in row) or (row[key] == value) or (isinstance(value, list) and any(v in row[key] for v in value) if not callable(value) else value(row[key]))
                   for key, value in conditions.items()):
                selected_records.append({col: row.get(col) for col in columns})
                
                
        return selected_records
    
    @staticmethod
    def select_nodes(iterable : Iterable, limit: int = None, **conditions):
        """ see select() docstring for more info. This method returns the actual records instead of just the selected rows.
        
        Args:    
            limit (int): The maximum number of rows to return. If None, all rows are returned.
        """
        selected_rows = []
        count = 0
        
        for _ , row in iterable():
            if all((key not in row) or (row[key] == value) or (isinstance(value, list) and any(v in row[key] for v in value) if not callable(value) else value(row[key]))
                   for key, value in conditions.items()):
                selected_rows.append(row)
                count += 1
                if limit and count >= limit:
                    break
                
        return selected_rows
    
    @staticmethod
    def left_join(iterable, other_tree, alias=None, onkey=None, select=None):
        """left join between two B+ trees on a common key

        Args:
            other_tree (BPlusTree): The other B+ tree to join with
            alias (str): The alias to use for the other tree columns. use alias to avoid column name conflicts
            onkey (str): The reference key to join the two trees on
            select (List[str]): The names of columns to select on the other tree

        Returns:
            rows (list): A list of rows containing the selected values from both trees.
            
            
        Example:
            Users tree references to tools tree using 'tools_id' column
            
            >>> users = BPTree(2)
            >>> tools = BPTree(2)
            
            >>> users.bulk_insert([
                {'id': 1, 'name': 'Bob', 'age': 35, 'tools_id': 1},
                {'id': 2, 'name': 'Alice', 'age': 25, 'tools_id': 2},
                {'id': 3, 'name': 'John', 'age': 45, 'tools_id': 1},
            ], key=lambda x: x['id'])
            
            
            >>> tools.bulk_insert([
                {'id': 1, 'name': 'hammer', 'price': 10},
                {'id': 2, 'name': 'screwdriver', 'price': 5},
                {'id': 3, 'name': 'wrench', 'price': 15},
            ], key=lambda x: x['id'])
            
            # Perform a left join on the 'tools_id' column using alias 'tools'
            
            >>> result = users.left_join(users.traverse, tools, alias='tools', onkey='tools_id', select=['name', 'price'])
            >>> print(result) 
            # Output: [{'id': 1, 'name': 'Bob', 'age': 35, 'tools_id': 1, 'tools.name': 'hammer', 'tools.price': 10}, 
            # {'id': 2, 'name': 'Alice', 'age': 25, 'tools.name': 'screwdriver', 'tools.price': 5},
            # {'id': 3, 'name': 'John', 'age': 45, 'tools.name': 'hammer', 'tools.price': 10}]
            
            # Perform a left join on the 'tools_id' column without alias
            
            >>> result = users.left_join(users.traverse, tools, onkey='tools_id', select=['price'])
            >>> print(result)
            # Output: [{'id': 1, 'name': 'Bob', 'age': 35, 'tools_id': 1, 'price': 10},
            # {'id': 2, 'name': 'Alice', 'age': 25, 'price': 5},
            # {'id': 3, 'name': 'John', 'age': 45, 'price': 10}]
        """
        if alias != None:
            alias = f'{alias}.'
        
        rows = []
        for _, value in iterable():
            if onkey in value:
                items = other_tree.point_query(value[onkey])
                for item in items:
                    rows.append({**value, **{f'{alias}{col}': item.get(col) for col in select}})
        return rows
    


class BPNode:
    def __init__(self, is_leaf=False, keys = [], children=[]):
        self.is_leaf = is_leaf
        self.keys = keys
        self.children = children
        self.next = None
        
    def __repr__(self):
        if self.is_leaf:
            return '<BPLeaf: {}>'.format(self.keys)
        return '<BPNode: {}>'.format(self.keys)


class BPTree:
    
    @classmethod
    def fromData(cls, data, key=lambda x: x, sort=False):
        """create new Tree and bulk load with data 
        
        Args:
            data (list): list of data to insert
            key (function): function to extract key from data. can also be used to edit data before inserting.
            sort (bool): sort data before bulk loading
        """
        l = len(data)
        tree = BPTree(int(l / (1 + log(l))))
        tree.bulk_insert(data, key, sort)
        return tree
    
    def __init__(self, factor, alias=None):
        ''' factor equals to order or max_keys in a node'''
        self.root = BPNode(is_leaf=True, keys=[], children=[])
        self.factor = factor
        self.alias = alias
        
    def insert(self, key, value):
        """Insert a key-value pair into the tree. If the key already exists, the key will be appended.
        
        Args:
            key (int): The key to insert.
            value (any): The value to insert
        """
        node = self.root
        path = []

        while not node.is_leaf:
            i = bisect.bisect_left(node.keys, key)
            path.append((node, i))
            node = node.children[i]

        i = bisect.bisect_left(node.keys, key)
        node.keys.insert(i, key)
        node.children.insert(i, value)

        while len(node.keys) >= self.factor:
            key, n = self.split(node)
           
            if not path:
                self.root = BPNode(keys=[key], children=[node, n])
                return

            parent, parent_index = path.pop()
            parent.keys.insert(parent_index, key)
            parent.children.insert(parent_index + 1, n)
            node = parent

        return None
    
    
    def bulk_insert(self, data, key=lambda x: x, sort=False):
        """Bulk load data into an empty BPTree.
        
        Args:
        
            data (list): list of data to insert
            key (function): function to extract key from data. Can also be used to update data before inserting.
            sort (bool): sort data before inserting
        
        """
        if sort:
            data.sort(key=key)
        
        for item in data:
            self.insert(key(item), item)
    
    
    def split(self, node):
        '''
        offset:
        0 - leaf node
        1 - internal node
        '''
        newnode = BPNode(node.is_leaf)
        offset = int(not node.is_leaf)
        
        i = len(node.keys) // 2
        split_key = node.keys[i]
        
        newnode.keys = node.keys[i + offset:]
        newnode.children = node.children[i + offset:]
        #newnode.values = node.values[i:]   # leaf
        
        node.keys = node.keys[:i]
        node.children = node.children[:i + offset]
        #node.values = node.values[i:]      # leaf
        
        if node.is_leaf : 
            newnode.next = node.next
            node.next = newnode
        
        return split_key, newnode
    
    
    def search(self, key):
        """search for a single key-value pair by its key."""
        node = self.root
        
        while not node.is_leaf:
            i = bisect.bisect(node.keys, key)
            node = node.children[i]
            
        i = bisect.bisect_left(node.keys, key)
        if i < len(node.keys) and node.keys[i] == key:
            return node, i
            
        return None, None
    
    
    def find(self, key):
        ''' find a specific value by its key-value key'''
        node, i = self.search(key)
        if node:
            return node.children[i]
    
    def point_query(self, key):
        """
        get all values associated with a specific key
        """
        node = self.root

        while not node.is_leaf:
            i = bisect.bisect(node.keys, key)
            node = node.children[i]
            
        values = [] 
        i = bisect.bisect_left(node.keys, key)
        while node and node.keys[i] == key:
            l = len(node.keys)
            while i < l and node.keys[i] == key:
                values.append(node.children[i])
                i+=1
            i = 0
            node = node.next
            
        return values
    
    def range_query(self, minkey, maxkey): 
        """Generator stream to get all key-value pairs between minimum key and maximum key.
        A key must be either ascending or descending.

        Args:
            minkey (any): minimum key
            maxkey (any): maximum key

        Yields:
            key (any), value (dict): A key-value pair
        """
        node = self.root
        
        while not node.is_leaf:
            i = bisect.bisect_left(node.keys, minkey)
            node = node.children[i]

        
        while node:
            i = bisect.bisect_left(node.keys, minkey)
            l = len(node.keys)
            
            while i < l and node.keys[i] <= maxkey:
                yield node.keys[i], node.children[i]
                i+=1
            
            if node.keys[-1] > maxkey: break
            else: node = node.next
    
    def traverse(self):
        ''' iterate through all the values in the tree '''
        node = self.root
        while not node.is_leaf:
            node = node.children[0]
            
        while node:
            for i in range(len(node.keys)):
                yield node.keys[i], node.children[i]
            node = node.next
            
            
    
    @classmethod
    def verbose_traverse(cls, node, depth=1):
        ''' print a depth map of nodes and leafs '''
        if node.is_leaf:
            #print(node.keys)
            print(depth, "leaf: ", node.children)
        else:
            print(depth, "node: ", node.keys, node.children)
            for child in node.children:
                cls.verbose_traverse(child, depth + 1)

  
    def delete_range(self, minkey, maxkey):
        '''
        deletes all key-value pairs between minimum key and maximum key (inclusive).
        ###Deletes key-values but does not rebalance the tree
        '''
        node = self.root
        parent = None
        node_index = None
        
        
        while not node.is_leaf:
            node_index = bisect.bisect(node.keys, minkey)
            parent = node
            node = node.children[node_index]
            
        while node:
            i = bisect.bisect(node.keys, minkey)
            l = len(node.keys) - 1
       
            while i <= l and node.keys[i] <= maxkey:
                del node.keys[i]
                del node.children[i]
                l-=1
                
        
           
           # node has no children
            #if len(node.keys) == 0:
            #    left_sibling = parent.children[node_index - 1]
            #    if left_sibling and left_sibling is not node:
            #        left_sibling.next = node.next
                    
            #    del parent.children[node_index]
            
            if len(node.keys) == 0:
                if node is self.root:
                    self.root = node.children[0]
                else:
                    parent.children.pop(node_index)
                    if node.next:
                        left_sibling = parent.children[node_index - 1] if node_index > 0 else None
                        if left_sibling:
                            left_sibling.next = node.next
                
                
                self._rebalance(parent)   
                
            if not node.is_leaf and node.keys[i] < maxkey:
                self._borrow_or_merge(node, i, minkey, maxkey)
                
            if node.keys and node.keys[-1] > maxkey: break
            else: 
                node = node.next
    
    def __iter__(self):
        yield from self.traverse()
                    
                    
            




def tests():  
            
    root = BPTree(5)
    bulk = BPTree(3)

    root.insert(6, "six")
    root.insert(7, "seven")
    root.insert(3, "three")
    root.insert(4, "four")
    root.insert(2, "two")
    root.insert(1, "one")

    root.insert(8, "eight")
    root.insert(3, "tres")
    root.insert(9, "nine")
    root.insert(5, "five")

    BPTree.verbose_traverse(root.root)

    print()
    print("search", end="\n")


    def prints(root, key):
        print("key", key, "find", root.find(key))


    prints(root, 1)
    prints(root, 2)
    prints(root, 3)
    prints(root, 4)
    prints(root, 5)
    prints(root, 6)
    prints(root, 7)
    prints(root, 8)
    prints(root, 9)

    print()
    print("point query")
    print(root.point_query(3))


    print()
    print("traverse leafs")

    for key, value in root.traverse():
        print(key, value, end=", ")

    print() 
    print() 
    print("range_query")

    for key, val in root.range_query(3, 6):
        print(key, val)
        
    print() 
    print() 
    print("delete")
    #root.delete(4)
    #root.delete(3)
    #root.delete(7)
    #root.delete(1)
    #root.delete(9)
    #root.delete(2)
    #root.delete(8)

    for key, value in root.traverse():
        print(key, value, end=", ")
        

    print()    
    print("select test")

    r = BPTree(3)

    r.insert('2023-04-03T15:35:00.000Z', {
        'train_id': 'IC11',
        'train_number': 11,
        'train_type': 'IC',
        'destination': 'Joensuu asema',
        'scheduled_time': '2023-04-03T15:35:00.000Z',
        'commercial_track': '4',
        'train_stopping': True,
        'stop_on_stations': ['Käpylä', 'Oulunkylä', 'Joensuu']
    })


    r.insert('2023-04-03T16:00:00.000Z', {
        'train_id': 'IC11',
        'train_number': 11,
        'train_type': 'IC',
        'destination': 'Joensuu asema',
        'scheduled_time': '2023-04-03T16:00:00.000Z',
        'commercial_track': '4',
        'train_stopping': True,
        'stop_on_stations': ['Käpylä', 'Oulunkylä', 'Pukinmäki']
    })


    r.insert('2023-04-03T16:05:00.000Z', {
        'train_id': 'IC12',
        'train_number': 12,
        'train_type': 'IC',
        'destination': 'Helsinki asema',
        'scheduled_time': '2023-04-03T16:05:00.000Z',
        'commercial_track': '5',
        'train_stopping': True,
        'stop_on_stations': ['Oulunkylä']
    })


    r.insert('2023-04-03T15:06:00.000Z', {
        'train_id': 'IC13',
        'train_number': 13,
        'train_type': 'IC',
        'destination': 'Pasila asema',
        'scheduled_time': '2023-04-03T16:06:00.000Z',
        'commercial_track': '6',
        'train_stopping': False,
        'stop_on_stations': ["Joensuu"]
    })
    selected = r.query(r.traverse, 'train_id', 'train_type', 'scheduled_time', 'destination', 'commercial_track',
                                    train_type='IC')

    for item in selected:
        print(item)
        
        

