
import math


class ItemBasedCF:
    def __init__(self, train_file):
        self.train_file = train_file
        self.productid2name = {}
        self.readData()

    def readData(self):

        self.train = dict()
        for line in open(self.train_file):
            # user,item,score = line.strip().split(",")
            user, score, item = line.strip().split(",")
            self.train.setdefault(user, {})
            self.train[user][item] = int(float(score))
            self.productid2name[item] = ''

        for line_name, k in zip(open("ID.txt"), self.productid2name):
            self.productid2name[k] = line_name.strip()

    def convertProductID2name(self, id):

        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    def ItemSimilarity(self):

        C = dict()
        N = dict()
        for user, items in self.train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1
                C.setdefault(i, {})
                for j in items.keys():
                    if i == j: continue
                    C[i].setdefault(j, 0)
                    C[i][j] += 1

        self.W = dict()
        for i, related_items in C.items():
            self.W.setdefault(i, {})
            for j, cij in related_items.items():
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        return self.W


    def Recommend(self, user, K=3, N=10):
        rank = dict()
        action_item = self.train[user]
        for item, score in action_item.items():
            datas = sorted(self.W[item].items(), key=lambda x: x[1], reverse=True)[0:K]
            for j, wj in datas:
                if j in action_item.keys():
                    continue
                rank.setdefault(j, 0)
                rank[j] += score * wj
        return sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]
Item = ItemBasedCF("uid_score_bid")
Item.ItemSimilarity()
recommedDic = Item.Recommend("cytun")
for k, v in recommedDic:
    print Item.convertProductID2name(k)
