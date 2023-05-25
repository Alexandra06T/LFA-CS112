import PDA

d = PDA.load_sections()
sigma = PDA.load_sigma()
if sigma == False:
    print('sigma', False)
else:
    states = PDA.load_states()
    if states == False:
        print('states', False)
    else:
        gama = PDA.load_gamma()
        if gama == False:
            print('gama',False)
        else:
            actions = PDA.load_actions()
            if actions == False:
                print('actions',False)
            else:
                pda = [sigma, states[0], states[1], states[2], gama, actions]
                input_string = input().split(' ')
                print(PDA.emulate_pda(pda, input_string))
