from py2neo import Graph
from igraph import Graph as IGraph


class Neo4jGraph:

    def __init__(self, uri, user, password):
        self.graph = Graph(uri, bolt=True, user=user, password=password)

    # vertex_name_attr = "name" as default
    # edge_attrs = "weight" if not assigned
    def get_igraph(self, query, vertex_attr):
        return IGraph.TupleList(self.graph.run(query), vertex_name_attr=vertex_attr)

    def save_graph(self, update_cypher, pgvs):
       return self.graph.run(update_cypher, nodes=pgvs)







