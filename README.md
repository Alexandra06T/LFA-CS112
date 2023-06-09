# Emulatoare automate

**Obs! Caracterele din input vor fi despartite prin spatii.**<br>
**Obs! Epsilon este codat ca '*', pentru ca '#' se suprapune cu simbolul pentru comentarii.**

## DFA

### Formatul Fisierului de configurare

>#______ # comentarii - pot aparea pe orice linie din fisier  
[Sigma] # nume_sectiune_alfabet   
_______ # continut_sectiune_alfabet  
[States] # nume_sectiune_stari  
_______ # continut_sectiune_stari - o linie: nume_stare[,stare initiala (S)][,stare finala (F)]  
[Actions] # nume_sectiune_actiuni  
_______ # continut_sectiune_actiuni - o linie:nume_stare1,litera_alfabet,nume_stare2  

**Obs!** In sectiunea [States], starea de start este urmata de virgula si caracterul 'S', starea finala de virgula si caracterul 'F, respectiv o stare care este si initiala si finala este urmata de ',S,F'.
    
### Implementarea emulatorului DFA


**Pasul 1.** Parcurgem input string-ul, aplicand pentru fiecare tranzitia corespunzatoare.

**Pasul 2.** Daca starea in care se afla automatul dupa terminarea parcurgerii string-ului este starea finala, string-ul a fost acceptat.


## NFA

### Formatul Fisierului de configurare

>#______ # comentarii - pot aparea pe orice linie din fisier  
[Sigma] # nume_sectiune_alfabet   
_______ # continut_sectiune_alfabet  
[States] # nume_sectiune_stari  
_______ # continut_sectiune_stari - o linie: nume_stare[,stare initiala (S)][,stare finala (F)]  
[Actions] # nume_sectiune_actiuni  
_______ # continut_sectiune_actiuni - o linie:nume_stare1,litera_alfabet,nume_stare2  
  
**Obs!** In sectiunea [States], starea de start este urmata de virgula si caracterul 'S', starea finala de virgula si caracterul 'F, respectiv o stare care este si initiala si finala este urmata de ',S,F'.
 
### Implementarea emulatorului NFA

Vom retine o lista de stari curente (starile in care se afla automatul la un moment dat) si o lista de stari viitoare (starile in care urmeaza sa ajunga automatul dupa incheierea rundei actuale).

**Pasul 1.** Parcurgem input string-ul, pentru fiecare litera in parte aplicand tranzitiile posibile. O tranzitie se aplica daca starea curenta coincide cu starea de plecare a tranzitiei si (litera citita coincide cu litera de tranzitie sau tranzitia nu necesita o litera( tranzitie cu epsilon)).
Daca pentru aplicarea unei tranzitii s-a consumat litera din input string, starea in care se ajunge prin tranzitie se adauga la lista de stari curente pentru a fi procesate in aceeasi runda.
Daca s-a consumat litera ( s-a facut match cu o tranzitie folosind-o), se adauga la lista de stari viitoare.

**Pasul 2.** Cand s-au terminat literele de citit din input_string parcurgem inca o data starile curente pentru a aplica si posibilele tranzitii in care nu este necesara consumarea unei litere ( tranzitii cu epsilon)

**Pasul 3.** Parcurgem lista de stari curente si verificam daca starea este una finala. Daca macar o stare curenta este stare finala, stringul este acceptat.

### Converter NFA to DFA

Convertorul preia un NFA si returneaza un DFA echivalent.

## CFG

### Formatul Fisierului de configurare

>#______ # comentarii - pot aparea pe orice linie din fisier  
[Vars] # nume_sectiune_variabile   
_______ # continut_sectiune_variabile  
[Sigma] # nume_sectiune_alfabet 
_______ # continut_sectiune_alfabet 
[Rules] # nume_sectiune_reguli  
_______ # continut_sectiune_reguli - o linie:nume_variabila1 -> substituitor (eg. nume_variabila2,terminal,etc. )

**Obs!** In sectiunea [Vars], variabila de start este urmata de virgula si caracterul 'S'.
  
### Implementarea emulatorului CFG

Incepem cu stringul format din variabila de start. Cat timp in acest string exista variabile nesubstituite ( nu contine numai terminali ) si stringul are lungimea mai mica decat cea maxim posibila, cautam prima variabila, alegem random o regula si substituim variabila corespunzator.

## PDA

### Formatul Fisierului de configurare

>#______ # comentarii - pot aparea pe orice linie din fisier  
[Sigma] # nume_sectiune_alfabet   
_______ # continut_sectiune_alfabet  
[States] # nume_sectiune_stari  
_______ # continut_sectiune_stari - o linie: nume_stare[,stare initiala (S)][,stare finala (F)]  
[Gama] # nume_sectiune_alfabet_stiva  
_______ # continut_sectiune_alfabet_stiva 
[Trans] # nume_sectiune_tranzitii  
_______ # continut_sectiune_tranzitii - o linie:nume_stare1,litera_alfabet,litera_alfabet_gama_pop,litera_alfabet_gama_push,nume_stare2

**Obs!** In sectiunea [States], starea de start este urmata de virgula si caracterul 'S', starea finala de virgula si caracterul 'F, respectiv o stare care este si initiala si finala este urmata de ',S,F'.

### Implementarea emulatorului PDA

O runda = procesarea unui caracter din input string
Vom retine o lista de stari curente (starile in care se afla automatul la un moment dat) si o lista de stari viitoare (starile in care urmeaza sa ajunga automatul dupa incheierea rundei actuale).
O astfel de lista va fi formata din tupluri (stare, stiva starii respective)

**Pasul 1.** Pornind din starea initiala, aplicam toate tranzitiile posibile care nu consuma litera din input string (citesc epsilon). 
Daca nu exista, lista de stari curente este formata din tuplul (stare_initiala, stiva vida).

**Pasul 2.** Parcurgem input string-ul, pentru fiecare litera in parte aplicand tranzitiile posibile. O tranzitie se aplica daca starea curenta coincide cu starea de plecare a tranzitiei si (litera citita coincide cu litera de tranzitie sau tranzitia nu necesita o litera( tranzitie cu epsilon)) si (caracterului caruia trebuie sa ii dam push conform tranzitiei coincide cu varful stivei sau nu trebuie sa dam pop la nimic (pop la epsilon)).
Daca pentru aplicarea unei tranzitii s-a consumat litera din input string, starea in care se ajunge prin tranzitie si stiva asociata se adauga la lista de stari curente pentru a fi procesate in aceeasi runda.
Daca s-a consumat litera ( s-a facut match cu o tranzitie folosind-o), se adauga la lista de stari viitoare.

**Pasul 3.** Cand s-au terminat literele de citit din input_string parcurgem inca o data starile curente pentru a aplica si posibilele tranzitii in care nu este necesara consumarea unei litere ( tranzitii cu epsilon)

**Pasul 4.** Parcurgem lista de stari curente si verificam daca starea este una finala si stiva este goala. Aceste doua conditii indeplinite simultan asigura faptul ca un branch a golit stiva concomitent cu terminarea parcurgerii inputului, adica stringul a fost acceptat.