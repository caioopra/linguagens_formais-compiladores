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
        
        self._has_epsilon = True if any([transition.symbol == "&" for transition in self.transitions]) else False 

    def printItself(self):
        print("[AUTOMATA] Number of states: ", self.states_number)
        print("[AUTOMATA] Initial state: ", self.initial_state)
        print("[AUTOMATA] Final states: ", self.final_states)
        print("[AUTOMATA] Alphabet: ", self.alphabet)
        print("[AUTOMATA] Transitions: ")
        for transition in self.transitions:
            print("[AUTOMATA] ", transition)
        print("[AUTOMATA] All states: ", self.all_states)

    def convertToDFA(self):
        if self._has_epsilon:
            closure = self._create_epsilon_closure()
        else:
            transitions = self._create_transitions()
    
    def _create_epsilon_closure(self) -> set:
        ...

    def _create_transitions(self) -> list:
        transitions = {}
        for transition in self.transitions:
            ...
