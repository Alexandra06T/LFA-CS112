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
    if not d["Sigma"]:
        raise RuntimeError("Alfabetul este vid.")
    return d["Sigma"]

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
    # daca starile initiale sunt mai multe decat cate una sau nu exista, eroare, daca nu exist astari finale eroare
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
    # vom retine tupluri (nume_stare1,simbol_alfabet,nume_stare2)
    lista_actiuni = []

    # pentru fiecare linie din sectiunea Actions verificam intai daca are cele trei parti obligatorii, apoi daca stare1 si stare2 sunt valide si daca simbol_alfabet apartine alfabetului
    for element in actions:
        lsaux = element.split(',')

        if len(lsaux) != 3:
            raise RuntimeError("Numar incorect de componente in tranzitie.")

        if lsaux[0] not in lista_stari or lsaux[2] not in lista_stari:
            raise RuntimeError("Tranzitia foloseste stari necunoscute.")

        if lsaux[1] not in sigma:
            raise RuntimeError("Simbol din alfabet necunoscut")

        # verificam daca exista mai multe tranzitii diferite de la aceeasi stare si pentru acelasi simbol
        if len([tuplu[2] for tuplu in lista_actiuni if tuplu[0] == lsaux[0] and tuplu[1] == lsaux[1] and tuplu[2] != lsaux[2]]) != 0:
            raise RuntimeError("Mai multe tranzitii aplicabile pentru aceeasi stare si acelasi simbol din alfabet.")

        lista_actiuni.append((lsaux[0], lsaux[1], lsaux[2]))

    # verificam daca avem pentru ficare stare o singura tranzitie pentru fiecare simbol din alfabet ( am verificat deja sa nu fie mai multe tranzitii, acum verificam sa avem macar una )
    for q in lista_stari:
        if len([tuplu for tuplu in lista_actiuni if tuplu[0] == q]) != len(sigma):
            raise RuntimeError(f"Nu exista tranzitie pentru toate simbolurile din alfabet din starea {q}")

    return lista_actiuni

def emulate_dfa(dfa, input_str):
    sigma = dfa[0]
    stare_init = dfa[2]
    lista_stari_finale = dfa[3]
    lista_actiuni = dfa[4]
    stare_crt = stare_init

    # parcurgem stringul de la input
    for litera in input_str:

        # verificam daca inputul ese valid
        if litera not in sigma:
            raise RuntimeError("Inputul contine simboluri necunoscute.")

        # cautam tranzitia pe care sa o aplicam
        for t in lista_actiuni:
            if t[0] == stare_crt and t[1] == litera:
                stare_crt = t[2]
                break

    if stare_crt not in lista_stari_finale:
        return 'rejected'
    return 'accepted'
