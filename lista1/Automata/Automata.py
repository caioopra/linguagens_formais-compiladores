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

        self.initial_state = initial_state
        if not isinstance(initial_state, list):
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
        self._determ_transitions = {}

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

        new_initial = set()
        for t in self.initial_state:
            for ts in self._eps_closure[t]:
                new_initial.add(ts)
        new_initial = sorted(list(new_initial))

        states_queue = [new_initial]
        visited_list = [new_initial]

        self.alphabet = list(filter(lambda x: x != "&", self.alphabet))

        while len(states_queue):
            state = states_queue.pop(0)

            for symbol in self.alphabet:
                target_states = self._get_targets_with_state_sybmol(
                    state=state, symbol=symbol
                )
                transitions_closure = set()

                for target in target_states:
                    for t in self._eps_closure[target]:
                        transitions_closure.add(t)

                transitions_closure = list(sorted(transitions_closure))
                if not state in visited_list:
                    visited_list.append(state)

                if (
                    transitions_closure != []
                    and transitions_closure not in visited_list
                    and transitions_closure not in states_queue
                ):
                    states_queue.append(transitions_closure)

                self._add_to_new_states(state, symbol, transitions_closure)

        return self._create_new_automata(str(new_initial))

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
        states = set()
        for s in state:
            for transition in self.transitions:
                if transition.symbol == symbol and transition.initial_state == s:
                    for t in transition.target_state:
                        states.add(t)

        return sorted(list(states))

    def _add_to_new_states(self, state, symbol, transitions):
        state = str(state)
        if state not in self._determ_transitions.keys():
            self._determ_transitions[state] = {symbol: transitions}
            return

        self._determ_transitions[state][symbol] = transitions

    def _create_new_automata(self, new_initial):
        states = set()
        transitions = []
        final_states = set()

        for new_state, data in self._determ_transitions.items():
            states.add(new_state)

            clear_state = list(filter(lambda x: x.isalpha(), new_state))
            for symbol in self.alphabet:
                target = data[symbol]

                t = Transition(clear_state, symbol, target)
                if t not in transitions:
                    transitions.append(t)

                if target != []:
                    states.add(str(target))

                for s in clear_state:
                    if s in self.final_states:
                        final_states.add(str(clear_state))

                for s in target:
                    if s in self.final_states:
                        final_states.add(str(target))

        states = sorted(list(states))
        new_states = sorted([list(filter(lambda x: x.isalpha(), s)) for s in states])

        final_states = sorted(list(final_states))
        final_states = sorted(
            [list(filter(lambda x: x.isalpha(), s)) for s in final_states]
        )

        return Automata(
            states_number=len(states),
            initial_state=list(filter(lambda x: x.isalpha(), new_initial)),
            final_states=final_states,
            alphabet=self.alphabet,
            transitions=transitions,
            all_states=new_states,
        )
