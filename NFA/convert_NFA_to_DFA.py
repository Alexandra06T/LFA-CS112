powerset = []
def powerSet(states_set, res ,n):
    global powerset
    if n == 0:
        cpyres = []
        cpyres.extend(res)
        powerset.append(cpyres)
        print(powerset)
    else:
        res.append(states_set[n-1])
        powerSet(states_set, res, n - 1)
        res.pop()
        powerSet(states_set, res, n - 1)


def convertNFAtoDFA(nfa):
    # preluam componentele nfa ului
    sigma_nfa = nfa[0]
    states_nfa = nfa[1]
    start_state_nfa = nfa[2]
    final_states_nfa = nfa[3]
    actions_nfa = nfa[4]

    # stabilim componentele dfa ului: dfa ul va fi o lista ce va contine [alfabetul, starile, starea de start, starile finale, tranzitiile]

    # alfabetul este acelasi
    sigma_dfa = sigma_nfa
    print(sigma_dfa)

    # starile dfa ului = power set (starile nfa ului)
    global powerset
    powerset = []
    res = []
    powerSet(states_nfa, res, len(states_nfa))
    states_dfa = powerset
    print(states_dfa)

    # stabilim starea de start
    start_state_dfa = [start_state_nfa]
    for state in start_state_dfa:
        for t in actions_nfa:
            if t[0] == state and t[1] == '*':
                print(t[2])
                start_state_dfa.append(t[2])
    print(start_state_dfa)

    # stabilim starile de final
    final_states_dfa = []
    for s in states_dfa:
        for f in final_states_nfa:
            if f in s:
                final_states_dfa.append(s)
    print(final_states_dfa)

    # stabilim tranzitiile
    actions_dfa = []
    for R in states_dfa:
        for symbol in sigma_dfa:
            lista = []
            # starile la care se ajunge prin simbol
            for r in R:
                for action in actions_nfa:
                    if action[0] == r and action[1] == symbol and action[2] not in lista:
                        lista.append(action[2])

            # starile la care se ajunge prin epsilon
            for stare in lista:
                for action in actions_nfa:
                    if action[0] == stare and action[1] == '*' and action[2] not in lista:
                        lista.append(action[2])

            # am gasit tranzitia, o adaugam la lista dfa ului
            if not lista:
                actions_dfa.append((R, symbol, []))
            else:
                actions_dfa.append((R, symbol, lista))

    return [sigma_dfa, states_dfa, start_state_dfa, final_states_dfa, actions_dfa]

# eliminare stari inutile, minimizare