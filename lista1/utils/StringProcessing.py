from Automata.Transition import Transition
from Automata.Automata import Automata

def parseInput(inputStr: str):
    states_number, initial_state, final_states, alphabet, *transitions = inputStr.split(
        ";"
    )

    final_states = _clearString(final_states)
    alphabet = _clearString(alphabet)
    all_states = sorted(list(_getAllStates(transitions)))
    transitions = _createTransitions(transitions, alphabet, all_states)

    return (
        int(states_number),
        initial_state,
        final_states,
        alphabet,
        transitions,
        all_states,
    )


def _clearString(rawString: str) -> list[str]:
    buffer = []
    for string in rawString:
        if string != "{" and string != "}" and string != ",":
            buffer.append(string)
    return buffer


def _createTransitions(
    transitions: list[str], alphabet: list[str], all_states
) -> list[tuple]:
    new_transitions = {}

    for transition in transitions:
        initial, _, _ = transition.split(",")

        tran = {}
        for symbol in alphabet:
            tran[symbol] = []

        new_transitions[initial] = tran

    for transition in transitions:
        initial, symb, target = transition.split(",")
        new_transitions[initial][symb].append(target)

    for state in all_states:
        if state not in new_transitions.keys():
            tran = {}
            for symb in alphabet:
                tran[symb] = []
            new_transitions[state] = tran

    transitions = []
    for transition_name, transition in new_transitions.items():
        for k, v in transition.items():
            transitions.append(Transition(transition_name, k, v))

    return transitions


def _getAllStates(transitions: list[Transition]) -> list[str]:
    states = set()
    for transition in transitions:
        init, _, final = transition.split(",")
        states.add(init)
        states.add(final)

    return states


def dfaToString(automata: Automata) -> str:
    result = ""
    
    result += f"{automata.states_number};"
    
    # initial state
    result += "{"
    for s in automata.initial_state:
        result += s
    result += "};"
    
    # final states
    result += "{"
    result += ",".join(["".join(final) for final in automata.final_states])
    result += "};"
    
    print(result)
    