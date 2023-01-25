import networkx as nx
import matplotlib.pyplot as plt
import random
import asyncio

from ant_testing import Node, Payment

class Network():
    def __init__(self,connections=None):
        if connections == None:
            tmp = nx.fast_gnp_random_graph(50, 0.069)
            subs = list(sorted(nx.connected_components(tmp), key=len, reverse=True))
            self.g = tmp.subgraph(list(subs[0])).copy()
        else:
            self.g = nx.Graph()
            for connection in connections:
                self.g.add_edge(connection[0],connection[1])
        self.g = nx.relabel_nodes(self.g, { node:i for i,node in enumerate(self.g.nodes)})
        self.nodes = list(self.g.nodes)
        self.lengths = list(nx.all_pairs_shortest_path_length(self.g))
        self.dists = []

        for node_id,node_dists in self.lengths:
            dist_max = 0
            for k,v in node_dists.items():
                if v > dist_max:
                    dist_max = v
            self.dists.append(dist_max)

        try:
            self.max_dist = sorted(self.dists, reverse=True)[len(self.nodes)//10]
        except:
            self.max_dist = self.dists
        self.alice = self.nodes[0]
        endpoints = [ k for k,v in self.lengths[self.alice][1].items() if v == self.dists[self.alice]]
        self.bob = self.nodes[len(self.nodes)-1]

        try:
            self.g.remove_edge(self.alice, self.bob)
        except:
            pass

        

    def display(self):
        print(f'Distance is {self.max_dist}')
        nx.draw(self.g, 
            node_color=["yellow" if node in (self.bob, self.alice) else "green"
                for node in self.nodes ],
            with_labels=True)
        plt.show(block=False)
        plt.pause(0.01)
        nx.draw(self.g) 

    async def find_shortest_path_logic(self):
        seed_ab = 'beef'
        amount = 1337
        c_0 = random.randint(64,128)

        node_objects = [Node(node, set(self.g.neighbors(node))) for node in self.nodes]

        for node in node_objects: node.set_nodes(node_objects)

        node_bob = node_objects[self.bob]
        node_alice = node_objects[self.alice]

        payment_alice = Payment(
                seed_ab,
                amount,
                False,
                True,
                node_bob,
                node_alice,
                node_bob.maxfees + node_alice.maxfees,
                c_0,
                )
        payment_bob = Payment(
                seed_ab,
                amount,
                True,
                False,
                node_bob,
                node_alice,
                node_bob.maxfees + node_alice.maxfees,
                c_0,
                )
        
        node_bob.set_payment(payment_bob)
        node_alice.set_payment(payment_alice)

        for node in node_objects:
            node.start()

        tasks = []
        for node in node_objects:
            task = asyncio.create_task(node.ant_route())
            tasks.append(task)
        

        await asyncio.gather(*tasks)

        print("## Ant routing done ##")

    def find_shortest_path(self):
        asyncio.run(self.find_shortest_path_logic())