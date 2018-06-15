from googletrans import Translator


class MessageTranslator:
    def __init__(self):
        self.translator = Translator()

    def translate_message(self, msg):
        return self.translator.translate(msg).text
