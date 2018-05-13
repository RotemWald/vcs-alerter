from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from tagger.tagger_ml_based import message_translator
from tagger.tagger_ml_based.bag_of_words_creator import BagOfWordsCreator
from tagger.tagger_ml_based import dictionary_handler
import pandas as pd
import numpy as np
import pickle
import util

RANDOM_FOREST_MODEL_FILE_PATH = util.PATH_TO_RESOURCES+"random_forest.txt"
KNN_MODEL_FILE_PATH = util.PATH_TO_RESOURCES+"knn.txt"
SVC_MODEL_FILE_PATH = util.PATH_TO_RESOURCES+"svc.txt"
NB_FILE_PATH = util.PATH_TO_RESOURCES+"nb.txt"
REGRESSION_MODEL_FILE_PATH = util.PATH_TO_RESOURCES+"regression.txt"

MESSAGE_COL_NAME = 'Message'
TAG_COL_NAME = 'Tag'
# here you should enter all the files you want to use to train the models
ALL_FILES_PATH = [util.PATH_TO_RESOURCES+"asaf.xlsx", util.PATH_TO_RESOURCES+"avia.xlsx",
                  util.PATH_TO_RESOURCES+"ety.xlsx", util.PATH_TO_RESOURCES+"galit.xlsx",
                  util.PATH_TO_RESOURCES+"nurit.xlsx"]
TRAIN_RATIO = 0.8
TRANSLATOR = message_translator.MessageTranslator()


def get_all_messages_and_tags_from_file(file_path):
    message_list = []
    tag_list = []

    df_from_file = pd.read_excel(file_path)
    for index, row in df_from_file.iterrows():
        message_text = row[MESSAGE_COL_NAME]
        tag = row[TAG_COL_NAME]

        if util.check_if_expression_is_in_hebrew(message_text) and tag is not np.nan:
            message_list.append(str(message_text))
            tag_list.append(str(tag))

    return message_list, tag_list


def get_all_messages_and_tags_from_all_files():
    message_list = []
    tag_list = []

    for file_path in ALL_FILES_PATH:
        (message_list_from_file, tag_list_from_file) = get_all_messages_and_tags_from_file(file_path)
        message_list.extend(message_list_from_file)
        tag_list.extend(tag_list_from_file)

    return message_list, tag_list


def pickle_model(model, path):
    with open(path, "wb") as fd:
        pickle.dump(model, fd)


def unpickle_model(path):
    with open(path, "rb") as fd:
        return pickle.load(fd)


(all_messages, all_tags) = get_all_messages_and_tags_from_all_files()
tags_as_df = pd.DataFrame({'Tag': np.array(all_tags)})
tags_as_df = np.ravel(tags_as_df)
cleaned_messages = util.preprocess_messages(all_messages, TRANSLATOR)
dictionary_handler.create_dictionary_for_bag_of_words(cleaned_messages, 1000)

bag_of_words_creator = BagOfWordsCreator()
train_data_features = bag_of_words_creator.create_bag_of_words_from_msgs_list(cleaned_messages)

forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit(train_data_features, tags_as_df)
pickle_model(forest, RANDOM_FOREST_MODEL_FILE_PATH)

knn = KNeighborsClassifier(n_neighbors = 13, weights = 'uniform')
knn = knn.fit(train_data_features, tags_as_df)
pickle_model(knn, KNN_MODEL_FILE_PATH)

svc = svm.SVC(gamma = 0.001, C = 100, degree = 3)
svc = svc.fit(train_data_features, tags_as_df)
pickle_model(svc, SVC_MODEL_FILE_PATH)

regression = LogisticRegression()
regression = regression.fit(train_data_features, tags_as_df)
pickle_model(regression, REGRESSION_MODEL_FILE_PATH)

nb = GaussianNB()
nb = nb.fit(train_data_features, tags_as_df)
pickle_model(nb, NB_FILE_PATH)
