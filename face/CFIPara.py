# coding=utf-8
# 测试
from __future__ import print_function
import random
from math import sqrt
import math


class recommender:
    def __init__(self, k, train):
        self.k = k
        # self.train_file = train_file
        self.train=train
        # self.readData()
    #
    # def readData(self):
    #     读取文件，并生成用户-物品的评分表和测试集
        # self.train = dict()  # 用户-物品的评分表
        # for line in open(self.train_file):
        #     user,item,score = line.strip().split(",")
            # user, score, item = line.strip().split(",")
            # self.train.setdefault(user, {})
            # self.train[user][item] = int(float(score))

    def ItemSimilarity(self):
        # 建立物品-物品的共现矩阵
        C = dict()  # 物品-物品的共现矩阵
        N = dict()  # 物品被多少个不同用户购买
        for user, items in self.train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1
                C.setdefault(i, {})
                for j in items.keys():
                    if i == j: continue
                    C[i].setdefault(j, 0)
                    C[i][j] += 1
        # 计算相似度矩阵
        self.W = dict()
        for i, related_items in C.items():
            self.W.setdefault(i, {})
            for j, cij in related_items.items():
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        return self.W

    # 给用户user推荐，前K个相关用户
    def recommend(self, user, N=10):
        K=self.k
        rank = dict()
        action_item = self.train[user]  # 用户user产生过行为的item和评分
        for item, score in action_item.items():
            datas = sorted(self.W[item].items(), key=lambda x: x[1], reverse=True)[0:K]
            for j, wj in datas:
                if j in action_item.keys():
                    continue
                rank.setdefault(j, 0)
                rank[j] += score * wj
        return sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]


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
    r = recommender(k, train)
    r.ItemSimilarity()
    k = r.recommend("%s" % user_id)

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
    for line in open('uid_score_bid'):
        lines = line.strip().split(",")
        if lines[0] not in users:
            users[lines[0]] = {}
        users[lines[0]][lines[2]] = float(lines[1])

    train, test = SplitData(users, 3, 2, 3.14)

    write_data("train.csv", train)
    write_data("test.csv", test)

    # print(Recall(train, test, 12))
    # for k in (20, 30, 40, 50):
    Precision(train, test, 12)
