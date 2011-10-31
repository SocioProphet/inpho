"""
Script to convert from InPhO data model to RDF triple store.
"""
import rdflib
from rdflib import Literal, Namespace
from rdflib.graph import ConjunctiveGraph as Graph

from inpho.model import *

g = Graph()

# add namespaces
inpho = Namespace("http://inpho.cogs.indiana.edu/")
g.bind("inpho", "http://inpho.cogs.indiana.edu/")

t = Namespace("http://inpho.cogs.indiana.edu/thinker/")
g.bind("thinker", "http://inpho.cogs.indiana.edu/thinker/")

# user namespace currently doesn't exist?
u = Namespace("http://inpho.cogs.indiana.edu/user/")
g.bind("user", "http://inpho.cogs.indiana.edu/user/")

e = Namespace("http://inpho.cogs.indiana.edu/entity/")
g.bind("entity", "http://inpho.cogs.indiana.edu/entity/")

foaf = Namespace("http://xmlns.com/foaf/0.1/")
g.bind("foaf", "http://xmlns.com/foaf/0.1/")

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
g.bind("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")

rdfs = Namespace("http://www.w3.org/TR/rdf-schema/#")
g.bind("rdfs", "http://www.w3.org/TR/rdf-schema/#")

owl = Namespace("http://www.w3.org/2002/07/owl#")
g.bind("owl", "http://www.w3.org/2002/07/owl#")

i = Namespace("http://inpho.cogs.indiana.edu/idea/")
g.bind("idea", "http://inpho.cogs.indiana.edu/idea/")

skos = Namespace("http://www.w3.org/2004/02/skos/core#")
g.bind("skos", "http://www.w3.org/2004/02/skos/core#")

dc = Namespace("http://purl.org/dc/elements/1.1/")
g.bind ("dc", "http://purl.org/dc/elements/1.1/")

# Select all Thinkers
thinkers = Session.query(Thinker).all()
g.add((inpho['thinker'], rdf['type'], foaf['person']))
g.add((inpho['thinker'], rdfs['subClassOf'], inpho['entity']))
for thinker in thinkers:
    g.add((t['t' + str(thinker.ID)], rdf['type'], inpho['thinker']))
    g.add((t['t' + str(thinker.ID)], foaf['name'], Literal(thinker.label)))
    g.add((t['t' + str(thinker.ID)], owl['sameAs'], e['e' + str(thinker.ID)]))
        

# Select all ConceptSchemes
g.add((skos['conceptscheme'], skos['hasTopConcept'], inpho['idea']))
g.add((inpho['idea'], rdfs['subClassOf'], inpho['entity']))

#Select all Ideas
ideas = Session.query(Idea).all()
g.add((inpho['idea'], rdfs['subClassOf'], inpho['entity']))
g.add((inpho['idea'], rdfs['subClassOf'], skos['Concept'])) 
for idea in ideas:
    g.add((i['idea' + str(idea.ID)], rdf['type'], inpho['idea']))
    g.add((t['t' + str(thinker.ID)], owl['sameAs'], e['e' + str(thinker.ID)]))

# Never create an instance of an inpho:user, used to tag provenance of evaluations
# Select all Users
users = Session.query(User).all()
g.add((inpho['user'], rdf['type'], foaf['Person']))
g.add((inpho['expert_user'], rdfs['subClassOf'], inpho['user']))
g.add((inpho['turk_user'], rdf['type'], foaf['Person']))
g.add((inpho['admin'], rdfs['subClassOf'], inpho['user']))
for user in users:
    g.add((u['u' + str(user.ID)], rdf['type'], inpho['user']))

# Select all Entities
entities = Session.query(Entity).all()
g.add((inpho['entity'], rdf['type'], owl['Thing']))
for entity in entities:
    g.add((e['e' + str(entity.ID)], rdf['type'], inpho['entity']))
    g.add((e['e' + str(entity.ID)], skos['prefLabel'], Literal(entity.label)))
    g.add((e['e' + str(entity.ID)], inpho['provenance'], Literal(entity.created_by)))
    g.add((e['e' + str(entity.ID)], dc['creator'], Literal(entity.created_by)))
    g.add((e['e' + str(entity.ID)], dc['created'], Literal(entity.created)))
    # g.add((e['e' + str(entity.ID)], skos['alt'], Literal(entity.alias)))

with open("out.rdf", "w") as f:
    f.write(g.serialize(format="n3"))