import re

def load_sections():
    # d - dictionar nume_sectiune:continut_sectiune
    d = {}
    with open("config_file_PDA_1") as f:
        for line in f:
            line = line.replace('\n','')
            try:
                if line[0] == '[':
                    nume = line[1:-1] # numele sectiunii
                    d[nume] = [] # incepem o noua sectiune
                elif line[0] != '#': # daca linia nu este un comentariu
                    d[nume].append(line) # adaugam linia la ultima sectiune deschisa
            except:
                pass # daca lina este goala
    return d

def load_sigma():
    d = load_sections()
    # daca alfabetul este vid, eroare, altfel returnam lista ce contine alfabetul
    if d["Sigma"] == []:
        return False
    print(d["Sigma"])
    return d["Sigma"]

def load_states():
    d = load_sections()
    lista_stari = []
    # contorizam starile initiale si pe cele finale
    nr_start = 0
    nr_final = 0
    ls_stari_finale = []
    # pentru fiecare element din alfabet cream un tuplu (nume_stare, tip stare); 0 - stare interna, 1 - stare initiala, 2 - stare finala
    for element in d["States"]:
        if element != '':
            lsaux = element.split(',')
            lista_stari.append(lsaux[0])
            for el in lsaux[1:]:
                if el == 'S':
                    nr_start += 1
                    stare_init = lsaux[0]
                elif el == 'F':
                    nr_final += 1
                    ls_stari_finale.append(lsaux[0])
    # daca starile initiale sunt mai multe decat cate una sau nu exista, eroare, daca starile finale nu exista, eroare
    if nr_start != 1 or nr_final < 1:
        return False
    # daca nu exista stari, eroare
    if lista_stari == []:
        return False
    print(lista_stari, stare_init, ls_stari_finale)
    return lista_stari,stare_init,ls_stari_finale

def load_gamma():
    d = load_sections()
    # daca alfabetul stack-ului este vid, eroare, altfel returnam lista ce contine alfabetul
    if d["Gama"] == []:
        return False
    print(d["Gama"])
    return d["Gama"]


def load_actions():
    d = load_sections()
    lista_stari = []
    try:
        lista_stari.extend(load_states()[0])
    except:
        return False
    # vom retine tupluri (nume_stare1,litera_alfabet_input,litera_stack_pop,litera_stack_push,nume_stare2)
    lista_actiuni = []
    # pentru fiecare linie din sectiunea Actions verificam intai daca are cele 5 parti obligatorii, apoi daca stare1 si stare2 sunt valide, daca litera_alfabet apartine alfabetului si daca lieterele stack apartin gamma
    for element in d["Trans"]:
        lsaux = element.split(',')
        if len(lsaux) != 5:
            return False
        if lsaux[0] not in lista_stari or lsaux[4] not in lista_stari:
            print("stari invalide",lsaux[0])
            return False
        if lsaux[1] not in d["Sigma"]:
            return False
        if lsaux[2] not in d["Gama"] or lsaux[3] not in d["Gama"]:
            return False
        lista_actiuni.append((lsaux[0],lsaux[1],lsaux[2],lsaux[3],lsaux[4]))
    return lista_actiuni

# print(load_sections())
# print(load_sigma())
# print(load_gamma())
# print(load_states())
# print(load_actions())

def emulate_pda(pda, input_str):
    # extragem alfabetul, multimea starilor, starea initiala, multimea starilor finale ale nfa ului, si functia de tranzitie
    sigma = pda[0]
    lista_stari = pda[1]
    stare_init = pda[2]
    lista_stari_finale = pda[3]
    gama = pda[4]
    lista_actiuni = pda[5]
    # stari_crt este lista care retine starile in care se afla simultan automatul la un anumit moment dat si stiva

    # parcurgem prima data lista de actiuni pentru a aplica toate tranzitiile cu * ( care nu necesita input)
    stari_crt = []
    for t in lista_actiuni:
        # se aplica tranzitia daca starea coincide, se citeste * si dam pop la *
        if stare_init == t[0] and t[1] == '*' and t[2] == '*':
            stari_crt.append((t[4],[t[3]]))
    # daca nu se aplica tranzitii, in lista de stari curente se afla doar tuplul (stare_initiala, stiva_vida)
    if stari_crt == []:
        stari_crt = [(stare_init, [])]

    # pentru fiecare litera citita
    for s in input_str:
        # print(' pentru ', s)
        # prin tranzitii se trece la o lista de stari
        next_states = []
        # pentru fiecare stare din lista curenta de stari in care se afla automatul
        for q in stari_crt:
            # print('     pentru ', q)
            # incercam sa facem match cu o tranzitie
            for t in lista_actiuni:
                # print('         verificam ', t)
                # preluam stiva din tuplul cu starea curenta
                stack = []
                stack.extend(q[1])
                # print('         acum q e ', q)
                # print('         stack initial ', stack)
                if t[0] == q[0]: # daca starile coincid
                    if t[1] == '*': # daca se citeste *
                        if t[2] == '*': # daca se da pop la *
                            # se aplica tranzitia
                            if t[3] != '*': # daca avem la ce sa dam push
                                stack.append(t[3])
                            # print('             adaugam la stari crt ', (t[4], stack))
                            # pentru ca nu s-a consumat nicio litera din input string starea in care s-a ajuns va fi evaluata tot in aceasta runda
                            stari_crt.append((t[4], stack))
                        elif stack != [] and t[2] == stack[-1]: # daca litera careia trebuie sa-i dam pop se afla in varful stivei
                            # se aplica tranzitia
                            stack.pop()
                            if t[3] != '*': # daca avem la ce sa dam push
                                stack.append(t[3])
                            # print('             adaugam la stari crt ',(t[4], stack))
                            # pentru ca nu s-a consumat nicio litera din input string starea in care s-a ajuns va fi evaluata tot in aceasta runda
                            stari_crt.append((t[4], stack))
                    elif t[1] == s: # daca ce trebuie sa se citeasca pt aplicare tranzitiei si ceea ce s-a citit coincid
                        if t[2] == '*': # daca nu trebuie sa dam pop la nimic
                            # se aplica tranzitia
                            if t[3] != '*': # daca avem la ce sa dam push
                                stack.append(t[3])
                            # print('             adaugam la stari next ', (t[4], stack), s)
                            # pentru ca s-a consumat litera de la input string, efectul tranzitiei va fi evaluat in runda urmatoare
                            next_states.append((t[4], stack))
                        elif stack != [] and t[2] == stack[-1]: # daca ceea ce cautam pentru a da pop se afla in varful stivei
                            # se aplica regula
                            stack.pop()
                            if t[3] != '*': # daca avem la ce sa dam push
                                stack.append(t[3])
                            # print('             adaugam la stari next ', (t[4], stack) , s)
                            # pentru ca s-a consumat litera de la input string, efectul tranzitiei va fi evaluat in runda urmatoare
                            next_states.append((t[4], stack))
        # trecem la runda urmatoare
        stari_crt = next_states
        # print('stari curente', stari_crt)

    # print('\n nu mai citim nimic')
    # daca au mai ramas de executat actiuni care nu necesita input
    # pentru fiecare din starile curente, verificam ca mai sus match-urile cu tranzitiile, dar efectuam doar tranzitiile pt care nu e necesar sa citim nimic, iar rezultatul va fi evaluat inaceeasi runda
    for q in stari_crt:
        for t in lista_actiuni:
            stack = []
            stack.extend(q[1])
            if q[0] == t[0] and t[1] == '*':
                if t[2] == '*':
                    if t[3] != '*':
                        stack.append(t[3])
                elif stack != [] and t[2] == stack[-1]:
                    stack.pop()
                    if t[3] != '*':
                        stack.append(t[3])
                stari_crt.append((t[4],stack))


    # verificam daca s-a ajuns in starea finala pentru macar un branch, daca da accepted, altfel rejected
    for q in stari_crt:
        if q[0] in lista_stari_finale and q[1] == []:
            return "accepted"
    return "rejected"


