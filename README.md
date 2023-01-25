# Ant Routing simulation
LN Ant Routing algorithm simulation using NetworkX and Python.  
The logic is based on https://github.com/LNantfarm/ant-routing-simul

## How to use
Import _Network_ class from [antrouting.py](antrouting.py)
```python
from antrouting import Network
```
To create your network, defines all connections between nodes. Alice is node 0 and Bob is the max index node
```python
connections = [
    (0,1),
    (1,2),
    (2,3),
    (3,4),
    (1,3),
    (4,5)
]
#Here, Alice is node 0, Bob is node 5
```
Create a network object from the _Network_ class
```python
network = Network(connections)
```

Display the network 
```python
network.display()
```

Calculate the shortest path 
```python
network.find_shortest_path()
```


_Check [example.py](example.py) to get an example on how to use the simulation._

## Room for improvement
The network creation is not really user friendly, an improvement could be done here. For example, an easy way of creating the network would be to draw the network in Polar, and automatically translate it to a list of connections.


