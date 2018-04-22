from math import sqrt
fp = open("uid_score_bid", "r")
users = {}
productid2name = {}
for line in open("uid_score_bid"):
    lines = line.strip().split(",")
    if lines[0] not in users:
        users[lines[0]] = {}
    if lines[2] not in productid2name:
        productid2name[lines[2]] = ''
    users[lines[0]][lines[2]] = float(lines[1])
for line_name,k in zip(open("ID.txt"), productid2name):
    productid2name[k] = line_name.strip()
class recommender:
    def __init__(self, data, productid2name={},k=3, metric='pearson', n=10, ):

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
    def recommend(self, user):
        recommendations = {}
        nearest = self.computeNearestNeighbor(user)
        # print nearest
        userRatings = self.data[user]
        #         print userRatings
        totalDistance = 0.0
        for i in range(self.k):
            totalDistance += nearest[i][1]
        if totalDistance == 0.0:
            totalDistance = 1.0
        for i in range(self.k):
            weight = nearest[i][1] / totalDistance
            name = nearest[i][0]
            neighborRatings = self.data[name]
            for artist in neighborRatings:
                if not artist in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist] * weight)
                    else:
                        recommendations[artist] = (recommendations[artist] + neighborRatings[artist] * weight)
        recommendations = list(recommendations.items())
        recommendations = [(self.convertProductID2name(k), v) for (k, v) in recommendations]
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return recommendations[:self.n], nearest
def adjustrecommend(id):
    bookid_list = []
    # def __init__(self, data, k=3, metric='pearson', n=12):
    r = recommender(users,productid2name)
    k, nearuser = r.recommend("%s" % id)
    for i in range(len(k)):
        bookid_list.append(k[i][0])
    return bookid_list, nearuser[:15]
bookid_list,near_list = adjustrecommend("cytun")
for i in bookid_list:
    print(i)
