from copy import deepcopy

from Automata.Transition import Transition
from Automata.Automata import Automata


def minimize(automata: Automata) -> Automata:
    min_states, min_final = _removeUnrecheable(automata)

    automata.all_states = min_states
    automata.final_states = min_final

    states, final = _removeDead(automata)
    automata.all_states = states
    automata.final_states = final

    equivalent_classes = _create_equiv_classes(automata)

    min_automata = _create_min_automata(automata, equivalent_classes)

    return min_automata


def _removeUnrecheable(automata: Automata):
    min_transitions = set()
    queue = [automata.initial_state]
    visited = []

    while len(queue) > 0:
        current = queue.pop(0)[0]
        visited.append(current)

        reachable = set()
        transitions = set()

        for transition in automata.transitions:
            if transition.initial_state == current:
                reachable.add(transition.target_state[0])
                transitions.add(transition)

        for current in reachable:
            if current not in queue and current not in visited:
                queue.append(current)

        min_transitions |= transitions

    min_states = sorted(list(set(visited) & set(automata.all_states)))
    min_final = sorted(list(set(visited) & set(automata.final_states)))

    return (min_states, min_final)


def _removeDead(automata: Automata) -> Automata:
    queue = list(automata.final_states)
    visited = []

    min_transitions = set(automata.transitions)

    while len(queue) > 0:
        state = queue.pop(0)[0]
        visited.append(state)

        valid = set()
        transitions = set()
        for t in automata.transitions:
            if t.target_state[0] == state:
                valid.add(t.initial_state)
                transitions.add(t)

        for state in valid:
            if not state in visited and not state in queue:
                queue.append(state)

        min_transitions |= transitions

    min_states = sorted(list(set(visited) & set(automata.all_states)))
    min_final = sorted(list(set(visited) & set(automata.final_states)))

    return (min_states, min_final)


def _create_equiv_classes(automata: Automata):
    current_equiv_classes = set()
    current_equiv_classes.add(frozenset(s for s in automata.final_states))
    current_equiv_classes.add(
        frozenset(
            filter(
                lambda x: x not in automata.final_states,
                [s for s in automata.all_states],
            )
        )
    )

    last_equiv_classes = deepcopy(current_equiv_classes)

    while True:
        for symbol in automata.alphabet:
            new_equiv_classes = set()

            for equiv_class in current_equiv_classes:
                current = set()

                aux = {}
                for eq in current_equiv_classes:
                    aux[eq] = set()
                aux["d"] = set()

                for state in equiv_class:
                    target = automata.get_targets_with_state_symbol(
                        state=[state], symbol=symbol
                    )

                    if target:
                        target = target[0]
                    ins = False

                    if target and target in equiv_class:
                        current.add(state)
                        ins = True
                    else:
                        for k in aux:
                            if target and target in k:
                                aux[k].add(state)
                                ins = True

                    if not ins:
                        aux["d"].add(state)

                new_set = set()
                if current:
                    new_set.add(frozenset(current))

                for s in aux.values():
                    if s:
                        new_set.add(frozenset(s))

                new_equiv_classes |= new_set

            current_equiv_classes = new_equiv_classes

        if (
            len(current_equiv_classes) == len(automata.all_states)
            or last_equiv_classes == current_equiv_classes
        ):
            break

        last_equiv_classes = current_equiv_classes

    return current_equiv_classes


def _create_min_automata(automata: Automata, equiv_classes: set) -> Automata:
    name_transpose = dict()

    equiv_classes = list(equiv_classes)
    for eq_class in [sorted(list(e)) for e in equiv_classes]:
        if len(eq_class) > 1:
            name_transpose[str(eq_class)] = eq_class[0]
        else:
            name_transpose[eq_class[0]] = eq_class[0]

    new_transitions = []
    inserted = []
    for transition in automata.transitions:
        src = _get_transpose_name(name_transpose, transition.initial_state)
        symbol = transition.symbol
        target = _get_transpose_name(name_transpose, transition.target_state)

        if [src, symbol, target] not in inserted and src != "0" and target is not None:
            new_transitions.append(Transition(src, symbol, target))
            inserted.append([src, symbol, target])

    new_states = set()
    for t in new_transitions:
        new_states.add(t.initial_state)
        new_states.add(t.target_state)

    finals = set()
    for t in new_states:
        if t in automata.final_states:
            finals.add(t)
    finals = sorted(list(finals))

    new_automata = Automata(
        states_number=len(new_states),
        initial_state=_get_transpose_name(name_transpose, automata.initial_state),
        final_states=finals,
        alphabet=automata.alphabet,
        transitions=new_transitions,
        all_states=new_states,
    )

    return new_automata


def _get_transpose_name(transpose_dict: dict, name: str):
    for k in transpose_dict.keys():
        if name[0] in k:
            return transpose_dict[k]
