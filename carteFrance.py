import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import PIL

img = plt.imread("carte.jpg")
G = nx.Graph()
Ga = nx.Graph() #graphe autoroute
Gd = nx.Graph() #graphe departemental
matricenode = []
matriceedge = []
pos = nx.get_node_attributes(G,"pos")
def openFichier(fichier):
    with open(fichier, 'r') as file:
        myArray = []
        csvreader = csv.reader(file, delimiter=";")
        headers = next(csvreader, None)
        for ligne in csvreader:
            myArray.append(ligne)  # créer une nouvelle ligne du line a chaque itération de (line)
    return myArray


def creategraphe(array):
    graphe = nx.Graph()
    for i in range(len(array)):
        graphe.add_node(array[i][0])
        pos[array[i][0]] = (int(array[i][1]), int(array[i][2]))  # ajoute les position des villes
    return graphe


def createedge(array, graphe):
    for ligne in array:
        graphe.add_edge(ligne[0], ligne[1], type=ligne[2], duree=int(ligne[3]), cout=float(ligne[4]))  # ajoute les arètes
        if ligne[2] == 'a':
            graphe.add_edge(ligne[0], ligne[1], type=ligne[2], duree=int(ligne[3]), cout=float(ligne[4]),
                        color="r")  # création autoroute
        else:
            graphe.add_edge(ligne[0], ligne[1], type=ligne[2], duree=int(ligne[3]), cout=float(ligne[4]),
                        color="g")  # création departemental
    return graphe
        # distance = [int(ligne[3])]
        # infoDep.append(liaison)


def creerAutoroute(array, graphe):
    for ligne in array:
        if ligne[2] == 'a':
            graphe.add_edge(ligne[0], ligne[1], type=ligne[2], duree=ligne[3], cout=ligne[4],
                        color="r")  # création autoroute
    return graphe


def creerDepartemental(array, graphe):
    for ligne in array:
        if ligne[2] == 'd':
            graphe.add_edge(ligne[0], ligne[1], type=ligne[2], duree=ligne[3], cout=ligne[4],
                        color="g")  # création departemental
    return graphe


def affichage(graphe):
    colors = []
    for edge in graphe.edges:
        colors.append(graphe.edges[edge]['color'])
    plt.figure(str(graphe))
    nx.draw_networkx(graphe, pos,edge_color=colors)
    plt.rcParams["figure.figsize"] = (60, 15)
    plt.imshow(img)


def is_connexe(graphe):
  # return nx.is_connected(graph)
  for city1 in graphe.nodes():
    for city2 in graphe.nodes():
      if city1 != city2:
        if nx.has_path(graphe, city1, city2) == False:
          return False
  return True


def cheminlepluscourt(graphe, ville1, ville2):
    return nx.shortest_paths(graphe, source= ville1, target= ville2)



matricenode = openFichier("TP2_position.csv")
matriceedge = openFichier("TP2_liaison.csv")
G = creategraphe(matricenode)
Ga = creategraphe(matricenode)
Gd = creategraphe(matricenode)

createedge(matriceedge,G)
creerAutoroute(matriceedge, Ga)
creerDepartemental(matriceedge, Gd)
print("G : ",G)
print("Ga : ",Ga)
print("Gd : ",Gd)
print("connected: ",nx.is_connected(Gd))
p = nx.shortest_path(G, source='Lille', target='Marseille',weight="duree")
print(p)
#print(cheminlepluscourt(G,"Paris","Marseille"))
affichage(G)
affichage(Ga)
affichage(Gd)
plt.show()