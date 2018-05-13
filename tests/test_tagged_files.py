from tagger.tagger_rule_based import file_tagger
import util
import pandas as pd
import numpy as np


class FileTaggerTest:
    def __init__(self):
        self.file_tagger = file_tagger.FileTagger()

    def test_file(self, file_name):
        self.file_tagger.tag_file_into_file(file_name, util.PATH_TO_RESOURCES+'test.xlsx')
        df_from_file = pd.read_excel(util.PATH_TO_RESOURCES+'test.xlsx')

        count_rows = 0
        count_matches = 0

        for index, row in df_from_file.iterrows():
            message_text = row[file_tagger.MESSAGE_COL_NAME]
            predicted_tag = row[file_tagger.PREDICTED_TAG_COL_NAME]
            real_tag = row[file_tagger.REAL_TAG_COL_NAME]

            if util.check_if_expression_is_in_hebrew(message_text) and real_tag is not np.nan:
                count_rows += 1
                if predicted_tag == real_tag:
                    count_matches += 1

        print('The success rate for file {0} is: {1}%'.format(file_name, str(count_matches/count_rows * 100)))


if __name__ == '__main__':
    file_tagger_test = FileTaggerTest()

    # logs from 29.09
    file_tagger_test.test_file(util.PATH_TO_RESOURCES + 'asaf.xlsx')
    file_tagger_test.test_file(util.PATH_TO_RESOURCES + 'avia.xlsx')
    file_tagger_test.test_file(util.PATH_TO_RESOURCES + 'ety.xlsx')
    file_tagger_test.test_file(util.PATH_TO_RESOURCES + 'galit.xlsx')
    file_tagger_test.test_file(util.PATH_TO_RESOURCES + 'nurit.xlsx')
