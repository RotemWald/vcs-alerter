import util
from message_tag import MessageTag


class WordTagger:
    def __init__(self):
        self.PlurarShapes = open(util.PATH_TO_RESOURCES+'dictionaries/PlurarShape.txt', 'r', encoding="utf8").read().split('\n')
        self.Shapes = open(util.PATH_TO_RESOURCES+'dictionaries/ShapesTerms.txt', 'r', encoding="utf8").read().split('\n')
        self.geo = open(util.PATH_TO_RESOURCES+'dictionaries/GeometryTerms.txt', 'r', encoding="utf8").read().split('\n')
        self.claim = open(util.PATH_TO_RESOURCES+'dictionaries/ClaimTerms.txt', 'r', encoding="utf8").read().split('\n')
        self.conclusion = open(util.PATH_TO_RESOURCES + 'dictionaries/ConclusionTerms.txt', 'r', encoding="utf8").read().split('\n')
        self.context = open(util.PATH_TO_RESOURCES + 'dictionaries/ContextTerms.txt', 'r', encoding="utf8").read().split('\n')
        self.structure = open(util.PATH_TO_RESOURCES + 'dictionaries/TaskStructure.txt', 'r',encoding="utf8").read().split('\n')

        self.software = open(util.PATH_TO_RESOURCES+'dictionaries/SoftwareUsage.txt', 'r', encoding="utf8").read().split('\n')
        self.tech = open(util.PATH_TO_RESOURCES+'dictionaries/TechTerms.txt', 'r', encoding="utf8").read().split('\n')
        self.negTech = open(util.PATH_TO_RESOURCES+'dictionaries/NegativeTechTerms.txt', 'r', encoding="utf8").read().split('\n')

        self.answer = open(util.PATH_TO_RESOURCES+'dictionaries/AnswerTerms.txt', 'r', encoding="utf8").read().split('\n')
        
        self.MATWordSet = set()
        self.TECWordSet = set()

        util.init_dict_in_set(self.MATWordSet, self.PlurarShapes)
        util.init_dict_in_set(self.MATWordSet, self.Shapes)
        util.init_dict_in_set(self.MATWordSet, self.geo)
        util.init_dict_in_set(self.MATWordSet, self.claim)
        util.init_dict_in_set(self.MATWordSet, self.conclusion)
        util.init_dict_in_set(self.MATWordSet, self.context)
        util.init_dict_in_set(self.MATWordSet, self.structure)
        util.init_dict_in_set(self.MATWordSet, self.answer)  # meant for DS

        util.init_dict_in_set(self.TECWordSet, self.software)
        util.init_dict_in_set(self.TECWordSet, self.tech)
        util.init_dict_in_set(self.TECWordSet, self.negTech)

    def tag_word(self, word):
        if word in self.MATWordSet:
            return MessageTag.MAT
        elif word in self.TECWordSet:
            return MessageTag.TEC
        else:
            return MessageTag.NMD
