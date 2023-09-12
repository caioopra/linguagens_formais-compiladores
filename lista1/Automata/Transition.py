class Transition:
    def __init__(self, initial_state: str, symbol: str, target_state: str):
        self.__initial_state = initial_state
        self.__symbol = symbol
        self.__target_state = target_state

    def __str__(self) -> str:
        return f"<({self.initial_state}, {self.symbol}) -> {self.target_state}>"

    @property
    def initial_state(self) -> str:
        return self.__initial_state

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def target_state(self) -> str:
        return self.__target_state
