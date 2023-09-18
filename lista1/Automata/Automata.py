from Automata.Transition import Transition


class Automata:
    def __init__(
        self,
        states_number: int,
        initial_state: str,
        final_states: list[str],
        alphabet: list[str],
        transitions: list[Transition],
        all_states: list[str],
    ):
        self.states_number = states_number
        self.initial_state = [initial_state]
        self.final_states = final_states
        self.alphabet = alphabet
        self.transitions = transitions
        self.all_states = all_states

        self._has_epsilon: bool = (
            True
            if any([transition.symbol == "&" for transition in self.transitions])
            else False
        )
        self._eps_closure = {}

    def printItself(self):
        print("[AUTOMATA] Number of states:", self.states_number)
        print("[AUTOMATA] All states:", self.all_states)
        print("[AUTOMATA] Initial state:", self.initial_state)
        print("[AUTOMATA] Final states:", self.final_states)
        print("[AUTOMATA] Alphabet:", self.alphabet)
        print("[AUTOMATA] Transitions:")
        for transition in self.transitions:
            print("    ", transition)

    def convertToDFA(self):
        if self._has_epsilon:
            self._create_epsilon_closure()
        else:
            self._create_determ_table()  # also in self._eps_closure

        print("eps_closure", self._eps_closure)

        states_queue = [self.initial_state]
        visited_list = []
        new_transitions = {}

        for state in states_queue:
            for symbol in self.alphabet:
                target_states = self._get_targets_with_state_sybmol(
                    state=state, symbol=symbol
                )
                transitions_closure = set()

                for target in target_states:
                    for t in self._eps_closure[target]:
                        transitions_closure.add(t)
                print(f"{state} - {symbol}: ", transitions_closure)
                

    def _create_epsilon_closure(self) -> set:
        for state in self.all_states:
            closure = set(state)
            self._eps_closure[state] = self._search_eps_closure(
                closure, state, self._get_states_with("&")
            )

    def _search_eps_closure(
        self, closure: set, state: str, transitions: list[Transition]
    ):
        for transition in transitions:
            if state == transition.initial_state:
                closure.add(*transition.target_state)

                for target in transition.target_state:
                    return self._search_eps_closure(closure, target, transitions)

        return closure

    def _get_states_with(self, symbol: str):
        states = set()
        for transition in self.transitions:
            if transition.symbol == symbol:
                if transition.target_state:
                    states.add(transition)

        return states

    def _create_determ_table(self) -> list:
        closure = {}
        for state in self.all_states:
            closure[state] = {state}

        self._eps_closure = closure

    def _get_targets_with_state_sybmol(self, state: str, symbol: str):
        for s in state:
            for transition in self.transitions:
                if transition.symbol == symbol and transition.initial_state == s:
                    return transition.target_state

