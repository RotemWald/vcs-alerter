import unittest
from tagger.tagger_ml_based import sentence_tagger as st
from message_tag import MessageTag


class SentenceTaggerTest(unittest.TestCase):
    sentence_tagger = st.SentenceTagger()

    def no_test_1(self):
        self.__class__.sentence_tagger.tag_sentence("המחשב נתקע לי")


if __name__ == '__main__':
    unittest.main()
