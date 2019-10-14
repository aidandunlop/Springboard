import sklearn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from collections import defaultdict
from sklearn.externals import joblib
import psycopg2
import numpy as np
import os
import logging


def talks_df_from_db(year=None):
    DATABASE_URI = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(DATABASE_URI)
    logging.debug('reading db')
    if year:
        return pd.read_sql_query(
            f"SELECT * FROM Talk Where year ='{year}';", conn)
    return pd.read_sql_query("SELECT * FROM Talk", conn)


def vectorize_talk_text(text_df):
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # TODO add nltk feature engg
    return vectorizer.fit_transform(text_df)


class ModelWrapper:
    def __init__(
            self,
            talks_df,
            model_file,
            vectorized_text_labeled,
            vectorized_text_predict,):
        self.talks_df = talks_df
        self.model_file = model_file
        self.vectorized_text_labeled = vectorized_text_labeled
        self.vectorized_text_predict = vectorized_text_predict
        self.user_model_dict = defaultdict()
        self.count_labeled = self.vectorized_text_labeled.shape[0]
        self._unpickle_model()

    def _pickle_model(self):
        with open(self.model_file, 'wb') as f:
            joblib.dump(self.user_model_dict, f)

    def _unpickle_model(self):
        try:
            with open(self.model_file, 'rb') as f:
                self.user_model_dict = joblib.load(f)

        except Exception as e:
            print('No model yet')

    def train(self, user_id, labeled_talk_ids):
        labels = np.zeros(self.count_labeled)
        indexes = [x-1 for x in labeled_talk_ids]
        labels[indexes] = 1

        X_train, X_test, y_train, y_test = train_test_split(
            self.vectorized_text_labeled, labels, test_size=self.count_labeled // 3)

        classifier = LinearSVC()
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        self.check_model(y_test, y_pred)
        return classifier

    @staticmethod
    def check_model(y_train, y_test):
        report = sklearn.metrics.classification_report(y_train, y_test)
        print(report)

    def predict(self, user_id, labeled_talk_ids):
        classifier = None
        if self.user_model_dict:
            classifier, prev_labeled_talk_ids = self.user_model_dict.get(user_id, (None, []))
        if classifier is None or prev_labeled_talk_ids != labeled_talk_ids:
            classifier = self.train(user_id, labeled_talk_ids)
            self.user_model_dict[user_id] = classifier, labeled_talk_ids
            self._pickle_model()

        predicted_talks_vector = classifier.predict(self.vectorized_text_predict)
        df = talks_df_from_db(year=2018)
        predicted_talks_indexes = np.array(predicted_talks_vector).nonzero()[0].tolist()
        print(len(predicted_talks_indexes))
        return df.loc[predicted_talks_indexes][['id', 'description', 'presenters', 'title', 'location']].to_dict('records')
