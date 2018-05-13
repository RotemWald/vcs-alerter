from tagger.sentence_tagger_interface import SentenceTagger
from tagger.tagger_ml_based import model_creator_script
from tagger.tagger_ml_based.bag_of_words_creator import BagOfWordsCreator
from tagger.tagger_ml_based.message_translator import MessageTranslator
import pandas as pd
from collections import Counter
import util


class SentenceTagger(SentenceTagger):
    def __init__(self):
        self.rf_model = model_creator_script.unpickle_model(model_creator_script.RANDOM_FOREST_MODEL_FILE_PATH)
        self.knn_model = model_creator_script.unpickle_model(model_creator_script.KNN_MODEL_FILE_PATH)
        self.svc_model = model_creator_script.unpickle_model(model_creator_script.SVC_MODEL_FILE_PATH)
        self.nb_model = model_creator_script.unpickle_model(model_creator_script.NB_FILE_PATH)
        self.regression_model = model_creator_script.unpickle_model(model_creator_script.REGRESSION_MODEL_FILE_PATH)
        self.bag_of_words = BagOfWordsCreator()
        self.translator = MessageTranslator()

    def tag_sentence(self, sentence):
        cleaned_sentence = util.preprocess_message(sentence, self.translator)
        sentence_in_bag_of_words = self.bag_of_words.create_bag_of_words_from_msg(cleaned_sentence)
        return self.majority_vote(sentence_in_bag_of_words)

    def majority_vote(self, sentence_in_bag_of_words):
        rf_predicted_tag = self.rf_model.predict(pd.DataFrame(data=[sentence_in_bag_of_words]))
        knn_predicted_tag = self.knn_model.predict(pd.DataFrame(data=[sentence_in_bag_of_words]))
        svc_predicted_tag = self.svc_model.predict(pd.DataFrame(data=[sentence_in_bag_of_words]))
        nb_predicted_tag = self.nb_model.predict(pd.DataFrame(data=[sentence_in_bag_of_words]))
        regression_predicted_tag = self.regression_model.predict(pd.DataFrame(data=[sentence_in_bag_of_words]))

        predicted_tags_list = [rf_predicted_tag[0], knn_predicted_tag[0],
                               svc_predicted_tag[0], nb_predicted_tag[0],
                               regression_predicted_tag[0]]

        # count appearances of each element in the list
        c = Counter(predicted_tags_list)
        return c.most_common(1)[0][0]


if __name__ == '__main__':
    st = SentenceTagger()
    print(st.tag_sentence("הכל נמחק לי"))
    print(st.tag_sentence("נראלי שזה מעוין כי האלכסונים שוים זה לזה ומאונכים זה לזה"))
    print(st.tag_sentence("חתולים הלכו לטייל"))
    print(st.tag_sentence("המחשב שלי נתקע"))
    print(st.tag_sentence("נראלי שזה מעוין כי האלכסונים שוים זה לזה ומאונכים זה לזה"))
    print(st.tag_sentence("2 חתולים הלכו לטייל"))
    print(st.tag_sentence("המחשב שלי נתקע"))
    print(st.tag_sentence("נראלי שזה מעוין כי האלכסונים שוים זה לזה ומאונכים זה לזה"))
    print(st.tag_sentence("2 חתולים הלכו לטייל"))
    print(st.tag_sentence("המחשב שלי נתקע"))
    print(st.tag_sentence("נראלי שזה מעוין כי האלכסונים שוים זה לזה ומאונכים זה לזה"))
    print(st.tag_sentence("2 חתולים הלכו לטייל"))
