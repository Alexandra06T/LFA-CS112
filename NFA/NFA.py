file_name = input("Introduceti numele fisierului.\n")

def load_sections():
    # d - dictionar nume_sectiune:continut_sectiune
    d = {}
    with open(file_name) as f:
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
    sigma = d["Sigma"]
    if not sigma:
        raise RuntimeError("Alfabetul este vid.")
    return sigma

def load_states():
    d = load_sections()
    states = d["States"]
    lista_stari = []
    # contorizam starile initiale si pe cele finale
    nr_start = 0
    nr_final = 0
    ls_stari_finale = []

    # pentru fiecare element din alfabet cream un tuplu (nume_stare, tip stare); 0 - stare interna, 1 - stare initiala, 2 - stare finala
    for element in states:
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
    # daca starile initiale sunt mai multe decat una sau nu exista, eroare, daca starile finale nu exista, eroare
    if nr_start != 1 or nr_final < 1:
        raise RuntimeError("Numar stari initiale si finale incorect")
    # daca nu exista stari, eroare
    if not lista_stari:
        raise RuntimeError("Nu exista stari.")
    return lista_stari,stare_init,ls_stari_finale


def load_actions():
    d = load_sections()
    actions = d["Actions"]
    sigma = d["Sigma"]
    lista_stari = load_states()[0]
    # vom retine tupluri (nume_stare1,litera_alfabet,nume_stare2)
    lista_actiuni = []
    # pentru fiecare linie din sectiunea Actions verificam intai daca are cele trei parti obligatorii, apoi daca stare1 si stare2 sunt valide si daca litera_alfabet apartine alfabetului
    for element in actions:
        lsaux = element.split(',')

        if len(lsaux) != 3:
            raise RuntimeError("Numar incorect de componente in tranzitie.")

        if lsaux[0] not in lista_stari or lsaux[2] not in lista_stari:
            raise RuntimeError("Tranzitia foloseste stari necunoscute.")

        if lsaux[1] not in sigma:
            raise RuntimeError("Simbol din alfabet necunoscut")

        lista_actiuni.append((lsaux[0], lsaux[1], lsaux[2]))

    return lista_actiuni

def emulate_nfa(nfa, input_str):
    # extragem starea initiala, multimea starilor finale ale nfa ului, si functia de tranzitie
    stare_init = nfa[2]
    lista_stari_finale = nfa[3]
    lista_actiuni = nfa[4]
    sigma = nfa[0]
    # stari_crt este lista care retine starile in care se afla simultan automatul la un anumit moment dat
    stari_crt = [stare_init]

    # pentru fiecare litera citita
    for s in input_str:

        # verificam daca inputul ese valid
        if s not in sigma:
            raise RuntimeError("Inputul contine simboluri necunoscute.")

        # prin tranzitii se trece la o lista de stari
        next_states = []
        # pentru fiecare stare din lista curenta de stari in care se afla automatul
        for q in stari_crt:
            # verificam daca exista tranzitie cu epsilon de la q, daca da trecem in lista de stari curente si starea la care se ajunge prin epsilon pentru a o putea evalua in aceeasi runda
            for t in lista_actiuni:
                if t[0] == q and t[1] == '*':
                    stari_crt.append(t[2])
                # gasim starea in care trece automatul in urma citirii literei s si aplicarii peste starea q
                if t[0] == q and t[1] == s:
                    # noua stare este retinuta in lista de stari urmatoare
                    next_states.append(t[2])
        # trecem la lista de stari urmatoare
        stari_crt = next_states

    # daca au mai ramas de executat actiuni care nu necesita input
    # pentru fiecare din starile curente, verificam ca mai sus match-urile cu tranzitiile, dar efectuam doar tranzitiile pt care nu e necesar sa citim nimic, iar rezultatul va fi evaluat inaceeasi runda
    for q in stari_crt:
        for t in lista_actiuni:
            if q[0] == t[0] and t[1] == '*':
                stari_crt.append(t[2])

    # verificam daca s-a ajuns in starea finala pentru macar un branch, daca da accepted, altfel rejected
    for q in stari_crt:
        if q in lista_stari_finale:
            return "accepted"
    return "rejected"


