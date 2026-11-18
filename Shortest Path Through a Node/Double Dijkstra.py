from __future__ import annotations
import math

class Location:

    def __init__(self, name: str) -> None:
        """
        Function description: This function creates a Location object

        Input: 
            name: the name of the object

        Time complexity: 
            O(1)
        Aux Space complexity:
            O(1)
        """

        self.id = name
        self.edges = []
        self.friend = None
        self.distance = math.inf
        self.discovered = False
        self.visited = False
        self.previous = None

    def __str__(self) -> str:
        """
        Function description: This function returns a string representation of the object
        
        Time complexity: 
            O(n)
            where n is the number of edges in self.edges
        Aux Space complexity:
            O(n)
            where n is the number of edges in self.edges
        """

        s = f"Location: {self.id}\n"
        for connection in self.edges:
            s += f"Edge:\n{connection}\n"
        s += f"Friend: {self.friend}\n"
        s += f"Distance: {self.distance}\n"
        return s

    """
	Function description: These functions override the default comparison functions so that the objects can be compared to each other
	
	Input: 
		__value: the item to be compared with
    
    Time complexity: 
        O(1)
    Aux Space complexity:
        O(1)
	"""

    def __lt__(self, __value: Location) -> bool:
        return self.distance < __value.distance
    
    def __le__(self, __value: Location) -> bool:
        return self.distance <= __value.distance
    
    def __gt__(self, __value: Location) -> bool:
        return self.distance > __value.distance
    
    def __ge__(self, __value: Location) -> bool:
        return self.distance >= __value.distance


class Edge:

    def __init__(self, p1: Location, p2: Location, weight: int) -> None:
        """
        Function description: This function creates an Edge object
        
        Input: 
            p1: the starting point of the edge
            p2: the ending point of the edge
            weight: the weight of the edge
        
        Time complexity: 
            O(1)
        Aux Space complexity:
            O(1)
        """

        self.p1 = p1
        self.p2 = p2
        self.weight = weight
    
    def __str__(self) -> str:
        """
        Function description: This function returns a string representation of the object
        
        Time complexity: 
            O(1)
        Aux Space complexity:
            O(1)
        """

        return f"Between {self.p1.id}  {self.p2.id}\nWeight {self.weight}"
        
class MinHeap:
    MIN_CAPACITY = 1

    def __init__(self, max_size: int) -> None:
        """
        Function description: This function creates a MinHeap object
        
        Input: 
            max_size: the maximum size of the MinHeap

        Time complexity: 
            O(n)
            where n is max_size
        Aux Space complexity:
            O(n)
            where n is max_size
        """

        self.length = 0
        self.array = [None] * (max(self.MIN_CAPACITY, max_size) + 1)

    def __len__(self) -> int:
        """
        Function description: This function returns the length o the MinHeap

        Time complexity: 
            O(1)
        Aux Space complexity:
            O(1)
        """

        return self.length
    
    def is_full(self) -> bool:
        """
        Function description: This function checks if the heap is full
        
        Time complexity: 
            O(1)
        Aux Space complexity:
            O(1)
        """

        return self.length + 1 == len(self.array)

    def smallest_child(self, k: int) -> int:
        """
        Function description: Returns the index of k's child with greatest value.

        Input: 
            k: the parent node to check the children of
                :pre: 1 <= k <= self.length // 2

        Time complexity: 
            O(1)
        Aux Space complexity:
            O(1)
        """

        if 2 * k == self.length or \
                self.array[2 * k] <= self.array[2 * k + 1]:
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self, k: int) -> None:
        """ 
        Function description: Make the element at index k sink to the correct position.

        Input: 
            k: the parent node to check the children of
                :pre: 1 <= k <= self.length

        Time complexity: 
            Best
                O(1)
            Worst
                O(log n)
                where n is the size of the Min Heap
        Aux Space complexity:
            O(1)
        """

        item = self.array[k]

        while 2 * k <= self.length:
            min_child = self.smallest_child(k)
            if self.array[min_child] > item:
                break
            self.array[k] = self.array[min_child]
            k = min_child

        self.array[k] = item

    def get_min(self) -> Location:
        """ 
        Function description: The function serves the highest priority item in the Min Heap

        Time complexity: 
            Best
                O(1)
            Worst
                O(log n)
                where n is the size of the Min Heap
        Aux Space complexity:
            O(1)
        """

        if self.length == 0:
            raise IndexError

        min = self.array[1]
        self.length -= 1
        if self.length > 0:
            self.array[1] = self.array[self.length+1]
            self.sink(1)
        return min
    
    @classmethod
    def heapify(cls, points: list, overwrite_size: int = 0) -> MinHeap[Location]:
        """ 
        Function description: This function creates a Min Heap out of the given list of points and optional overridden size

        Input: 
            points: the list of points to put in the Min Heap
            overwrite_size: the new size to use for iteration
                :pre: overwrite_size < len(points)

        Time complexity: 
            Best
                O(1)
            Worst
                O(nlogn)
                where n is the number of items in points.
        Aux Space complexity:
            O(n)
            where n is the number of items in points.
        """

        self = MinHeap((2 * len(points) + 2))
        self.length = overwrite_size
        for i in range(overwrite_size):
            self.array[i+1] = points[i]

        for k in range(overwrite_size, 0, -1):
            self.sink(k)
        return self

class CityMap:
    def __init__(self, roads: list[tuple[int, int, int]], tracks: list[tuple[int, int, int]], friends: list[tuple[str, int]]) -> None:
        """
        Function description:
            It creates a CityMap object and takes in a list of road edges, track edges, and friends then
            initializes the object attributes with the processed data using the processRoadNodes method.
        
        Approach description:
            My approach was that in order to find the shortest path between two distances considering each 
            call of dijkstra would only get a map of the shortest paths to every node from teh starting node,
            I need to have two maps so I can calculate to every node from the starting node and from the ending
            node. To accomplish this, I made a helper function that adds all the road edges undirected and all the
            locations friends could be in using the track edges directed. The first loop adds all the road nodes
            and the original locations of the friend nodes. The second loop checks if there is a friend that is at 
            most 1 edge away from their origin at the node that is the start of the edge and if there is then adds
            another friend at the end of the edge.

        :Input:
            roads: a list of edges for roads in tuple form <node1, node2, weight>
            tracks: a list of edges for tracks in tuple form <node1, node2, weight>
            friends: a list of friends in tuple form <friendname, friendlocation>

        :Time complexity:
            O(|R| + |T|)
            where |R| is the number of edges in roads
            where |T| is the number of edges in tracks

        :Aux Space complexity:
            O(|R|)
            where |R| is the number of edges in roads
        """

        self.length = 0
        self.map1, self.map2 = self.processRoadNodes(roads, tracks, friends)

    def processRoadNodes(self, roads: list[tuple[int, int, int]], tracks: list[tuple[int, int, int]], friends: list[tuple[str, int]]) -> tuple[list[Location], list[Location]]:
        """
        Function description:
            It takes in a list of road edges, track edges, and friends and creates two identical maps of them
            with all modifications made so they can be processed to be used in dijkstras algorithm.

        :Input:
            roads: a list of edges for roads in tuple form <node1, node2, weight>
            tracks: a list of edges for tracks in tuple form <node1, node2, weight>
            friends: a list of friends in tuple form <friendname, friendlocation>

        :Output:
            Two identical lists of Locations.

        :Time complexity:
            O(|R| + |T|)
            where |R| is the number of edges in roads
            where |T| is the number of edges in tracks

        :Aux Space complexity:
            O(|R|)
            where |R| is the number of edges in roads
        """

        locationList = [None] * (len(roads) + 1)
        locationList2 = [None] * (len(roads) + 1)

        for i in range(len(roads) + 1):
            
            if i < len(roads):
                if locationList[roads[i][0]] is None:
                    locationList[roads[i][0]] = Location(roads[i][0])
                    locationList2[roads[i][0]] = Location(roads[i][0]+(len(roads) + 1))
                    locationList2[roads[i][0]].id -= (len(roads) + 1)
                    self.length += 1
                
                if locationList[roads[i][1]] is None:
                    locationList[roads[i][1]] = Location(roads[i][1])
                    locationList2[roads[i][1]] = Location(roads[i][1]+(len(roads) + 1))
                    locationList2[roads[i][1]].id -= (len(roads) + 1)
                    self.length += 1

                locationList[roads[i][0]].edges.append(Edge(locationList[roads[i][0]], locationList[roads[i][1]], roads[i][2]))
                locationList2[roads[i][0]].edges.append(Edge(locationList2[roads[i][0]], locationList2[roads[i][1]], roads[i][2]))

                locationList[roads[i][1]].edges.append(Edge(locationList[roads[i][1]], locationList[roads[i][0]], roads[i][2]))
                locationList2[roads[i][1]].edges.append(Edge(locationList2[roads[i][1]], locationList2[roads[i][0]], roads[i][2]))
                
            if i < len(friends):
                if locationList[friends[i][1]] is None:
                    locationList[friends[i][1]] = Location(friends[i][1])
                    locationList2[friends[i][1]] = Location(friends[i][1]+(len(roads) + 1))
                    locationList2[friends[i][1]].id -= (len(roads) + 1)
                    self.length += 1
                locationList[friends[i][1]].friend = (friends[i][0], 0, 0)
                locationList2[friends[i][1]].friend = (friends[i][0], 0, 0)

        for track in tracks:
            if (locationList[track[0]].friend is not None) and locationList[track[0]].friend[1] < 2 and locationList[track[1]].friend is None:
                locationList[track[1]].friend = (locationList[track[0]].friend[0], locationList[track[0]].friend[1] + 1, locationList[track[0]].friend[2] + track[2])
                locationList2[track[1]].friend = (locationList2[track[0]].friend[0], locationList2[track[0]].friend[1] + 1, locationList2[track[0]].friend[2] + track[2])

        return locationList, locationList2

    def plan(self, start: int, destination: int) -> tuple[int, list[int], str, int]: 
        """
        Function description:
            The function takes in a starting point and ending point within the map and returns in a tuple, the
            total time of the path, a list of nodes it visited from start to end, the friend to pick up, and 
            the node the friend was picked up
        
        Approach description:
            My approach to finding the path with a checkpoint is to make two maps one with the shortest paths
            between alls and the start and all nodes and the end then mark the checkpoint that will give the
            shortest path between the two nodes. To accomplish this, I modified my dijkstra so on the second
            iteration, the first map can be provided so it marks which friend node would give the shortest path.
            I made this an optional parameter so I can avoid code repetition. Afterwards, I can use the Location
            I have saved to backtrack the path taken on both maps. The backtracking is done with the backtrack
            method. since I have two same nodes on different maps, I use the previous node of one of the maps 
            to start backtracking from to avoid repetition. Since the two sides are going in different directions,
            I reverse the first half of the path and extend the rest of the path. Other than that, the dijkstra
            algorithm is a normal minheap dijkstra.

        :Input:
            start: the starting node
            destination: the ending node

        :Time complexity:
            O(|L| + |R|log|L|)
            where |R| is the number of road edges
            where |L| is the number of locations in the map

        :Aux Space complexity:
            O(|L|)
            where |L| is the number of locations in the map

        """

        def dijkstra(map: list[Location], start: int, startMap: list[Location] | None =None) -> Location | None:
            """
            Function description:
                It takes in a list of road edges, track edges, and friends and creates two identical maps of them
                with all modifications made so they can be processed to be used in dijkstras algorithm.

            :Input:
                map: the map to be traversed
                start: the starting point in the map
                startMap: the optional second map to find checkpoints for
                    pre: the startMap needs to have gone through dijkstra already

            :Output:
                None or the checkpoint that gives the shortest path from start to end

            :Time complexity:
                O(|R|log|L|)
                where |R| is the number of road edges
                where |L| is the number of locations in the map

            :Aux Space complexity:
                O(|L|)
                where |L| is the number of locations in the map
            """
            
            map[start].discovered = True
            map[start].distance = 0
            heap = MinHeap.heapify(map, self.length)
            midpoint = None
            while len(heap) > 0:
                current_node = heap.get_min()
                current_node.visited = True

                if startMap is not None:
                    if current_node.friend is not None and midpoint is not None:
                        if current_node.distance + startMap[current_node.id].distance < midpoint.distance + startMap[midpoint.id].distance:
                            midpoint = current_node
                        elif current_node.distance + startMap[current_node.id].distance == midpoint.distance + startMap[midpoint.id].distance and current_node.friend[2] < midpoint.friend[2]:
                            midpoint = current_node
                    elif current_node.friend is not None:
                        midpoint = current_node

                for edge in current_node.edges:
                    adj_node = edge.p2
                    if adj_node.discovered == False:
                        adj_node.discovered = True
                        adj_node.distance = current_node.distance + edge.weight
                        adj_node.previous = current_node

                    elif adj_node.visited == False:
                        if adj_node.distance > current_node.distance + edge.weight:
                            adj_node.distance = current_node.distance + edge.weight
                            adj_node.previous = current_node 
                
            return midpoint

        def backtrack(node: Location | None) -> list[int]:
            """
            Function description:
                It takes in a node and returns a list of very node it visited to reach the current node
            :Input:
                node: A node that has already been processed through Dijkstras algorithm
                    
            :Output, return or postcondition:
                a list of all previously visited nodes to reach the given node.
            :Time complexity:
                O(n)
                where n is the number of backtracked nodes
            :Aux Space complexity:
                O(n)
                where n is the number of backtracked nodes
            """

            l = []
            if node is None:
                return l
            while node is not None:
                l.append(node.id)
                node = node.previous
            
            return l

        dijkstra(self.map1, start)
        friend = dijkstra(self.map2, destination, self.map1).id

        path = backtrack(self.map1[friend]) 
        path.reverse() #time O(n) n is the number of items in the list
        path.extend(backtrack(self.map2[friend].previous)) #O(m) m is the number of items to be added

        #^ time worst case O(|L|) |L| is the number of locations in the map
        #  Aux Space worst case O(|L|) |L| is the number of locatiosn in the map

        return (self.map1[friend].distance + self.map2[friend].distance, path, self.map1[friend].friend[0], friend)


print(int("Source"))