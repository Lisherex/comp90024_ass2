class Config:
    def __init__(self, isConfig: bool = True, namespace: str = "default") -> None:
        self.namespace = namespace if namespace else "default"
        self.type = "configs" if isConfig else "secrets"

    def __call__(self, name, k):
        path = f"/{self.type}/{self.namespace}/{name}/{k}"
        with open(path) as f:
            return f.read()