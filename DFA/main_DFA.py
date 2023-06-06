import DFA as dfa
try:
    d = dfa.load_sections()
    sigma = dfa.load_sigma()
    states = dfa.load_states()
    actions = dfa.load_actions()
    dfaE = [sigma, states[0], states[1], states[2], actions]
    input_string = input("Introduceti string-ul cu spatii intre simboluri.\n").split(' ')
    print(dfa.emulate_dfa(dfaE, input_string))
except RuntimeError as err:
    print(err)
except Exception as err:
    print(repr(err))