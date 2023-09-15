from utils.InputParser import parseInput

from Automata.Automata import Automata


TEST1 = "3;A;{C};{1,2,3,&};A,1,A;A,&,B;B,2,B;B,&,C;C,3,C"
states_number, initial_state, final_states, alphabet, transitions, all_states = parseInput(TEST1)
print(states_number)
print(initial_state)
print(final_states)
print(alphabet)

print("Transitions: ")
for transition in transitions:
    print(transition)

print(all_states)

automata = Automata(
    states_number=int(states_number), 
    initial_state=initial_state,
    final_states=final_states,
    alphabet=alphabet,
    transitions=transitions,
    all_states=all_states
)

automata.convertToDFA()
