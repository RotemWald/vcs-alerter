from abc import ABCMeta, abstractmethod


class SentenceTagger:
    __metaclass__ = ABCMeta

    @abstractmethod
    def tag_sentence(self): raise NotImplementedError
