from collections import deque
import time
import tracemalloc
import matplotlib
matplotlib.use('Agg')  # <- Use non-GUI backend (no window)

import matplotlib.pyplot as plt



#0 = libre, 1 = mur
maze = {
    (0, 0): 0, (0, 1): 1, (0, 2): 0, (0, 3): 0,
    (1, 0): 0, (1, 1): 1, (1, 2): 0, (1, 3): 1,
    (2, 0): 0, (2, 1): 0, (2, 2): 0, (2, 3): 1,
    (3, 0): 0, (3, 1): 1, (3, 2): 0, (3, 3): 0,

}

directions = [(-1,0),(1,0),(0,-1), (0,1)]


start1 = (0,0)
goal1 = (3,3)


def get_neighbors(node):
    x, y = node
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (nx, ny) in maze and maze[(nx, ny)] == 0:
            neighbors.append((nx, ny))
    return neighbors




def print_maze(maze, path=None):
    for x in range(4):
        for y in range(4):
            if path and (x, y) in path:
                print("P", end=" ") #chemin
            elif maze[(x, y)] == 1:
                print("#", end=" ") # Mur
            else:
                print(".", end=" ") # Libre
        print(" ")



 # DFS search algorithm
def DFS(start, goal):

    stack = [start]
    came_from = {start: None} #{ neighbor : parent  }
    i = 1

    print("1st Stack : ", stack)
    print("1st Came_from : ", came_from)
    print(" ")

    while stack:
        print(f"\n------loop N° {i}----------\n")
        print("Stack: ", stack)

        current = stack.pop()

        print("Current : ", current)
        print("Stack after pop: ", stack)

        if current == goal:
            print(f"\n{current} = goal")
            print("-----We break----\n")
            break

        for neighbor in get_neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)
                print("Came from : ", came_from)

        i+= 1

    path = []
    node = goal
    while node is not None:
        print("Node : ", node)

        path.append(node)

        print("Path : ", path)

        node = came_from[node]
        print(" ")

    print ("\nReverse path",path[::-1])
    return path[::-1]




 # BFS search algorithm

def BFS(start, goal):
    queue = deque([start])
    came_from = {start: None}

    print("1st Queue : ", list(queue))
    print("1st Came_from : ", came_from)
    print(" ")
    i = 1

    while queue:

        print(f"\n------loop N° {i}----------\n")
        print("Queue: ", list(queue))

        current = queue.pop()

        print("Current : ", current)
        print("Queue after pop: ", list(queue))

        if current == goal :
            print(f"\n{current} = goal")
            print("-----We break----\n")
            break

        print("Neighbors: ", get_neighbors(current))

        for neighbor in get_neighbors(current):
            if neighbor not in came_from :
                came_from[neighbor] = current
                queue.appendleft(neighbor)
                print("Came from : ", came_from)
        i+=1

    node = goal
    path = []

    while node is not None :

        print("Node : ", node)

        path.append(node)
        node = came_from[node]
        print("Path: ", path[::-1])

    return path[::-1]





#Fonction pour mesurer les performances

def measure_performance(algorithm, start, goal):
    #Mesure du temps
    start_time = time.time()
    #Mesure de la memoire
    tracemalloc.start()

    #Run the algo
    path = algorithm(start, goal)

    #stop memory measuring
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    #Calc elapsed time
    elapsed_time = time.time() - start_time

    return path, elapsed_time, peak/1024 #mem in KB


#Configuration des tests

#List of algorithmes to test
algorithms = [(BFS, "BFS"), (DFS, "DFS")]

#Measure results
results = []
paths = {} #Dictionnaire pour stocker les chemins trouvés

for algo, name in algorithms:
    path, time_taken, mem_used = measure_performance(algo, start1, goal1)
    paths[name] = path #Stocker le chemin dans le dictionnaire
    results.append((name, len(path), time_taken, mem_used))







# Affichage des résultats
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

# Données pour les graphiques
names = [res[0] for res in results]
times = [res[2] * 1000 for res in results] # en millisecondes
memory = [res[3] for res in results]
lengths = [res[1] for res in results]

# Graphique du temps d'exécution
ax1.bar (names, times, color='skyblue')
ax1.set_title('Temps d\'exécution')
ax1.set_ylabel('Millisecondes')
ax1.grid(axis='y', linestyle= '--')

# Graphique de la mémoire utilisée
ax2.bar(names, memory, color='lightgreen')
ax2.set_title('Mémoire utilisée')
ax2.set_ylabel('Kilobytes')
ax2.grid(axis='y', linestyle='--')

# Graphique de la longueur du chemin

ax3.bar(names, lengths, color='salmon')
ax3.set_title('Longueur du chemin')
ax3.set_ylabel('Nombre de noeuds')
ax3.grid(axis= 'y', linestyle= '--')

plt.tight_layout()
plt.savefig('results.png')
print("Graphs saved as 'results.png'!")













print("********Labyrinthe initial********** ")
print_maze(maze)


print("\n**********chemin DFS************")
dfs_path = DFS(start1, goal1)
print_maze(maze, dfs_path)

print("\n************chemin BFS***********")
bfs_path = BFS(start1, goal1)
print_maze(maze, bfs_path)


