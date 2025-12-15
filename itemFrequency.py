import random
import itertools
from fractions import Fraction

from flask import Flask, render_template, request

app = Flask(__name__)



class apriori:

    def __init__(self):
        self.items = []
        self.itemSets = ()
        self.supThresh = 20

    def createDataStream(self, items):
        self.items = items
        itemSet = []
        count = 0

        while count < 100:
            setSize = random.randrange(1, len(self.items))
            for _ in range(setSize):
                item = random.choice(self.items)
                if item not in itemSet:
                    itemSet.append(item)
                if item == 'apples' and 'pears' not in itemSet:
                    chance = random.choice([1,2])
                    if chance == 1:
                        itemSet.append('pears')
                if item == 'pears' and 'apples' not in itemSet:
                    chance = random.choice([1, 2])
                    if chance == 1:
                        itemSet.append('apples')
            self.itemSets = self.itemSets + (tuple(sorted(itemSet)),)
            itemSet = []
            count = count + 1

    def findSupport(self):
        support = {item: 0 for item in self.items}
        for i in range(len(self.itemSets)):
            for j in range(len(self.itemSets[i])):
                support[self.itemSets[i][j]] = support.get(self.itemSets[i][j], 0) + 1
        L1 = {item for item, count in support.items()
              if count >= self.supThresh}
        all_L = []
        all_L.append(L1)
        loopCount = 2
        Lremain = list(itertools.combinations(sorted(L1), loopCount))
        while not (len(Lremain) == 0):
            support2 = {}
            for item in Lremain:
                for i in range(len(self.itemSets)):
                    if set(item).issubset(self.itemSets[i]):
                        support2[item] = support2.get(item, 0) + 1
            Lprune = {item for item, count in support2.items()
                      if count >= self.supThresh}
            if len(Lprune) == 0:
                break
            all_L.append(Lprune)
            loopCount += 1
            Lremain = list(itertools.combinations(sorted(set(itertools.chain.from_iterable(Lprune))), loopCount))
        return all_L

    def Support(self, item):
        support = 0
        for i in range(len(self.itemSets)):
            for j in range(len(self.itemSets[i])):
                if item == self.itemSets[i][j]:
                    support = support + 1
        return support

    def SupportXUY(self, item1, item2):
        support = 0
        item1in = False
        item2in = False
        for i in range(len(self.itemSets)):
            for j in range(len(self.itemSets[i])):
                if item1 == self.itemSets[i][j]:
                    item1in = True
                if item2 == self.itemSets[i][j]:
                    item2in = True
                if item1in and item2in:
                    break
            if item1in and item2in:
                support += 1
            item1in = False
            item2in = False
        return support

    def findConfidence(self, item1, item2):
        confidence = float(self.SupportXUY(item1, item2) / self.Support(item1))
        confidence = round(confidence * 100, 2)
        return confidence

    def findInterest(self, confidence, item2):
        support = self.Support(item2)
        pSupport = (support / len(self.itemSets)) * 100
        interest = confidence-pSupport
        interestFinal = Fraction(interest/100).limit_denominator(100)
        return interestFinal

    def findAllSupports(self, item):
        allSupports = {}
        allSupports[item] = self.Support(item)
        for allOtherItems in self.items:
            if allOtherItems != item:
                allSupports[allOtherItems] = (self.SupportXUY(item, allOtherItems))
        return allSupports

a = apriori()
items = ["bread", "eggs", "coffee", "donuts", "apples", "pears", "cookies", "soda", "cereal", "applesauce"]
a.createDataStream(items)

@app.route("/", methods=["GET", "POST"])
def main():
    global a
    result = 0
    error = None
    display = False
    levels = 0


    if request.method == "POST":
        action = request.form.get("action")

        result = a.findSupport()
        levels = len(result)
        displayAll = True

        if action == "confidence":
            item1 = request.form.get("item1")
            item2 = request.form.get("item2")
            display = True
            displayAll = True
            requestedSupport = a.SupportXUY(item1, item2)
            requestedConfidence = a.findConfidence(item1, item2)
            requestedInterest = a.findInterest(requestedConfidence, item2)
            return render_template("itemFrequency.html", requestedConfidence=requestedConfidence, requestedSupport=requestedSupport, requestedInterest=requestedInterest,
                                item1=item1, item2=item2, display=display, displayAll=displayAll, levels = levels,result = result)

        if action == "allSupports":
            item3 = request.form.get("item3")
            display2 = True
            displayAll = True
            requestedAllSupports = a.findAllSupports(item3)
            return render_template("itemFrequency.html", requestedAllSupports=requestedAllSupports, item3=item3, display2=display2, displayAll=displayAll, levels = levels, result = result )
        
        if action == "support":
            try:
                supThresh = int(request.form.get("supThresh", 20))
                a.supThresh = supThresh
                result = a.findSupport()
                levels = len(result)
                return render_template("itemFrequency.html", displayAll=displayAll, result=result, error=error, levels=levels)

            except ValueError:
                error = "Must be a number 1-100"

    return render_template("itemFrequency.html", error=error)


if __name__ == "__main__":
    test = apriori()
    items = ["bread", "eggs", "coffee", "donuts", "apples", "pears", "cookies", "soda", "cereal", "applesauce"]
    test.createDataStream(items)
    print(test.Support("bread"))
    print(test.SupportXUY("bread", "coffee"))
    print(test.findConfidence("bread", "coffee"))

    app.run(debug=True)


