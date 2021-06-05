from legal_doc_processing.utils import get_pipeline


def _if_not_pipe(nlpipe):

    return get_pipeline() if not nlpipe else nlpipe


def _ask(txt: str, quest: str, nlpipe, topk: int = 3) -> list:

    nlpipe = _if_not_pipe(nlpipe)

    return nlpipe(question=quest, context=txt, topk=3)
