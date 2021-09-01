import requests


def get_text(url: str) -> str:
    """  """

    # print(url)
    if (not url) or (not isinstance(url, str)):
        # print("not_url")
        return ""
    try:
        res = requests.get(url)
        # print(res)
        txt = res.text
        print(txt[:30].replace("\n", "..."))
        return txt
    except Exception as e:
        # print(str(e) + "\n")
        return ""
    return ""