def add_base_url(
    url: str,
    URL_BASE: str = "https://storage.googleapis.com/theolex_documents_processing",
) -> str:
    try:
        if "https://" in url:
            return url
        url = url if url[0] == "/" else "/" + url
        return URL_BASE + url

    except Exception as e:
        # print(e)
        return ""
    return url


def replace_originial_to_text(url: str) -> str:
    """ """

    try:
        return url.replace("/original/", "/text/")
    except Exception as e:
        return ""


def replace_pdf_to_txt(url: str) -> str:
    """ """

    try:
        return url.replace(".pdf", ".txt")
    except Exception as e:
        return ""


def clean_url(url: str) -> str:
    """ """

    url = add_base_url(url)
    url = replace_originial_to_text(url)
    url = replace_pdf_to_txt(url)

    return url