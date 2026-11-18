from boyer_moore import dl_distance
class Node2:
    def __init__(self, letter):
        self.letter = letter
        self.branches = []
    
    def __getitem__(self, letter):
        for node in self.branches:
            if node.letter is letter:
                return node
        return None
    
    def add_node(self, letter):
        self.branches.append(Node2(letter))

    def __str__(self):
        """s = f"Node: {self.letter}\n"
        for node in self.branches:
            s += f"Child{node}\n"""

        return "Node: " + self.letter

class Node3:
    def __init__(self, name):
        self.name = name
        self.edges = [None] * 26
    
    def __str__(self):
        s = f"Node: {self.name}\n"
        for e in self.edges:
            if e is not None:
                s += e.__str__() + "\n"
        return s
    
class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {}
        self.link = None
    
    def __getitem__(self, letter):
        try:
            return self.edges[letter]
        except KeyError:
            return None
    
    def __setitem__(self, letter, item):
        self.edges[letter] = item
        
    def get_all_edges(self):
        return self.edges.values()
    
    def get_all_keys(self):
        return self.edges.keys()
    
    def __str__(self):
        s = f"Node: {self.name}\nlink: {self.link if self.link is None else self.link.name}\n"
        for e in self.edges:
            if e is not None:
                s += f"belongs to {self.name}\n" + e.__str__() + "\n"
        return s + "\n\n"

class End:
    def __init__(self, num):
        self.end = num

    def increment(self):
        self.end += 1
    
    def update_end(self, num):
        self.end = num

    def __str__(self):
        return f"End: {self.end}"

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.end_node = None
        self.index = None
    
    def add_leaf(self):
        self.end.end += 1

    def __len__(self):
        return self.end.end - self.start + 1
    
    def __str__(self):
        s = f"Start: {self.start}\n{self.end.__str__()}\nEndNode: {self.end_node}\n========="
        return s

def uggkonen(text):
    base = Node2("$")
    for i in range(len(text)):
        for x in range(i+1):
            node = base
            for l in text[x:i]:
                prev = node
                node = node[l]
                if node is None:
                    prev.add_node(l)
    return base

def traverse(text, base_text, base):
    current_node = base
    edge = current_node.edges[ord(text[0])%26] 
    current_len = len(text)
    while edge is not None and edge.end_node is not None and len(edge) < current_len:
        current_len -= len(edge)
        current_node = edge.end_node
        edge = current_node.edges[ord(text[len(text) - current_len])%26]
    if edge is None:
        current_node.edges[ord(text[len(text) - current_len])%26] = Edge(x, i)
    else:
        if current_len > len(edge):
            edge.add_leaf()
        elif text[len(text) - current_len] != base_text[edge.start + current_len - 1]:
            new_node = Node(text[len(text) - current_len])
            new_node.edges[ord(text[len(text) - current_len])%26] = Edge(len(text) - current_len, End(-1))
            new_node.edges[ord(base_text[edge.start + current_len - 1])%26] = Edge(edge.start + current_len - 1, edge.end)
            edge.end_node = new_node
            edge.end = End(edge.start + current_len - 2)

    return edge

def ukkonen_naive(text):
    base = Node("$")
    for i in range(len(text)):
        for x in range(i+1):
            current_node = base
            edge = current_node[text[x]] 
            current_len = i - x + 1
            while edge is not None and edge.end_node is not None and len(edge) < current_len:
                current_len -= len(edge)
                current_node = edge.end_node
                edge = current_node[text[i + 1 - current_len]]
            
            if edge is None:
                current_node[text[i + 1 - current_len]] = Edge(i + 1 - current_len, End(i))
                current_node[text[i + 1 - current_len]].index = x
            else:
                if current_len > len(edge):
                    edge.add_leaf()
                elif text[i] != text[edge.start + current_len - 1]:
                    new_node = Node("")
                    new_node[text[i]] = Edge(i, End(i))
                    new_node[text[edge.start + current_len - 1]] = Edge(edge.start + current_len - 1, edge.end)
                    new_node[text[edge.start + current_len - 1]].index = x
                    edge.end_node = new_node
                    edge.end = End(edge.start + current_len - 2)
    return base

"""
if active_len == 0:
                        active_edge = active_node[text[r]]
                        if active_edge is None:
                            break
                    r += 1
                    end.increment()
                    active_len += 1
                    if active_len == len(active_edge):
                        active_len = 0
                        active_node = active_edge.end_node
"""

def ukkonen(text):
    text += "$"
    end = End(0)
    l = 0
    r = 0
    root = Node("root")
    active_edge = None
    active_node = root
    active_len = 0
    suffix_link = None

    while r < len(text):
        if l == r:
            suffix_link = None
            active_edge = root[text[r]]
            active_node = root
            active_len = 0
            if active_edge is None:
                root[text[r]] = Edge(r, end)
                root[text[r]].index = l
                print(l,r,"New Leaf")
                l += 1
                r += 1
                end.increment()
            else:
                while active_edge is not None and text[r] == text[active_edge.start + active_len]:
                    if active_len == len(active_edge):
                        active_len = 0
                        active_node = active_edge.end_node
                        r += 1
                        end.increment()
                        active_edge = active_node[text[r]]
                    else:
                        r += 1
                        active_len += 1
                        end.increment()
                    print(l,r,"traversing")

        else:
            if active_edge is None:
                active_node[text[r]] = Edge(r, end)
                print(l, r, "New Leaf on branch")
                active_node[text[r]].index = l
            else:
                print(l, r, "branching", active_edge.start)
                new_edge = Edge(active_edge.start, End(active_edge.start + active_len - 1))
                new_node = Node(text[l] + f"{active_edge.start}")
                active_edge.start = active_edge.start + active_len
                if suffix_link is not None:
                    suffix_link.link = new_node
                suffix_link = new_node
                new_node.link = root
                new_edge.end_node = new_node
                new_node[text[active_edge.start]] = active_edge
                new_node[text[r]] = Edge(r, end)
                new_node[text[r]].index = l
                active_node[text[new_edge.start]] = new_edge
            l += 1
            if active_node.link is not None:
                active_len = (r - l)
                active_node = active_node.link
                active_edge = active_node[text[r - active_len]]
                while active_edge is not None and len(active_edge) <= active_len:
                    active_len -= len(active_edge)
                    active_node = active_edge.end_node
                    active_edge = active_node[text[r - active_len]]
                print(l,r,"short cut", active_len)
            elif active_node is root:
                active_len -= 1
                active_edge = active_node[text[l]]
    end.update_end(r-1)
    
    return root

def ukkonen_v2(text):
    text += "$"
    n = len(text)
    i = 0
    end = End(0)
    root = Node("Root")
    remainder = 0
    active_len = 0
    active_node = root
    active_edge = None
    suffix_link = None

    for j in range(n):
        if i <= j:
            i = j
            print(j,i,"Back to Root")
            end.update_end(j)
            suffix_link = None
            active_len = 0
            remainder = 0
            print("searching", text[i - active_len],"from root")
            active_edge = active_node[text[i - active_len]]
            if active_edge is not None and i == active_edge.start and i != n-1:
                continue
            while active_edge is not None and text[i] == text[active_edge.start + active_len]:    
                i += 1
                if i < n:
                    end.increment()
                active_len += 1
                remainder += 1
                print(j,i,"Traversing", active_node.name, active_len, len(active_edge), active_edge.end_node is not None)
                if active_len == len(active_edge) and active_edge.end_node is not None:
                    active_len = 0
                    active_node = active_edge.end_node
                    active_edge = active_node[text[i]]
        else:
            print("searching", text[i - active_len],"from", active_node.name, active_len)
            active_edge = active_node[text[i - active_len]]
            link_len = active_len
            while active_edge is not None and active_edge.end_node is not None and link_len >= len(active_edge):
                print("skipping count", active_edge.end_node.name,"remaining len", active_len)
                link_len -= len(active_edge)
                active_node = active_edge.end_node
                active_edge = active_node[text[i - link_len]]

        
        if active_edge is None:
            print(j,i,"New Leaf", active_node.name, text[i])
            active_node[text[i]] = Edge(i, end)
            active_node[text[i]].index = j
        else:
            print(active_edge.start + active_len)
            if text[active_edge.start + active_len] == text[i]:
                i += 1
                active_len += 1
                end.increment()
                suffix_link = None

            new_edge = Edge(active_edge.start, End(active_edge.start + active_len - 1))
            new_node = Node(text[active_edge.start + active_len - 1] + f"{active_edge.start + active_len - 1}")
            
            if suffix_link is not None:
                suffix_link.link = new_node
            suffix_link = new_node
            new_node.link = root

            print(j,i,"Branching", active_node.name, new_node.name, text[active_edge.start + active_len], text[i])
            active_edge.start = active_edge.start + active_len
            new_edge.end_node = new_node
            new_node[text[active_edge.start]] = active_edge
            new_node[text[i]] = Edge(i, end)
            new_node[text[i]].index = j
            active_node[text[new_edge.start]] = new_edge

        remainder -= 1

        if active_node.link is not None:
            active_node = active_node.link
            print(j,i,"Shortcut", active_node.name)
        elif active_node is root:
            active_len -= 1
            
def ukkonen_v3(text):
    text += "$"
    n = len(text)
    i = 0
    end = End(0)
    root = Node("Root")
    active_len = 0
    phase_len = 0
    active_node = root
    active_edge = None
    suffix_link = None

    for j in range(n):
        if i <= j:
            i = j
            end.update_end(j)
            suffix_link = None
            active_len = 0
            phase_len = 0
            active_edge = active_node[text[i - active_len]]
            if active_edge is not None and i == active_edge.start and i != n-1:
                continue
            while active_edge is not None and text[i] == text[active_edge.start + active_len]:    
                i += 1
                if i < n:
                    end.increment()
                active_len += 1
                if active_len == len(active_edge) and active_edge.end_node is not None:
                    active_len = 0
                    active_node = active_edge.end_node
                    active_edge = active_node[text[i]]
            phase_len = active_len
        else:
            active_edge = active_node[text[i - active_len]]
            active_len = phase_len
            while active_edge is not None and active_edge.end_node is not None and active_len >= len(active_edge):
                active_len -= len(active_edge)
                active_node = active_edge.end_node
                active_edge = active_node[text[i - active_len]]

        
        if active_edge is None:
            active_node[text[i]] = Edge(i, end)
            active_node[text[i]].index = j
        else:
            if text[active_edge.start + active_len] == text[i]:
                i += 1
                active_len += 1
                phase_len += 1
                end.increment()
                suffix_link = None

            new_edge = Edge(active_edge.start, End(active_edge.start + active_len - 1))
            new_node = Node(text[active_edge.start + active_len - 1] + f"{active_edge.start + active_len - 1}")
            
            if suffix_link is not None:
                suffix_link.link = new_node
            suffix_link = new_node
            new_node.link = root

            active_edge.start = active_edge.start + active_len
            new_edge.end_node = new_node
            new_node[text[i]] = active_edge
            new_node[text[i]] = Edge(i, end)
            new_node[text[i]].index = j
            active_node[text[new_edge.start]] = new_edge

        if active_node.link is not None:
            active_node = active_node.link
        elif active_node is root:
            active_len -= 1
        
    return root

def ukkonen_v4(text):
    text += "$"
    n = len(text)
    root = Node("root")
    active_node = root
    active_edge = None
    active_len = 0
    suffix_link = None
    end = End(0)
    j = 0

    for i in range(n):
        end.update_end(i)
        if i == j:
            active_node = root
            active_edge = active_node[text[j]] 
            active_len = 1
            suffix_link = None

            while j < n:
                if active_edge is None:
                    break
                elif len(active_edge) == active_len:
                    active_len = 1
                    active_node = active_edge.end_node
                    active_edge = active_node[text[j]]
                elif text[active_edge.start + active_len] == text[j]:
                    active_len += 1
                else:
                    break
                j += 1
        else:
            temp_len = active_len
            while active_edge is not None and active_edge.end_node is not None and len(active_edge) >= temp_len:
                temp_len -= len(active_edge)
                active_node = active_edge.end_node
                active_edge = active_node[j - temp_len]
        
        if active_edge is None:
            active_node[text[i]] = Edge(j, end)
            active_node[text[i]].index = i
            j += 1
        else:
            new_edge = Edge(active_edge.start, End(active_edge.start + active_len - 1))
            new_node = Node(text[active_edge.start + active_len - 1] + f"at index {active_edge.start + active_len - 1}")
            
            if suffix_link is not None:
                suffix_link.link = new_node
            suffix_link = new_node
            new_node.link = root

            active_edge.start = active_edge.start + active_len
            new_edge.end_node = new_node
            print(j)
            new_node[text[j]] = active_edge
            new_node[text[j]] = Edge(j, end)
            new_node[text[j]].index = i
            active_node[text[new_edge.start]] = new_edge

        if active_node.link is not None:
            active_node = active_node.link
        else:
            active_len -= 1

    return root

def ukkonen_arun(text):
    text += "$"
    n = len(text)
    root = Node("Root")
    root.link = root
    active_node = root
    remainder = 0
    lastj = 0
    globalEnd = End(0)

    base = Edge(0, globalEnd)
    base.index = 0
    active_node[text[0]] = base


    for i in range(n-1):
        globalEnd.increment()
        link = None
        for j in range(lastj + 1, i + 2):
            edge = active_node[text[i+1 - remainder]]
            while edge is not None and edge.end_node is not None and remainder >= len(edge):
                remainder -= len(edge)
                active_node = edge.end_node
                edge = active_node[text[i+1 - remainder]]
            
            if edge is None:
                active_node[text[i+1]] = Edge(i+1, globalEnd)
                active_node[text[i+1]].index = j
                lastj += 1
                if link is not None:
                    link.link = active_node
                    link = None
            else:
                if text[i+1] == text[edge.start + remainder]:
                    remainder += 1
                    if link is not None:
                        link.link = active_node
                    break
                else:
                    new_edge = Edge(edge.start, End(edge.start + remainder - 1))
                    new_node = Node(text[edge.start + remainder - 1] + f" at index {edge.start + remainder - 1}")
                    new_edge.end_node = new_node
                    active_node[text[edge.start]] = new_edge

                    edge.start += remainder
                    new_node[text[edge.start]] = edge
                    new_leaf = Edge(i+1, globalEnd)
                    new_node[text[i+1]] = new_leaf
                    new_leaf.index = j
                    new_node.link = root

                    lastj += 1

                    if link is not None:
                        link.link = new_node
                    link = new_node

                    if active_node.link is not None and active_node.link is active_node:
                        remainder -= 1

            if active_node.link is not None:
                active_node = active_node.link
    return root


def traverse(text, tree, text2):
    current_node = tree
    current_edge = current_node[text[0]] 
    current_len = len(text)
    while current_edge is not None and current_edge.end_node is not None and len(current_edge) < current_len:
        current_len -= len(current_edge)
        current_node = current_edge.end_node
        current_edge = current_node[text[len(text) - current_len]]
    if current_edge is not None:
        full_match = True
        for x in range(1, current_len):
            full_match = full_match and text[len(text) - 1 - current_len + 1 + x] == text2[current_edge.start + x]
            
    return current_edge if full_match else None

def traverse_v2(text, pattern, tree):
    active_node = tree
    active_edge = active_node[pattern[0]] 
    active_len = 0
    for i in range(0, len(pattern)):
        if active_edge is None:
            break
        elif pattern[i] != text[active_edge.start + active_len]:
            active_edge = None
            break
        if active_len == len(active_edge):
            active_len = 0
            active_node = active_edge.end_node
            active_edge = active_node[pattern[i]]
        active_len += 1
    
    return active_edge

def traverse_v3(text, pattern, tree):
    if len(pattern) == 0:
        return None
    active_node = tree
    active_edge = active_node[pattern[0]] 
    active_len = 1

    for i in range(1, len(pattern)):
        if active_edge is None:
            break
        elif len(active_edge) == active_len:
            active_len = 1
            active_node = active_edge.end_node
            active_edge = active_node[pattern[i]]
        elif text[active_edge.start + active_len] == pattern[i]:
            active_len += 1
        else:
            active_edge = None
            break
        
    return active_edge

def dfs(active_edge):
    queue = [active_edge]
    indexes = []

    while queue:
        edge = queue.pop()

        if edge.end_node is not None:
            queue.extend(edge.end_node.get_all_edges())
        else:
            indexes.append(edge.index+1)

    return indexes

def get_all_indices(tree):
    queue = list(tree.get_all_edges())
    indexes = []

    while queue:
        edge = queue.pop()

        if edge.end_node is not None:
            queue.extend(edge.end_node.get_all_edges())
        else:
            indexes.append(edge.index)

    return indexes


def dl_distance_tree(text, patt, tree):
    def substitution(text, patt, edge, node, active_len, mismatch, matches):
        if mismatch < 0:
            print("too many mismatches", patt)
            return matches
        if len(patt) > 1:
            if edge is None:
                print("new edge", patt)
                print("oh yea")
                for x in node.get_all_keys():
                    if node[x] is not None:
                        if x == patt[0]:
                            print("matched", patt, x)
                            matches.extend(substitution(text, patt, node[x], node, 1, mismatch, []))
                            print("matched", patt, x)
                        elif x == patt[1]:
                            print("insert", patt, x)
                            matches.extend(substitution(text, patt[1:], node[x], node, 1, mismatch-1, []))
                            print("insert", patt, x)
                        elif len(node[x]) == 1 and node[x].end_node is not None:
                            print("deleted or sub", patt, x)
                            if node[x].end_node[patt[1]] is not None:
                                matches.extend(substitution(text, patt[1:], node[x].end_node[patt[1]], node[x].end_node, 1, mismatch-1, []))
                            elif node[x].end_node[patt[0]] is not None:
                                matches.extend(substitution(text, patt, node[x].end_node[patt[0]], node[x].end_node, 1, mismatch-1, []))
                            print("deleted or sub", patt, x)
                        elif len(node[x]) > 1:
                            print("i dont know", patt, x)
                            if text[node[x].start+1] == patt[1]:
                                matches.extend(substitution(text, patt[1:], node[x], node, 2, mismatch-1, []))
                            elif text[node[x].start+1] == patt[0]:
                                matches.extend(substitution(text, patt, node[x], node, 2, mismatch-1, []))
                            print("i dont know", patt, x)
                print("oh no")
                return matches
            elif len(edge) <= active_len:
                print("end of edge",patt, mismatch)
                if len(patt) - 1 == 1 and mismatch > 0:
                    for x in edge.end_node.get_all_keys():
                        if x == patt[1]:
                            print("PERFECTTTTTTTTTTTTTTmatched with 0 mismatches")
                            matches.append((edge.end_node[x], 0))
                        else:
                            print("DL1REACCCCCCCCCCCCCCCCCCHmatched with 1 mismatches")
                            matches.append((edge.end_node[x], 1))
                    return matches
                elif len(patt) - 1 == 1:
                    return substitution(text, patt[1:], edge.end_node[patt[1]], edge.end_node, 1, mismatch, matches)
                elif patt[0] != text[edge.start + active_len - 1]:
                    return substitution(text, patt[1:], edge.end_node[patt[1]], edge.end_node, 1, mismatch - 1, matches)
                else:
                    print("starting herer ======================", patt)
                    return substitution(text, patt[1:], None, edge.end_node, 1, mismatch, matches)
            else:
                if patt[0] == text[edge.start + active_len - 1]:
                    print("matched at", patt,"with", 1 - mismatch, "mismatches")
                    return substitution(text, patt[1:], edge, node, active_len + 1, mismatch, matches)
                elif patt[1] == text[edge.start + active_len - 1] and patt[0] == text[edge.start + active_len]:
                    print("mismatched at", patt,"with", 1 - mismatch, "mismatches", "swapping=====================================dfadsafdas", mismatch)
                    return substitution(text, patt[2:], edge, node, active_len + 3, mismatch-1, matches)
                elif patt[0] == text[edge.start + active_len]:
                    print("mismatched at", patt,"with", 1 - mismatch, "mismatches", "deletion")
                    return substitution(text, patt, edge, node, active_len + 1, mismatch-1, matches)
                else:
                    print("mismatched at", patt,"with", 1 - mismatch, "mismatches", "substitution")
                    return substitution(text, patt[1:], edge, node, active_len + 2, mismatch-1, matches)
        else:
            if edge is None:
                print("OIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
                if mismatch - 1 < 0 :
                    return matches
                else:
                    matches.append((None, 1))
                    return matches
            else:
                if patt[0] == text[edge.start + active_len - 1]:
                    print("PERFECTTTTTTTTTTTTTTmatched with 0 mismatches")
                    matches.append((edge, 1 - mismatch))
                    return matches
                elif mismatch == 1:
                    print("DL1REACCCCCCCCCCCCCCCCCCHmatched with 1 mismatches")
                    matches.append((edge, 1 - mismatch-1))
                    return matches
                else:
                    print("too many mismatches on final char")
                    return matches
        
    def dl_distance_v2(text, patt, edge, node, active_len, mismatch, matches):
        if mismatch > 1:
            print("too many mismatches", patt)
            return matches
        
        if len(patt) > 1:
            if edge is None:
                for x in node.get_all_keys():
                    if node[x] is not None:
                        print(patt, x)
                        if x == patt[0]:
                            if len(node[x]) > 1: #Match
                                print(patt, x)
                                matches.extend(dl_distance_v2(text, patt[1:], node[x], node, 1, mismatch, []))
                            else: #Match on own edge
                                matches.extend(dl_distance_v2(text, patt, node[x], node, 1, mismatch, []))
                        elif x == patt[1]: #Transpose at start
                            if len(node[x]) > 1 and text[node[x].start + 1] == patt[0]:
                                matches.extend(dl_distance_v2(text, x + patt[2:], node[x], node, 1, mismatch + 1, []))
                            elif len(node[x]) > 1: #Insertion at node
                                matches.extend(dl_distance_v2(text, patt[2:], node[x], node, 1, mismatch + 1, []))
                            elif node[x].end_node is None: #Insertion on own edge
                                matches.extend(dl_distance_v2(text, patt, node[x], node[x], 1, mismatch + 1, []))
                        elif len(node[x]) == 1 and node[x].end_node is None:
                            continue
                        elif len(node[x]) == 1 and x == patt[1] and node[x].end_node[patt[0]] is not None: 
                            if len(node[x].end_node[patt[0]]) > 1: #Transpose on own edge
                                matches.extend(dl_distance_v2(text, patt[2:], node[x].end_node[patt[0]], node[x].end_node, 1, mismatch + 1, []))
                            else: #Transpose on two own edge
                                matches.extend(dl_distance_v2(text, patt[0] + patt[2:], node[x].end_node[patt[0]], node[x].end_node, 1, mismatch + 1, []))
                        elif len(node[x]) == 1 and node[x].end_node[patt[1]] is not None: #Substitution on own edge
                            matches.extend(dl_distance_v2(text, patt[2:], node[x].end_node[patt[1]], node[x].end_node, 1, mismatch + 1, []))
                        elif len(node[x]) == 1 and node[x].end_node[patt[0]] is not None: #Deletion on own edge
                            matches.extend(dl_distance_v2(text, patt[1:], node[x].end_node[patt[0]], node[x].end_node, 1, mismatch + 1, []))
                        elif text[node[x].start + 1] == patt[0]: #Deletion at node
                            matches.extend(dl_distance_v2(text, patt, node[x], node, 1, mismatch + 1, []))
                        elif text[node[x].start + 1] == patt[1]: #Substitution at node
                            matches.extend(dl_distance_v2(text, patt[1:], node[x], node, 1, mismatch + 1, []))
                return matches
            elif len(edge) <= active_len:
                if patt[0] == text[edge.end.end]:
                    if len(patt) == 2 and edge.end_node[patt[0]] is None and mismatch == 0: #Insertion at end of pattern
                        matches.append((edge, mismatch + 1))
                    matches.extend(dl_distance_v2(text, patt[1:], None, edge.end_node, 0, mismatch, []))
                elif patt[1] == text[edge.end.end]: #Insertion right before node
                    matches.extend(dl_distance_v2(text, patt[1:], edge, node, active_len, mismatch + 1, []))
                elif edge.end_node[patt[0]] is not None and text[edge.end.end] == patt[1]: #Transpose between edges
                    if len(edge.end_node[patt[0]]) == 1 and edge.end_node[patt[0]].end_node is not None:
                        matches.extend(dl_distance_v2(text, patt[0] + patt[2:], edge.end_node[patt[0]], edge.end_node, 1, mismatch + 1, []))
                    else:
                        matches.extend(dl_distance_v2(text, patt[2:], edge.end_node[patt[0]], edge.end_node, 1, mismatch + 1, []))
                elif edge.end_node[patt[1]] is not None: #Substitute before next node
                    matches.extend(dl_distance_v2(text, patt[1:], edge.end_node[patt[1]], edge.end_node, 0, mismatch + 1, []))
                return matches
            else:
                print(patt, text[edge.start + active_len])
                if text[edge.start + active_len] == text[0]:
                    if active_len + 1 == len(edge):
                        print("true")
                        matches.extend(dl_distance_v2(text, patt, edge, edge.end_node, active_len + 1, mismatch, []))
                    else:
                        matches.extend(dl_distance_v2(text, patt[1:], edge, edge.end_node, active_len + 1, mismatch, []))
                elif len(edge) >= active_len + 1 and text[edge.start + active_len + 1] == text[1]:
                    matches.extend(dl_distance_v2(text, patt[1:], edge, edge.end_node, active_len + 1, mismatch + 1, []))
                elif len(edge) > active_len + 1 and text[edge.start + active_len + 1] == text[0] and text[edge.start + active_len] == text[1]:
                    matches.extend(dl_distance_v2(text, patt[2:], edge, edge.end_node, active_len + 2, mismatch + 1, []))
                elif len(edge) >= active_len + 1 and text[edge.start + active_len + 1] == text[0]:
                    matches.extend(dl_distance_v2(text, patt, edge, edge.end_node, active_len + 1, mismatch + 1, []))
                return matches
        else:
            print(patt,"========Match?")
            if edge is not None:
                if len(patt) == 1:
                    if text[edge.start + active_len] == patt[0]:
                        matches.append((edge, mismatch))
                    elif mismatch == 0:
                        matches.append((edge, mismatch + 1))
                else:
                    matches.append((edge, mismatch))
            else:
                if node[patt[0]] is not None:
                    matches.append((node[patt[0]], mismatch))
            return matches
        
    def dl_distance_v3(text, patt, tree):
        def mid_to_end_DL1(edge, index, active_len):

            while index < len(patt) and edge is not None:
                print(index, active_len, patt[index])
                if active_len >= len(edge) and edge.end_node is not None:
                    print("this happened")
                    #print(edge.end_node.name)
                    edge = edge.end_node[patt[index]]
                    active_len = 0
                elif text[edge.start + active_len] != patt[index]:
                    print(edge.start, active_len, index, len(edge))
                    print("mismatched")
                    return None
                index += 1
                active_len += 1
            if edge is not None:
                print(edge.start, index,"matched dl1")
            return edge
        
        def start_from_node(node, index):
            matches = []
            for x in node.get_all_keys():
                if node[x] is not None:
                    print(x, index)
                    if len(patt) > index + 1:
                        if len(node[x]) > 1 and x == patt[index + 1]:
                            if text[node[x].start + 1] == patt[index] and len(patt) > index + 2 and patt[index] != patt[index+2]: #Transposition at the start
                                matches.append((mid_to_end_DL1(node[x], index + 2, 2), 1))
                            else: #Insertion at the start
                                matches.append((mid_to_end_DL1(node[x], index + 2, 1), 1))
                        if len(node[x]) > 1 and text[node[x].start + 1] == patt[index + 1]: #Substitution at the start
                            matches.append((mid_to_end_DL1(node[x], index + 1, 1), 1))
                        if len(node[x]) == 1:
                            if node[x].end_node is None:
                                continue
                            else:
                                for y in node[x].end_node.get_all_keys():
                                    if node[x].end_node[y] is not None:
                                        print(x, y, index)
                                        if x == patt[index + 1] and y == patt[index]:
                                            matches.append((mid_to_end_DL1(node[x].end_node[y], index + 2, 1), 1))
                                        elif y == patt[index]:
                                            matches.append((mid_to_end_DL1(node[x].end_node[y], index, 0), 1))
                                        elif x == patt[index + 1]:
                                            matches.append((mid_to_end_DL1(node[x].end_node[y], index + 2, 0), 1))
                                        elif y == patt[index + 1]:
                                            matches.append((mid_to_end_DL1(node[x].end_node[y], index + 1, 0), 1))
                    else:
                        if x == patt[index]:
                            matches.extend(mid_to_end_DL0(node[x], [], index + 1, 1))
                        if len(node[x]) > 1 and text[node[x].start + 1] == patt[index]: #Substitution at the start
                            matches.append((mid_to_end_DL1(node[x], index, 1), 1))    
                        
            return matches
        
        def mid_to_end_DL0(edge, matches, index, active_len):
            mismatch = 0

            while index < len(patt) and mismatch < 2:
                print("dl0 matching")
                if active_len == len(edge) and edge.end_node is not None:
                    matches.extend(start_from_node(edge.end_node, index))
                    return matches
                elif text[edge.start + active_len] != patt[index]:
                    mismatch += 1
                    if mismatch == 2:
                        return matches
                    if index == len(patt) - 1: #Final char mismatch
                        matches.append((edge, mismatch))
                    elif active_len + 1 == len(edge):
                        if text[edge.start + active_len] == patt[index+1]: 
                            if edge.end_node[patt[index]] is not None: #Transposition at end of edge
                                matches.append((mid_to_end_DL1(edge.end_node[patt[index]], index + 2, 1), 1))
                            else: #Insertion at end of edge
                                matches.append((mid_to_end_DL1(edge, index + 1, active_len), 1))

                        elif edge.end_node[patt[index]] is not None:#Deletion at end of edge
                            matches.append((mid_to_end_DL1(edge.end_node[patt[index]], index + 1, 1), 1))

                        elif edge.end_node[patt[index+1]] is not None: #Substitution at end of edge
                            matches.append((mid_to_end_DL1(edge.end_node[patt[index+1]], index + 2, 1), 1))
                    else:
                        if text[edge.start + active_len + 1] == patt[index + 1]: #Substitution in middle of edge and patt
                            matches.append((mid_to_end_DL1(edge, index + 1, active_len+1), 1))
                        elif text[edge.start + active_len] == patt[index + 1]: 
                            if text[edge.start + active_len + 1] == patt[index] and index + 2 < len(patt): #Transposition in middle of edge and patt
                                matches.append((mid_to_end_DL1(edge, index + 2, active_len+2), 1))
                            else: #Insertion in middle of edge and patt
                                matches.append((mid_to_end_DL1(edge, index + 2, active_len+1), 1))
                        elif text[edge.start + active_len + 1] == patt[index]: #Deletion in middle of edge and patt
                            matches.append((mid_to_end_DL1(edge, index + 1, active_len+2), 1))
                    return matches
                else: 
                    print("dl 0 matching")
                    index += 1
                    active_len += 1
            print("matched at dl0")
            matches.append((edge, mismatch))
            return matches

        text += "$"
        matches = []
        if len(patt) > 1:
            matches = start_from_node(tree, 0)
        return matches


    text += "$"
    if len(patt) > 0:
        matches = dl_distance_v3(text, patt, tree)
    return matches



text = "abcabxabbbabbbx"
text2 = "tctcatcaazggaaccattgAtcc"

tree = ukkonen_arun(text2)

patt = "bab"

first = dl_distance_tree(text2, patt, tree)
#second, x = dl_distance_tree(text, "abbbx", tree)
all_matches = []
for edge, dis in first:
    if edge is not None:
        for index in dfs(edge):
            all_matches.append((index, dis))

print(all_matches)

print(dl_distance(text2, patt))

"""print(x)
print(second)
if second is not None:
    print(dfs(second))"""











#edge = traverse_v2(text, "tc", tree)
"""if edge is not None:
    print(dfs(edge))"""
"abacabad"
"""print(t)
if t is not None:
    print(dfs(t))"""
#print(get_all_indices(tree))
#print(tree["a"])

"""edges = [(traverse_v3(text2, patt[:x], tree), traverse_v3(text2, patt[x:], tree)) for x in range(1, len(patt)+1)]
f = [0] * (len(text2)+1)
b = [0] * (len(text2)+1)
y = 0
for x in edges:
    front = x[0]
    back = x[1]
    if front is not None:
        for ind in dfs(front):
            if f[ind] < len(patt[:y]):
                f[ind] = len(patt[:y])

    if back is not None:
        for ind in dfs(back):
            if b[ind + len(patt[y:]) -1] < len(patt[y:]):
                b[ind + len(patt[y:]) - 1] = len(patt[y:])
    y+=1

print(f)
print(b[::-1])
text = text2
pattern = patt
zarr1 = f
zarr2 = b[::-1]

output = []
"""

"""
"abcabxabbbabbbx"
[16, 7, 11, 1, 4, 10, 9, 8, 12, 13, 2, 14, 5, 3, 15, 6]
"""
"""
"tctcatcaazggaaccattgAtcc"
[20, 12, 7, 13, 4, 16, 8, 23, 6, 3, 
15, 22, 14, 1, 19, 11, 10, 5, 2, 21, 
0, 18, 17, 9, 20, 12, 7, 13, 4, 16, 
8, 23, 6, 3, 15, 22, 14, 1, 19, 11, 
10, 5, 2, 21, 0, 18, 17, 9]
"""

"""base = Node("$")
e = Edge(0,End(1))
base.edges[ord("a")%26] = e

n = Node("b")
e.end_node = n

e = Edge(2,End(6))
n.edges[ord("x")%26] = e
e = Edge(5,End(6))
n.edges[ord("c")%26] = e

n = Node("c")
e.end_node = n

e = Edge(7,End(8))
n.edges[ord("a")%26] = e
e = Edge(9,End(10))
n.edges[ord("y")%26] = e

(traverse("abxe", "abxfr",base))

print(base)"""
