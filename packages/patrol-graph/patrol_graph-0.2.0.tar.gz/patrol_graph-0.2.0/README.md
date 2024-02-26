# patrol-graph

using python and metis to separate scouts into patrols based on their preferences

## installation

python -m venv venv
venv/bin/activate
python -m pip install -r requirements.txt

you also have to install the "dot" command (arch, ubuntu, debian, fedora: graphviz) to convert from dot file to png. Available here: [Graphviz.org](https://graphviz.org/download/)

## usage

### edges (friends)

create a file data/edges.txt with:

    scout1 scout2 scout4 scout8
    scout2 scout3
    scout3
    scout4 scout5
    scout5 scout8

where the first scout listed is the origin, and all subsequent scouts in the line will be considered friends, separated by a space.
any scouts listed alone will not have any outgoing edges

### besties (best friends)

besties are given additional configurable weight in making the graph, this makes the graph algorithm less likely to separate that link

create a file data/besties.txt with:

    scout1 scout2
    scout2
    scout3
    scout4 scout5
    scout5

where the first scout listed is the origin, and all subsequent scouts in the line will be considered best friends

### negs (scouts to avoid pairing)

negs provide a graph link with a negative score, encouraging the graph algorithm to separate the two scouts

create a file data/negs.txt with:

    scout1 scout3
    scout2
    scout3
    scout4 scout5
    scout5

where the first scout listed is the origin, and all subsequent scouts in the line will be considered scouts to avoid in pairing

### Config file

edit config.toml to configure integer weights to normal friends, best friends, and negatives

also configure the number of patrols for partitioning and the colors for the patrols chosen

## run 

    python script.py

where N is the number of patrols to divide the scouts into

output graph information is in output/output.dot

convert this using dot or the command from the graphviz package. A helper script in scripts/ is provided

    dot -Tpng output/output.dot > output/example.png

output text is in output/output.txt
