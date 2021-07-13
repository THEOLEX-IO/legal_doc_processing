from legal_doc_processing import logger
from legal_doc_processing._legal_doc import LegalDoc
from legal_doc_processing._press_release import PressRelease
from legal_doc_processing.base import (
    Base,
)


class Decision(Base):
    def __init__(
        self,
        press_release_text: str,
        legal_doc_text: str,
        source,
        nlpipe=None,
        nlspa=None,
    ):

        Base.__init__(
            self,
            text="",
            obj_name="Decision",
            source=source,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )

        self.legal_doc = LegalDoc(
            legal_doc_text,
            source=source,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )
        self.press_release = PressRelease(
            press_release_text,
            source=source,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )

    ######################

    def predict(self, feature) -> str:
        """ """

        if feature == "all":
            return self.predict_all()

        if feature in self.feature_list:
            # try:
            self.press_release.predict(feature)
            self.legal_doc.predict(feature)
            val = self._predict[feature](
                self.press_release._feature_dict, self.legal_doc._feature_dict
            )
            setattr(self, "_" + feature, val)
            return val
            # except:
            #     return "--Error--"
        return "--Unknowned feature--"

    def predict_all(self) -> str:
        """return self.predict("all") """

        for feature in self.feature_list:

            self.press_release.predict_all()
            self.legal_doc.predict_all()

            setattr(
                self,
                "_" + feature,
                self._predict[feature](self.press_release.data, self.legal_doc.data),
            )


class _Decision:
    Decision = Decision


# def from_file(press_release, legal_doc, nlpipe=None, nlspa=None):

#     nlpipe = nlpipe if nlpipe else get_pipeline()
#     nlspa = nlspa if nlspa else get_spacy()
#     try:
#         nlspa.add_pipe("sentencizer")
#     except Exception as e:
#         pass

#     press_release_text = ""
#     try:
#         with open(press_release, "r") as f:
#             press_release_text = f.read()
#     except Exception as e:
#         print(e.__str__())

#     legal_doc_text = ""
#     try:
#         with open(legal_doc, "r") as f:
#             legal_doc_text = f.read()
#     except Exception as e:
#         print(e.__str__())

#     if legal_doc_text and press_release_text:
#         return Decision(
#             press_release_text,
#             legal_doc_text,
#             press_release_file_path=press_release,
#             legal_doc_file_path=legal_doc,
#             nlpipe=nlpipe,
#             nlspa=nlspa,
#         )
#     elif legal_doc_text and (not press_release_text):
#         return LegalDoc(
#             legal_doc_text,
#             file_path=legal_doc,
#             nlpipe=nlpipe,
#             nlspa=nlspa,
#         )
#     elif (not legal_doc_text) and press_release_text:
#         return PressRelease(
#             press_release_text,
#             file_path=press_release,
#             nlpipe=nlpipe,
#             nlspa=nlspa,
#         )
#     else:
#         raise NotImplementedError("something went wrong mother fucker :) ")


# def from_text(press_release, legal_doc, nlpipe=None, nlspa=None):

#     nlpipe = nlpipe if nlpipe else get_pipeline()
#     nlspa = nlspa if nlspa else get_spacy()
#     try:
#         nlspa.add_pipe("sentencizer")
#     except Exception as e:
#         pass

#     if legal_doc and press_release:
#         return Decision(
#             press_release,
#             legal_doc,
#             press_release_file_path=press_release,
#             legal_doc_file_path=legal_doc,
#             nlpipe=nlpipe,
#             nlspa=nlspa,
#         )
#     elif legal_doc and (not press_release):
#         return LegalDoc(
#             legal_doc,
#             nlpipe=nlpipe,
#             nlspa=nlspa,
#         )
#     elif (not legal_doc) and press_release:
#         return PressRelease(
#             press_release,
#             nlpipe=nlpipe,
#             nlspa=nlspa,
#         )
#     else:
#         raise NotImplementedError("something went wrong mother fucker :) ")


# if __name__ == "__main__":

#     # import
#     import time
#     from legal_doc_processing.utils import get_pipeline, get_spacy
#     from legal_doc_processing.decision.utils import decision_X_y

#     # load
#     nlpipe = get_pipeline()
#     nlspa = get_spacy()
#     nlspa.add_pipe("sentencizer")

#     # legal_doc df AND  OBj
#     df = decision_X_y()
#     df = df.iloc[:, :]
#     # df["obj"] = df.txt.apply(lambda i: LegalDoc(i, nlpipe=nlpipe, nlspa=nlspa))

#     # clean
#     df["press_txt"] = df.press_txt.fillna("")
#     df["legal_txt"] = df.legal_txt.fillna("")

#     _dec = lambda i, j: Decision(i, j, nlpipe=nlpipe, nlspa=nlspa)
#     df["ds"] = [_dec(i, j) for i, j in zip(df.press_txt.values, df.legal_txt.values)]

#     # preds
#     t = time.time()
#     # 28 objects --> 181 secondes so --> +/-10 secondes per objects
#     df["pred_defendant"] = df.ds.apply(lambda i: i.predict("defendant"))
#     t = time.time() - t

#     #     # labels
#     #     preds_labels = list(df.preds.iloc[0].keys())
#     #     for k in preds_labels:
#     #         df["pred_" + k] = df.preds.apply(lambda i: i[k])

#     # 1st one
#     one = df.iloc[0, :]
#     one_ob = obj = self = one.ds