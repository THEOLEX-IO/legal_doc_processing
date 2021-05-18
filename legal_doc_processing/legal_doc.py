class LegalDoc:
    """main class of our project"""

    def __init__(self, path):
        """init method """

        self.path = path

        with open(path) as f:
            self.raw_text = f.read()

    def _clean(self):
        """first text cleaning based on regex """

        # article text
        article_text = re.sub(r"\[[0-9]*\]", " ", file)
        self.article_text = re.sub(r"\s+", " ", article_text)

        # formated text
        formatted_article_text = re.sub("[^a-zA-Z]", " ", article_text)
        self.formatted_article_text = re.sub(r"\s+", " ", formatted_article_text)
