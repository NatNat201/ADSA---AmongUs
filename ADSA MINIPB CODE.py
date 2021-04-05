################################################

    #ADVANCED DATA STRUCTURES AND ALGORITHMS

################################################

#ROSSIGNOL Vincent & ZAKRZACKA Natalia





################################################

                    #STEP 1

################################################
print("_____ STEP 1 _____")

import names
from random import randint,choice
from statistics import mean
from operator import attrgetter

##Player class

class Player():

    def __init__(self, name, score):
        self.name=name
        if score is not None:
            self.score = score
        else:
            self.score = 0
        self.right = None
        self.left = None
        self.height = 1


##AVLTree class

class AVLTree():
    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

    def insert(self, player):
        if self.node == None:
            self.node = player
            self.node.right = AVLTree()
            self.node.left = AVLTree()
        elif player.score > self.node.score:
            self.node.right.insert(player)
        else:
            self.node.left.insert(player)
        self.rebalance()


    def delete(self, player):
        if self.node != None:
            if self.node.name == player.name:
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None
                elif self.node.left.node == None:
                    self.node = self.node.right.node
                elif self.node.right.node == None:
                    self.node = self.node.left.node

                # both children are present, we have to find logical successor
                else:
                    replacement = self.logical_successor(self.node)
                    if replacement != None: # sanity check
                        self.node = replacement

                        # replaced. Now delete the key from right child
                        self.node.right.delete(replacement)

                self.rebalance()
                return
            elif player.score <= self.node.score:
                self.node.left.delete(player)
            elif player.score > self.node.score:
                self.node.right.delete(player)

            self.rebalance()
        else:
            return


    def logical_successor(self, node):
        #Find the smallest valued node in RIGHT child

        node = node.right.node
        if node != None:
            while node.left != None:
                if node.left.node == None:
                    return node
                else:
                    node = node.left.node
        return node


    def rebalance(self):
        #let's check first if the tree is balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotate_left()
                    self.update_heights()
                    self.update_balances()
                self.rotate_right()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rotate_right()
                    self.update_heights()
                    self.update_balances()
                self.rotate_left()
                self.update_heights()
                self.update_balances()


    def update_heights(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()

            self.height = max(self.node.left.height,
                              self.node.right.height) + 1
        else:
            self.height = -1

    def update_balances(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0


    def rotate_right(self):
        A = self.node
        B = self.node.left.node
        T = B.right.node

        self.node = B
        B.right.node = A
        A.left.node = T


    def rotate_left(self):
        A = self.node
        B = self.node.right.node
        T = B.left.node

        self.node = B
        B.left.node = A
        A.right.node = T


    def inorder(self):
        #inorder traversal of the tree
        #this way, we can get a list of all the players contained in the AVL tree
        result = []
        if not self.node:
            return result
        result.extend(self.node.left.inorder())
        result.append(self.node)
        result.extend(self.node.right.inorder())
        return result


    def get_min(self):
        # return the objet from Player() with the minimum score
        #print(self)
        #print(self.inorder())
        last=[]
        list=self.inorder()
        #print("Taille Liste : ", len(last))
        for i in range (10):
            #print(i,list[i].name,list[i].score)
            last.append(list[i])
        return last


##Tournament class

class Tournament():

    def __init__(self):
        print("Welcome to our Among Us tournament\n\n")
        Names=[]
        for i in range(100):
            Names.append(names.get_first_name(gender ='male'))
        self.players = [Player(player[0], player[1]) for player in list(zip(Names, [0 for _ in range(100)]))]
        self.database = AVLTree()
        [self.database.insert(player) for player in self.players]


    def random_games(self):
        #the function will form groups of randomly selected people
        groups=[]
        for i in range (len(self.players)//10):
            list=[]
            for j in range (10):
                list.append(choice(self.players))
            groups.append(list)
        return groups

    def rounds(self, number):
        print(f"\n\nRound number {number} is being played:")

        #we form the random groups
        groups = self.random_games()
        for i in range (len(groups)):
            print(f"\nThe random group {i+1} is composed of :")
            for j in range (len(groups[0])):
                print(groups[i][j].name)

        print("\nFirst game...")
        score_game1 = [randint(0,12) for _ in range(100 - ((number - 1) * 10))]
        print("Second game...")
        score_game2 = [randint(0, 12) for _ in range(100 - ((number - 1) * 10))]
        print("Third game...")
        score_game3 = [randint(0, 12) for _ in range(100 - ((number - 1) * 10))]
        averageScores = [round(mean(data), 2) for data in list(zip(score_game1, score_game2, score_game3))]
        #print(averageScores)
        self.update_database(averageScores)
        #print("Len de liste avant suppression:",len(self.database.inorder()))

        worstPlayers = self.database.get_min()

        print("Eliminated players are : ")

        for i in range (10):
            print(i,worstPlayers[i].name, worstPlayers[i].score)
            self.players.remove(worstPlayers[i])
            #print("Longueur actuelle :",len(self.players))

        self.database=AVLTree()
        [self.database.insert(player) for player in self.players]


    def ranked_games(self):
        #the function will form groups of people selected by their rank
        groups=[]
        ranked = self.database.inorder()
        for i in range (len(ranked)//10):
            list=[]
            for j in range (10):
                list.append(ranked[i*10+j])
            groups.append(list)
        return groups

    def rounds_ranked(self,number):
        print(f"\n\nRound number {number} is being played:")

        #we form the ranked groups
        groups = self.random_games()
        for i in range (len(groups)):
            print(f"\nThe ranked group {i+1} is composed of :")
            for j in range (len(groups[0])):
                print(groups[i][j].name)

        print("\nFirst game...")
        score_game1 = [randint(0,12) for _ in range(100 - ((number - 1) * 10))]
        print("Second game...")
        score_game2 = [randint(0, 12) for _ in range(100 - ((number - 1) * 10))]
        print("Third game...")
        score_game3 = [randint(0, 12) for _ in range(100 - ((number - 1) * 10))]
        averageScores = [round(mean(data), 2) for data in list(zip(score_game1, score_game2, score_game3))]
        #print(averageScores)
        self.update_database(averageScores)
        #print("Len de liste avant suppression:",len(self.database.inorder()))

        #we eliminate the last players
        worstPlayers = self.database.get_min()
        print("Elmiminated players are : ")
        for i in range (10):
            print(i,worstPlayers[i].name, worstPlayers[i].score)
            self.players.remove(worstPlayers[i])
            #print("Longueur actuelle :",len(self.players))

        self.database=AVLTree()
        [self.database.insert(player) for player in self.players]


    def update_database(self, averageScores):
        #we update the score of the players
        newdatabase = AVLTree()
        i = 0
        for player in self.database.inorder():
            player.score += averageScores[i]
            newdatabase.insert(player)
            i += 1
        self.database = newdatabase


    def final(self):
        print("\n\n*** *** Finals *** ***")
        print("\nHere are the players taking place in the game, all the scores are reinitialized fro the final :")
        for i in range (10):
            self.players[i].score=0
            print(self.players[i].name,self.players[i].score)
        scores = [[randint(0, 12) for _ in range(5)] for i in range(10)]
        averageScores = [round(mean(data), 2) for data in scores]
        self.update_database(averageScores)
        scoreboard = self.database.inorder()
        podium = sorted(scoreboard, key=attrgetter("score"), reverse=True)
        print("\nHere are the average scores after 5 games:")
        print([finalist.name + " " + str(finalist.score) for finalist in podium])
        print("\nWe are happy to announce the winners of the tounament :")
        if podium[0].score!=podium[1].score and podium[1].score!=podium[2].score :
            print("1ST : ",podium[0].name," with a score of : ",podium[0].score)
            print("2ND : ",podium[1].name," with a score of : ",podium[1].score)
            print("3RD : ",podium[2].name," with a score of : ",podium[2].score)
        elif podium[0].score==podium[1].score and podium[1].score==podium[2].score:
            print("We have 3 winners at the first place : ")
            for i in range (3):
                print(podium[i].name,podium[i].score)
        elif podium[0].score==podium[1].score and podium[1].score!=podium[2].score:
            print("We have 2 winners at the 1ST place : ",podium[0].name, " and ",podium[1].name, " with both a score of : ",podium[0].score)
            print("3RD : ",podium[2].name," with a score of : ",podium[2].score)
        else:
            print("1ST : ",podium[0].name," with a score of : ",podium[0].score)
            print("We have 2 winners at the 3RD place : ",podium[1].name, " and ",podium[2].name, " with both a score of : ",podium[1].score)


##RUN THE STEP 1
#Execution of part 1 :
step1=Tournament()
#the 3 first rounds are played with random groups
for i in range (1,4):
    step1.rounds(i)
#the next ones are played with groups according to the ranking of the players
for i in range (4,10):
    step1.rounds_ranked(i)

#then we have the final part with the last 10 players
step1.final()





################################################

                    #STEP 2

################################################
print("\n\n\n")
print("_____ STEP 2 _____")

##Information
#First we make the graph representing the relationship "has seen"
Graph = [
            [0, 1, 0, 0, 1, 1, 0, 0, 0, 0],#Player 0 : has seen player 1,4 et 5
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],#Player 1 : has seen player 0,2 et 6
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],#Player 2 : has seen player 1,3 et 7
            [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],#Player 3 : has seen player 2, 4 et 8
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],#Player 4 : has seen player 0, 3 et 9
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],#Player 5 : has seen player 0, 7 et 8
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 1],#Player 6 : has seen player 1, 8 et 9
            [0, 0, 1, 0, 0, 1, 0, 0, 0, 1],#Player 7 : has seen player 2, 5 et 9
            [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],#Player 8 : has seen player 3, 5 et 6
            [0, 0, 0, 0, 1, 0, 1, 1, 0, 0] #Player 9 : has seen player 4, 6 et 7
        ]

#We list all the dead players of the game
dead=[0] # the player 0 is dead in our case

#Then we list the suspects according to the infomation we have just above
suspects=[1,4,5]
'''
Indeed, player 1, player 4 and player 5 might be impostors because player 0 was with them before he died.
'''

##Functions
#We can also create a function to indentify automatically the suspects given the list of dead players
def find_suspects(graph,dead):
    suspects=[]
    for i in range (len(dead)):
        for j in range (len(graph[dead[i]])):
            if graph[dead[i]][j]==1 and j not in suspects : suspects.append(j)
    #print(suspects)
    return suspects


def find_pairs(graph,dead,suspects):
    predicted_impostors = []
    #Selection of the suspect point of views
    for suspect in suspects:
        for i in range(len(graph[suspect])):
            if i not in dead and graph[suspect][i] == 0 and i != suspect:
                 predicted_impostors.append((min(i, suspect), max(i, suspect)))
    predicted_impostors = sorted(predicted_impostors, key = lambda x: (x[0], x[1]))

    print("Number of possible couples of imposters : ",len(predicted_impostors))
    print(predicted_impostors)
    return predicted_impostors


def chance(imposters):
    #We get the list of couples of possible imposters and we will calculate the chance to sum up the previous list

    #We list the players suspected :
    suspects = []
    for i in range (len(imposters)):
        if imposters[i][0] not in suspects : suspects.append(imposters[i][0])
        if imposters[i][1] not in suspects : suspects.append(imposters[i][1])
        #We have all the suspects
    #print(suspects)

    #Now we count how many times they appear in the results
    chance=[0 for i in range (len(suspects))]
    for i in range (len(suspects)):
        for j in range (len(imposters)):
            if suspects[i] in imposters[j]:
                chance[i]+=1
        chance[i]=chance[i]/len(imposters)*100
        print(f"Player {suspects[i]} : ",chance[i],"%")


##RUN THE STEP 2
suspects_found=find_suspects(Graph,dead)
pairs=find_pairs(Graph,dead,suspects_found)
pairs
chance(pairs)





################################################

                    #STEP 3

################################################
print("\n\n\n")
print("_____ STEP 3 _____")

#Question 3

#We will be working on two maps : one for the crewmates and one for the imposters
#First of all, here is the list of all the rooms, the very last is the additional vent in the middle of the corridor

# 1 - Reactor
# 2 - Upper Engine
# 3 - Lower Engine
# 4 - Security
# 5 - MedBay
# 6 - Electrical
# 7 - Cafeteria
# 8 - Storage
# 9 - Admin
# 10- Weapons
# 11- O2
# 12- Navigation
# 13- Shields
# 14- Communication
# 15- Vent(only for imposters and not counted as a room in the following list)

#We list all the room, it'll be used further for the listing of the time to travel between two of these rooms :
rooms =["Reactor","Upper Engine","Lower Engine","Security","MedBay","Electrical","Cafeteria","Storage","Admin","Weapons","O2","Navigation","Shields","Communication"]

#A constant we will initialize here is 'inf', that will stand for 'infinity'
inf = float('inf')


#First we have the crewmates' map
crewmates_map =[
[0,3.5,4,4,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf], #Reactor
[3.5,0,6,3.5,4,inf,6.5,inf,inf,inf,inf,inf,inf,inf], #Upper Engine
[4,6,0,4,inf,6,inf,7,inf,inf,inf,inf,inf,inf], #Lower Engine
[4,3.5,4,0,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf], #Security
[inf,4,inf,inf,0,inf,4,inf,inf,inf,inf,inf,inf,inf], #MedBay
[inf,inf,6,inf,inf,0,inf,5,inf,inf,inf,inf,inf,inf], #Electrical
[inf,6.5,inf,inf,4,inf,0,5,5,4,inf,inf,inf,inf], #Cafeteria
[inf,inf,7,inf,inf,5,5,0,3,inf,inf,inf,4,3], #Storage
[inf,inf,inf,inf,inf,inf,5,3,0,inf,inf,inf,inf,inf], #Admin
[inf,inf,inf,inf,inf,inf,4,inf,inf,0,2.5,5,7,inf], #Weapons
[inf,inf,inf,inf,inf,inf,inf,inf,inf,2.5,0,4,6,inf], #O2
[inf,inf,inf,inf,inf,inf,inf,inf,inf,5,4,0,6,inf], #Navigation
[inf,inf,inf,inf,inf,inf,inf,4,inf,7,6,6,0,2], #Shields
[inf,inf,inf,inf,inf,inf,inf,3,inf,inf,inf,inf,2,0] #Communication
]

imposters_map =[
[0,0,0,4,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf,inf], #Reactor
[0,0,6,3.5,4,inf,6.5,inf,inf,inf,inf,inf,inf,inf,inf], #Upper Engine
[0,6,0,4,inf,6,inf,7,inf,inf,inf,inf,inf,inf,inf], #Lower Engine
[4,3.5,4,0,0,0,inf,inf,inf,inf,inf,inf,inf,inf,inf], #Security
[inf,4,inf,0,0,0,4,inf,inf,inf,inf,inf,inf,inf,inf], #MedBay
[inf,inf,6,0,inf,0,inf,5,inf,inf,inf,inf,inf,inf,inf], #Electrical
[inf,6.5,inf,inf,4,inf,0,5,0,4,inf,inf,inf,inf,0], #Cafeteria
[inf,inf,7,inf,inf,5,5,0,3,inf,inf,inf,4,3,inf], #Storage
[inf,inf,inf,inf,inf,inf,0,3,0,inf,inf,inf,inf,inf,0], #Admin
[inf,inf,inf,inf,inf,inf,4,inf,inf,0,2.5,0,7,inf,4.5], #Weapons
[inf,inf,inf,inf,inf,inf,inf,inf,inf,2.5,0,4,6,inf,2.5], #O2
[inf,inf,inf,inf,inf,inf,inf,inf,inf,5,4,0,0,inf,3.5], #Navigation
[inf,inf,inf,inf,inf,inf,inf,4,inf,7,6,6,0,2,2.5], #Shields
[inf,inf,inf,inf,inf,inf,inf,3,inf,inf,inf,inf,2,0,inf], #Communication
[inf,inf,inf,inf,inf,inf,0,inf,0,4.5,3.5,3.5,2.5,inf,0] #Vent
]


#Now we code the Floyd-Warshall algorithm we'll use to print the time between each set of room

def Floyd_Warshall(graph):
    #First we implement the algorithm
    for k in range(len(graph)):
        for i in range(len(graph)):
            for j in range(len(graph)):
                graph[i][j] = min(graph[i][j] ,graph[i][k]+ graph[k][j])

    #And now we print the time of travel between each room
    for i in range(len(rooms)):
        for j in range(i+1, len(rooms)):
            print(f"FROM {rooms[i]} TO {rooms[j]} : {graph[i][j]}")
        print()


##RUN THE STEP 3
print("Time to travel between rooms for CREWMATES")
Floyd_Warshall(crewmates_map)
print("Time to travel between rooms for IMPOSTERS")
Floyd_Warshall(imposters_map)






################################################

                    #STEP 4

################################################
print("\n\n\n")
print("_____ STEP 4 _____")

#As we are dealing with tasks problems, we will only work with the crewmates point of view
#First we list back all the rooms so we can see them here

# 1 - Reactor
# 2 - Upper Engine
# 3 - Lower Engine
# 4 - Security
# 5 - MedBay
# 6 - Electrical
# 7 - Cafeteria
# 8 - Storage
# 9 - Admin
# 10- Weapons
# 11- O2
# 12- Navigation
# 13- Shields
# 14- Communication


Set = {"Reactor":["Upper Engine","Lower Engine","Security"],
"Upper Engine":["Reactor","Lower Engine","Security","MedBay","Cafeteria"],
"Lower Engine":["Reactor","Upper Engine","Security","Electrical","Storage"],
"Security":["Reactor","Upper Engine","Lower Engine"],
"MedBay":["Upper Engine","Cafeteria"],
"Electrical":["Lower Engine","Storage"],
"Cafeteria":["Upper Engine","MedBay","Storage","Admin","Weapons"],
"Storage":["Lower Engine","Electrical","Cafeteria","Admin","Shields","Communication"],
"Admin":["Cafeteria","Storage"],
"Weapons":["Cafeteria","O2","Navigation","Shields"],
"O2":["Weapons","Navigation","Shields"],
"Navigation":["Weapons","O2","Shields"],
"Shields":["Storage","Weapons","O2","Navigation","Communication"],
"Communication":["Storage","Shields"]}

#The second set was added just in case the first one didn't work
Set2 = {1:[2,3,4],
2:[1,3,4,5,7],
3:[1,2,4,6,8],
4:[1,2,3],
5:[2,7],
6:[3,8],
7:[2,5,8,9,10],
8:[3,6,7,9,13,14],
9:[7,8],
10:[7,11,12,13],
11:[10,12,13],
12:[10,11,13],
13:[8,10,11,12,14],
14:[8,13]}

#We now define the hailton funtion which will have to find the hamiltonian path starting from a room we will decide of and based on the graph we have above
def hamilton(G, start, path=[]):
    if start not in set(path):
        #We begin by adding the starting point to the path list
        path.append(start)

        if len(path)==14:
            #we have visited all the rooms no need to continue
            return path
        #if not, we continue searching for the rest of the list
        for j in G.get(start, []):
            res_path = [i for i in path]
            x = hamilton(G, j, res_path)

            if x is not None:
                return x


#We run all the function with a little interface
def run4():
    rooms=list(Set.keys())
    #print(list)
    print("Here is the list of all the rooms of the game :")
    print(rooms)
    choice = input("\nChoose the room from which the group will start : ")
    Finished = hamilton(Set,choice,[])
    print(Finished)
    if Finished!=[] and Finished!=None:
        print("\n\nHere is the path to take in order to visit all the rooms only once, starting from ",choice," : \n")
        str=""
        for i in range (13):
            str+=Finished[i]
            str+=", "
        str+=Finished[13]
        print(str)
    else:
        print("We are sorry but no path has been found from this point on.")


##♥RUN THE STEP 4
run4()
