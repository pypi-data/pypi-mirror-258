# graph-express

Python package for the analysis and visualization of network graphs with familiar libraries such as
[NetworkX](https://networkx.org/), [NetworKit](https://networkit.github.io/), [igraph](https://igraph.org/), [cdlib](https://cdlib.readthedocs.io/en/latest/), and [Plotly](https://plotly.com/).

## Requirements

* **Python 3.6.8+**
* cdlib>=0.3.0
* datashader>=0.10.0
* kaleido>=0.2.1
* leidenalg>=0.8.3
* networkit>=7.0
* networkx>=2.3
* networkx-gdf>=1.1
* openpyxl>=3.1.2
* pandas>=0.25.3
* plotly>=3.10.0
* python-igraph>=0.8.3
* python-louvain>=0.14

## Usage

> The following is an overview of the package, to be replaced with guidelines detailing its usage with examples.

### Import high-level class

```python
import graph_express.graph_express as gx
```

#### Read graph from file

Accepted extensions include all formats supported by [networkx](https://networkx.org/documentation/stable/reference/readwrite/index.html) and [networkx-gdf](https://pypi.org/project/networkx-gdf/).

```python
G = gx.read_graph("/path/to/file.ext", ...)
```

#### Compute centrality and communities

Generates a data frame with node centrality values and communities, e.g., using the Leiden algorithm:

```python
df = gx.compute(G, attrs=["degree", "leiden"])
```

#### Plot network graph

Calculates positions and plots the network graph.

```python
fig = gx.draw(G, layout="forceatlas2", renderer="networkx")
```

<!-- For details on implemented layouts and renderers, please see the [documentation](). -->

___

### Import specific classes

This package implements six classes with static methods to allow inheriting their implemented methods:

```python
import graph_express

Centrality = graph_express.Centrality()
Community = graph_express.Community()
Convert = graph_express.Convert()
Draw = graph_express.Draw()
Graph = graph_express.Graph()
Layout = graph_express.Layout()
```

Note that all implemented methods are static and also exposed by `graph_express.graph_express` (see example above).

#### Centrality

Computes weighted or unweighted (in-/out-) degree, bridging, and brokering centrality. Wrappers available for NetworkX (`nx`) and NetworKit (`nk`).

```python
from graph_express import Centrality

# Centrality.bridging_centrality
# Centrality.bridging_coef
# Centrality.brokering_centrality
# Centrality.degree
# Centrality.in_degree
# Centrality.nk_centrality
# Centrality.nx_centrality
# Centrality.out_degree
# Centrality.weighted_degree
# Centrality.weighted_in_degree
# Centrality.weighted_out_degree
```

#### Community

Computes Louvain or Leiden community modules, as implemented by the authors. Wrappers available for cdlib and NetworKit (`nk`).

```python
from graph_express import Community

# Community.cdlib_community
# Community.leiden
# Community.louvain
# Community.nk_community
```

#### Convert

Converts graphs from and to igraph (`ig`), NetworKit (`nk`), NetworkX (`nx`), Pandas (`pd`), and PyTorch Geometric (`pyg`) formats.

```python
from graph_express import Convert

# Convert.ig2nk
# Convert.ig2nx
# Convert.nk2ig
# Convert.nk2nx
# Convert.nx2ig
# Convert.nx2nk
# Convert.nx2pyg
# Convert.pd2nx
# Convert.pyg2nx
```

#### Draw

Plots network graphs using NetworkX (`nx`) or Plotly, as well as degree histograms and similarity matrices among graphs.

```python
from graph_express import Draw

# Draw.draw
# Draw.draw_nx
# Draw.draw_plotly
# Draw.histogram
# Draw.similarity_matrix
```

#### Graph

Convenience functions to read or write from file, as well as manipulate graph objects.

```python
from graph_express import Graph

# Graph.adjacency
# Graph.agg_edge_attr
# Graph.agg_nodes
# Graph.compose
# Graph.density
# Graph.diameter
# Graph.edges
# Graph.graph
# Graph.info
# Graph.is_graph
# Graph.isolates
# Graph.k_core
# Graph.nodes
# Graph.read_graph
# Graph.remove_edges
# Graph.remove_nodes
# Graph.remove_selfloop_edges
# Graph.set_edge_attributes
# Graph.set_node_attributes
# Graph.write_graph
```

#### Layout

Calculate node positions to use for `graph_express.draw`.

```python
from graph_express import Layout

# Layout.layout
# Layout.circular_layout
# Layout.forceatlas2_layout
# Layout.kamada_kawai_layout
# Layout.random_layout
```

___

### Command line interface

An experimental CLI is partially implemented and may be executed with `graph-express`.

```
graph-express [-h] [-o OUTPUT] [-a ATTRS [ATTRS ...]] [-c NODE_COLOR]
               [-e EDGE_ATTR [EDGE_ATTR ...]] [-g GROUPS] [-k K_CORE]
               [-l LAYOUT] [-n NODE_ATTR [NODE_ATTR ...]] [-p POS]
               [-r SEED] [-s SOURCE] [-t TARGET] [--directed]
               [--multigraph] [--no-edges-attrs] [--no-node-attrs]
               [--normalized] [--selfloops]
               {build,compute,plot} input [input ...]

positional arguments:
  {build,compute,plot}  Action to execute.
  input                 Path to input graphs or data set files.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output path to write returned data.
  -a ATTRS [ATTRS ...], --attrs ATTRS [ATTRS ...]
                        Available attributes: ['bridging_centrality',
                        'bridging_coef', 'brokering_centrality', 'degree',
                        'in_degree', 'nk_centrality', 'nx_centrality',
                        'out_degree', 'weighted_degree', 'weighted_in_degree',
                        'weighted_out_degree', 'cdlib_community', 'label',
                        'leiden', 'louvain', 'nk_community'].
  -c NODE_COLOR, --color NODE_COLOR
                        Set node color (example: '#ccc').
  -e EDGE_ATTR [EDGE_ATTR ...], --edge-attrs EDGE_ATTR [EDGE_ATTR ...]
                        Set edge attributes to consider when building graphs.
  -g GROUPS, --groups GROUPS
                        Get node groups from file (containing two columns,
                        indexed by 'id').
  -k K_CORE, --k-core K_CORE
                        Apply k-core to graph.
  -l LAYOUT, --layout LAYOUT
                        Available layouts: ['circular_layout',
                        'forceatlas2_layout', 'kamada_kawai_layout', 'layout',
                        'random_layout'] (default: 'kamada_kawai').
  -n NODE_ATTR [NODE_ATTR ...], --node-attrs NODE_ATTR [NODE_ATTR ...]
                        Set node attributes to consider when building graphs.
  -p POS, --positions POS
                        Get node 2 or 3-dimensional positions from file.
  -r SEED, --random-seed SEED
                        Specify random seed for predictable randomness.
  -s SOURCE, --source SOURCE
                        Field name to consider as source.
  -t TARGET, --target TARGET
                        Field name to consider as target.
  --directed            Set as directed graph.
  --multigraph          Set as multigraph (allow multiple edges connecting a
                        same pair of nodes).
  --no-edges-attrs      Ignore edge attributes when building graphs.
  --no-node-attrs       Ignore node attributes when building graphs.
  --normalized          Returns normalized centrality values (from 0 to 1.0).
  --selfloops           Allow edges connecting a node to itself.
```

___

## References

* [cdlib](https://cdlib.readthedocs.io/)
* [Datashader](http://datashader.org)
* [igraph](https://igraph.org)
* [Leiden](https://leidenalg.readthedocs.io)
* [Louvain](https://python-louvain.readthedocs.io)
* [NetworkX](https://networkx.github.io)
* [Networkit](https://networkit.github.io/)
* [Pandas](https://pandas.pydata.org/)
* [Plotly](https://plot.ly)
