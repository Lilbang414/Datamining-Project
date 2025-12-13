import random
import itertools
class apriori:
    
    def __init__(self):
        self.items = []
        self.itemSets = ()
        self.supThresh = 20
        self
        
    def createDataStream(self,items):
        self.items = items
        itemSet = []
        count = 0
        while count < 100:
            setSize = random.randrange(1,len(self.items))
            for _ in range(setSize):
                item = random.choice(self.items)
                if item not in itemSet:
                    itemSet.append(item)
                
            self.itemSets = self.itemSets + (itemSet,)
            itemSet = []
            count = count + 1
        for i in range(len(self.itemSets)):
                print(self.itemSets[i])
        self.findSupport()


    def findSupport(self):
        support = {item: 0 for item in self.items}
        for i in range(len(self.itemSets)):
           for j in range(len(self.itemSets[i])):
            support[self.itemSets[i][j]] = support.get(self.itemSets[i][j], 0) + 1
        L1 = {item for item, count in support.items()
            if count >= self.supThresh}
        loopCount = 2
        Lremain = list(itertools.combinations(L1, loopCount))
        while not (len(Lremain) == 0):
            support2 = {}
            for item in Lremain:
                for i in range(len(self.itemSets)):
                    if set(item).issubset(self.itemSets[i]):
                        support2[item] = support2.get(item, 0) + 1
            Lprune = {item for item, count in support2.items()
                    if count >= self.supThresh}
            loopCount += 1
            Lremain = list(itertools.combinations(set(itertools.chain.from_iterable(Lprune)), loopCount))

        
items = ["bread", "eggs", "coffee", "donuts", "apples", "pears", "cookies", "soda", "cereal", "applesauce"]
test = apriori()
test.createDataStream(items)