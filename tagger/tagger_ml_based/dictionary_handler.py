import util
import pickle

dict_path = util.PATH_TO_RESOURCES + "words_vocabulary.txt"


# Clean the message from all chars that are not letters, than stem each msg, and creates dict from those
# steamed messages by word popularity.
def create_dictionary_for_bag_of_words(cleaned_message_list, dict_max_size):
    word_appearances_dict = {}
    for msg in cleaned_message_list:
        for word in msg.split():
            if word in word_appearances_dict:
                word_appearances_dict[word] += 1
            else:
                word_appearances_dict[word] = 1

    words_in_dict_sorted = sorted(word_appearances_dict, key=word_appearances_dict.__getitem__, reverse=True)
    words_set = set()
    for i in range(dict_max_size):
        if i < len(words_in_dict_sorted):
            words_set.add(words_in_dict_sorted[i])

    with open(dict_path, "wb") as dp:
        pickle.dump(words_set, dp)


# This function can be called only after create_dictionary_for_bag_of_words has been called.
# returns set of words in dict.
def load_dictionary_from_file():
    with open(dict_path, "rb") as dp:
        return pickle.load(dp)
