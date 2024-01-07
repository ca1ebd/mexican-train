import networkx as nx
import matplotlib.pyplot as plt

from Table import Table

class Visualizer:
    def __init__(self, table: Table):
        self.table = table
        self.colors = ["red", "cyan", "pink", "yellow", "orange"]
        self.graph = self.build_graph_from_table(table)

    def build_graph_from_table(self, table: Table) -> Table:
        DG = nx.DiGraph()
        DG.add_node(table.spinner, color="green")
        for player in table.trains:
            DG.add_nodes_from(table.trains[player].dominoes, color=player.color)
            for i in range(0, len(table.trains[player].dominoes) - 1):
                dominoes = table.trains[player].dominoes
                DG.add_edge(dominoes[i], dominoes[i+1])
            # TODO make this better...
            if player.is_real and len(table.trains[player].dominoes) > 0:
                # add connection to spinner
                DG.add_edge(table.spinner, table.trains[player].dominoes[0])
        return DG


    def test_nx(self):
        G = nx.Graph()

        G.add_node(1)
        G.add_nodes_from([2, 3])

        nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40)
        plt.show()

    def on_key(self, event):
        if event.key == ' ':
            plt.close()

    def render(self):
        # pos = nx.shell_layout(self.graph, [self.table.trains[x].dominoes for x in self.table.trains].insert(0, self.table.spinner))
        pos = nx.circular_layout(self.graph)
        pos[self.table.spinner] = (0, 0)
        # print(self.graph.nodes[0]["color"])
        fig, ax = plt.subplots(figsize=(10, 8))
        nx.draw(
            self.graph, 
            pos = pos,
            ax=ax,
            with_labels=True, 
            node_size=100, 
            node_color=[self.graph.nodes[node]["color"] for node in self.graph.nodes], 
            node_shape="s", 
            # alpha=0.5,
            linewidths=10)
        
        fig.canvas.mpl_connect('key_press_event', self.on_key)

        plt.show()

if __name__ == "__main__":
    vis = Visualizer(Table([], []))
    vis.test_nx()

