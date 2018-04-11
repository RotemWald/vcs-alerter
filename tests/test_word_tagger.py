import unittest
from tagger import word_tagger as wt
from message_tag import MessageTag


class WordTaggerTest(unittest.TestCase):
    word_tagger = wt.WordTagger()

    def test_tag_word(self):
        word1 = "ריבוע"
        word2 = "חתול"
        word3 = "ארנק"
        word4 = "מאונך"
        word5 = "פתרון"
        word6 = "התשובה"
        word7 = "אלכסון"
        word8 = "שליטה"
        word9 = "כדורגל"
        word10 = "כדור"

        assert self.__class__.word_tagger.tag_word(word1) is MessageTag.MAT, "ERROR"
        assert self.__class__.word_tagger.tag_word(word2) is MessageTag.NMD, "ERROR"
        assert self.__class__.word_tagger.tag_word(word3) is MessageTag.NMD, "ERROR"
        assert self.__class__.word_tagger.tag_word(word4) is MessageTag.MAT, "ERROR"
        assert self.__class__.word_tagger.tag_word(word5) is MessageTag.MAT, "ERROR"
        assert self.__class__.word_tagger.tag_word(word6) is MessageTag.MAT, "ERROR"
        assert self.__class__.word_tagger.tag_word(word7) is MessageTag.MAT, "ERROR"
        assert self.__class__.word_tagger.tag_word(word8) is MessageTag.TEC, "ERROR"
        assert self.__class__.word_tagger.tag_word(word9) is MessageTag.NMD, "ERROR"
        assert self.__class__.word_tagger.tag_word(word10) is MessageTag.MAT, "ERROR"


if __name__ == '__main__':
    unittest.main()
