Toteutusdokumentti

Ohjelman ydintoteutus löytyy main.py-tiedostosta, jossa on toteutettu DungeonGen
 -luokkaolio. DungeonGen on pygamea käyttävä pelipohja, jossa on etusivu ja karttasivu,
jolle pääsee etusivulta. Karttasivulla voi "new":ta painamalla generoida satunnaisia
huonekarttoja. 

Perus pygame-funktioiden (loop ja display_screen) lisäksi sieltä
löytyvät funktiot make_room, joka generoi huoneiden x- ja y-koordinaatit sekä
nelikulmaisten huoneiden leveydet ja pituudet. Huoneiden väliset käytävät, "passages",
perustuvat Boywer-Watson algoritmiin, jonka toteutus on funktiossa triangulation.

Tämän lisäksi mainista löytyy omat luokat Room-, Passage- ja Button-olioille.

Mainin lisäksi srcssä on circumcenter-koodi, jossa on matemaattisia funktioita, joita
tarvitaan triangulation-funktioon.

Triangulation eli Boywer-Watsonin algoritmi on ohjelman ydinalgoritmi, ja sen 
aikavaativuuden pitäisi ainakin pseudokoodin tietojen perusteella olla O(n²).

Työ on vielä kesken, ja toistaiseksi itse käytävät ovat aikalailla idean tasolla.
Yhteyksiä tulee vähentää ja ne tulee visualisoida yhteneväisemmiksi huoneiden kanssa.


Laajoja kielimalleja ei ole käytetty.

Lähteet:
https://vazgriz.com/119/procedurally-generated-dungeons/
https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm (hox. pseudokoodi, jota
seurasin Boywer-Watsoniin)
https://en.wikipedia.org/wiki/Delaunay_triangulation
