from antrouting import Network

#create the connections in your network (Alice is node 0, Bob is node with the max index)
connections = [
    (0,1),
    (1,2),
    (2,3),
    (3,4),
    (1,3),
    (4,5)
]
#Here, Alice is node 0, Bob is node 5

#create network
network = Network(connections)

#display network 
network.display()

#find shortest payment path
network.find_shortest_path()