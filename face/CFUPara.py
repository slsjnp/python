# coding=utf-8
# 测试
from __future__ import print_function
import random
from math import sqrt


class recommender:
    # data：数据集，这里指users
    # k：表示得出最相近的k的近邻
    # metric：表示使用计算相似度的方法
    # n：表示推荐book的个数
    def __init__(self, k, data, productid2name={}, metric='pearson', n=12):

        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = productid2name

        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        if type(data).__name__ == 'dict':
            self.data = data

    def convertProductID2name(self, id):

        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    # 定义的计算相似度的公式，用的是皮尔逊相关系数计算方法
    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0

        # 皮尔逊相关系数计算公式
        denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    def computeNearestNeighbor(self, username):
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username], self.data[instance])
                distances.append((instance, distance))

        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return distances

    # 推荐算法的主体函数
    def recommend(self, user):
        # 定义一个字典，用来存储推荐的预测书单和预测user会给这个书的预测分数
        recommendations = {}
        # 计算出user与所有其他用户的相似度，返回一个list
        nearest = self.computeNearestNeighbor(user)
        # print nearest

        userRatings = self.data[user]
        #         print userRatings
        totalDistance = 0.0
        # 得出最近的k个近邻的总距离
        for i in range(self.k):
            totalDistance += nearest[i][1]
        if totalDistance == 0.0:
            totalDistance = 1.0

        # 将与user最相近的k个人中user没有看过的书推荐给user，并且这里又做了一个分数的计算排名
        for i in range(self.k):

            # 第i个人的与user的相似度，转换到[0,1]之间
            weight = nearest[i][1] / totalDistance

            # 第i个人的name
            name = nearest[i][0]

            # 第i个用户看过的书和相应的打分
            neighborRatings = self.data[name]

            for artist in neighborRatings:
                if not artist in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist] * weight)
                    else:
                        recommendations[artist] = (recommendations[artist] + neighborRatings[artist] * weight)

        recommendations = list(recommendations.items())
        # recommendations = [(self.convertProductID2name(k), v) for (k, v) in recommendations]

        # 做了一个排序
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)

        return recommendations[:self.n], nearest


def SplitData(data, M, K, seed):
    """

    :param data:{'user1':{'item1': 4,'item2':5},'user2':{'item1': 5,'item2':4}}
    :param M:numbers of split Data
    :param k:0<=k<=M-1
    :param seed:
    :return:
    """
    test = {}
    train = {}
    random.seed(seed)
    for user, item in data.items():
        for key, value in item.items():
            if random.randint(0, M) == K:
                if user not in test:
                    test[user] = {}
                test[user][key] = value
            else:
                if user not in train:
                    train[user] = {}
                train[user][key] = value

    return train, test


def write_data(path, data):
    fp = open(path, "w")
    for user, item in data.items():
        for k, v in item.items():
            data_line = "{},{},{}\n".format(user, v, k)
            fp.writelines(data_line)


def GetRecommendation(train, user_id, N, k):
    r = recommender(k, train, n=N)
    k, nearuser = r.recommend("%s" % user_id)

    return k


def Recall(train, test, N, k):
    hit = 0
    all = 0
    count = 0
    for user in train.keys():
        tu = test[user]
        rank = GetRecommendation(train, user, N, k)
        for item, pui in rank:
            if item in tu:
                hit += 1
        all = len(tu)
        count += 1
        if count == 300:
            break
    return 0 if all == 0 else hit / (all * 1.0)


def Precision(train, test, N):
    hit = 0
    count = 0
    for user in train.keys():
        max_k = 0
        hit_max = 0
        max_recall = 0
        tu = test[user]
        for k in (20, 30, 40, 50):
            rank = GetRecommendation(train, user, N, k)
            for item, pui in rank:
                if item in tu:
                    hit += 1
                    # all += N
            all = len(tu)
            recall = 0 if all == 0 else hit / (all * 1.0)
            # print(recall)
            if (hit + recall) >= (hit_max + max_recall):
                hit_max = hit
                max_k = k
                max_recall = recall
            hit = 0
            recall = 0
        result = "{}:{}:{}:{}".format(user, max_k, round(hit_max / 12.0, 2), round(max_recall, 2))
        print(result)
        # print(user + ":" + max_k)
        count += 1
        if count == 300:
            break
            # return hit


if __name__ == "__main__":
    users = {}
    for line in open("uid_score_bid"):
        lines = line.strip().split(",")
        if lines[0] not in users:
            users[lines[0]] = {}
        users[lines[0]][lines[2]] = float(lines[1])

    train, test = SplitData(users, 3, 2, 3.14)

    # write_data("train.csv", train)
    # write_data("test.csv", test)

    # print(Recall(train, test, 12))
    # for k in (20, 30, 40, 50):
    Precision(train, test, 12)
