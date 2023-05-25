# Fisier de configurare

### Utilizare
- In fisierul *date.in* se vor introduce date dupa formatul   

  >#______ # comentarii - pot aparea pe orice linie din fisier  
  [Sigma] # nume_sectiune_alfabet   
  _______ # continut_sectiune_alfabet  
  [States] # nume_sectiune_stari  
  _______ # continut_sectiune_stari - o linie: nume_stare[,stare initaiala (S)][,stare finala (F)]  
  [Actions] # nume_sectiune_actiuni  
  _______ # continut_sectiune_actiuni - o linie:nume_stare1,litera_alfabet,nume_stare2  

- In *configuration_file.py* se regasesc functiile care parseaza si verifica datele din fisierul date.in.  

- In *main.py* se vor scrie instructiunile care trebuie executate

### PDA

Obs! Caracterele din input vor fi despartite prin spatii.

O runda = procesarea unui caracter din input string
Vom retine o lista de stari curente (starile in care se afla automatul la un moment dat) si o lista de stari viitoare (starile in care urmeaza sa ajunga automatul dupa incheierea rundei actuale).
O astfle de lista va fi formata din tupluri (stare, stiva starii respective)

Pasul 1. Pornind din starea initiala, aplicam toate tranzitiile posibile care nu consuma litera din input string (citesc epsilon). 
Daca nu exista, lista de stari curente este formata din tuplul (stare_initiala, stiva vida).

Pasul 2. Parcurgem input string-ul, pentru fiecare litera in parte aplicand tranzitiile posibile. O tranzitie se aplica daca starea curenta coincide cu starea de plecare a tranzitiei si (litera citita coincide cu litera de tranzitie sau tranzitia nu necesita o litera( tranzitie cu epsilon)) si (caracterului caruia trebuie sa ii dam push conform tranzitiei coincide cu varful stivei sau nu trebuie sa dam pop la nimic (pop la epsilon)).
Daca pentru aplicarea unei tranzitii s-a consumat litera din input string, starea in care se ajunge prin tranzitie si stiva asociata se adauga la lista de stari curente pentru a fi procesate in aceeasi runda.
Daca s-a consumat litera ( s-a facut match cu o tranzitie folosind-o), se adauga la lista de stari viitoare.

Pasul 3. Cand s-au terminat literele de citit din input_string parcurgem inca o data starile curente pentru a aplica si posibilele tranzitii in care nu este necesara consumarea unei litere ( tranzitii cu epsilon)

Pasul 4. Parcurgem lista de stari curente si verificam daca starea este una finala si stiva este goala. Aceste doua conditii indeplinite simultan asigura faptul ca un branch a golit stiva concomitent cu terminarea parcurgerii inputului, adica limbajul a fost acceptat.



#   L F A - C S 1 1 2  
 