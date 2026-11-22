"""Maschere, dominio, risoluzione e allineamento: pagine 20–48."""
from componenti import *

slide(20,'La maschera definisce il dominio disponibile',
 raster_grid('mask')+
 eq(r"""m_{ij}=\begin{cases}1&\text{cella valida}\\0&\text{cella esclusa}\end{cases}"""),
 p(r'Una maschera distingue le celle utilizzabili dalle altre. L’esclusione può dipendere da assenza di misura, qualità insufficiente o scelta del dominio.')+
 info(r'Conserviamo separatamente i valori e la loro validità. Il colore delle celle escluse deve essere riconoscibile senza confondersi con la scala delle quote.')+
 p(r'Il motivo della mancanza può essere legato alla morfologia o al fenomeno studiato.'),
 r'La maschera appartiene al dato e condiziona l’interpretazione delle sue sintesi.',notebook=4,source=[7,25])

slide(21,'NoData e quota zero hanno significati diversi',
 table(['Stato','Interpretazione'],[
 ['Quota 0 m','Valore fisico valido nel riferimento verticale'],
 ['NA in R','Valore mancante nel calcolo'],
 ['NoData nel file','Codice riservato alla mancanza'],
 ['Cella fuori dominio','Posizione esclusa dalla domanda'],
 ['Valore non valido','Misura respinta secondo un criterio']], [4.0,5.0]),
 p(r'Il GeoTIFF originale dichiara il valore $-9999$ come NoData. terra lo interpreta come mancante, non come una quota da usare nelle medie.')+
 info(r'Una codifica mancante deve essere compatibile con l’intervallo dei valori validi. La stessa sentinella non è automaticamente adatta a ogni variabile.')+
 p(r'Un terreno a quota zero può essere pianeggiante o inclinato: lo zero non indica assenza di informazione.'),
 r'La validità della cella deve essere verificata prima di interpretare il suo numero.',notebook=4,source=[7])

slide(22,'Ventiquattro celle escluse restano localizzabili',
 fig('maschera',r'Finestra esclusa: indici originali riga 4–7 e colonna 9–14. La maschera contiene 24 celle.'),
 p(r'In R gli indici corrispondenti sono righe 5–8 e colonne 10–15. Il controllo del numero di celle rende esplicita la conversione.')+
 info(r'Le quote disponibili conservano la scala cromatica della carta iniziale. La mancanza è rappresentata con un colore separato.'),
 r'Conservare la posizione delle celle escluse evita che la maschera diventi un semplice conteggio.',
 code('Zm <- Z\nZm[5:8,10:15] <- NA_real_\nstopifnot(sum(is.na(Zm))==24)\ncopertura <- mean(is.finite(Zm))','R · maschera dichiarata'),notebook=4,source=[7])

slide(23,'La copertura accompagna ogni media',
 eq(r"""c=\frac{696}{720}\approx0{,}9667""")+
 eq(r"""\overline z_{\mathrm{disp}}=\frac{\sum_{ij}m_{ij}z_{ij}}{\sum_{ij}m_{ij}}""")+
 info(r'La notazione della somma si riferisce ai valori validi: nel codice selezioniamo esplicitamente le celle disponibili prima di calcolare la media.'),
 p(r'La media dei disponibili descrive le celle rimaste. Il suo trasferimento al dominio completo richiederebbe informazioni sul processo di mancanza.')+
 p(r'La copertura del 96,67\% non dimostra che le celle osservate siano rappresentative della parte esclusa.')+
 sm(r'Il dataset completo ci permette di confrontare le due medie come esperimento didattico.'),
 r'Numero di celle valide, loro posizione e causa di esclusione devono accompagnare il risultato.',notebook=4,source=[7,8])

slide(24,'Sostituire i mancanti con zero altera il risultato',
 fig('medie_maschera',r'Confronto fra terreno completo, celle disponibili e sostituzione impropria con zero. Le quantità hanno domini e significati diversi.'),
 p(r'La sostituzione aggiunge quote che non sono state osservate. Nel terreno del caso guida introduce valori molto inferiori alle quote circostanti.')+
 info(r'Il risultato numerico è calcolabile, ma la procedura cambia la variabile e la superficie rappresentata.'),
 r'Una scelta di codifica non deve introdurre valori fisici inventati nelle statistiche.',
 code('Zzero <- Zm\nZzero[is.na(Zzero)] <- 0\nc(completa=mean(Z),\n disponibile=mean(Zm,na.rm=TRUE),\n sostituita=mean(Zzero))','R · confronto dei significati'),notebook=4,source=[7])

slide(25,'Ritagliare seleziona una parte del territorio',
 fig('dominio_crop',r'Selezione dei centri con 300 ≤ x ≤ 600 m e 180 ≤ y ≤ 510 m: 132 celle, pari a 11,88 ha nella griglia locale.'),
 p(r'La finestra contiene una parte diversa della morfologia. La sua media non risponde alla stessa domanda della media dell’intero dominio.')+
 info(r'Dichiariamo se il criterio riguarda i centri o l’intersezione con i bordi delle celle. Per confini irregolari le regole possono dare risultati diversi.'),
 r'Il ritaglio è una scelta geografica da documentare insieme alla sintesi.',
 code('sel <- with(d,x_m>=300 & x_m<=600 &\n                  y_m>=180 & y_m<=510)\nstopifnot(sum(sel)==132)\nmean(d$quota_m[sel])','R · dominio dei centri'),notebook=5,source=[8])

slide(26,'Ritaglio e maschera hanno ruoli distinti',
 boxes([('a',2.1,3.8,'Raster di partenza',3.7,'GeoA'),
        ('b',7.3,3.8,'Finestra rettangolare',3.7,'GeoB'),
        ('c',2.1,1.2,'Criterio di inclusione',3.7,'GeoC'),
        ('d',7.3,1.2,'Celle valide nel dominio',3.7,'GeoA')],
       [('a','b',''),('a','c',''),('b','d',''),('c','d','')]),
 p(r'Il ritaglio riduce l’estensione rettangolare. Una maschera può escludere celle al suo interno e descrivere un dominio irregolare.')+
 info(r'La superficie del rettangolo esterno e la superficie valida non sono necessariamente uguali. Le riportiamo separatamente.')+
 p(r'Una geometria di ritaglio che attraversa celle richiede una regola di inclusione o un peso frazionario esplicito.'),
 r'Dimensione del file, estensione geometrica e superficie valida descrivono proprietà differenti.',notebook=5,source=[8,9])

slide(27,'Dal conteggio delle celle agli ettari',
 fig('07_superficie_zone',r'Area piana dei domini: 720, 696, 24 e 132 celle rispettivamente.',height=4.65)+
 eq(r"""a=\Delta x\,\Delta y=900\ \mathrm{m}^2=0{,}09\ \mathrm{ha}"""),
 p(r'Il prodotto dei passi misura l’area piana della cella. La somma delle aree valide quantifica la copertura discretizzata.')+
 info(r'Questa area è planimetrica. Non è l’area reale della superficie inclinata del terreno.'),
 r'La stessa parola «superficie» deve essere accompagnata dalla geometria a cui si riferisce.',
 code('area_cella_ha <-\n prod(terra::res(r))/1e4\nc(totale=720*area_cella_ha,\n valida=696*area_cella_ha)','R · area piana della griglia'),notebook=6,source=[9])

slide(28,'Una griglia in gradi richiede un calcolo di area',
 eq(r"""A_{\mathrm{valida}}=\sum_{k\in V}a_k""")+
 eq(r"""\overline z_A=\frac{\sum_{k\in V}a_k z_k}{\sum_{k\in V}a_k}""")+
 info(r'$a_k$ è l’area rappresentata dalla cella valida $k$. La media assume che i valori siano appropriati alla sintesi su quelle aree.'),
 p(r'Uguali intervalli angolari non definiscono celle di uguale area sulla Terra. Anche una proiezione può introdurre distorsioni di area.')+
 p(r'Nel caso locale metrico usiamo l’area piana. Un’analisi geografica reale deve scegliere una misura di area coerente con il riferimento e con la domanda.')+
 sm(r'La funzione terra::cellSize permette di calcolare aree tenendo conto della collocazione geografica; la scelta va documentata.'),
 r'La media semplice delle celle coincide con una media di area solo quando i pesi appropriati sono uguali.',notebook=6,source=[9,26])

slide(29,'Le maschere si combinano conservando le cause',
 table(['Criterio','Informazione da registrare'],[
 ['Valore disponibile','Assenza della misura'],
 ['Qualità ammessa','Nuvole, saturazione o altro criterio'],
 ['Dominio scelto','Inclusione territoriale'],
 ['Calcolo definito','Vicinato o denominatore valido'],
 ['Maschera finale','Intersezione dei criteri necessari']], [4.1,4.9]),
 p(r'La maschera complessiva può essere una congiunzione logica. Conservare i singoli motivi consente di capire perché una cella è stata esclusa.')+
 info(r'Quando calcoliamo una derivata, servono anche i vicini richiesti. Una cella con quota valida può avere una pendenza non calcolabile.')+
 p(r'Le esclusioni introdotte dal metodo devono essere distinte dalle mancanze del dato originale.'),
 r'La tracciabilità della maschera spiega come cambia il dominio lungo la catena di elaborazione.',source=[7,17,25])

slide(30,'Una cella mancante può influenzare i vicini',
 stencil(),
 p(r'Il calcolo centrato utilizza quattro quote adiacenti. Se una di esse manca, la derivata richiesta non è disponibile.')+
 info(r'Adottiamo un criterio esplicito: centro valido e quattro vicini validi. Il bordo esterno richiede una convenzione separata.')+
 p(r'Riempire automaticamente i buchi cambia il metodo e introduce un modello di interpolazione. La decisione deve essere motivata prima delle derivate.'),
 r'Il dominio di una grandezza derivata dipende dal vicinato necessario a calcolarla.',source=[7,14,17])

slide(31,'Una sintesi riproducibile dichiara il denominatore',
 table(['Quantità','Denominatore'],[
 ['Copertura per numero','Celle ammesse nella griglia di riferimento'],
 ['Media dei disponibili','Celle valide utilizzate'],
 ['Media per area','Somma delle aree rappresentate'],
 ['Frazione di una classe','Dominio valido definito'],
 ['Densità territoriale','Area coerente con gli eventi contati']], [4.2,4.8]),
 p(r'Una percentuale o una media possono cambiare perché cambiano i valori, il dominio oppure entrambi.')+
 info(r'Nel confronto fra prodotti riportiamo i conteggi e usiamo, quando serve, una maschera comune. Confrontiamo così lo stesso insieme di celle.')+
 p(r'Una mappa dei mancanti è spesso più informativa di una sola percentuale di copertura.'),
 r'Il denominatore fa parte della definizione scientifica della statistica.',notebook=6,source=[7,9,26])

slide(32,'Laboratorio: conservare il dominio osservato',
 experiment('maschere','Esperimento online · maschere e superficie')+
 table(['Attività','Controllo'],[
 ['N04: NoData','24 celle mancanti, zero distinto'],
 ['N05: ritaglio','132 centri inclusi nella finestra'],
 ['N06: area','900 m² per cella nel piano'],
 ['Consegna','Quote, maschera e copertura'],
 ['Interpretazione','Dominio al quale si riferisce la media']], [4.2,4.8]),
 p(r'La consegna permette di ricostruire le esclusioni e il loro effetto. Ogni confronto conserva la definizione del dominio.')+
 info(r'Passare a una nuova risoluzione cambierà il modo in cui le celle rappresentano quel dominio. La maschera dovrà seguire anche questa trasformazione.'),
 r'Le celle escluse devono rimanere riconoscibili dopo ogni passaggio.',notebook=6,source=[7,8,9,30])

slide(33,'Cambiare griglia richiede di scegliere l’operazione',
 table(['Operazione','Scopo'],[
 ['Aggregare','Riassumere gruppi di celle'],
 ['Disaggregare','Suddividere la geometria delle celle'],
 ['Ricampionare','Stimare valori su una griglia diversa'],
 ['Riproiettare','Trasformare il riferimento e definire l’uscita'],
 ['Ritagliare','Selezionare un’estensione']], [3.6,5.4]),
 p(r'Le operazioni possono produrre immagini simili ma hanno significati differenti. Esplicitiamo sempre griglia di partenza, griglia di arrivo e regola per i valori.')+
 info(r'La geometria obiettivo include passo, origine, estensione e CRS. Un numero di righe e colonne non è sufficiente.')+
 p(r'Il metodo dipende anche dal tipo di variabile: quota continua, categoria o quantità da conservare.'),
 r'La trasformazione della griglia e quella dei valori devono essere documentate insieme.',source=[10,11,12,13])

slide(34,'Quattro celle diventano una media',
 fig('aggregazione_2x2',r'Confronto fra griglia originale da 30 m e aggregazione 2×2 da 60 m. Scala delle quote comune.'),
 p(r'I blocchi sono completi e allineati con l’origine. Ogni nuovo valore riassume quattro quote; il numero di celle passa da 720 a 180.')+
 info(r'Il dominio esterno resta lo stesso. Il valore del blocco rappresenta una media dei quattro valori, con perdita di dettaglio locale.'),
 r'Una cella aggregata ha un supporto diverso da quello dei valori di partenza.',
 code('r60 <- terra::aggregate(r,fact=2,\n                       fun=mean)\nstopifnot(terra::ncell(r60)==180,\n all(terra::res(r60)==60))','R · aggregazione dichiarata'),notebook=7,source=[10])

slide(35,'La conservazione della media deriva dai pesi',
 eq(r"""\overline z_b=\frac14\sum_{k\in b}z_k""")+
 eq(r"""\frac1{180}\sum_{b=1}^{180}\overline z_b
       =\frac1{720}\sum_{k=1}^{720}z_k""")+
 info(r'La relazione vale per 180 blocchi completi, ciascuno formato da quattro celle con lo stesso peso.'),
 p(r'Il risultato è un’identità algebrica. Non dimostra che le distribuzioni o le forme locali del terreno restino uguali.')+
 sm(r'Verifichiamo separatamente media, intervallo dei valori, risoluzione ed estensione.'),
 r'La media globale si conserva perché ogni valore di partenza riceve lo stesso peso finale.',
 code('m30 <- mean(terra::values(r))\nm60 <- mean(terra::values(r60))\nstopifnot(abs(m30-m60)<1e-9)','R · controllo della media'),notebook=7,source=[10])

slide(36,'I blocchi con mancanti possono avere pesi diversi',
 eq(r"""\overline z_{\mathrm{disp}}
 =\frac{\sum_b n_b\,\overline z_b}{\sum_b n_b}""")+
 table(['Blocco','Valori validi','Media'],[
 ['A','1','10'],
 ['B','3','20'],
 ['Media dei quattro valori','4','17,5'],
 ['Media semplice dei blocchi','2 blocchi','15']], [3.8,2.2,2.7]),
 p(r'Dopo na.rm=TRUE, due medie di blocco possono riassumere quantità diverse di celle valide. La loro media semplice cambia i pesi.')+
 info(r'Pesare per $n_b$ ricostruisce la media dei disponibili. Per inferire la media del dominio completo occorrono ulteriori ipotesi sulla mancanza.'),
 r'Il conteggio delle celle valide deve accompagnare il valore di ogni blocco.',
 code('nb <- c(1,3); mb <- c(10,20)\nc(per_cella=weighted.mean(mb,nb),\n per_blocco=mean(mb))','R · due pesature'),notebook=7,source=[10])

slide(37,'Un massimo aggregato descrive una scala diversa',
 fig('statistiche_aggregazione',r'Minimo, media e massimo prima e dopo l’aggregazione. Le differenze sono calcolate sullo stesso dominio.'),
 p(r'La media di un blocco è compresa fra i suoi valori estremi. Di conseguenza il massimo delle medie non può superare il massimo originale.')+
 info(r'Una cima stretta può attenuarsi nella griglia aggregata. La sua minore quota rappresentata non implica un cambiamento del terreno.')+
 p(r'Le differenze dipendono da come le forme si collocano rispetto ai blocchi e dalla scala scelta.'),
 r'La perdita di dettaglio morfologico può essere rilevante anche quando la media globale rimane identica.',notebook=7,source=[10,11])

slide(38,'Più celle memorizzate non aggiungono misure',
 eq(r"""n_{\mathrm{nuovo}}=n_{\mathrm{origine}}
 \left(\frac{\Delta_{\mathrm{origine}}}{\Delta_{\mathrm{nuovo}}}\right)^2""")+
 info(r'Relazione per celle quadrate sullo stesso dominio, con suddivisione compatibile. Da 30 a 10 m, il conteggio cresce di un fattore nove.'),
 p(r'La disaggregazione può copiare i valori oppure un ricampionamento può interpolarli. In entrambi i casi il dato originario resta quello della griglia di partenza.')+
 p(r'Una rappresentazione più fitta può essere utile per allineare prodotti, ma non giustifica interpretazioni a una nuova scala di misura.')+
 sm(r'Dimensione del pixel in uscita e capacità di risolvere strutture vicine devono restare distinte.'),
 r'Una griglia più fitta descrive una scelta di rappresentazione e di calcolo.',source=[11])

slide(39,'Interpolare una superficie continua',
 fig('ricampionamento_continuo',r'Confronto di regole di ricampionamento sullo stesso campo e sulla stessa griglia obiettivo.'),
 p(r'Il vicino più prossimo seleziona un valore esistente. L’interpolazione combina valori circostanti secondo una regola dichiarata.')+
 info(r'La superficie più liscia può essere utile per una variabile continua, ma la sua accuratezza richiede un riferimento di verifica.')+
 p(r'Ai bordi e vicino ai mancanti bisogna controllare quali contributi sono disponibili.'),
 r'Il metodo di ricampionamento deve essere coerente con la variabile e con il compito.',notebook=8,source=[12])

slide(40,'La combinazione bilineare usa pesi geometrici',
 bilinear()+
 eq(r"""\widehat z=(1-u)(1-v)z_{00}+u(1-v)z_{10}
                 +(1-u)vz_{01}+uvz_{11}"""),
 p(r'Nello schema, $u$ e $v$ sono posizioni relative comprese fra zero e uno. I quattro pesi sono non negativi e sommano a uno.')+
 info(r'È un modello locale di interpolazione fra quattro centri. Nel software specifichiamo il metodo effettivo e controlliamo anche bordi, mancanti e cambiamenti di scala.')+
 p(r'La formula conserva una costante e riproduce un piano all’interno del rettangolo.'),
 r'I pesi rendono verificabili le proprietà della regola di interpolazione.',source=[12])

slide(41,'Le categorie richiedono regole proprie',
 fig('ricampionamento_categorie',r'Le categorie 1 e 2 rappresentano classi nominali. Il valore interpolato 1,5 non identifica una terza classe valida.'),
 p(r'Una carta litologica richiede una regola che conservi il significato delle categorie, come il vicino più prossimo o una sintesi modale dichiarata.')+
 info(r'Il risultato dipende anche dalle regole di pareggio e dalla posizione dei confini rispetto alle celle.')+
 p(r'Il fatto che i codici siano numerici non autorizza a trattarli come una scala quantitativa.'),
 r'La scelta del metodo segue il significato della variabile, non il formato numerico della colonna.',notebook=8,source=[12])

slide(42,'Quale proprietà deve conservarsi?',
 table(['Variabile','Domanda da verificare'],[
 ['Quota o temperatura','La regola ricostruisce una grandezza continua?'],
 ['Quantità totale per cella','La somma si conserva sul dominio?'],
 ['Densità per unità di area','Il peso considera l’area rappresentata?'],
 ['Categoria nominale','I codici restano appartenenti alle classi?'],
 ['Maschera di validità','Che cosa rende valida una cella di uscita?']], [4.0,5.0]),
 p(r'Una media è adatta a riassumere alcuni campi intensivi. Una quantità totale per cella richiede di considerare come viene distribuita o sommata.')+
 info(r'Prima dell’operazione scegliamo una proprietà controllabile: media, somma, intervallo, appartenenza o copertura.')+
 p(r'La stessa procedura non conserva automaticamente tutte queste proprietà.'),
 r'Un controllo di conservazione deve essere scelto in funzione della quantità scientifica.',source=[10,12])

slide(43,'Stessa forma della matrice, origine diversa',
 fig('allineamento_mezzo_pixel',r'Due griglie di passo 30 m traslate di 15 m lungo Est. Le dimensioni delle matrici coincidono; i centri no.'),
 p(r'Una sottrazione per indice associa luoghi differenti. Il problema può restare poco visibile quando il campo varia gradualmente.')+
 info(r'Prima di combinare bande o epoche confrontiamo CRS, estensione, risoluzione e origine.'),
 r'La compatibilità degli array deve essere verificata anche nella geometria territoriale.',
 code('origine_A <- c(500000,5000000)\norigine_B <- origine_A+c(15,0)\n(origine_B-origine_A)/30','R · spostamento in pixel'),notebook=19,source=[13])

slide(44,'La griglia obiettivo rende esplicito l’allineamento',
 boxes([('a',2.1,3.8,'Raster da trasformare',3.7,'GeoA'),
        ('b',7.3,3.8,'Griglia obiettivo dichiarata',3.7,'GeoB'),
        ('c',2.1,1.2,'Metodo coerente con i valori',3.7,'GeoC'),
        ('d',7.3,1.2,'Valori e geometria verificati',3.7,'GeoA')],
       [('a','c',''),('b','d',''),('c','d','')]),
 p(r'Il ricampionamento trasferisce i valori sulla geometria del modello di riferimento. Se cambia il CRS, occorre una riproiezione.')+
 info(r'Conserviamo la griglia obiettivo nel progetto. Controlliamo anche maschere e significato dei valori.'),
 r'Una griglia comune è una decisione del progetto che deve poter essere ricostruita.',
 code('r_shift <- terra::shift(r,dx=15)\nterra::compareGeom(r,r_shift,\n                   stopOnError=FALSE)\nr_align <- terra::resample(r_shift,r,\n method="bilinear")','R · allineare una griglia'),notebook=19,source=[13])

slide(45,'Lo scarto prodotto da mezzo pixel',
 fig('15_allineamento_errori',r'Stessi valori attribuiti a una griglia spostata di 15 m verso Est e poi riallineati: scarto dalla superficie originale.',height=4.4)+
 eq(r"""f(x-\delta,y)-f(x,y)\approx-\delta\,f_x(x,y)"""),
 p(r'Spostare la georeferenziazione dei valori verso Est costruisce un campo traslato. La differenza può derivare dalla geometria anziché da un cambiamento del terreno.')+
 info(r'Sul piano $f=ax+by+c$ lo scarto interno è $-a\delta$. Vicino ai bordi intervengono anche le regole del ricampionamento.'),
 r'La verifica geometrica viene prima dell’interpretazione delle mappe di cambiamento.',
 code('a <- 0.12; delta <- 15\nscarto_atteso <- -a*delta\nstopifnot(abs(scarto_atteso+1.8)<1e-12)','R · effetto noto della traslazione'),notebook=19,source=[13,15])

panorama(46,'Il passo cambia il campionamento',
 'sensibilita_risoluzione',
 r'Esperimento analitico separato dal raster originale: stesso campo e dominio di 900×600 m, griglie di 10, 30 e 100 m. I valori sono valutati secondo la regola documentata nel codice; non sono nuove misure del terreno del corso. La scala cromatica comune rende confrontabile il dettaglio rappresentato.',
 r'Per isolare l’effetto della risoluzione manteniamo fissi campo, dominio e regola di campionamento.',source=[11,17,30])

slide(47,'Prima aggregare o prima derivare?',
 boxes([('a',2.1,3.8,'Quote a 30 m',3.7,'GeoA'),
        ('b',7.3,3.8,'Medie delle quote a 60 m',3.7,'GeoB'),
        ('c',2.1,1.2,'Pendenze a 30 m, poi media',3.7,'GeoA'),
        ('d',7.3,1.2,'Pendenze calcolate a 60 m',3.7,'GeoB')],
       [('a','b',''),('a','c',''),('b','d','')])+
 eq(r"""\overline{\alpha(z_{30})}\ \ne\
       \alpha(\overline z_{60})\quad\text{in generale}"""),
 p(r'Una derivata calcolata dopo l’aggregazione usa un campo più liscio e un passo diverso. La media di pendenze già calcolate riassume invece una grandezza non lineare.')+
 info(r'Non assumiamo l’uguaglianza dei due risultati. Li confrontiamo sul dominio valido comune, considerando anche i bordi.')+
 p(r'La scala del DEM deve accompagnare la carta delle pendenze e ogni confronto fra prodotti.'),
 r'Il metodo deve specificare sia l’operazione sia l’ordine in cui viene applicata.',notebook=7,source=[10,17,30])

slide(48,'Laboratorio: trasformare la griglia con un controllo',
 experiment('ricampionamento','Esperimento online · aggregare e ricampionare')+
 experiment('allineamento','Esperimento online · allineamento')+
 table(['Attività','Verifica'],[
 ['N07: aggregazione','180 blocchi completi, media conservata'],
 ['N08: metodo','Quote continue e categorie distinte'],
 ['N19: origine','Traslazione di mezzo pixel riconosciuta'],
 ['Approfondimento','Risoluzioni 10, 30 e 100 m'],
 ['Consegna','Geometria obiettivo, metodo e maschere']], [4.2,4.8]),
 p(r'La trasformazione deve produrre un oggetto interpretabile e controllabile. Una figura più gradevole non basta a stabilire la qualità del dato.')+
 info(r'Le prossime sezioni useranno la griglia originale da 30 m per le differenze centrate, salvo esperimenti di sensibilità esplicitamente indicati.'),
 r'La trasformazione è riuscita quando valori, geometria e proprietà attese risultano coerenti.',notebook=19,source=[10,11,12,13,30])
