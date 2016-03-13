# Decision problems are often just as hard as as actually returning an answer.
# Show how a k-clique can be found using a solution to the k-clique decision 
# problem.  Write a Python function that takes a graph G and a number k 
# as input, and returns a list of k nodes from G that are all connected 
# in the graph.  Your function should make use of "k_clique_decision(G, k)", 
# which takes a graph G and a number k and answers whether G contains a k-clique.  
# We will also provide the standard routines for adding and removing edges from a graph.

# Returns a list of all the subsets of a list of size k
def k_subsets(lst, k):
    if len(lst) < k:
        return []
    if len(lst) == k:
        return [lst]
    if k == 1:
        return [[i] for i in lst]
    return k_subsets(lst[1:],k) + map(lambda x: x + [lst[0]], k_subsets(lst[1:], k-1))

# Checks if the given list of nodes forms a clique in the given graph.
def is_clique(G, nodes):
    for pair in k_subsets(nodes, 2):
        if pair[1] not in G[pair[0]]:
            return False
    return True

# Determines if there is clique of size k or greater in the given graph.
def k_clique_decision(G, k):
    nodes = G.keys()
    result = None
    for i in range(k, len(nodes) + 1):
        for subset in k_subsets(nodes, i):
            if is_clique(G, subset):
                return subset
    return False

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def break_link(G, node1, node2):
    if node1 not in G:
        print "error: breaking link in a non-existent node"
        return
    if node2 not in G:
        print "error: breaking link in a non-existent node"
        return
    if node2 not in G[node1]:
        print "error: breaking non-existent link"
        return
    if node1 not in G[node2]:
        print "error: breaking non-existent link"
        return
    del G[node1][node2]
    del G[node2][node1]
    return G

def remove_node(G, node):
    neighbours = G[node].copy()
    for neighbour in neighbours:
        break_link(G, node, neighbour)    
    return neighbours

def add_node(G, node, neighbours):
    for neighbour in neighbours:
        make_link(G, node, neighbour)
            
def k_clique(G, k):
    if not k_clique_decision(G, k):
        return False
    
    if k == 1:
        return [G.keys()[0]]

    for node in G:
        neighbours = remove_node(G, node)
        if not k_clique_decision(G, k):
            add_node(G, node, neighbours)
    return sorted([key for key in G.keys() if len(G[key]) > 0])

print k_clique({1:{}}, 1) == [1]
print k_clique({1:{2:1, 3:1}, 2:{1:1}, 3:{1:1}}, 3) == False
print k_clique({1:{2:1, 3:1, 4:1}, 2:{1:1, 4:1}, 3:{1:1}, 4:{1:1, 2:1}}, 3) == [1, 2, 4]
print k_clique({1:{2:1, 3:1, 4:1}, 2:{1:1, 3:1, 4:1}, 3:{1:1, 2:1, 4:1}, 4:{1:1, 2:1, 3:1}}, 4) == [1, 2, 3, 4]
