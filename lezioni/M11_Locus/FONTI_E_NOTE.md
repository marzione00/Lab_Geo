# Locus — fonti e convenzioni scientifiche

Marzio De Corato · GeoStat Lab · M11 · edizione 20 novembre 2026.

## Materiali del corso

Il punto di partenza è [M11 nel repository Lab_Geo](https://github.com/marzione00/Lab_Geo/tree/649f7cc577b96bd1044d81e78a2f530813e4f96b/moduli/M11), revisione 649f7cc577b96bd1044d81e78a2f530813e4f96b, consultata il 20 novembre 2026. I 36 file acquisiti comprendono README e JSON del modulo, sorgenti Python/XeLaTeX/R, due CSV, 20 laboratori R e nove esperimenti. Le copie originali sono conservate nel pacchetto, con confronto al Git blob SHA-1 e impronte SHA-256.

La lezione sviluppa il modulo in 110 slide. Mantiene i 20 identificativi M11_N01–M11_N20 e i temi del corso, aggiungendo formalizzazione, esempi, controlli, risultati eseguiti e discussione dei limiti. La tabella di raccordo permette di distinguere l’estensione editoriale dai materiali originali.

## Fonti primarie e documentazione

Consultate il 20 novembre 2026. Il testo del modulo è originale; le fonti sono riferimenti per definizioni, convenzioni e comportamento del software.

| Riferimento | Uso nel modulo |
| --- | --- |
| [sf: st_transform](https://r-spatial.github.io/sf/reference/st_transform.html) | Trasformazione delle coordinate e ordine esplicito degli assi con OGC:CRS84. |
| [sf: st_crs e st_set_crs](https://r-spatial.github.io/sf/reference/st_crs.html) | Distinzione fra assegnazione di un riferimento e trasformazione dei numeri. |
| [spdep: moran.mc](https://r-spatial.github.io/spdep/reference/moran.mc.html) | Riferimento per permutazione, alternativa e dichiarazione dei pesi. |
| [gstat: krige e idw](https://r-spatial.github.io/gstat/reference/krige.html) | Distinzione fra IDW, kriging ordinario/universale e supporti di previsione. |
| [gstat: vgm](https://r-spatial.github.io/gstat/reference/vgm.html) | Modelli, sill parziale, nugget e convenzioni dei parametri. |
| [Pebesma e Bivand, Spatial Data Science, capitolo 12](https://r-spatial.org/book/12-Interpolation.html) | Semivariogrammi, interpolazione e distinzione fra campo e misura. |
| [RFC 7946: The GeoJSON Format](https://www.rfc-editor.org/rfc/rfc7946.html) | WGS 84, gradi decimali, ordine longitudine–latitudine nella consegna. |

Le versioni delle pagine online possono differire dalle versioni usate per l’esecuzione. L’ambiente effettivo è registrato in Verifiche/SESSIONE_R.txt e Verifiche/VERSIONI_SF.txt.

## Dati, unità e riferimenti

spazio_v3.csv contiene 64 siti sintetici su una griglia 8 × 8, con passo 250 m e coordinate locali da 0 a 1750 m. La concentrazione è in unità arbitrarie; la quota è sintetica e in metri. Le coordinate locali non hanno un codice EPSG attribuibile dalla sola unità.

Le colonne geografiche descrivono una collocazione sintetica vicina a 9° E e 45° N. Sono trattate come longitudine/latitudine WGS 84 nell’esercizio di proiezione. La relazione approssimata con la griglia locale non equivale a una trasformazione UTM esatta. Le distanze locali, sferiche e proiettate restano distintamente etichettate.

La funzione haversine usa metri e raggio sferico 6 371 000 m, in accordo con i 6371 km del laboratorio originale. Gli angoli entrano in radianti nel calcolo. Non viene presentata come geodetica ellissoidale.

casuali_comuni_v3.csv conserva i numeri usati nelle permutazioni originali. Le impronte dei due file sono in Dati/PROVENIENZA.json.

## Relazioni, statistiche e inferenza

La matrice A collega siti distinti con distanza locale non superiore a 260 m: 112 archi non orientati, 224 celle non nulle, gradi 2/3/4. W divide ciascuna riga per il grado. La rete è la stessa, ma le statistiche pesate sono diverse.

I risultati eseguiti sono I_A = 0,7195277292 e I_W = 0,7975650044. Lo scatter usa W: la pendenza coincide con I_W, mentre l’intercetta è circa 0,011109. La normalizzazione di riga non impone che la media del ritardo sia zero.

Il test principale conserva le 100 permutazioni originali ottenute ordinando blocchi successivi di 64 uniformi. L’approfondimento usa 999 permutazioni con seme 20261109. Si dichiara un’alternativa unilaterale positiva e si calcola (1 + conteggio)/(B + 1). I risultati sono rispettivamente 1/101 e 1/1000. La scambiabilità delle etichette è l’ipotesi del riferimento; un gradiente la può violare. Il test non distingue da solo un trend da dipendenza residua.

Il confronto con i residui di un piano è descrittivo. Non si presenta la permutazione libera dei residui OLS come un test esatto: la stima introduce vincoli e covarianze. I quadranti dello scatter sono classificazioni descrittive, non test locali.

## Semivarianza, supporto e copertura

Le 2016 coppie non ordinate vengono raggruppate negli intervalli (0,300], (300,600], (600,1000] e (1000,2500] m. Le ascisse della curva sono distanze medie effettive, con conteggi 112, 362, 476 e 1066. Le coppie condividono osservazioni e non sono considerate repliche indipendenti.

Il legame fra semivarianza e covarianza viene formulato sotto stazionarietà al secondo ordine. L’isotropia è un’ipotesi ulteriore. I modelli teorici illustrati hanno parametri dichiarati; non sono presentati come adattamenti ai 64 valori. Per l’esponenziale il parametro di scala a non è un range finito; 3a corrisponde a circa il 95% del sill strutturale.

La media dei siti, la media dei blocchi e una media areale hanno bersagli e pesi diversi. I quattro blocchi della griglia contengono 16 siti ciascuno; il bilanciamento spiega la coincidenza delle prime due medie. L’esempio separato con numerosità 2/8 e medie 10/20 produce 18 per sito e 15 per blocco.

Il campione lungo la strada seleziona 16 siti con y ≤ 250 m. Il confronto con la griglia completa è possibile perché il dataset didattico è noto; non si presume disponibile la media del territorio escluso in un’indagine reale.

## Previsione e verifica geografica

La soglia descrittiva Ovest/Est a 1000 m (32/32 siti) è diversa dalla soglia del test a 1250 m. Il test usa 40 siti con x < 1250 m per prevedere 24 siti con x ≥ 1250 m. Si tratta di trasferimento verso Est oltre l’estensione del train, non soltanto di interpolazione interna.

Il risultato principale usa IDW con p=2 prefissato e confronta media del train e vicino più prossimo sugli stessi bersagli. Gli errori sono osservato − previsto: un bias positivo significa sottostima. La graduatoria RMSE del caso è vicino più prossimo 2,6323, IDW p=2 3,8078, media 4,7315 u.a. Non viene generalizzata a qualunque dominio.

L’approfondimento seleziona p fra 1, 2 e 3 con tre frontiere interne a 500, 750 e 1000 m. Ogni stima usa solo siti a Ovest della frontiera e valuta la sua colonna di 8 siti, per 24 previsioni interne per candidato. I valori del test Est restano esclusi da ogni scelta. Il candidato selezionato è p=3; questa analisi non sostituisce retroattivamente il protocollo principale p=2.

La carta IDW sui 64 siti serve alla descrizione della regola. È distinta dalla previsione costruita con i soli 40 siti ammessi. Una griglia 45 × 45 non aggiunge campioni. Le coincidenze riproducono il valore del sito; per repliche alla stessa coordinata la convenzione della funzione è la media, dichiarata prima del calcolo.

## Kriging verificabile

Il caso illustrativo usa tre siti a 0, 500 e 1000 m, valori 10/15/12 u.a., bersaglio a 250 m e covarianza gaussiana dichiarata C(h)=4 exp(-(h/800)^2). È distinto dal caso principale con gradiente. Il modello ha media costante ignota, covarianza fissata e nessun errore di misura.

Il sistema [C,1;1',0] [lambda;nu] = [c0;1] produce pesi circa 0,4651253, 0,6918785 e −0,1570038. La previsione è 13,145385 u.a. La varianza C00 − 2 lambda' c0 + lambda' C lambda coincide con C00 − lambda' c0 − nu nella convenzione scritta, e vale 0,03696075 (u.a.)².

I pesi possono essere negativi. La varianza è condizionata al modello della covarianza e al bersaglio; non ingloba automaticamente l’incertezza della stima o della scelta del modello. Campo latente, nuova misura e media di blocco sono bersagli diversi. Le proprietà lineari di minima varianza non richiedono da sole Gaussianità; eventuali intervalli gaussiani la richiedono come ipotesi ulteriore.

## Esecuzione e grafica

Calcoli, 46 frammenti delle slide e 100 blocchi dei notebook sono eseguiti in R. sf esegue trasformazioni e I/O geografico; gli altri algoritmi sono espliciti in R base, con verifiche numeriche. Non viene dichiarata un’esecuzione dei pacchetti spdep o gstat.

Le 40 figure scientifiche sono prodotte dai dati e dai calcoli in R. I diagrammi concettuali sono geometrie vettoriali TikZ. La copertina è una scena Blender/Cycles modellata, con 35 campioni e 75 connessioni illustrative. Non rappresenta la geometria dei 64 siti didattici e non usa immagini o texture generate con IA.

Le verifiche effettivamente concluse sono registrate nei file di audit del pacchetto. Gli esiti dei moduli M01–M10 restano quelli storici: i loro materiali sono preservati, non rieseguiti in questa edizione.

