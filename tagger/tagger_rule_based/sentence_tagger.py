from tagger.tagger_rule_based import parser, word_tagger
import util
from message_tag import MessageTag
from tagger.sentence_tagger_interface import SentenceTagger


class SentenceTagger(SentenceTagger):
    def __init__(self):
        self.parser = parser.TagParser()
        self.word_tagger = word_tagger.WordTagger()

    def tag_sentence(self, sentence):
        if util.check_if_expression_is_in_hebrew(sentence):
            parsed_message = self.parser.parse_text(sentence)

            subj_list = util.get_all_values_by_key(parsed_message, 'nsubj')
            root_list = util.get_all_values_by_key(parsed_message, 'root')
            obj_list = util.get_all_values_by_key(parsed_message, 'obj')

            tagged_list = self.tag_all_words(obj_list, root_list, subj_list)

            return self.tag_sentence_from_tagged_list(tagged_list)

    def tag_sentence_from_tagged_list(self, tagged_list):
        mat_count = 0
        tc_count = 0
        for tag in tagged_list:
            if tag is MessageTag.MAT:
                mat_count += 1
            elif tag is MessageTag.TEC:
                tc_count += 1
        if mat_count is 0 and tc_count is 0:
            return MessageTag.NMD
        return MessageTag.MAT if mat_count > tc_count else MessageTag.TEC

    def tag_all_words(self, obj_list, root_list, subj_list):
        tagged_list = []
        for word in subj_list:
            tagged_list.append(self.word_tagger.tag_word(word))
        for word in root_list:
            tagged_list.append(self.word_tagger.tag_word(word))
        for word in obj_list:
            tagged_list.append(self.word_tagger.tag_word(word))
        return tagged_list
