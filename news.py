

class Article:
    def __init__(self, title, url, source):
        self.title = title
        self.url = url
        if source == "guardian":
            self.source = "Guardian"
        elif source == "thetimes":
            self.source = "Times"
        elif source == "nyt":
            self.source = "NYT"
        elif source == "telegraph":
            self.source = "Telegraph"
        elif source == "cityam":
            self.source = "City A.M."

    def __str__(self):
        return self.title
