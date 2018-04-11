from __future__ import unicode_literals
import HspellPy

ANSWER_ELEMENT_LOCATION = 0
BASE_WORD_LOCATION = 1


class Speller:
    def __init__(self):
        self.speller = HspellPy.Hspell(linguistics=True)

    def get_correct_word(self, word):
        ans_list = self.speller.try_correct(word)

        if not ans_list:
            return word
        else:
            return ans_list[ANSWER_ELEMENT_LOCATION]

    def get_base_word(self, word):
        ans_list = self.speller.enum_splits(word)

        if not ans_list:
            return word
        else:
            return ans_list[ANSWER_ELEMENT_LOCATION][BASE_WORD_LOCATION]
