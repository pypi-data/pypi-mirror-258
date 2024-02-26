from .linear_submodular_bandit import LSB
import numpy as np
import math
from fair_dynamic_rec.core.util.utils import get_param_config_name
from fair_dynamic_rec.core.util.outputs import make_output_dir

class HybridLSBLinUCB(LSB):
    def __init__(self, config, dataObj, parameters=None):
        """
        The first part of features are for the diversity and the second part is for relevance.
        :param args:
        :param kwargs:
        """
        super(HybridLSBLinUCB, self).__init__(config, dataObj, parameters)
        self.topic_dim = self.dataObj.feature_data['train_item_topical_features'].shape[1]
        self.latent_dim = self.dataObj.feature_data['train_item_latent_features'].shape[1]

        if config.load_model and self.__class__.__name__ == 'HybridLSBLinUCB':
            self.load_parameters(config, parameters)
        else:
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

            # self.X_topical = np.zeros((self.dataObj.n_users, self.dataObj.feature_data['train_item_topical_features'].shape[0], self.dataObj.feature_data['train_item_topical_features'].shape[1]))
            # self.X_latent = np.zeros((self.dataObj.n_users, self.dataObj.feature_data['train_item_latent_features'].shape[0], self.dataObj.feature_data['train_item_latent_features'].shape[1]))
            # for i in range(self.dataObj.n_users):
            #     self.X_topical[i] = self.dataObj.feature_data['train_item_topical_features']
            #     self.X_latent[i] = self.dataObj.feature_data['train_item_latent_features']
            # self.gamma = float(parameters.get("gamma", {}).get("value", 0))
            # self.window = int(parameters.get('window', {}).get('value', 0))
            # self.click_history_x = np.zeros((self.dataObj.n_users, self.latent_dim))
            # self.click_history = np.zeros((self.dataObj.n_users, self.dim))

            # self.shuffle_K = int(parameters.get('shuffle_K', {}).get('value', 0))
            # self.epsilon = float(parameters.get('epsilon', {}).get('value', 0))
            # self.ears_gamma = float(parameters.get('ears_gamma', {}).get('value', 0))

            self.click_history_x = np.zeros((self.dataObj.n_users, self.latent_dim))
            self.click_history_z = np.zeros((self.dataObj.n_users, self.topic_dim))

    def save_parameters(self, config, ranker_config):
        pre_path = make_output_dir(config, get_param_config_name(ranker_config))
        np.savetxt(pre_path/'n_samples', self.n_samples, fmt='%i')
        np.savetxt(pre_path / 'n_clicks', self.n_clicks, fmt='%i')
        text_file = open(pre_path / 'ill_matrix_counter', "w")
        text_file.write(str(self.ill_matrix_counter))
        text_file.close()
        np.savetxt(pre_path / 'theta', self.theta, fmt='%f')
        # np.savetxt(pre_path / 'b', self.b, fmt='%f')
        # self.save_3d_array(pre_path / 'M', self.M, '%f')
        # self.save_3d_array(pre_path / 'MInv', self.MInv, '%f')
        # np.savetxt(pre_path / 'b_tmp', self.b_tmp, fmt='%f')
        # self.save_3d_array(pre_path / 'MInv_tmp', self.MInv_tmp, '%f')
        np.savetxt(pre_path / 'click_history', self.click_history, fmt='%f')
        # np.savetxt(pre_path / 'item_coef', self.item_coef, fmt='%f')
        # np.savetxt(pre_path / 'exp_recommended', self.exp_recommended, fmt='%f')
        # np.savetxt(pre_path / 'exp_examined', self.exp_examined, fmt='%f')
        np.savetxt(pre_path / 'beta', self.beta, fmt='%f')
        np.savetxt(pre_path / 'b_z', self.b_z, fmt='%f')
        self.save_3d_array(pre_path / 'A_z', self.A_z, '%f')
        self.save_3d_array(pre_path / 'A_z_inv', self.A_z_inv, '%f')
        np.savetxt(pre_path / 'b_x', self.b_x, fmt='%f')
        self.save_3d_array(pre_path / 'A_x', self.A_x, '%f')
        self.save_3d_array(pre_path / 'A_x_inv', self.A_x_inv, '%f')
        self.save_3d_array(pre_path / 'B', self.B, '%f')
        np.savetxt(pre_path / 'click_history_x', self.click_history_x, fmt='%f')
        np.savetxt(pre_path / 'click_history_z', self.click_history_z, fmt='%f')
    def load_parameters(self, config, ranker_config):
        pre_path = make_output_dir(config, get_param_config_name(ranker_config))
        self.n_samples = np.loadtxt(pre_path/'n_samples', dtype='int')
        self.n_clicks = np.loadtxt(pre_path / 'n_clicks', dtype='int')
        with open(pre_path / 'ill_matrix_counter') as file:
            line = file.readline().rstrip()
            self.ill_matrix_counter = int(line)
        self.theta = np.loadtxt(pre_path / 'theta')
        # self.b = np.loadtxt(pre_path / 'b')
        # self.M = self.load_3d_array(pre_path / 'M', (self.dataObj.n_users, self.dim, self.dim))
        # self.MInv = self.load_3d_array(pre_path / 'MInv', (self.dataObj.n_users, self.dim, self.dim))
        # self.b_tmp = np.loadtxt(pre_path / 'b_tmp')
        # self.MInv_tmp = np.loadtxt(pre_path / 'MInv_tmp')
        self.click_history = np.loadtxt(pre_path / 'click_history')
        # self.item_coef = np.loadtxt(pre_path / 'item_coef')
        # self.exp_recommended = np.loadtxt(pre_path / 'exp_recommended')
        # self.exp_examined = np.loadtxt(pre_path / 'exp_examined')
        self.beta = np.loadtxt(pre_path / 'beta')
        self.b_z = np.loadtxt(pre_path / 'b_z')
        self.A_z = self.load_3d_array(pre_path / 'A_z', (self.dataObj.n_users, self.topic_dim, self.topic_dim))
        self.A_z_inv = self.load_3d_array(pre_path / 'A_z_inv', (self.dataObj.n_users, self.topic_dim, self.topic_dim))
        self.b_x = np.loadtxt(pre_path / 'b_x')
        self.A_x = self.load_3d_array(pre_path / 'A_x', (self.dataObj.n_users, self.latent_dim, self.latent_dim))
        self.A_x_inv = self.load_3d_array(pre_path / 'A_x_inv', (self.dataObj.n_users, self.latent_dim, self.latent_dim))
        self.B = self.load_3d_array(pre_path / 'B', (self.dataObj.n_users, self.latent_dim, self.topic_dim))
        self.click_history_x = np.loadtxt(pre_path / 'click_history_x')
        self.click_history_z = np.loadtxt(pre_path / 'click_history_z')
    def save_3d_array(self, fn_out, arr, frmt):
        # Write the array to disk
        with open(fn_out, 'w') as outfile:
            # I'm writing a header here just for the sake of readability
            # Any line starting with "#" will be ignored by numpy.loadtxt
            outfile.write('# Array shape: {0}\n'.format(arr.shape))

            # Iterating through a ndimensional array produces slices along
            # the last axis. This is equivalent to data[i,:,:] in this case
            for data_slice in arr:
                # The formatting string indicates that I'm writing out
                # the values in left-justified columns 7 characters in width
                # with 2 decimal places.
                np.savetxt(outfile, data_slice, fmt=frmt)

                # Writing out a break to indicate different slices...
                outfile.write('# New slice\n')
    def load_3d_array(self, fn_in, shp):
        # Read the array from disk
        arr = np.loadtxt(fn_in)

        # However, going back to 3D is easy if we know the
        # original shape of the array
        return arr.reshape(shp)

    def update(self, batch_users, rankings, clicks, round=None, user_round=None):
        for i in range(len(batch_users)):
            user = batch_users[i]
            _clicks, _batch_features = self.__collect_feedback(clicks, i)

            discount_coef = [(1 / (math.log(1 + j, rankings.shape[1]))) for j in range(1, len(rankings[0]) + 1)]
            if self.processing_type == 'feature_weight':
                discount_coef_reward = [1. / math.log(1+j,rankings.shape[1]) for j in range(1, len(_clicks) + 1)]
            elif self.processing_type == 'feature_weight_reverse':
                discount_coef_reward = [math.log(1+j, rankings.shape[1]) for j in range(1, len(_clicks) + 1)]
            discount_coef_penalization = [self.gamma * 1. / (math.log(1+j,rankings.shape[1])) for j in range(1, len(_clicks) + 1)]

            if self.processing_type == 'recommended_discountfactor':
                self.exp_recommended[user][np.array(rankings[0])] += discount_coef
            elif self.processing_type == 'examined_discountfactor':
                if len(clicks) == 0:
                    self.exp_examined[user][np.array(rankings[0])] += discount_coef
                else:
                    self.exp_examined[user][np.array(rankings[0][:len(clicks)])] += discount_coef[:len(clicks)]

            """
            Algorithm 2 of WWW 2010

            Return: self.theta is updated.
            """
            z = _batch_features[:, :self.topic_dim]
            x = _batch_features[:, self.topic_dim:]
            if self.processing_type == 'item_weight':
                x, z = self.update_item_weight_xz(rankings[0], x, z, _clicks, discount_coef_penalization, discount_coef_reward,user, user_round)

            BA = np.matmul(self.B[user].T, self.A_x_inv[user])
            self.A_z[user] += np.matmul(BA, self.B[user])
            self.b_z[user] += np.dot(BA, self.b_x[user])

            self.A_x[user] += np.dot(x.T, x)
            self.B[user] += np.dot(x.T, z)

            if self.processing_type == 'feature_weight' or self.processing_type == 'feature_weight_reverse':
                self.update_feature_x_weight(x, _clicks, discount_coef_penalization, discount_coef_reward, user, user_round)
            else:
                self.b_x[user] += np.dot(_clicks, x)

            try:
                self.A_x_inv[user] = np.linalg.inv(self.A_x[user])
            except:
                self.A_x_inv[user] = np.linalg.pinv(self.A_x[user])

            BA = np.matmul(self.B[user].T, self.A_x_inv[user])
            self.A_z[user] += np.dot(z.T, z) - np.matmul(BA, self.B[user])

            if self.processing_type == 'feature_weight' or self.processing_type == 'feature_weight_reverse':
                self.update_feature_z_weight(z, _clicks, discount_coef_penalization, discount_coef_reward, user, user_round, BA)
            else:
                self.b_z[user] += np.dot(_clicks, z) - np.dot(BA, self.b_x[user])

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
        elif self.config.feedback_model == 'eacascade':
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
            scores = []
            user = batch_users[i]
            # for CB
            BA_X = np.matmul(self.B[user].T, self.A_x_inv[user])  # B.T  A_x^-1
            ABA = np.matmul(self.A_z_inv[user], BA_X)  # A_z^-1 B.T A_X^-1
            ABABA = np.matmul(BA_X.T, ABA)

            # score and cb for the relevance
            x = self.dataObj.feature_data['train_item_latent_features']
            if self.processing_type == 'item_weight':
                x = self.item_coef[user].reshape(self.dataObj.n_items, 1) * x
            score_x = np.dot(x, self.theta[user])
            XAX = np.multiply(np.dot(x, self.A_x_inv[user]), x).sum(axis=1)  # x^T A_X^-1 X^T
            cb_x = np.multiply(np.dot(x, ABABA), x).sum(axis=1) + XAX
            ucb_x = score_x + 1e-6 * tie_breaker
            ABAX = np.dot(ABA, x.T).T
            # score and cb for the topic
            # delta_t = []
            batch_features = []
            coverage = np.zeros(self.topic_dim)
            ranking = []
            cbs = []
            # ranking_set = set()
            for j in range(self.config.list_size):
                # Line 8 - 11 of Nips 11
                z_t = self.conditional_coverage(x=self.dataObj.feature_data['train_item_topical_features'], coverage=coverage)
                z = z_t
                if self.processing_type == 'item_weight':
                    z = self.item_coef[user].reshape(self.dataObj.n_items, 1) * z
                ZAZ = np.multiply(np.dot(z, self.A_z_inv[user]), z).sum(axis=1)  # Z^T A_Z^-1 Z^T
                # cb_z = ZAZ - 2 * np.multiply(np.dot(z_t, ABA), x).sum(axis=1)
                cb_z = ZAZ - 2 * np.multiply(z, ABAX).sum(axis=1)

                if self.processing_type == 'recommended_discountfactor':
                    cb = self.alpha * (1 - (self.exp_recommended[user] / (round + 1))) * np.sqrt(cb_z + cb_x)
                elif self.processing_type == 'examined_discountfactor':
                    cb = self.alpha * (1 - (self.exp_examined[user] / (round + 1))) * np.sqrt(cb_z + cb_x)
                else:
                    cb = self.alpha * np.sqrt(cb_z + cb_x)
                score_z = np.dot(z, self.beta[i])
                ucb = ucb_x + score_z + cb

                winner = np.argmax(ucb)
                while winner in ranking:
                    ucb[winner] = -np.inf
                    winner = np.argmax(ucb)

                ranking.append(winner)
                # ranking_set.add(winner)
                batch_features.append(z_t[winner])

                scores.append(ucb[winner])
                cbs.append(cb[winner])

                coverage = self.ranking_coverage(self.dataObj.feature_data['train_item_topical_features'][ranking])

            if self.processing_type == "EARS":
                rankings[i] = np.asarray(self.shuffling_topK(ranking, scores, self.config.list_size))
            else:
                rankings[i] = np.asarray(ranking)
            self.batch_features[i][:, :self.topic_dim] = np.asarray(batch_features)
            self.batch_features[i][:, self.topic_dim:] = self.dataObj.feature_data['train_item_latent_features'][rankings[i]]
            self.writeCB(round + i, user, cbs)
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

    def update_feature_x_weight(self, _batch_features, _clicks, discount_coef_penalization, discount_coef_reward, user, user_round):
        clicked_items_index = np.where(_clicks == 1)[0]
        _x = _batch_features
        if len(clicked_items_index) == 0:
            _x = -np.multiply(np.array(discount_coef_penalization).reshape(len(_clicks), 1), _x)
        else:
            previous_clicked_item_index = 0
            for clicked_item_index in clicked_items_index:
                current_clicked_item_index = clicked_item_index
                _x[current_clicked_item_index, :] = discount_coef_reward[current_clicked_item_index] * _x[current_clicked_item_index,:]
                _x[previous_clicked_item_index: current_clicked_item_index, :] = -np.multiply(np.array(discount_coef_penalization[previous_clicked_item_index: current_clicked_item_index]).reshape(current_clicked_item_index - previous_clicked_item_index, 1), _x[previous_clicked_item_index: current_clicked_item_index,:])
                previous_clicked_item_index = current_clicked_item_index + 1
        self.click_history_x[user] += _x.sum(axis=0)
        if user_round[user] % self.window == 0:
            self.b_x[user] = self.click_history_x[user] / self.window
            self.click_history_x[user] = np.zeros(self.latent_dim)
        else:
            self.b_x[user] += np.dot(_clicks, _batch_features)
    def update_feature_z_weight(self, _batch_features, _clicks, discount_coef_penalization, discount_coef_reward, user, user_round, _BA):
        clicked_items_index = np.where(_clicks == 1)[0]
        _z = _batch_features
        if len(clicked_items_index) == 0:
            _z = -np.multiply(np.array(discount_coef_penalization).reshape(len(_clicks), 1), _z)
        else:
            previous_clicked_item_index = 0
            for clicked_item_index in clicked_items_index:
                current_clicked_item_index = clicked_item_index
                _z[current_clicked_item_index, :] = discount_coef_reward[current_clicked_item_index] * _z[current_clicked_item_index,:]
                _z[previous_clicked_item_index: current_clicked_item_index, :] = -np.multiply(np.array(discount_coef_penalization[previous_clicked_item_index: current_clicked_item_index]).reshape(current_clicked_item_index - previous_clicked_item_index, 1), _z[previous_clicked_item_index: current_clicked_item_index,:])
                previous_clicked_item_index = current_clicked_item_index + 1
        self.click_history_z[user] += _z.sum(axis=0)
        if user_round[user] % self.window == 0:
            self.b_z[user] = (self.click_history_z[user] / self.window) - np.dot(_BA, self.b_x[user])
            self.click_history_z[user] = np.zeros(self.topic_dim)
        else:
            self.b_z[user] += np.dot(_clicks, _batch_features) - np.dot(_BA, self.b_x[user])
    def update_item_weight_xz(self, rankings, _batch_features_x, _batch_features_z, _clicks, discount_coef_penalization, discount_coef_reward,user, user_round):
        clicked_items_index = np.where(_clicks == 1)[0]
        _x = _batch_features_x
        _z = _batch_features_z
        if len(clicked_items_index) == 0:
            self.item_coef[user][rankings] += -np.array(discount_coef_penalization)
            _x = self.item_coef[user][rankings][:len(_clicks)].reshape(len(_clicks), 1) * _x
            _z = self.item_coef[user][rankings][:len(_clicks)].reshape(len(_clicks), 1) * _z
        else:
            previous_clicked_item_index = 0
            for clicked_item_index in clicked_items_index:
                current_clicked_item_index = clicked_item_index
                self.item_coef[user][rankings[current_clicked_item_index]] += discount_coef_reward[current_clicked_item_index]
                _x[current_clicked_item_index, :] = self.item_coef[user][rankings[current_clicked_item_index]] * _x[current_clicked_item_index,:]
                _z[current_clicked_item_index, :] = self.item_coef[user][rankings[current_clicked_item_index]] * _z[current_clicked_item_index,:]
                if current_clicked_item_index != previous_clicked_item_index:
                    self.item_coef[user][rankings[previous_clicked_item_index:current_clicked_item_index]] += -np.array(discount_coef_penalization[previous_clicked_item_index:current_clicked_item_index])
                    _x[previous_clicked_item_index:current_clicked_item_index, :] = self.item_coef[user][rankings[previous_clicked_item_index:current_clicked_item_index]].reshape(current_clicked_item_index - previous_clicked_item_index, 1) * _x[previous_clicked_item_index: current_clicked_item_index,:]
                    _z[previous_clicked_item_index:current_clicked_item_index, :] = self.item_coef[user][rankings[previous_clicked_item_index:current_clicked_item_index]].reshape(current_clicked_item_index - previous_clicked_item_index, 1) * _z[previous_clicked_item_index: current_clicked_item_index,:]
                previous_clicked_item_index = current_clicked_item_index + 1
        if user_round[user] % self.window == 0:
            return _x, _z
        else:
            return _batch_features_x, _batch_features_z