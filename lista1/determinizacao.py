from utils.InputParser import parseInput

from Automata.Automata import Automata


TEST1 = "3;A;{C};{1,2,3,&};A,1,A;A,&,B;B,2,B;B,&,C;C,3,C"
TEST2 = "4;A;{D};{a,b};A,a,A;A,a,B;A,b,A;B,b,C;C,b,D"
TEST3 = "4;P;{S};{0,1};P,0,P;P,0,Q;P,1,P;Q,0,R;Q,1,R;R,0,S;S,0,S;S,1,S"
states_number, initial_state, final_states, alphabet, transitions, all_states = parseInput(TEST1)

automata = Automata(
    states_number=states_number, 
    initial_state=initial_state,
    final_states=final_states,
    alphabet=alphabet,
    transitions=transitions,
    all_states=all_states
)

automata.printItself()
automata.convertToDFA()


