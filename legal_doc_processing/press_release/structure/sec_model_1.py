def split_intro_article_1(txt: str, n=30) -> str:
    """ """

    txt_lines_30 = txt.splitlines()[:n]

    s0, s1, s2 = ("Washington D", "Washington, D", "Washington,D")
    is_in = lambda j: any([(j.startswith(s.lower())) for s in [s0, s1, s2]])
    idx_cands = [i for i, j in enumerate(txt_lines_30) if is_in(j.lower())]

    if not len(idx_cands):
        s = "washington"
        idx_cands = [i for i, j in enumerate(txt_lines_30) if j.lower().startswith(s)]

    idx = idx_cands[0]

    txt_lines = txt.splitlines()
    intro_lines, article_lines = txt_lines[:idx], txt_lines[idx:]

    intro, article = "\n".join(intro_lines), "\n".join(article_lines)

    return intro, article


def extract_id_1(intro: str) -> tuple:
    """ """
