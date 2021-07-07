import os
from pprint import pformat, pprint

from legal_doc_processing import logger
from legal_doc_processing.press_release.structure import (
    clean_in_line_break,
    do_strip,
    split_intro_article,
    find_id_line_in_intro,
    find_date_line_in_intro,
    clean_very_short_lines,
)


def structure_press_release(txt):

    dd = {
        "id": "--ERROR--",
        "date": "--ERROR--",
        "h1": "--ERROR--",
        "article": "--ERROR--",
        "end": "--ERROR--",
        "error": 0,
    }

    try:

        # clean double breaks and fake lines
        new_txt_1 = clean_in_line_break(txt)

        # strip
        new_txt_2 = do_strip(new_txt_1)

        # intro article
        intro, article = split_intro_article(new_txt_2)

        # idx id and date
        idx_id_line = find_id_line_in_intro(intro)
        idx_date_line = find_date_line_in_intro(intro)

        # split extract
        intro_lines = intro.splitlines()
        if idx_id_line != -1:
            dd["id"] = intro_lines[idx_id_line]

        if idx_date_line != -1:
            dd["date"] = intro_lines[idx_date_line]

        # h1
        intro_lines[idx_id_line] = ""
        intro_lines[idx_date_line] = ""

        intro_intermediate = "\n".join(intro_lines)
        dd["h1"] = clean_very_short_lines(intro_intermediate)

        # article and end
        split_article = article.split("\n\n")
        dd["article"] = "\n\n".join(split_article[:-2])
        dd["end"] = "\n\n".join(split_article[-2:])
    except Exception as e:
        logger.error(e)
        dd["error"] = e

    return dd