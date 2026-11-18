#Pine Hein Swe #33438234

import random
import sys

class Node:
    """
    BTree Node
    Holds the list of keys, children, and the key upperbound
    """
    def __init__(self, t):
        self.key_bound = t*2-1
        self.key = []
        self.child = []

    def is_full(self):
        """
        Checks if the node is full
        """
        return self.key_bound == len(self)

    def is_leaf(self):
        """
        Checks if the node is a leaf
        """
        return len(self.child) == 0

    def __len__(self):
        """
        Gets the total number of keys held by the node
        """
        return len(self.key)
    
    def total_len(self):
        """
        Gets the total number of keys held by the node and children
        """
        l = len(self.key)
        for node in self.child:
            l += node.total_len()
        return l

class BTree:
    """
    BTree
    Available commands:
        Insert
        Delete
        Select
        Rank
        Range/PrimeRange
    """
    def __init__(self, t):
        self.t = t
        self.root = Node(t)
        self.count = 0

    def __len__(self):
        return self.count

    def traverse(self, node, item: int):
        """
        Traverses to the correct index in a node where a key should be located
        """
        i = 0
        while i < len(node) and item > node.key[i]:
            i += 1
        return i

    def insert(self, item: int):
        """
        Inserts an item into the BTree
        """
        def split(node):
            """
            Splits a node if the node is full
            """
            new_node = Node(self.t)
            for i in range(self.t, 2*self.t):
                if i < 2*self.t-1:
                    new_node.key.append(node.key.pop(self.t))
                if not node.is_leaf():
                    new_node.child.append(node.child.pop(self.t))
            return node.key.pop(self.t-1), node, new_node
        
        def insert_aux(node: Node, item: int):
            """
            Recursive insertion of a key
            """
            i = self.traverse(node, item)
            if node.is_leaf(): #Inserted
                node.key.insert(i, item)
                self.count += 1
            else:
                if node.child[i].is_full(): #Splitting
                    median, _, right = split(node.child[i])
                    node.key.insert(i, median)
                    node.child.insert(i+1, right)
                    if item > median:
                        i += 1
                insert_aux(node.child[i], item)

        if self.root.is_full(): #Base case at root
            median, left, right = split(self.root)
            self.root = Node(self.t)
            self.root.key.append(median)
            self.root.child.append(left)
            self.root.child.append(right)
        insert_aux(self.root, item)

    def delete(self, item):
        """
        Deletes an item from the BTree
        """
        def merge(node, i):
            """
            Merges a node with an immediate neighbor when both are at the minimum number of keys
            """
            node.child[i].key.append(node.key.pop(i))
            for _ in range(max(len(node.child[i+1].child), len(node.child[i+1]))):
                if len(node.child[i+1]) > 0:
                    node.child[i].key.append(node.child[i+1].key.pop(0))
                if not node.child[i+1].is_leaf():
                    node.child[i].child.append(node.child[i+1].child.pop(0))
            node.child.pop(i+1)

        def inorder_max(node):
            """
            Finds the relative maximum key in BTree starting from a node
            """
            while not node.is_leaf():
                node = node.child[-1]
            return node.key[-1]
        
        def inorder_min(node):
            """
            Finds the relative minimum key in BTree starting from a node
            """
            while not node.is_leaf():
                node = node.child[0]
            return node.key[0]
        
        def delete_aux(node, item):
            """
            Recursive deletion of a key
            """
            i = self.traverse(node, item)
            if i < len(node) and node.key[i] == item:
                if node.is_leaf():
                    if len(node) >= self.t: #Case 1
                        node.key.pop(i)
                        self.count -= 1
                else:
                    if len(node.child[i]) >= self.t: #Case 2a
                        item = inorder_max(node.child[i])
                        node.key[i] = item
                        node = node.child[i]
                    elif len(node.child[i+1]) >= self.t: #Case 2b
                        item = inorder_min(node.child[i+1])
                        node.key[i] = item
                        node = node.child[i+1]
                    else: #Case 2c
                        merge(node, i)
                    delete_aux(node, item)
            elif not node.is_leaf():
                if len(node.child[i]) == self.t-1:
                    if i == len(node):
                        if len(node.child[i-1]) == self.t-1: #Case 3b
                            merge(node, i-1)
                            if len(self.root) == 0:
                                self.root = self.root.child[i-1]
                            i -= 1
                        else: #Case 3a
                            node.child[i].key.insert(0, node.key[i-1])
                            node.key[i-1] = node.child[i-1].key.pop(-1)
                            if not node.child[i-1].is_leaf():
                                node.child[i].child.insert(0, node.child[i-1].child.pop(-1))
                    else:
                        if len(node.child[i+1]) == self.t-1: #Case 3b
                            merge(node, i)
                            if len(self.root) == 0:
                                self.root = self.root.child[i]
                        else: #Case 3a
                            node.child[i].key.append(node.key[i])
                            node.key[i] = node.child[i+1].key.pop(0)
                            if not node.child[i+1].is_leaf():
                                node.child[i].child.append(node.child[i+1].child.pop(0))
                delete_aux(node.child[i], item)
        delete_aux(self.root, item)
    
    def select(self, k):
        """
        Selects the n-th lowest key in the BTree
        """
        def select_aux(node, k):
            """
            Recursive selection of a key
            """
            if node.is_leaf():
                return node.key[k-1]
            else:
                i = 0
                current = node.child[i].total_len()
                while k > current: #Narrows down the subtree which the item could be located
                    k -= current + 1
                    if k == 0 and i != len(node):
                        return node.key[i]
                    i += 1
                    current = node.child[i].total_len()
                return select_aux(node.child[i], k)
            
        #Returns -1 when the desired index is greater than the number of keys
        return select_aux(self.root, k) if len(self) >= k else -1 

    def rank(self, item):
        """
        Finds the rank of the given key in the BTree
        """
        def rank_aux(node, item, rank):
            """
            Recursive ranking of a key
            """
            i = 0
            rank = rank
            #Counts the total number of keys in the subtrees that do not hold the key to find the rank
            while i < len(node) and item > node.key[i]:
                if node.is_leaf():
                    rank += 1
                else:
                    rank += node.child[i].total_len() + 1
                i += 1
            #Adds in the remaining keys when the correct key is located
            if i < len(node) and item == node.key[i]:
                if node.is_leaf():
                    rank += 1
                else:
                    rank += node.child[i].total_len() + 1
                return rank
            #When a key is not found
            if node.is_leaf():
                return -1
            else:
                return rank_aux(node.child[i], item, rank)
        return rank_aux(self.root, item, 0)

    def range(self, start, end, prime = False):
        """
        Finds all the (optionally prime) keys in a given range (inclusive) in the BTree
        """
        def miller_rabin(num):
            """
            Determines if a number is possibly a prime
            """
            def randomized_primality(num):
                """
                Determines if a number is possibly a prime for odd numbers greater than 3
                """
                k = 64 #Number of tests
                s = 0
                t = num - 1
                while t % 2 == 0:
                    s = s + 1
                    t = t//2
                for _ in range(k):
                    a = random.randint(2,num-2)
                    x = pow(a, t, num)
                    if x == 1: #Case 4
                        continue
                    for _ in range(1, s):
                        prev = x
                        x = pow(x, x, num)
                        if x == 1:
                            if prev != num-1: #Case 3
                                return True
                            else: #Case 2
                                x = 1
                                break
                    if x != 1 % num: #Case 1
                        return True #Definitely a prime
                return False #Needs more testing to be 100% sure
            
            if num % 2 == 1 and num > 3: #Input must be an odd number greater than 3
                return randomized_primality(num)
            if num == 2 or num == 3: #2 and 3 are prime
                return True
            return False #Incase of 1 and lower

        def range_aux(node, array):
            """
            Recursive range collection of keys
            """
            i = self.traverse(node, max(min_item, start))
            if i < len(node) and min(max_item, end) < node.key[i]: #Collects the keys when i does not move between the start and end
                if not node.is_leaf():
                    array = range_aux(node.child[i], array)
                if min(max_item, end) == node.key[i]:
                    if not prime or miller_rabin(node.key[i]):
                        array.append(node.key[i])
            while i < len(node) and min(max_item, end) >= node.key[i]: #Collects the keys when i does move between the start and end
                if not node.is_leaf():
                    array = range_aux(node.child[i], array)
                if not prime or miller_rabin(node.key[i]):
                    array.append(node.key[i])
                i += 1
            if not node.is_leaf() and i == len(node): #Recursively calls itself when the node is not a leaf and i is at the end of the node
                array = range_aux(node.child[i], array)
            return array
        
        min_item = self.select(1)
        max_item = self.select(len(self))
        if start <= max_item and end >= min_item: #Makes sure there are numbers in the tree that are within the range
            array = range_aux(self.root, [])
            if array: #Checks if the list returns empty
                return array
        return [-1]

def read_keys(file_path: str):
    f = open(file_path, 'r')
    line = f.read().split('\n')
    f.close()
    return [int(key) for key in line]

def read_commands(file_path: str):
    f = open(file_path, 'r')
    line = f.read().split('\n')
    f.close()
    return [l.split(" ") for l in line]

def write_file(output):
    f = open("output_a2.txt", 'w')
    f.write("\n".join(output))
    f.close()

if __name__ == "__main__":
    _, t, insert_file_name, delete_file_name, commands_file_name = sys.argv

    print("Number of arguments passed :", len(sys.argv))
    print("Degree Parameter:", t)
    print("Keys to Insert File:", insert_file_name)
    print("Keys to Delete File:", delete_file_name)
    print("Commands to Execute File:", commands_file_name)

    tree = BTree(int(t))
    for key in read_keys(insert_file_name):
        tree.insert(key)
    for key in read_keys(delete_file_name):
        tree.delete(key)
    output = []
    commands = read_commands(commands_file_name)
    for command in commands:
        match command[0]:
            case "select":
                output.append(str(tree.select(int(command[1]))))
            case "rank":
                output.append(str(tree.rank(int(command[1]))))
            case "keysInRange":
                output.append(" ".join([str(key) for key in tree.range(int(command[1]), int(command[2]))]))
            case "primesInRange":
                output.append(" ".join([str(key) for key in tree.range(int(command[1]), int(command[2]), True)]))
    
    write_file(output)