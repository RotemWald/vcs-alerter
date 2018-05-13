from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from tagger.tagger_ml_based import message_translator
from tagger.tagger_ml_based.bag_of_words_creator import BagOfWordsCreator
from tagger.tagger_ml_based import dictionary_handler
from tagger.tagger_ml_based import model_creator_script
import pandas as pd
import numpy as np
import util

TRAIN_RATIO = 0.8
TRANSLATOR = message_translator.MessageTranslator()


(all_messages, all_tags) = model_creator_script.get_all_messages_and_tags_from_all_files()
tags_as_df = pd.DataFrame({'Tag': np.array(all_tags)})
cleaned_messages = util.preprocess_messages(all_messages, TRANSLATOR)
dictionary_handler.create_dictionary_for_bag_of_words(cleaned_messages, 1000)

bag_of_words_creator = BagOfWordsCreator()
train_data_features = bag_of_words_creator.create_bag_of_words_from_msgs_list(cleaned_messages)

msk = np.random.rand(len(train_data_features)) < TRAIN_RATIO
train_x = train_data_features[msk]
test_x = train_data_features[~msk]
train_y = tags_as_df.loc[msk, 'Tag']
test_y = tags_as_df.loc[~msk, 'Tag']

forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit(train_x, train_y)

# Evaluate accuracy best on the test set
random_forest = forest.score(test_x, test_y)

print('random_forest='+str(random_forest))

knn = KNeighborsClassifier(n_neighbors = 13, weights = 'uniform')
knn = knn.fit(train_x, train_y)

# Evaluate accuracy best on the test set
k_near_neighbur = knn.score(test_x, test_y)

print('k_near_neighbur'+str(k_near_neighbur))

svc = svm.SVC(gamma = 0.001, C = 100, degree = 3)
svc = svc.fit(train_x, train_y)

# Evaluate accuracy best on the test set
support_vector = svc.score(test_x,test_y)

print('support_vector='+str(support_vector))

regression = LogisticRegression()
regression = regression.fit(train_x, train_y)

# Evaluate accuracy best on the test set
regression_logistic = regression.score(test_x, test_y)

print('regression_logistic='+str(regression_logistic))

nb = GaussianNB()
nb = nb.fit(train_x, train_y)

# Evaluate accuracy best on the test set
naive_bayes = nb.score(test_x,test_y)

print('naive_bayes='+str(naive_bayes))
