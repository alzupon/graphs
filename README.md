# Description
The python script `graphs.py` will create a Graph object from `coling2016_explanation_sentences.txt`, using each sentence as a node/vertex in the graph.

It will print out the content of nodes 1, 2, and 3, print out the edge weights between 1-2 and 1-3, and print out the total number of nodes in the graph.

The script will also make a `Graphviz` graph of the Graph object, allowing you to export it as a DOT file.

The type of comparison you want (e.g. tokens, lemmas, tagged_tokens, tagged_lemmas) can be included as `sys.argv[1]`.

Also, the default behavior of making the Graphviz graph is to make the dot file but not render it. 

I've included some renders of each of the four graphs using only the first 15 sentences from the text file. Much more than that causes my machine to freeze. 

However, I do include the `dot` file for the complete set of data for all four comparison types, so with the right hardware one can make a render of those.


### Requirements
- spaCy, with `en_core_web_sm` model
- graphviz
- tqdm


### Easy parts
A lot of the Python wasn't too bad. Yiyun Zhou sent me a nice resource for making graphs with Python (the source of my `Vertex` and `Graph` classes, excepting my additions)


### Challenging parts
The concepts weren't too challenging, but dealing with some of the minutiae of Python was a pain. In particular, I had a bit of a hard time keeping track of types.

In addition, before now I had never made a class in Python, and I've rarely made my own functions. That took a bit of getting used to, but eventually it got easier.

Lastly, I did not try to attempt the final question (asking about the shortest path). This was mostly due to time constraints, but also unfamiliarity with graph traversal. Based on my limited knowledge, I would guess that breadth-first search would be the way to do this, but I haven't formally learned about it yet (probably will in Spring from Mihai), and I don't know the Python implementation.


### Timeline
About 2.5 hours on Wednesday 11/7.
About 1 hour on Thursday 11/8
About 3 hours on Friday 11/9

