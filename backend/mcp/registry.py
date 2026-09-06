class MCPRegistry:

    def __init__(self):

        self.tools = {}

    def register(
        self,
        name,
        tool,
    ):

        self.tools[name] = tool

    def get(self, name):

        return self.tools.get(name)

    def list_tools(self):

        return list(self.tools.keys())