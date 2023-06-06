import NFA

try:
    d = NFA.load_sections()
    sigma = NFA.load_sigma()
    states = NFA.load_states()
    actions = NFA.load_actions()
    nfaE = [sigma, states[0], states[1], states[2], actions]
    input_string = input("Introduceti string-ul cu spatii intre simboluri.\n").split(' ')
    print(NFA.emulate_nfa(nfaE, input_string))
except RuntimeError as err:
    print(err)
except Exception as err:
    print(repr(err))

