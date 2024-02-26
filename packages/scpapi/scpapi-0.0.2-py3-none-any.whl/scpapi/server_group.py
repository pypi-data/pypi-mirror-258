from . import Client


class ServerGroup(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, query: dict = None):
        self.set_method("GET")
        self.set_path('/server-group/v2/server-groups')
        return self.invoke(query=query)

    def detail(self, server_group_id: str):
        self.set_method("GET")
        self.set_path('/server-group/v2/server-groups/{serverGroupId}'.format(serverGroupId=server_group_id))
        return self.invoke()

    def create(self, body: dict = None):
        self.set_method("POST")
        self.set_path('/server-group/v2/server-groups')
        return self.invoke(body=body)

    def delete(self, server_group_id: str):
        self.set_method("DELETE")
        self.set_path('/server-group/v2/server-groups/{serverGroupId}'.format(serverGroupId=server_group_id))
        return self.invoke()
