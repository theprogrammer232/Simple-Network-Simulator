#!/usr/bin/python

#Link class
class Link:
    linkWeight = 0
    
    router1 = ""
    router2 = ""
    
    def __init__(self, w, l1, l2):
        self.linkWeight = w
        self.router1 = l1
        self.router2 = l2
    
    def getWeight(self):
        return self.linkWeight
    
    def setWeight(self, w):
        self.linkWeight = w
    
    def getLink(self, num):
        if(num == 1):
            return self.router1
        else:
            return self.router2
    
#Router class
class Router:
    IPAddr = ""
    listLinks = []
    listNeighbors = []
    visited = []
    table = []
    pathCost = 0
    numLinks = 0
    
    def __init__(self, ipadd, links, neigh):
        self.IPAddr = ipadd
        self.listLinks = links
        self.listNeighbors = neigh
        self.table = []
        self.visited = []
        self.pathCost = 0
        self.numLinks = 0

    def addLink(self, weight, dest, graph):
        if(self.getIP() != dest):
            l = Link(weight, self.getIP(), dest)
            self.listLinks.append(l)
            
            if(self.isLink(l, graph)):
                return "True"
            else:
                graph.links.append(l)
            
            return "True"
        else:
            return "Can not add link between a node and itself."
    
    def isNeigh(self, ip):
        for n in self.getNeighbors():
            if(n.getIP() == ip):
                return True
        return False
        
    def isLink(self, link, graph):
        for l in graph.links:
            if((l.getLink(1) == link.getLink(1) or l.getLink(1) == link.getLink(2))
               and (l.getLink(2) == link.getLink(1) or l.getLink(2) == link.getLink(2))):
                return True
        return False

    def removeLink(self, rter):
        for l in self.getLinks():
            l1 = l.getLink(1)
            l2 = l.getLink(2)
            if((l1 == rter.getLink(1) or l1 == rter.getLink(2)) and (l2 == rter.getLink(2) or l2 == rter.getLink(1))):
                self.listLinks.remove(l)
                self.numLinks -= 1
                break;
    
    def addNeigh(self, neigh, graph):
        if(neigh != self.getIP()):
            self.listNeighbors.append(graph.getRouter(neigh))
            print("neighbor appended", neigh, "to", self.getIP())
    
    def removeNeigh(self, neigh, graph):
        for n in self.listNeighbors:
            if(n.getIP() == neigh):
                self.listNeighbors.remove(n)
                for l in self.getLinks():  
                    if(l.getLink(1) == neigh or l.getLink(2) == neigh):
                        self.listLinks.remove(l)
                        graph.removeGLink(l)
         
    def getIP(self):
        return self.IPAddr
       
    def getLinks(self):
        return self.listLinks

    def getNeighbors(self):
        return self.listNeighbors
    
    def printTable(self):
        print("--Forwarding Table for:",self.getIP(),"---")
        print("Destination\tOutput Link")
        for t in self.table:
            print(t[0], "\t", t[1])
        print("--------------------------------------\n")
        
    def printLinks(self):
        print(self.getIP(),"links:")
        for l in self.listLinks:
            print("(",l.getLink(1)+",",l.getLink(2)+")\n")
    
    def printNeighbors(self):
        print("neighbors of", self.getIP())
        for n in self.getNeighbors():
            print(n.getIP(), "->N")
    
    def printVisited(self):
        for r in self.visited:
            print(r.getIP()+":"+str(r.pathCost), "->")


#Graph class
class Graph:
    listRouters = []
    links = []
    mostcurrentip = 0
    
    def __init__(self):
        self.listRouters = []
        self.links = []
        self.mostcurrentip = 0
    
    def genIP(self):
        subnet= "200.25.3."
        self.mostcurrentip += 1
        return subnet+str(self.mostcurrentip)
    
    def getGLinks(self):
        return self.links
    
    def getRouter(self, ip):
        for r in self.listRouters:
            if(r.getIP() == ip):
                return r
        return "Router does not exist."
    
    def getLinkWeight(self, rter1, rter2):
        toReturn = None;
        for x in self.links:
            if((x.getLink(1) == rter1.getIP()
               or x.getLink(1) == rter2.getIP()) and 
               (x.getLink(2) == rter1.getIP() 
               or x.getLink(2) == rter2.getIP())):
                toReturn = x
                return toReturn.getWeight()
        return 0
    
    def isVisited(self, ip, visited):
        for v in visited:
            if(v.getIP() == ip):
                return True
        return False
    
    def removeGLink(self, rter):
        rml1 = rter.getLink(1)
        rml2 = rter.getLink(2)
        for l in self.links:
            if((l.getLink(1) == rml1 or l.getLink(1) == rml2) and (l.getLink(2) == rml1 or l.getLink(2) == rml2)):
                self.links.remove(l)
    
    def printGLinks(self):
        print("Graph links:")
        for l in self.links:
            print("(",l.getLink(1)+",",l.getLink(2)+")\n")
    
    def rmRouter(self, ip):
        toRemove = None;
        # remove router w/given ip from listRouters
        for r in self.listRouters:
            if(r.getIP() == ip):
                toRemove = self.getRouter(r.getIP())
                self.listRouters.remove(toRemove)
                break
        for x in self.listRouters:
            x.removeNeigh(toRemove.getIP(), graph)
#         self.listRouters.remove(toRemove)
        # remove link from graph.links where either
        # 1 or both link-routers = toRemove
#         localLinks = []
#         for l in self.links:
#             r1 = l.getLink(1)
#             r2 = l.getLink(2)
#             if(r1 == toRemove.getIP()):
#                 localLinks.append((l, r2))
#                 self.removeGLink(l) 
#                 self.printGLinks()
#             if(r2 == toRemove.getIP()):
#                 localLinks.append((l, r1))
#                 self.removeGLink(l) 
#                 self.printGLinks()
        # remove links on each router containing a connection to the removed
#         for x in localLinks:
#             n = self.getRouter(x[1])
#             n.printLinks()
#             n.removeLink(x[0])
#             n.printLinks()
#             n.removeNeigh(toRemove.getIP()) #Try removing links along with neighbors
        
#         for y in self.listRouters:
#             self.createTable(y)
        print("Router removed ...", ip)
        for y in self.listRouters:
            if(y.getLinks() != None and y.getNeighbors() != None):
                y.printNeighbors()
                print("Creating table for", y.getIP())
                self.createTable(y)   
        
    def addRouter(self):
        lnks = []
        neigh = []
        ip = self.genIP()
        i = 1
        toAdd = Router(ip, lnks, neigh)
        self.listRouters.append(toAdd)
        if(self.mostcurrentip < 2):
            print("First Router created ...", ip)
            return 0
        numLinks = int(input("Please enter the number of links you'd like to add for this newly-created router:"))
        while(i <= numLinks):
            linkIP = input("Please enter the destination IP address for link #"+str(i))
            weight = int(input("Now, please enter the weight for link #"+str(i)))
            print(toAdd.addLink(weight, linkIP, self))
            toAdd.addNeigh(linkIP, self)
            toAdd.printNeighbors()
            for r in self.listRouters:
                if(r.getIP() == linkIP and r.getIP() != ip):
                    print(r.addLink(weight, ip, self))
                    r.addNeigh(ip, self)
                    r.printNeighbors()
                    print("Link added between",r.getIP(), "and", ip)
            i += 1
        print("Router created ...", ip)
        
        for n in self.listRouters:
            if(n.getLinks() != None and n.getNeighbors() != None):
                n.printNeighbors()
                print("Creating table for", n.getIP())
                self.createTable(n)
            
    def createTable(self, src):
        src.visited = []
        src.pathCost = 0;
        src.visited.append(src);
        print("appending", src.getIP())
        minCost = float("inf")
        for r in self.listRouters:
            if(r.getIP() != src.getIP()):
                r.pathCost = float("inf")
        x = None
        minLink = None
        for l in src.getLinks():
            print("l is", l.getLink(1), "-", l.getLink(2))
            if(l.getLink(1) == src.getIP()):
                x = self.getRouter(l.getLink(2))
                print("grabbed link 2", l.getLink(2))
                x.pathCost = l.getWeight()
                
            if(l.getLink(2) == src.getIP()):
                x = self.getRouter(l.getLink(1))
                print("grabbed link 1", l.getLink(1))
                x.pathCost = l.getWeight()
                
            print("x is", x.getIP(), "path cost:", x.pathCost)
            if(x.pathCost <= minCost):
                minCost = x.pathCost
                print("minCost is", minCost)
                minLink = x
                
        if(x == None or minLink == None):
            return 0
        
        src.visited.append(minLink)
        print("appending", minLink.getIP())
        src.visited = self.updatePaths(minLink, src, src.visited)
        
        #################################################
        #################################################
        src.printVisited()
        src.table = []
        for n in src.visited:
            print("n is", n.getIP())
            if(n.getIP() != src.getIP() ):
#                 index = src.visited.index(n)-1
#                 newPath = []
#                 newPath.append(self.getRouter(src.getIP()))
#                 print("appended to newPath", src.getIP())
                index = 0
                curr = self.getRouter(n.getIP())
                newSrc = self.getRouter(src.getIP())
#                 while(src.visited[index+1].getIP() != src.getIP()):
                while(True):
#                     curr.printNeighbors()
                    print("are neighbors:", curr.isNeigh(newSrc.getIP()))
                    print("correct path:", newSrc.pathCost + self.getLinkWeight(curr, newSrc) == curr.pathCost)
                    if((curr.isNeigh(newSrc.getIP())) and 
                       (newSrc.pathCost + self.getLinkWeight(curr, newSrc) == curr.pathCost)):
                        if(newSrc.getIP() == src.getIP()):
                            print("neighbors and source newSrc:", newSrc.getIP(), "curr:", curr.getIP(), "index:", index)
                            break
                        else:
                            print("neighbors not source newSrc:", newSrc.getIP(), "curr:", curr.getIP(), "index:", index)
#                             curr = self.getRouter(newPath[index].getIP())
                            curr = self.getRouter(src.visited[index].getIP())
                            break
                    else:
                        print("not neighbors/not path newSrc:", newSrc.getIP(), "curr:", curr.getIP(), "index:", index)
#                         if(newSrc.getIP() != src.getIP()):
#                             newPath.append(self.getRouter(newSrc.getIP()))
#                             print("2appended to newPath", newSrc.getIP())
                        index += 1
                        if(index > 2):
                            src.printTable()
                            return  
                        print("index changed to", index)
                        newSrc = self.getRouter(src.visited[index].getIP())
                        
                src.table.append((n.getIP(), curr.getIP()))
                src.printTable()
        src.printTable()                
        #################################################
        #################################################
        
    def updatePaths(self, min, src, visited):
        newMin = None
        minCost = float("inf")
        print("min =", min.getIP())
        for l in min.getLinks():
            r2IP = ""
            if(l.getLink(1) == min.getIP()):
                r2IP = l.getLink(2)
                print("2grabbed link 2", r2IP, "from", min.getIP())
                
            if(l.getLink(2) == min.getIP()):
                r2IP = l.getLink(1)
                print("2grabbed link 1", r2IP, "from", min.getIP())
            
            r2 = self.getRouter(r2IP)
            if(r2 == "Router does not exist."):
                continue
            print("r2 is", r2.getIP())
            if(r2IP != src.getIP() and r2.pathCost > l.getWeight() + min.pathCost):
                r2.pathCost = l.getWeight() + min.pathCost
#                 if(r2.pathCost <= minCost):
#                     minCost = r2.pathCost
#                    newMin = r2
        #len(visited) == len(self.listRouters)
        for r in self.listRouters:
            if(r.pathCost <= minCost and r.getIP() != src.getIP() and not(self.isVisited(r.getIP(), visited))):
                minCost = r.pathCost
                newMin = self.getRouter(r.getIP())
        if(newMin == None):
            return visited
        visited.append(newMin)
        newMin.printLinks()
        print("appending", newMin.getIP())
        if(len(visited) == len(self.listRouters)):
            print("visited returned")
            return visited
        else: 
            return self.updatePaths(newMin, min, visited)  



graph = Graph()

print("Welcome to Group Awful's Awful-Network-Simulator\u00a9 (by Travis Anderson & Chandler Staggs)",
      "\nBelow, you can see the current state of the network.", 
      "\nType the appropriate key to add routers, remove routers, and view a particular router's forwarding table.")

while(True):

    ######### DISPLAY NETWORK STATE HERE #############
    print("------------- Network State -------------",
          "\n Router | -Link Weight-> | Link ")
    
    
    if(graph.listRouters != []):
        for r in graph.listRouters:
            i = 1
            for l in r.getLinks():
                if(i == 1):
                    print(r.getIP(), "-"+ str(graph.getLinkWeight(r, graph.getRouter(l.getLink(2)))) +"->", l.getLink(2))
                    i += 1
                else:
                    print("          ", "-"+ str(graph.getLinkWeight(r, graph.getRouter(l.getLink(2)))) +"->", l.getLink(2))
        
    
    userIn = input("Add router: 'a' || Remove router: 'r' || View Forwarding Table: 'f' || Exit: 'e' -> ")
    
    if(userIn == "a"):
        graph.addRouter()
    elif(userIn == "r"):
        ip = input("Please enter the IP address of the router you wish to remove")
        graph.rmRouter(ip)
    elif(userIn == "f"):
        ip = input("Please enter the IP address of the router you wish to see the forwarding table of")
        graph.getRouter(ip).printTable()
    elif(userIn == "e"):
        exit(0)
    else:
        print("Please enter a valid key option")

    



    

