import random
class apriori:
    
    def __init__(self):
        self.items = []
        self.itemSets = ()
        self.supThresh = 3
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
        print(self.itemSets[0])
        print(self.itemSets[78])
        print(self.itemSets[50])
       # self.findSupport()


 #   def findSupport(self):
       # for i in range(len(self.itemSets)):
           # for j in range(len(self.itemSets[i])):
              #  print(self.itemSets[i][j])
        
        
items = ["bread", "eggs", "coffee", "donuts", "apples", "pairs", "cookies", "soda", "cereal", "applesauce"]
test = apriori()
test.createDataStream(items)