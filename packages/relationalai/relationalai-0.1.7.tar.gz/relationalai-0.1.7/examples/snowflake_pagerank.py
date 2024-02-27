#pyright: reportUnusedExpression=false
from typing import Tuple
import rich
import relationalai as rai
from relationalai.graphs import Graph
from relationalai.clients.snowflake import Snowflake, PrimaryKey

model = rai.Model("SFPagerank", dry_run=False)

#--------------------------------------------------
# Initialize Snowflake data
#--------------------------------------------------

sf = Snowflake(model)
Account = sf.sandbox.public.accounts
Account.describe(
    account_id=PrimaryKey,
)

Transaction = sf.sandbox.public.transactions
Transaction.describe(
    id=PrimaryKey,
    from_account=(Account, "from_"),
    to_account=(Account, "to")
)

#--------------------------------------------------
# Add types
#--------------------------------------------------

Merchant = model.Type("Merchant")
Person = model.Type("Person")

with model.rule():
    a = Account()
    with a.account_type == "Merchant":
        a.set(Merchant)
    with a.account_type == "User":
        a.set(Person)

#--------------------------------------------------
# Create a graph
#--------------------------------------------------

graph = Graph(model)
nodes, edges = graph.nodes, graph.edges

nodes.extend(Account, hover=Account.name)
nodes.extend(Person, color="#bbb")
nodes.extend(Merchant, color="green", label=Merchant.name)

with model.rule():
    t = Transaction()
    edges.add(t.from_, t.to, size=t.amount / 50, color="#ccc", opacity=0.3)

with model.rule():
    m = Merchant()
    rank = graph.compute.pagerank(m)
    nodes.add(m, size=((rank * 100) ** 2.2) + 10, rank=rank)
    m.set(rank=rank)

#--------------------------------------------------
# Visualize the graph
#--------------------------------------------------

graph.visualize(
    three=True,
    node_label_size_factor=1.2,
    use_links_force=True,
    links_force_distance=140,
    node_hover_neighborhood=True,
).display()

#--------------------------------------------------
# Export the analysis
#--------------------------------------------------

@model.export("sandbox.public")
def merchant_rank(minimum: float) -> Tuple[str, float, int]:
    m = Merchant()
    m.rank >= minimum
    t = Transaction(to=m)
    total = model.aggregates.sum(t, t.amount, per=[m])
    return m.name, m.rank, total #type: ignore

print("\nCalling merchant rank from Snowflake!\n")
for row in model.resources._exec("call sandbox.public.merchant_rank(0.04);"):
    rich.print(row)







