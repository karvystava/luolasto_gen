Toteutusdokumentti

Ohjelma käynnistyy main.py-tiedostosta, jossa on toteutettu DungeonGen
 -luokkaolio. DungeonGen luo pygame-pelipohjan, hoitaa peliloopin ja piirtää näytön.
 
Ohjelman tietorakenteiden manageroiminen tapahtuu map.py-tiedostossa, jossa Map-luokkaolio luo uuden sokkelokartan ja sen oliot, kuten huoneet, reitit, käytävät ja apugridin. Huoneiden generointi tapahtuu täällä.
 
Näiden olioiden luomista varten Map-luokan funktiot kutsuvat algorithms.py-tiedoston algoritmeja, jotka hoitavat triangulaation, mst:n ja A*-reitin. (Hox. aiemmin mukana ollut huoneita kiertävä ominaisuus on tietoisesti poistettu A*:den toiminnasta funktion rekonfiguroinnin yhteydessä.)

Triangulaation ja A*:den apuna tiedostosta formulae.py löytyy matemaattisia funktioita, esimerkiksi A*:den heuristinen funktio Manhattan Distance.

Items.py pitää sisällään luokat Button, InputBox, Room ja Passage eli näiden luokka-olioiden alustamisen, prosessoinnnin peliloopin sisällä sekä renderöinnin.

Aloitussivulla on ohjeteksti sekä InputBox-olio, johon voi syöttää toivotun kartan huonemäärän välillä 0-50 ja Enteriä painamalla siirrytään karttasivulle. Karttasivulla on kartta, New-nappula josta voi generoida uuden kartan samalla huonemäärällä sekä toinen huonemäärän syöttöboksi, joka luo uuden kartan Enterillä tai täyttämällä ensin InputBoxin ja sitten painamalla New.

Laajoja kielimalleja ei ole käytetty.


Lähteet:
https://vazgriz.com/119/procedurally-generated-dungeons/

https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm 
(Pseudokoodi, jota seurasin Boywer-Watsoniin)

https://en.wikipedia.org/wiki/Delaunay_triangulation

https://www.freecodecamp.org/news/prims-algorithm-explained-with-pseudocode/ 
(Pseudokoodi Primiin)

https://www.datacamp.com/tutorial/a-star-algorithm?dc_referrer=https%3A%2F%2Fduckduckgo.com%2F 
(Pseudokoodi A*:teen. Sivulta löytyy myös Pythonilla algoritmin muodostusesimerkki, mutta seurasin ylempänä olevaa pseudokoodia.)

https://en.wikipedia.org/wiki/A*_search_algorithm 
(Toinen A*:den toteutukseen käyttämäni pseudokoodi)
