import random
import string

file_name = input("Introduceti numele fisierului.\n")


def load_sections():
    # d - dictionar nume_sectiune:continut_sectiune
    d = {}
    with open(file_name) as f:
        for line in f:
            line = line.replace('\n', '')
            try:
                if line[0] == '[':
                    nume = line[1:-1]  # numele sectiunii
                    d[nume] = []  # incepem o noua sectiune
                elif line[0] != '#':  # daca linia nu este un comentariu
                    d[nume].append(line)  # adaugam linia la ultima sectiune deschisa
            except:
                pass  # daca lina este goala
    return d


def load_sigma():
    # preluam alfabetul
    d = load_sections()
    sigma = d["Sigma"]
    # daca alfabetul e vid, eroare
    if not sigma:
        raise RuntimeError("Alfabetul este vid.")

    # verificam daca e o variabila lowercase
    for element in sigma:
        if element not in string.ascii_uppercase.split():
            pass
        else:
            raise RuntimeError(f"Simbolul din alfabet {element} nu are toate caracterele lowercase. ")

    return d["Sigma"]


def load_vars():
    # preluam variabilele
    d = load_sections()
    var = d["Vars"]
    vars_list = []
    S = 'a' # S e variabila de start, initializata cu 'a', valoare imposibila

    # daca nu exista variabile
    if not var:
        raise RuntimeError("Nu exista variabile.")

    for element in var:
        split = element.split(',')

        # daca nu e variabila uppercase, eroare
        if split[0] not in string.ascii_lowercase.split():
            pass
        else:
            raise RuntimeError(f"Variabila {element} nu are toate caracterele uppercase. ")

        # daca e variabila de start
        if len(split) == 2:
            S = split[0]

        vars_list.append(split[0])

    if S == 'a':
        raise RuntimeError("Nu exista variabila de start.")

    return S, vars_list


def load_rules():
    # preluam rules
    d = load_sections()
    rules = d["Rules"]
    # preluam variabilele
    vars_list = load_vars()[1]
    # preluam simbolurile
    sigma = load_sigma()

    # d_rules dictionar: retine Variabila:lista efect regula, unde efect regula este o lista de simboluri si variabile
    d_rules = {}

    # daca nu exista reguli, eroare
    if not rules:
        raise RuntimeError("Nu exista reguli.")

    # parsam fiecare regula
    for element in rules:
        r_split = element.split(' -> ')
        var = r_split[0]

        # daca var nu e in lista de variabile, eroare
        if var not in vars_list:
            raise RuntimeError(f"\'{element}\' nu este recunoscut ca variabila. ")

        # daca inca nu se gaseste in dictionarul de reguli, cream o noua lista
        if var not in d_rules:
            d_rules[var] = []

        symbols = r_split[1].split(',')
        for symbol in symbols:
            if symbol not in vars_list:  # inseamna ca e un string de terminals, verificam daca sunt din alfabet
                for ch in symbol:
                    if ch not in sigma:
                        raise RuntimeError(f"Simbolul {ch} nu este recunoscut ca simbol sau ca variabila. ")

        d_rules[var].append(symbols)

    return d_rules


def generate_lang():
    # preluam simbolurile, variabilele si regulile
    v = load_vars()
    vars_list = v[1]
    s = v[0]
    symbols = load_sigma()
    rules = load_rules()

    # pornim de la variabila de start
    crt_str = [s]
    exists = True
    first_var = s

    while exists is True and len(crt_str) < 10:
        exists = False
        var_pos = 0  # pozitia variabilei in crt_string
        i = 0

        # cautam prima variabila
        while i in range(len(crt_str)) and exists is False:
            element = crt_str[i]
            if element in vars_list:
                first_var = element
                exists = True
            var_pos += 1
            i += 1

        # daca am gasit o variabila, o substituim
        if exists is True:
            # alegem o regula random
            chosen_rule = random.choice(rules[first_var])

            # facem substitutia
            new_str = []
            if var_pos != 1:
                new_str.extend(crt_str[:var_pos-1])  # stringul pana la variabila
            new_str.extend(chosen_rule)  # regula
            new_str.extend(crt_str[var_pos:])  # stringul de dupa variabila

            crt_str = new_str

    return " ".join(crt_str)
