class Transition:
    def __init__(
        self, initial_state: str = None, symbol: str = None, target_state: list = None
    ):
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

    @initial_state.setter
    def initial_state(self, value) -> None:
        self.__initial_state = value

    @symbol.setter
    def symbol(self, value) -> None:
        self.__symbol = value

    @target_state.setter
    def target_state(self, value) -> None:
        self.__target_state = value

    def getInitialState(self) -> list:
        if isinstance(list, self.initial_state):
            return self.initial_state

        return [self.initial_state]

