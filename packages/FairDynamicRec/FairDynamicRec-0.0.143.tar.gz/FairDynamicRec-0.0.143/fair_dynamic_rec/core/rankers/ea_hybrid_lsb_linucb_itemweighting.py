from .ea_linear_submodular_bandit import EALSB
import numpy as np
import math

class EAHybridLSBLinUCBItemWeight(EALSB):
    def __init__(self, config, dataObj, parameters=None):
        """
        The first part of features are for the diversity and the second part is for relevance.
        :param args:
        :param kwargs:
        """
        super(EAHybridLSBLinUCBItemWeight, self).__init__(config, dataObj, parameters)
        self.topic_dim = self.dataObj.feature_data['train_item_topical_features'].shape[1]
        self.latent_dim = self.dataObj.feature_data['train_item_latent_features'].shape[1]

        # for the topic
        self.beta = np.ones((self.dataObj.n_users, self.topic_dim))
        self.b_z = np.zeros((self.dataObj.n_users, self.topic_dim))  # d
        self.A_z = np.zeros((self.dataObj.n_users, self.topic_dim, self.topic_dim))  # d by d
        self.A_z_inv = np.zeros((self.dataObj.n_users, self.topic_dim, self.topic_dim))
        for i in range(self.dataObj.n_users):
            self.A_z[i] = np.eye(self.topic_dim)
            self.A_z_inv[i] = np.eye(self.topic_dim)

        # for the relevance
        self.theta = np.ones((self.dataObj.n_users, self.latent_dim))
        self.b_x = np.zeros((self.dataObj.n_users, self.latent_dim))
        self.A_x = np.zeros((self.dataObj.n_users, self.latent_dim, self.latent_dim))
        self.A_x_inv = np.zeros((self.dataObj.n_users, self.latent_dim, self.latent_dim))
        for i in range(self.dataObj.n_users):
            self.A_x[i] = np.eye(self.latent_dim)
            self.A_x_inv[i] = np.eye(self.latent_dim)
        self.B = np.zeros((self.dataObj.n_users, self.latent_dim, self.topic_dim))

        self.X_topical = np.zeros((self.dataObj.n_users, self.dataObj.feature_data['train_item_topical_features'].shape[0], self.dataObj.feature_data['train_item_topical_features'].shape[1]))
        self.X_latent = np.zeros((self.dataObj.n_users, self.dataObj.feature_data['train_item_latent_features'].shape[0], self.dataObj.feature_data['train_item_latent_features'].shape[1]))
        for i in range(self.dataObj.n_users):
            self.X_topical[i] = self.dataObj.feature_data['train_item_topical_features']
            self.X_latent[i] = self.dataObj.feature_data['train_item_latent_features']
        self.gamma = float(parameters["gamma"]["value"])

    def update(self, batch_users, rankings, clicks, round=None, user_round=None):
        for i in range(len(batch_users)):
            user = batch_users[i]
            _clicks, _batch_features = self.__collect_feedback(clicks, i)

            discount_coef = [pow(self.gamma, j) for j in range(1, len(_clicks) + 1)]
            # 1
            # discount_coef_reward = [1 + pow(self.gamma, len(rankings[i])-j+1) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [x+1 for x in discount_coef]
            # 2
            # discount_coef_reward = [pow(self.gamma, len(rankings[i]) - j + 1) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [x for x in discount_coef]
            # 3
            # discount_coef_reward = [pow(self.gamma, len(rankings[i]) - j + 1) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [pow(1 - self.gamma, j) for j in range(1, len(_clicks) + 1)]
            # # 4
            # discount_coef_reward = [1 + pow(self.gamma, len(rankings[i]) - j + 1) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [pow(1 - self.gamma, j) for j in range(1, len(_clicks) + 1)]
            # 6
            discount_coef_reward = [1 + math.log(j) for j in range(1, len(_clicks) + 1)]
            # # 7
            # discount_coef_reward = [1 + math.log(j) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [self.gamma * 1 / (1 + math.log(j)) for j in range(1, len(_clicks) + 1)]

            if self.type == 'item_weight':
                clicked_items_index = np.where(_clicks == 1)[0]
                if len(clicked_items_index) == 0:
                    self.X_topical[user][rankings[i], :] = np.multiply(np.array(discount_coef).reshape(len(_clicks), 1), self.X_topical[user][rankings[i], :])
                    self.X_latent[user][rankings[i], :] = np.multiply(np.array(discount_coef).reshape(len(_clicks), 1), self.X_latent[user][rankings[i], :])
                else:
                    previous_clicked_item_index = 0
                    for clicked_item_index in clicked_items_index:
                        current_clicked_item_index = clicked_item_index
                        # penalizing unclicked items
                        self.X_topical[user][rankings[i][current_clicked_item_index], :] = (2 - discount_coef[current_clicked_item_index]) * self.X_topical[user][rankings[i][current_clicked_item_index], :]
                        self.X_latent[user][rankings[i][current_clicked_item_index], :] = (2 - discount_coef[current_clicked_item_index]) * self.X_latent[user][rankings[i][current_clicked_item_index], :]
                        # rewarding clicked items
                        self.X_topical[user][rankings[i][previous_clicked_item_index: current_clicked_item_index], :] = np.multiply(np.array(discount_coef[previous_clicked_item_index: current_clicked_item_index]).reshape(current_clicked_item_index - previous_clicked_item_index, 1), self.X_topical[user][rankings[i][previous_clicked_item_index: current_clicked_item_index], :])
                        self.X_latent[user][rankings[i][previous_clicked_item_index: current_clicked_item_index], :] = np.multiply(np.array(discount_coef[previous_clicked_item_index: current_clicked_item_index]).reshape(current_clicked_item_index - previous_clicked_item_index, 1), self.X_latent[user][rankings[i][previous_clicked_item_index: current_clicked_item_index], :])
                        previous_clicked_item_index = current_clicked_item_index + 1

            """
            Algorithm 2 of WWW 2010

            Return: self.theta is updated.
            """
            z = _batch_features[:, :self.topic_dim]
            x = _batch_features[:, self.topic_dim:]

            BA = np.matmul(self.B[user].T, self.A_x_inv[user])
            self.A_z[user] += np.matmul(BA, self.B[user])
            self.b_z[user] += np.dot(BA, self.b_x[user])

            self.A_x[user] += np.dot(x.T, x)
            self.B[user] += np.dot(x.T, z)
            if self.type == 'feature_weight':
                clicked_items_index = np.where(_clicks == 1)[0]
                _x = x
                # if len(clicked_items_index) == 0:
                #     _x = -np.multiply(np.array(discount_coef_penalization).reshape(len(_clicks), 1), _x)
                # else:
                #     previous_clicked_item_index = 0
                for clicked_item_index in clicked_items_index:
                    current_clicked_item_index = clicked_item_index
                    _x[current_clicked_item_index, :] = discount_coef_reward[current_clicked_item_index] * _x[current_clicked_item_index, :]
                        # _x[previous_clicked_item_index: current_clicked_item_index, :] = -np.multiply(np.array(discount_coef_penalization[previous_clicked_item_index: current_clicked_item_index]).reshape(current_clicked_item_index-previous_clicked_item_index,1), _x[previous_clicked_item_index: current_clicked_item_index, :])
                        # previous_clicked_item_index = current_clicked_item_index + 1
                # self.b_x[user] += _x.sum(axis=0)
            # else:
            self.b_x[user] += np.dot(_clicks, _x)

            try:
                self.A_x_inv[user] = np.linalg.inv(self.A_x[user])
            except:
                self.A_x_inv[user] = np.linalg.pinv(self.A_x[user])

            BA = np.matmul(self.B[user].T, self.A_x_inv[user])
            self.A_z[user] += np.dot(z.T, z) - np.matmul(BA, self.B[user])
            if self.type == 'feature_weight':
                clicked_items_index = np.where(_clicks == 1)[0]
                _z = z
                # if len(clicked_items_index) == 0:
                #     _z = -np.multiply(np.array(discount_coef_penalization).reshape(len(_clicks), 1), _z)
                # else:
                #     previous_clicked_item_index = 0
                for clicked_item_index in clicked_items_index:
                    current_clicked_item_index = clicked_item_index
                    _z[current_clicked_item_index, :] = discount_coef_reward[current_clicked_item_index] * _z[current_clicked_item_index, :]
                        # _z[previous_clicked_item_index: current_clicked_item_index, :] = -np.multiply(np.array(discount_coef_penalization[previous_clicked_item_index: current_clicked_item_index]).reshape(current_clicked_item_index-previous_clicked_item_index,1), _z[previous_clicked_item_index: current_clicked_item_index, :])
                        # previous_clicked_item_index = current_clicked_item_index + 1
                # self.b_z[user] += _z.sum(axis=0) - np.dot(BA, self.b_x[user])
            # else:
            self.b_z[user] += np.dot(_clicks, _z) - np.dot(BA, self.b_x[user])

            try:
                self.A_z_inv[user] = np.linalg.inv(self.A_z[user])
            except:
                self.A_z_inv[user] = np.linalg.pinv(self.A_z[user])

            self.beta[user] = np.dot(self.A_z_inv[user], self.b_z[user])
            B_tmp = self.b_x[user] - np.dot(self.B[user], self.beta[user])
            self.theta[user] = np.dot(self.A_x_inv[user], B_tmp)

            self.n_samples[user] += len(_clicks)
            self.n_clicks[user] += sum(_clicks)

    # def __collect_feedback(self, y):
    #     """
    #     With Cascade assumption, only the first click counts.
    #     :param y: click feedback
    #     :return: position of first click
    #     """
    #     if np.sum(y) == 0:
    #         return len(y)
    #     first_click = np.where(y)[0][0]
    #
    #     return first_click + 1

    # def update(self, y, delta=None):
    #     if delta is None:
    #         delta = self.delta_t
    #     feedback_len = self.__collect_feedback(y=y)
    #     delta = delta[:feedback_len].reshape((feedback_len, self.d))  # make sure it is a matrix
    #     self.__compute_parameters(delta=delta, y=y[:feedback_len])
    #     self.n_samples += len(y)
    #     self.n_clicks += sum(y)

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

    def get_ranking(self, batch_users, sampled_item=None, round=None):
        """
        :param x: n * (n_topic + n_feature) np array
        :param k: number of positions
        :return: ranking: the ranked item id.
        """
        # assert x.shape[0] >= k
        rankings = np.zeros((len(batch_users), self.config.list_size), dtype=int)
        self.batch_features = np.zeros((len(batch_users), self.config.list_size, self.topic_dim + self.latent_dim))
        tie_breaker = self.prng.rand(len(self.dataObj.feature_data['train_item_latent_features']))

        # self.delta_t = np.zeros((k, x.shape[1]))
        # delta = x

        # z = delta[:, :self.n_z]  # topic
        # x = delta[:, self.n_z:]  # feature

        # tie_breaker = self.prng.rand(len(delta))
        for i in range(len(batch_users)):
            user = batch_users[i]
            # for CB
            BA_X = np.matmul(self.B[user].T, self.A_x_inv[user])  # B.T  A_x^-1
            ABA = np.matmul(self.A_z_inv[user], BA_X)  # A_z^-1 B.T A_X^-1
            ABABA = np.matmul(BA_X.T, ABA)

            # score and cb for the relevance
            score_x = np.dot(self.X_latent[user], self.theta[user])
            XAX = np.multiply(np.dot(self.X_latent[user], self.A_x_inv[user]), self.X_latent[user]).sum(axis=1)  # x^T A_X^-1 X^T
            cb_x = np.multiply(np.dot(self.X_latent[user], ABABA), self.X_latent[user]).sum(axis=1) + XAX
            ucb_x = score_x + 1e-6 * tie_breaker
            ABAX = np.dot(ABA, self.X_latent[user].T).T
            # score and cb for the topic
            # delta_t = []
            batch_features = []
            coverage = np.zeros(self.topic_dim)
            ranking = []
            # ranking_set = set()
            for j in range(self.config.list_size):
                # Line 8 - 11 of Nips 11
                z_t = self.conditional_coverage(x=self.X_topical[user], coverage=coverage)
                ZAZ = np.multiply(np.dot(z_t, self.A_z_inv[user]), z_t).sum(axis=1)  # Z^T A_Z^-1 Z^T
                # cb_z = ZAZ - 2 * np.multiply(np.dot(z_t, ABA), x).sum(axis=1)
                cb_z = ZAZ - 2 * np.multiply(z_t, ABAX).sum(axis=1)

                # if (self.mitigation is None):
                cb = self.alpha * np.sqrt(cb_z + cb_x)
                # else:
                #     cb = self.alpha * (1 - (self.n_recommended / (t + 1))) * np.sqrt(cb_z + cb_x)
                score_z = np.dot(z_t, self.beta[i])
                ucb = ucb_x + score_z + cb
                # ucb = ucb_x + (1-user_avg_popularity)*score_z + cb

                # if(self.mitigation is not None):
                #     # tmp_n_recommended = self.n_recommended.copy()
                #     # tmp_n_recommended[np.where(tmp_n_recommended == 0)] = 1
                #     # ucb = (1-pow(self.n_recommended/(t+1),2)) * ucb
                #     ucb = (1 - (self.n_recommended / (t + 1))) * ucb

                winner = np.argmax(ucb)
                while winner in ranking:
                    ucb[winner] = -np.inf
                    winner = np.argmax(ucb)

                ranking.append(winner)
                # ranking_set.add(winner)
                batch_features.append(z_t[winner])

                coverage = self.ranking_coverage(self.X_topical[user][ranking])

            rankings[i] = np.asarray(ranking)
            self.batch_features[i][:, :self.topic_dim] = np.asarray(batch_features)
            self.batch_features[i][:, self.topic_dim:] = self.X_latent[user][rankings[i]]
        return rankings

    # def score(self, delta):
    #     """
    #     return score for an item
    #     """
    #     return np.dot(delta[:, :self.n_z], self.beta) + np.dot(delta[:, self.n_z:], self.theta)

    # def ucb(self, delta):
    #     """
    #     return the upper confident bound of each item. This is for debugging.
    #     :param x:
    #     :return:
    #     """
    #     score = self.score(delta)
    #     z = delta[:, :self.n_z]  # topic
    #     x = delta[:, self.n_z:]  # feature
    #
    #     ZAZ = np.multiply(np.dot(z, self.A_z_inv), z).sum(axis=1)  # Z^T A_Z^-1 Z^T
    #     XAX = np.multiply(np.dot(x, self.A_x_inv), x).sum(axis=1)  # x^T A_X^-1 X^T
    #     BA_X = np.matmul(self.B.T, self.A_x_inv)  # B.T  A_x^-1
    #     ABA = np.matmul(self.A_z_inv, BA_X)  # A_z^-1 B.T A_X^-1
    #     ABABA = np.matmul(BA_X.T, ABA)
    #     s = ZAZ + XAX + np.multiply(np.dot(x, ABABA), x).sum(axis=1) - 2 * np.multiply(np.dot(z, ABA), x).sum(axis=1)
    #     cb = self.alpha * np.sqrt(s)
    #     return score + cb
