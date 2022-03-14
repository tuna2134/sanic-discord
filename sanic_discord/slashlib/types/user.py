class User:
    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        return self._data["id"]

    @property
    def name(self):
        return self._data["username"]

    @property
    def discriminator(self):
        return self._data["discriminator"]

    @property
    def avatar(self):
        return self._data["avatar"]
