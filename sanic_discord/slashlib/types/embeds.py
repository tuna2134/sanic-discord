class Embed:
    def __init__(self, *, title=None, description=None):
        self.payload = {}
        if title is not None:
            self.payload["title"] = title
        if description is not None:
            self.payload["description"] = description
