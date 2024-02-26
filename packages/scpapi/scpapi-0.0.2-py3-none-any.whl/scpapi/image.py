from . import Client


class StandardImage(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, query: dict = None):
        self.set_method("GET")
        self.set_path('/image/v2/standard-images')
        return self.invoke(query=query)
