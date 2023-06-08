import NFA
import convert_NFA_to_DFA

try:
    d = NFA.load_sections()
    sigma = NFA.load_sigma()
    states = NFA.load_states()
    actions = NFA.load_actions()
    nfa = [sigma, states[0], states[1], states[2], actions]
    print(f"NFA: \nSigma: {sigma}\nMultime stari: {states[0]}\nStare initiala: {states[1]}\nMultime stari finale: {states[2]}\nTranzitii: ")
    for t in actions:
        print(t)
    dfa = convert_NFA_to_DFA.convertNFAtoDFA(nfa)
    print(
        f"DFA: \nSigma: {dfa[0]}\nMultime stari: {dfa[1]}\nStare initiala: {dfa[2]}\nMultime stari finale: {dfa[3]}\nTranzitii: ")
    for t in dfa[4]:
        print(t)

    # input_string = input("Introduceti string-ul cu spatii intre simboluri.\n").split(' ')
    # print(NFA.emulate_nfa(nfaE, input_string))
except RuntimeError as err:
    print(err)
except Exception as err:
    print(repr(err))

