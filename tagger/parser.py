# importing libraries
import requests
import string
import util
from tagger import speller

# consts
NEW_SENTENCE = 'sent_id'
REAL_WORD_LOC = 1
BASE_WORD_LOC = 2
DEP_LOC = 7


class TagParser:
    def __init__(self):
        # api-endpoint
        self.URL = "http://lindat.mff.cuni.cz/services/udpipe/api/process"
        self.speller = speller.Speller()

    def parse_text(self, data):
        # defining a params dict for the parameters to be sent to the API
        params = {'data': data, 'model': 'hebrew-ud-2.0-170801', 'tokenizer': True, 'tagger': True, 'parser': True}

        # sending get request and saving the response as response object
        r = requests.get(url=self.URL, params=params)

        # extracting data in json format
        data = r.json()

        # parse data
        result = data['result']
        result_in_list = result.split('\n')
        ans = []
        for i in range(0, len(result_in_list)):
            if result_in_list[i].find(NEW_SENTENCE) != -1:
                i = i + 2  # to get into the parsed sentence
                sentence = {}
                while i < len(result_in_list):
                    words = result_in_list[i].split('\t')
                    if words[0] == '\n' or words[0] == '':
                        ans.append(sentence)
                        break
                    if words[REAL_WORD_LOC] not in string.punctuation:
                        word_to_clean = util.remove_punctuation_from_str(str(words[REAL_WORD_LOC]))
                        cleaned_word_to_add = self.speller.get_base_word(word_to_clean)

                        util.add_word_and_context_to_dict(sentence, str(words[DEP_LOC]), cleaned_word_to_add)
                    i = i + 1

        return ans
