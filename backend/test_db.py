import os
from graphviz import Digraph


def create_graph(path, graph):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            graph.node(dir)
            graph.edge(os.path.basename(root), dir)
        for file in files:
            graph.node(file, shape="box")
            graph.edge(os.path.basename(root), file)


dot = Digraph(comment="Project Structure")
create_graph("main", dot)
dot.render("project_structure.png", view=True)
