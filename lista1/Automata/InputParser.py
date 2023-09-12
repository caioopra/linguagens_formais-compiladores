# 4;A;{D};{a,b};A,a,A;A,a,B;A,b,A;B,b,C;C,b,D
# 3;A;{C};{1,2,3,&};A,1,A;A,&,B;B,2,B;B,&,C;C,3,C
from Automata.Transition import Transition

def parseInput(inputStr: str):
    states_number, initial_state, final_states, alphabet, *transitions = inputStr.split(
        ";"
    )

    final_states = clearString(final_states)
    alphabet = clearString(alphabet)
    transitions = createTransitions(transitions)

    return states_number, initial_state, final_states, alphabet, transitions


def clearString(rawString: str) -> list[str]:
    buffer = []
    for string in rawString:
        if string != "{" and string != "}" and string != ",":
            buffer.append(string)
    return buffer


def createTransitions(transitions: list[str]) -> list[tuple]:
    buffer = []
    for transition in transitions:
        init, symb, final = transition.split(",")
        buffer.append(Transition(init, symb, final))

    return buffer
