class Option:
    def __init__(self, value, *args) -> None:
        self.value = value
        self.args = args
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __eq__(self, value: object) -> bool:
        return self.value == value
