from neo4j_config import neo4j_graph as neo4j
import datetime

uri = "bolt://192.168.1.242:7687"
# uri = "bolt://localhost:7687"
user = "neo4j"
password = "beidasoft"

# query = "MATCH (m:Character)-[r:INTERACTS]->(n:Character) RETURN m.name,n.name,r.weight as weight"
query = "MATCH (m)-[r]->(n:Company) RETURN m.id, n.id limit 100"

vertex_attr = "id"

write_pagerank_cypher = '''
    UNWIND {nodes} AS n
    MATCH (c:Company) WHERE c.id = n.id
    SET c.pagerank = n.pg
    '''
write_walktrap_cypher = '''
UNWIND {nodes} AS n
MATCH (c) WHERE c.id = n.id
SET c.community = toInt(n.community)
'''


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

print("Begin export data from neo4j... current time :", get_current_time())

iGraph = neo4j.Neo4jGraph(uri, user, password)

ig = iGraph.get_igraph(query, vertex_attr)

print("exporting is completed !!! current time :", get_current_time())


print('vertex:', ig.vcount())
print('edges:', ig.ecount())


def page_rank():
    pg = ig.pagerank()
    pgvs = []
    for p in zip(ig.vs, pg):
        print("id:", p[0][vertex_attr], "   rank:", p[1])
        pgvs.append({vertex_attr: p[0][vertex_attr], "pg": p[1]})
    # print(pgvs)
    return pgvs


def walk_trap():
    print("Begin walk trap... current time :", get_current_time())
    # clusters = neo4j.IGraph.community_walktrap(ig).as_clustering()
    clusters = neo4j.IGraph.community_multilevel(ig)

    print("walk trap end !!! current time :", get_current_time())
    nodes = []
    count = 0
    for node in ig.vs:
        # idx = ig.vs.find(id=node["id"]).index
        node["community"] = clusters.membership[count]
        nodes.append({"id": node["id"], "community": node["community"]})
        count += 1
        print("id:", node["id"], "  community:", node["community"], "   count:", count)
    return nodes

# nodes = page_rank()
# iGraph.save_graph(write_pagerank_cypher, nodes)

nodes1 = walk_trap()
print(nodes1)
print("Begin update data to neo4j... current time :", get_current_time())
# iGraph.save_graph(write_walktrap_cypher, nodes1)
print("Writing data to neo4j is completed !!! current time :", get_current_time())

