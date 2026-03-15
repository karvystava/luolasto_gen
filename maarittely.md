# Määrittelydokumetti

- Käytän Pythonia, en hallitse muita koodikieliä. Kuulun tietojenkäsittelytieteen kandidaatin opinto-ohjelmaan.
- Tulen toteuttamaan luolastojen generoimiseen algoritmin, joka koostuu useammasta eri algoritmista.
Yksi tuottaa huoneet, toinen niiden väliset käytävät, kolmas ulkoasun ja tulen käyttämään Bowerin-Watsonin algoritmia/delanay triangulaatiota (ja ehkä tetrahedralisaatiota).
- Ongelma, jonka ratkaisen: Kuinka generoida dynaamisesti jonkinlainen luolasto?
- Aika- ja tilavaativuudet: Bowerin-Watsonin algoritmilla voi kestää O(N log N) operaatiota N pisteen trianguloimiseen,
ja joissai harvoissa tapauksissa voi kestää myös O(N^2).
- Lähteinä ainakin tuota vazgrizin "Procedurally Generated Dungeons" blogia https://vazgriz.com/119/procedurally-generated-dungeons/ ja Emergent Blogin "Dungeon generation -- from simple to complex" https://tiendil.org/en/posts/dungeon-generation-from-simple-to-complex .

Aiheen ydin on luoda dynaamisesti muodostuva luolasto, jota voisi käyttää pelipohjana. Huoneiden väliset yhteydet luodaan delaunay trianguloinnilla, ja käytävät muodostetaan niiden yhteyksien pohjalle.

Mahdollinen laajempa soveltamismuoto voisi olla etukäteen annetut parametrit luolastolle (esim. onko luolasto, metsä, jokin rakennus yms.)
