import pandas as pd
import util
from tagger import parser, sentence_tagger

PREDICTED_TAG_COL_NAME = 'predicted_tag'
REAL_TAG_COL_NAME = 'Tag'
SUBJECT_COL_NAME = 'subject'
ROOT_COL_NAME = 'root'
OBJECT_COL_NAME = 'object'
MESSAGE_COL_NAME = 'Message'


class FileTagger:
    def __init__(self):
        self.tag_parser = parser.TagParser()
        self.sentence_tagger = sentence_tagger.SentenceTagger()

    def tag_file_into_file(self, file_to_tag, file_to_write):
        df_from_file = pd.read_excel(file_to_tag)
        df_from_file[SUBJECT_COL_NAME] = ""
        df_from_file[ROOT_COL_NAME] = ""
        df_from_file[OBJECT_COL_NAME] = ""
        df_from_file[PREDICTED_TAG_COL_NAME] = ""

        for index, row in df_from_file.iterrows():
                message_text = row[MESSAGE_COL_NAME]
                if util.check_if_expression_is_in_hebrew(message_text):
                    parsed_message = self.tag_parser.parse_text(message_text)
                    message_tag = self.sentence_tagger.tag_sentence(message_text)

                    subj_list = util.get_all_values_by_key(parsed_message, 'nsubj')
                    root_list = util.get_all_values_by_key(parsed_message, 'root')
                    obj_list = util.get_all_values_by_key(parsed_message, 'obj')

                    df_from_file.set_value(index=index, col=SUBJECT_COL_NAME, value=util.create_string_from_list(subj_list))
                    df_from_file.set_value(index=index, col=ROOT_COL_NAME, value=util.create_string_from_list(root_list))
                    df_from_file.set_value(index=index, col=OBJECT_COL_NAME, value=util.create_string_from_list(obj_list))
                    df_from_file.set_value(index=index, col=PREDICTED_TAG_COL_NAME, value=message_tag.value)

        writer = pd.ExcelWriter(file_to_write)
        df_from_file.to_excel(writer,'Sheet1')
        writer.save()
