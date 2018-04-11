import unittest
from tagger import sentence_tagger as st
from message_tag import MessageTag


class SentenceTaggerTest(unittest.TestCase):
    sentence_tagger = st.SentenceTagger()

    def test_tag_sentence_from_tagged_list(self):
        tagged_list1 = [MessageTag.MAT]
        tagged_list2 = [MessageTag.NMD]
        tagged_list4 = [MessageTag.TEC]

        assert self.__class__.sentence_tagger.tag_sentence_from_tagged_list(tagged_list1) is MessageTag.MAT, "ERROR"
        assert self.__class__.sentence_tagger.tag_sentence_from_tagged_list(tagged_list2) is MessageTag.NMD, "ERROR"
        assert self.__class__.sentence_tagger.tag_sentence_from_tagged_list(tagged_list4) is MessageTag.TEC, "ERROR"

    def test_tag_sentence_from_tagged_list_tec_complex(self):
        tagged_list1 = [MessageTag.TEC, MessageTag.TEC, MessageTag.MAT]
        tagged_list2 = [MessageTag.MAT, MessageTag.TEC]

        assert self.__class__.sentence_tagger.tag_sentence_from_tagged_list(tagged_list1) is MessageTag.TEC, "ERROR"
        assert self.__class__.sentence_tagger.tag_sentence_from_tagged_list(tagged_list2) is MessageTag.TEC, "ERROR"

    def test_tag_sentence_from_tagged_list_mat_complex(self):
        tagged_list1 = [MessageTag.MAT, MessageTag.MAT, MessageTag.NMD, MessageTag.TEC]
        tagged_list2 = [MessageTag.MAT, MessageTag.NMD]

        assert self.__class__.sentence_tagger.tag_sentence_from_tagged_list(tagged_list1) is MessageTag.MAT, "ERROR"
        assert self.__class__.sentence_tagger.tag_sentence_from_tagged_list(tagged_list2) is MessageTag.MAT, "ERROR"

    def test_tag_sentence_from_tagged_list_nmd_complex(self):
        tagged_list1 = [MessageTag.NMD, MessageTag.NMD]
        tagged_list2 = [MessageTag.NMD, MessageTag.NMD, MessageTag.NMD, MessageTag.TEC]

        assert self.__class__.sentence_tagger.tag_sentence_from_tagged_list(tagged_list1) is MessageTag.NMD, "ERROR"
        assert self.__class__.sentence_tagger.tag_sentence_from_tagged_list(tagged_list2) is not MessageTag.NMD, "ERROR"


if __name__ == '__main__':
    unittest.main()
