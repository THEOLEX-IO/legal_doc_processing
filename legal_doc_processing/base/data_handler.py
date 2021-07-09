class DataHandler:
    def __init__(self, obj):

        # pipe spacy
        self.nlpipe = obj.nlpipe
        self.nlspa = obj.nlspa
        # feature
        self._feature_dict = obj._feature_dict
        self.feature_dict = obj.feature_dict
        # text
        self.source = obj.source
        self.raw_text = obj.raw_text
        self.date = obj.date
        self.h1 = obj.h1
        self.content = obj.content
        self.abstract = obj.abstract
        # sents
        self.h1_sents = obj.h1_sents
        self.abstract_sents = obj.abstract_sents
        self.content_sents = obj.content_sents
        # entities
        self.pers_h1 = obj.pers_h1
        self.pers_abstract = obj.pers_abstract
        self.org_h1 = obj.org_h1
        self.org_abstract = obj.org_abstract
        self.date_h1 = obj.date_h1
        self.date_abstract = obj.date_abstract
        self.cost_h1 = obj.cost_h1
        self.cost_abstract = obj.cost_abstract
        self.pers_all = obj.pers_all
        self.org_all = obj.org_all
        self.pers_org_all = obj.pers_org_all
        self.date_all = obj.date_all
        self.cost_all = obj.cost_all