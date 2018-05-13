from tagger.tagger_ml_based import dictionary_handler as dh
import pandas as pd


class BagOfWordsCreator:
    def __init__(self):
        self.vocabulary = dh.load_dictionary_from_file()
        self.words_location_dict = self.get_words_location_dict()

    def create_bag_of_words_from_msgs_list(self, msgs_list):
        bag_of_words_from_msgs_list = []
        for msg in msgs_list:
            bag_of_words_from_msgs_list.append(self.create_bag_of_words_from_msg(msg))

        return pd.DataFrame(bag_of_words_from_msgs_list)

    def create_bag_of_words_from_msg(self, msg):
        bag_of_word = [0] * len(self.vocabulary)
        for word in msg.split():
            if word in self.words_location_dict:
                location = self.words_location_dict[word]
                bag_of_word[location] += 1

        return bag_of_word

    def get_words_location_dict(self):
        words_location_dict = {}
        i = 0
        for word in self.vocabulary:
            words_location_dict[word] = i
            i += 1

        return words_location_dict
