import numpy as np
from .abstract_ranker import AbstractRanker
import math

class EALSB(AbstractRanker):
    def __init__(self, config, dataObj, parameters=None):
        super(EALSB, self).__init__(config, dataObj)
        self.n_samples = np.zeros(dataObj.n_users)
        self.n_clicks = np.zeros(dataObj.n_users)
        self.dim = self.dataObj.feature_data['train_item_topical_features'].shape[1]
        self.prng = np.random.RandomState(seed=config.seed)
        self.alpha = float(parameters["alpha"]["value"])

        self.sigma = float(parameters["sigma"]["value"])
        self.ill_matrix_counter = 0
        self.theta = np.ones((self.dataObj.n_users, self.dim))  # d-dimensional
        self.b = np.zeros((self.dataObj.n_users, self.dim))  # d
        self.M = np.zeros((self.dataObj.n_users, self.dim, self.dim))  # d by d
        self.MInv = np.zeros((self.dataObj.n_users, self.dim, self.dim))  # for fast matrix inverse computation, d by d
        for i in range(self.dataObj.n_users):
            self.M[i] = np.eye(self.dim)
            self.MInv[i] = np.eye(self.dim)

        # for ill inverse
        self.b_tmp = np.zeros((self.dataObj.n_users, self.dim))
        self.MInv_tmp = np.zeros((self.dataObj.n_users, self.dim, self.dim))
        self.batch_features = None

        # self.X = np.zeros((self.dataObj.n_users, self.dataObj.feature_data['train_item_topical_features'].shape[0], self.dataObj.feature_data['train_item_topical_features'].shape[1]))
        # for i in range(self.dataObj.n_users):
        #     self.X[i] = self.dataObj.feature_data['train_item_topical_features']
        self.gamma = float(parameters["gamma"]["value"])
        self.type = parameters["type"]["value"]
        self.window = int(parameters['window']['value'])
        self.click_history = np.zeros((self.dataObj.n_users, self.dim))

    def get_ranking(self, batch_users, sampled_item=None, round=None):
        """
        :param x: features
        :param k: number of positions
        :return: ranking: the ranked item id.
        delta: the conditional topic coverage of each item. Eq. (3) of NIPS 11 paper.
        """
        # assert x.shape[0] >= k
        rankings = np.zeros((len(batch_users), self.config.list_size), dtype=int)
        self.batch_features = np.zeros((len(batch_users), self.config.list_size, self.dim))
        tie_breaker = self.prng.rand(len(self.dataObj.feature_data['train_item_topical_features']))
        for i in range(len(batch_users)):
            user = batch_users[i]
            coverage = np.zeros(self.dim)
            ranking = []
            for j in range(self.config.list_size):
                # Line 8 - 11 of Nips 11
                gain_in_topic_coverage = self.conditional_coverage(x=self.dataObj.feature_data['train_item_topical_features'], coverage=coverage)
                cb = self.alpha * np.sqrt(np.multiply(np.dot(gain_in_topic_coverage, self.MInv[user]), gain_in_topic_coverage).sum(axis=1))
                score = np.dot(gain_in_topic_coverage, self.theta[user])
                ucb = score + cb + 1e-6 * tie_breaker

                winner = np.argmax(ucb)
                while winner in ranking:
                    ucb[winner] = -np.inf
                    winner = np.argmax(ucb)

                ranking.append(winner)
                self.batch_features[i][j] = gain_in_topic_coverage[winner]

                coverage = self.ranking_coverage(self.dataObj.feature_data['train_item_topical_features'][ranking])
            rankings[i] = np.asarray(ranking)
        return rankings

    def update(self, batch_users, rankings, clicks, round=None, user_round=None):
        for i in range(len(batch_users)):
            user = batch_users[i]
            _clicks, _batch_features = self.__collect_feedback(clicks, i)

            discount_coef = [pow(self.gamma, j) for j in range(1,len(_clicks)+1)]
            #1
            # discount_coef_reward = [1 + pow(self.gamma, len(rankings[i])-j+1) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [x+1 for x in discount_coef]
            #2
            # discount_coef_reward = [pow(self.gamma, len(rankings[i]) - j + 1) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [x for x in discount_coef]
            #3
            # discount_coef_reward = [pow(self.gamma, len(rankings[i]) - j + 1) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [pow(1-self.gamma, j) for j in range(1, len(_clicks) + 1)]
            # # 4
            # discount_coef_reward = [1 + pow(self.gamma, len(rankings[i]) - j + 1) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [pow(1 - self.gamma, j) for j in range(1, len(_clicks) + 1)]
            # # 6
            # discount_coef_reward = [1 + math.log(j) for j in range(1, len(_clicks) + 1)]
            # 7
            discount_coef_reward = [1 + math.log(j) for j in range(1, len(_clicks) + 1)]
            discount_coef_penalization = [self.gamma * 1 / (1 + math.log(j)) for j in range(1, len(_clicks) + 1)]

            # if self.type == 'item_weight':
            #     clicked_items_index = np.where(_clicks == 1)[0]
            #     if len(clicked_items_index) == 0:
            #         self.X[user][rankings[i], :] = np.multiply(np.array(discount_coef).reshape(len(_clicks), 1), self.X[user][rankings[i], :])
            #     else:
            #         previous_clicked_item_index = 0
            #         for clicked_item_index in clicked_items_index:
            #             current_clicked_item_index = clicked_item_index
            #             self.X[user][rankings[i][current_clicked_item_index], :] = (2 - discount_coef[current_clicked_item_index]) * self.X[user][rankings[i][current_clicked_item_index], :]
            #             self.X[user][rankings[i][previous_clicked_item_index: current_clicked_item_index], :] = np.multiply(np.array(discount_coef[previous_clicked_item_index: current_clicked_item_index]).reshape(current_clicked_item_index-previous_clicked_item_index,1), self.X[user][rankings[i][previous_clicked_item_index: current_clicked_item_index], :])
            #             previous_clicked_item_index = current_clicked_item_index + 1

            """
            This is for computing self.theta (Line 3-5 of Alogirthm 1 of NIPS 11)
            For fast matrix inverse, we use Woodbury matrix identity (https://en.wikipedia.org/wiki/Woodbury_matrix_identity)

            Return: self.theta is updated.
            """
            # for the inverse of M, feature matrix
            # x * m^-1 * x^T
            xmx = np.dot(_batch_features, np.dot(self.MInv[user], _batch_features.T))
            # (1/sigma I + xmx)^-1
            try:
                tmp_inv = np.linalg.inv(1 / self.sigma * np.eye(len(_batch_features)) + xmx)
            except np.linalg.LinAlgError:
                # for the ill matrix. if the matrix is not invertible, we ignore this update
                self.ill_matrix_counter += 1
                return
            # m^-1*x^T
            MInv_xT = self.MInv[user].dot(_batch_features.T)
            # MInv_xT*tmp_inv*MInv_xT^T
            self.MInv_tmp[user] = np.dot(np.dot(MInv_xT, tmp_inv), MInv_xT.T)
            # MInv - the new part
            self.MInv[user] -= self.MInv_tmp[user]

            self.M[user] += self.sigma * _batch_features.T.dot(_batch_features)

            # for b: feedback
            # if self.type == 'feature_weight' and round % self.window == 0:
            #     clicked_items_index = np.where(_clicks == 1)[0]
            #     if len(clicked_items_index) == 0:
            #         _batch_features = -np.multiply(np.array(discount_coef_penalization).reshape(len(_clicks), 1), _batch_features)
            #     else:
            #         previous_clicked_item_index = 0
            #         for clicked_item_index in clicked_items_index:
            #             current_clicked_item_index = clicked_item_index
            #             _batch_features[current_clicked_item_index, :] = discount_coef_reward[current_clicked_item_index] * _batch_features[current_clicked_item_index, :]
            #             _batch_features[previous_clicked_item_index: current_clicked_item_index, :] = -np.multiply(np.array(discount_coef_penalization[previous_clicked_item_index: current_clicked_item_index]).reshape(current_clicked_item_index-previous_clicked_item_index,1), _batch_features[previous_clicked_item_index: current_clicked_item_index, :])
            #             previous_clicked_item_index = current_clicked_item_index + 1
            #     self.b_tmp[user] = _batch_features.sum(axis=0)
            # else:
            #     self.b_tmp[user] = np.dot(_clicks, _batch_features)
            if self.type == 'feature_weight':
                clicked_items_index = np.where(_clicks == 1)[0]
                _x = _batch_features
                if len(clicked_items_index) == 0:
                    _x = -np.multiply(np.array(discount_coef_penalization).reshape(len(_clicks), 1), _batch_features)
                else:
                    previous_clicked_item_index = 0
                    for clicked_item_index in clicked_items_index:
                        current_clicked_item_index = clicked_item_index
                        _x[current_clicked_item_index, :] = discount_coef_reward[current_clicked_item_index] * _batch_features[current_clicked_item_index, :]
                        _x[previous_clicked_item_index: current_clicked_item_index, :] = -np.multiply(np.array(discount_coef_penalization[previous_clicked_item_index: current_clicked_item_index]).reshape(current_clicked_item_index-previous_clicked_item_index,1), _batch_features[previous_clicked_item_index: current_clicked_item_index, :])
                        previous_clicked_item_index = current_clicked_item_index + 1
                self.click_history[user] += _x.sum(axis=0)
                self.b_tmp[user] = np.dot(_clicks, _batch_features)
                if user_round[user] % self.window == 0:
                    self.b_tmp[user] = self.click_history[user] / self.window
                    self.click_history[user] = np.zeros(self.dim)
            else:
                self.b_tmp[user] = np.dot(_clicks, _batch_features)
            self.b[user] += self.b_tmp[user]

            # for parameter theta
            self.theta[user] = np.dot(self.MInv[user], self.b[user])
            # self.theta[self.theta < 0] = 0

            self.n_samples[user] += len(_clicks)
            self.n_clicks[user] += sum(_clicks)

    def __collect_feedback(self, clicks, batch_user_id):
        """
        :param y:
        :return: the last observed position.
        """
        # With  Cascade assumption, only the first click counts.
        if self.config.feedback_model == 'cascade':
            if np.sum(clicks[batch_user_id]) == 0:
                return clicks[batch_user_id], self.batch_features[batch_user_id]
            first_click = np.where(clicks[batch_user_id])[0][0]
            return clicks[batch_user_id][:first_click + 1], self.batch_features[batch_user_id][:first_click + 1]
        elif self.config.feedback_model == 'dcm':
            if np.sum(clicks[batch_user_id]) == 0:
                return clicks[batch_user_id], self.batch_features[batch_user_id]
            last_click = np.where(clicks[batch_user_id])[0][-1]
            return clicks[batch_user_id][:last_click + 1], self.batch_features[batch_user_id][:last_click + 1]
        # all items are observed
        else:
            return clicks[batch_user_id], self.batch_features[batch_user_id]