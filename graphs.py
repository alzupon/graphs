# Andrew Zupon
# last edited 02018.11.08

import sys
import spacy
import en_core_web_sm
from graphviz import Graph
from tqdm import tqdm


# load text file
collection = open("coling2016_explanation_sentences.txt", 'r')
training_data = collection.read()
collection.close()

# load spaCy model
nlp = spacy.load("en_core_web_sm")

# split training data into sentences (by lines)
train_data = training_data.strip().split('\n')



class Sentence:
    '''
    class for sentences, with text, token, lemma, tag properties
    '''
    def __init__(self,text,tokens,lemmas,tagged_tokens,tagged_lemmas):
        self.text = text    # text of sentence
        self.tokens = tokens    # tokens
        self.lemmas = lemmas    # lemmas
        self.tagged_tokens = tagged_tokens  # tokens+tags
        self.tagged_lemmas = tagged_lemmas  # lemmas+tags



class Vertex:
    '''
    This Vertex class comes from an online tutorial at interactivepython.org.
    '''
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]



class GraphClass:
    '''
    Most of this Graph class comes from an online tutorial at interactivepython.org. My additions are indicated with comments.
    '''
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def getNodeSentence(self,idx):  
        '''
        returns the sentence text for a given node
        '''
        return list(self.getVertices())[idx].text

    def getEdgeWeightBetweenNodes(self,idx, idx2):
        '''
        returns the weight between two given nodes
        '''
        try:
            return self.getVertex(list(self.getVertices())[idx]).getWeight(self.getVertex(list(self.getVertices())[idx2]))
        except:
            return
            #print("Nodes not connected.")
        #return self.getVertex(list(self.getVertices())[idx]).getWeight(self.getVertex(list(self.getVertices())[idx2]))

    def getSize(self):
        '''
        returns the total number of nodes in the graph
        '''
        return len(self.getVertices())

    def addEdgesBetweenNodes(self, comparison_type='tokens'):
        '''
        adds all edges between nodes based on type of comparison (e.g tokens, lemmas, etc.)
        type can be specified with sys.argv argument, default is tokens
        '''
        comp = comparison_type
        for i in self.vertList:
            for j in self.vertList:
                if comp == "tokens":
                    node1 = i.tokens
                    node2 = j.tokens
                elif comp == "lemmas":
                    node1 = i.lemmas
                    node2 = j.lemmas
                elif comp == "tagged_tokens":
                    node1 = i.tagged_tokens
                    node2 = j.tagged_tokens
                elif comp == "tagged_lemmas":
                    node1 = i.tagged_lemmas
                    node2 = j.tagged_lemmas
                similar_words = 0
                for word in node1:
                    if word in node2:
                        similar_words += 1
                weight = similar_words
                if i != j and weight > 0:
                    if self.getVertex(i) in self.getVertex(j).getConnections():
                        continue
                    else:
                        self.addEdge(i,j,weight)
                else:
                    continue
        return self

    def ExportToDOT(self, filename="gViz.dot", comparison_type="tokens", output="build"):
        '''
        Creates Graphviz graph out of graph nodes and edges.
        The comparison type will be which similarity measure you want to use to compare sentences.
        By default, will only create the dot file.
        If output="view", it will also show the render of the graph.

        '''
        comp = comparison_type
        # initialize empty graphviz graph
        gViz = Graph("gViz", filename=filename, engine="dot")
        # add all nodes in g to gViz
        i = 0
        for node in tqdm(list(self.getVertices())):
            if comp == "tokens":
                label = node.tokens
            elif comp == "lemmas":
                label = node.lemmas
            elif comp == "tagged_tokens":
                label = node.tagged_tokens
            elif comp == "tagged_lemmas":
                label = node.tagged_lemmas
            gViz.node(str(i), str(label))
            i+=1
        # add all edge weights in g to gViz
        i = 0   # node1 in gViz
        x = 0   # node1 in g
        for node1 in tqdm(self.getVertices()):
            #print("Adding edges for node", x)
            j = 0   # node2 in gViz
            y = 0   # node2 in g
            for node2 in self.getVertices():
                try:
                    gViz.edge(str(i), str(j), label=str(self.getVertex(list(self.getVertices())[x]).getWeight(self.getVertex(list(self.getVertices())[y]))))
                    y += 1
                except:
                    y += 1
                j += 1
            i += 1
            x += 1
        if output=="view":
            return gViz.view()
        else:
            return gViz.save()

# initialize an empty graph
g = GraphClass()


# initialize an empty list of Sentence objects
sentences = []


# loop over traning data, turning sentences into Sentence objects and adding to list
for sentence in tqdm(train_data):
    sentence = sentence.lower() # fold case
    sentence = sentence[:-1]   # strip terminal punctuation
    doc = nlp(sentence)
    stoken = []
    for token in doc:
        stoken.append(token.text)
    slemma = []
    for token in doc:
        slemma.append(token.lemma_)
    staggedTokens = []
    for token in doc:
        staggedTokens.append(token.text+"_"+token.pos_)
    staggedLemma = []
    for token in doc:
        staggedLemma.append(token.lemma_+"_"+token.pos_)
    sentence = Sentence(sentence,stoken, slemma, staggedTokens, staggedLemma)
    sentences.append(sentence)


# add each sentence as a node in the graph
for sent in sentences:
    g.addVertex(sent)


# add edges between nodes, comparison type is sys.argv[1]
g.addEdgesBetweenNodes(comparison_type=sys.argv[1])


## checks all connections between nodes
#for v in g:
#    for w in v.getConnections():
#        print("( %s, %s )" % (v.getId().text, w.getId().text))


## prints out all pairs of sentences with their edge weights
#for node in g:
#    for edge in node.getConnections():
#        print(node.getId().text, "\n", edge.getId().text, "\n", edge.getWeight(node), "\n")


# prints sentence corresponding to node 1
print("Node {}: {}".format(1, g.getNodeSentence(1)))
# prints sentence corresponding to node 2
print("Node {}: {}".format(2, g.getNodeSentence(2)))
# prints sentence corresponding to node 3
print("Node {}: {}\n".format(3, g.getNodeSentence(3)))


# prints weight between nodes 1 and 2
print("Weight between nodes {} and {}: {}".format(1, 2, g.getEdgeWeightBetweenNodes(1,2)))
# prints weight between nodes 1 and 3
print("Weight between nodes {} and {}: {}\n".format(1, 3, g.getEdgeWeightBetweenNodes(1,3)))


# prints total number of nodes
print("Total number of nodes:", g.getSize())


# create Graphviz graph, where comparison type is sys.argv[1]
print(g.ExportToDOT(comparison_type=sys.argv[1],output="build"))
