from collections import deque, defaultdict

from Automata.Transition import Transition


class Automata:
    def __init__(
        self,
        states_number: int,
        initial_state: str,
        final_states: list[str],
        alphabet: list[str],
        transitions: list[Transition],
        all_states: list[str]
    ):
        self.states_number = states_number
        self.initial_state = initial_state
        self.final_states = final_states
        self.alphabet = alphabet
        self.transitions = transitions
        self.all_states = all_states
        
    def convertToDFA(self):
        epsilon_transitions = [] 
        determ_transitions = {}

        for transition in self.transitions:
            if transition.symbol == "&":
                epsilon_transitions.append(transition)

        print("Epsilon: ", self._create_epsilon_closure(epsilon_transitions)) 
    
    def _create_epsilon_closure(self, epsilon_transitions) -> set:
        closure = set(self.initial_state)
        stack = list(self.all_states)

        while stack:
            state = stack.pop()

            if state in epsilon_transitions:
                for epsilon_target in epsilon_transitions[state.initial_state]:
                    if epsilon_target not in closure:
                        closure.add(epsilon_target)
                        stack.append(epsilon_target)

        return closure
