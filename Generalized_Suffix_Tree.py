class Node(object):
    """
    A node in the suffix tree
    
    suffix_node
        the index of a node that the current node points to via a suffix link
        -1 indicates the current node has no suffix link
        
    dist_from_root
        the total length of edges from the root to the current node
    """
    def __init__(self):
        self.suffix_node = -1
        self.dist_from_root = 0

class Edge(object):
    """
    An edge in the suffix tree.
    It stores info of a sublist and the two nodes that the current edge connects
    
    
    start_list_index
        index of the start element on the current edge
        
    end_list_index
        index of the end element on the current edge
        
    source_node_index
        index of source node of the current edge
    
    dest_node_index
        index of destination node of the current edge    
    """
    def __init__(self, start_list_index, end_list_index, source_node_index, dest_node_index):
        self.start_list_index = start_list_index
        self.end_list_index = end_list_index
        self.source_node_index = source_node_index
        self.dest_node_index = dest_node_index
    
    @property
    
    def length(self): # Length of the current edge
        return self.end_list_index - self.start_list_index + 1


class Activepoint(object):
    """
    Indicates where the current activepoint is
    
    source_node_index
        index of the source node to go from
    
    start_list_index
        index of the start element to tell which edge to go along
        
    end_list_index
        index of the end element to tell where to stop to get the current activepoint
    """
    def __init__(self, source_node_index, start_list_index, end_list_index):
        self.source_node_index = source_node_index
        self.start_list_index = start_list_index
        self.end_list_index = end_list_index
        
    @property

    def length(self): # Distance from the source node to the current activepoint
        return self.end_list_index - self.start_list_index + 1
                
    def explicit(self): # An activepoint is explicit if it is exactly at a node
        return self.length <= 0
    
    def implicit(self): # An activepoint is implicit if it is on an edge
        return self.length > 0

class GeneralizedSuffixTree(object):
    """
    Uses Ukkonen's algorithm to build a generalized suffix tree for list[list[int]].
    """
    def __init__(self, lists): # Input is list[list[int]] for which to construct a generalized suffix tree
        # Initialization
        self.nodes = [Node()]
        self.edges = {}
        self.lis = []
        self.N = -1 # The end of suffixes at each iteration
        self.active = Activepoint(0, 0, -1)
        
        # Adds str(i) at the end of the i-th list[int] as the ending symbol of the i-th list[int]
        # conbines all lists to get a large list
        for i, lis in enumerate(lists):
            self.lis += lis + [str(i)]
        
        # Iterates over all elements in the large list to build the suffix tree
        """
        ADDING ENDING SYMBOL str(i) AND CHANGE OF self.N IS THE KEY POINT OF BUILDING THIS TREE.
        When iterating over the k-th list[int], assigns self.N to be the index of str(k) which indicates the end of the k-th list[int].
        By doing this, when iterating over the k-th list[int], it only builds suffix tree for the k-th list[int] but not the rest lists.
        All suffixes constructed at phase i = self.N are explicit, so self.active = Activepoint(0, self.N + 1, self.N) when moving on to the next list.
        This automatically being the initialization needed for starting a new list.
        """
        j = 0
        for i in range(len(self.lis)):
            if i > self.N:
                self.N += len(lists[j])+1
                j += 1
            self._add_prefix(i)
            
    def _add_prefix(self, current_index):
        """
        The core construction.
        """
        last_parent_node = -1
        while True:
            parent_node = self.active.source_node_index
            if self.active.explicit():
                if (self.active.source_node_index, self.lis[current_index]) in self.edges:
                    # Prefix is already in the tree
                    break
            else:
                e = self.edges[self.active.source_node_index, self.lis[self.active.start_list_index]]
                if self.lis[e.start_list_index + self.active.length] == self.lis[current_index]:
                    # Prefix is already in the tree
                    break
                # Prefix is not in the tree, loop continues.
                # Activepoint is implicit, needs to split an old edge to add a node for the current_index
                parent_node = self._split_edge(e, self.active)
            
            # Builds a new node.
            self.nodes.append(Node())
            
            # Builds an edge from the parent node to the current node, containing current_index to the end index of the current list
            e = Edge(current_index, self.N, parent_node, len(self.nodes) - 1)
            
            # Update dist_from_root for the current node
            self.nodes[-1].dist_from_root = e.length + self.nodes[e.source_node_index].dist_from_root
            self._insert_edge(e)
            
            # Update suffix link if needed
            if last_parent_node > 0:
                self.nodes[last_parent_node].suffix_node = parent_node
            last_parent_node = parent_node
            
            # Update activepoint
            if self.active.source_node_index == 0:
                self.active.start_list_index += 1
            else:
                self.active.source_node_index = self.nodes[self.active.source_node_index].suffix_node
            self._walking_down(self.active)
            
        if last_parent_node > 0:
            self.nodes[last_parent_node].suffix_node = parent_node # update suffix link
        self.active.end_list_index += 1 # update activepoint
        self._walking_down(self.active)
        
    def _insert_edge(self, edge): # Inserts an edge to the edges dictionary
        self.edges[(edge.source_node_index, self.lis[edge.start_list_index])] = edge
        
    def _remove_edge(self, edge): # Removes an edge from the edges dictionary 
        self.edges.pop((edge.source_node_index, self.lis[edge.start_list_index]))
        
    def _split_edge(self, edge, activepoint): # Splits an edge at the activepoint to add in a new node
        self.nodes.append(Node())
        e = Edge(edge.start_list_index, edge.start_list_index + activepoint.length - 1, activepoint.source_node_index, len(self.nodes) - 1)
        self.nodes[-1].dist_from_root = e.length + self.nodes[e.source_node_index].dist_from_root
        self._remove_edge(edge)
        self._insert_edge(e)
        self.nodes[e.dest_node_index].suffix_node = activepoint.source_node_index
        edge.start_list_index += activepoint.length
        edge.source_node_index = e.dest_node_index
        self._insert_edge(edge)
        return e.dest_node_index

    def _walking_down(self, activepoint): # Updates activepoint by walking down to the nearest node
        while True:
            if not activepoint.explicit():
                e = self.edges[activepoint.source_node_index, self.lis[activepoint.start_list_index]]
                if e.length <= activepoint.length:
                    activepoint.start_list_index += e.length
                    activepoint.source_node_index = e.dest_node_index
                else: break
            else: break
    
    def find_longest_common_sublist(self):
        """
        Solves the longest 2-common sublist problem.
        Checks each edge to see if it ends at a string type element, if so, the source node of this edge is the end of common sublist of at least two lists.
        If there're multiple 2-common sublists with the same longest length, it only returns one of them.
        """
        max_length = 0 # max_length stores the length of longest 2-common sublist
        for x in self.edges:
            edge = self.edges[x]
            if isinstance(self.lis[edge.end_list_index], str):
                node_index = edge.source_node_index
                if self.nodes[node_index].dist_from_root > max_length:
                    max_length = self.nodes[node_index].dist_from_root
                    node_need_index = node_index
                    files_need = [node_index, (int(self.lis[edge.end_list_index]), - (edge.length + max_length - 1))]
                    # files_need stores [node_index, (index of list, offset)]
                elif node_index in files_need:
                    files_need.append((int(self.lis[edge.end_list_index]), - (edge.length + max_length - 1)))
        if max_length == 0: return False
        return max_length, files_need[1:]
        # It returns max_length, [(index of list, offset)]
