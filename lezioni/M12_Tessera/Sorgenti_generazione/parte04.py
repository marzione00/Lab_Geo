"""Bande, indici e sintesi territoriali: pagine 77–102."""
from componenti import *

slide(77,'Le bande collegano posizione e risposta spettrale',
 layers(),
 p(r'Una banda associa un valore a ciascuna cella per una parte dello spettro e per una specifica acquisizione. La geometria deve restare collegata ai metadati radiometrici.')+
 info(r'Il modulo usa due bande sintetiche, rosso e vicino infrarosso. Non sono immagini satellitari reali e non consentono una classificazione ecologica del territorio.')+
 p(r'Il caso serve a verificare allineamento, trasformazioni numeriche e comportamento dell’indice.'),
 r'Prima del rapporto fra bande verifichiamo geometria, unità e qualità dei valori.',source=[23])

panorama(78,'Due bande sintetiche sulla stessa griglia',
 '27_bande_R_NIR',
 r'Rosso e vicino infrarosso sono costruiti matematicamente sulla griglia locale. Le carte riportano la stessa geometria; le scale dei valori e la natura sintetica sono esplicite. L’indice verrà calcolato soltanto dopo il controllo della corrispondenza fra le celle.',
 r'La combinazione fra bande richiede che i valori confrontati rappresentino posizioni e supporti compatibili.',notebook=13,source=[23])

slide(79,'Il caso sintetico rende verificabili i valori',
 eq(r"""R(y)=0{,}20+0{,}05\cos\!\left(\frac{y}{150\ \mathrm m}\right)""")+
 eq(r"""N(x)=0{,}40+0{,}10\sin\!\left(\frac{x}{180\ \mathrm m}\right)""")+
 info(r'$R$ e $N$ rappresentano riflettanze sintetiche adimensionali. Gli argomenti delle funzioni trigonometriche sono adimensionali.'),
 p(r'I valori sono positivi e variano in modo controllato. L’assenza di un denominatore nullo si può verificare direttamente.')+
 sm(r'Le funzioni definiscono l’esperimento didattico; non sono un modello fisico della vegetazione o di una litologia.'),
 r'La provenienza sintetica consente di conoscere le proprietà del dato prima di applicare l’indice.',
 code('R_band <- 0.2+0.05*cos(d$y_m/150)\nNIR <- 0.4+0.1*sin(d$x_m/180)\nstopifnot(all(R_band>=0),all(NIR>=0))','R · costruire le due bande'),notebook=13,source=[23])

slide(80,'L’indice normalizzato misura un contrasto relativo',
 eq(r"""I=\frac{N-R}{N+R}""")+
 eq(r"""N\ge0,\ R\ge0,\ N+R>0\quad\Longrightarrow\quad -1\le I\le1""")+
 info(r'La formula coincide con quella dell’NDVI quando $N$ e $R$ sono bande appropriate di vicino infrarosso e rosso. Qui resta un indice di bande sintetiche.'),
 p(r'Il numeratore descrive la differenza, il denominatore la normalizza rispetto alla somma. Il risultato non ha unità fisica.')+
 sm(r'La normalizzazione non sostituisce le verifiche radiometriche o geometriche.'),
 r'Un rapporto acquista significato scientifico dalle variabili che contiene e dalle condizioni del calcolo.',
 code('indice <- (NIR-R_band)/(NIR+R_band)\nstopifnot(all(is.finite(indice)),\n          all(abs(indice)<=1))','R · indice e condizioni'),notebook=13,source=[23])

slide(81,'Lo stesso indice può derivare da valori diversi',
 fig('29_spettro_indice',r'Confronto fra valori delle bande e indice normalizzato: il rapporto sintetizza il contrasto e perde parte dell’informazione originaria.'),
 p(r'Le coppie $(R,N)=(0{,}2,0{,}4)$ e $(0{,}1,0{,}2)$ producono entrambe $I=1/3$. La somma delle bande è però diversa.')+
 info(r'Conserviamo quindi le bande e gli indicatori di qualità insieme all’indice. Un valore isolato non ricostruisce il segnale di partenza.')+
 p(r'L’interpretazione dipende dal prodotto, dal supporto e dalle condizioni di acquisizione.'),
 r'Un indice è una sintesi: il suo uso richiede di riconoscere quale informazione viene conservata.',notebook=13,source=[23])

slide(82,'Un fattore comune si cancella, un offset no',
 fig('31_scaling_offset',r'Bande sintetiche codificate con scala e offset: indice applicato ai numeri memorizzati e indice dopo la conversione.')+
 eq(r"""\frac{cN-cR}{cN+cR}=\frac{N-R}{N+R},\qquad c>0"""),
 p(r'Il rapporto è invariato se entrambe le bande sono moltiplicate per lo stesso fattore positivo. Un termine additivo comune modifica invece il denominatore.')+
 info(r'Le conversioni dei valori memorizzati devono seguire i metadati del prodotto. Fattori differenti fra bande non si cancellano in generale.'),
 r'La normalizzazione non autorizza a ignorare scale e offset radiometrici.',
 code('I0 <- (NIR-R_band)/(NIR+R_band)\nI2 <- (2*NIR-2*R_band)/(2*NIR+2*R_band)\nstopifnot(max(abs(I0-I2))<1e-12)','R · invarianza verificabile'),source=[23])

slide(83,'L’allineamento delle bande precede l’algebra',
 table(['Controllo','Motivo'],[
 ['Stesso riferimento','Posizioni espresse nello stesso sistema'],
 ['Stessi centri','Rapporto fra valori dello stesso luogo'],
 ['Supporto compatibile','Confronto della stessa scala spaziale'],
 ['Acquisizione documentata','Interpretazione delle differenze temporali'],
 ['Qualità e maschere','Esclusione dei valori non utilizzabili']], [4.0,5.0]),
 p(r'Due bande con la stessa forma di matrice possono essere traslate. Il rapporto sarebbe numericamente calcolabile, ma combinerebbe luoghi diversi.')+
 info(r'Il controllo di mezzo pixel studiato in precedenza vale anche qui. Dopo un eventuale ricampionamento conserviamo metodo e griglia obiettivo.')+
 p(r'Le maschere devono essere combinate sullo stesso insieme di posizioni.'),
 r'La compatibilità numerica degli array non basta per definire un indice geograficamente coerente.',notebook=19,source=[13,23])

slide(84,'Un denominatore piccolo amplifica le perturbazioni',
 fig('30_denominatore',r'Sensibilità del rapporto quando la somma delle bande si avvicina a zero. Le soglie appartengono al protocollo dichiarato.'),
 p(r'Un valore finito può essere instabile. Piccole variazioni delle bande possono produrre grandi variazioni del rapporto quando la loro somma è piccola.')+
 info(r'La soglia va scelta rispetto a precisione e rumore dei dati. Il valore $10^{-6}$ usato nell’esercizio è una convenzione didattica, non una soglia universale.')+
 p(r'Il risultato deve conservare anche le celle escluse dal criterio.'),
 r'La validità numerica e la stabilità del risultato sono proprietà da controllare separatamente.',notebook=14,source=[24])

slide(85,'Le derivate descrivono la sensibilità dell’indice',
 eq(r"""\frac{\partial I}{\partial N}=\frac{2R}{(N+R)^2},
       \qquad
       \frac{\partial I}{\partial R}=-\frac{2N}{(N+R)^2}""")+
 eq(r"""\delta I\approx
      \frac{\partial I}{\partial N}\delta N+
      \frac{\partial I}{\partial R}\delta R""")+
 info(r'Approssimazione locale al primo ordine, dove il denominatore è diverso da zero e le perturbazioni sono piccole.'),
 p(r'Le due componenti possono avere effetti opposti. La sensibilità dipende dalla somma e dai valori delle singole bande.')+
 p(r'Per quantificare l’incertezza servono anche variabilità e covarianza degli errori delle bande. La formula dell’indice, da sola, non le fornisce.'),
 r'La stabilità del rapporto deve essere discussa rispetto alle perturbazioni plausibili dei dati.',notebook=14,source=[24])

slide(86,'La soglia viene applicata prima della divisione',
 table(['R','N','Somma','Uso'],[
 ['0,2','0,4','0,6','sì'],
 ['0','0','0','no'],
 [r'$10^{-10}$',r'$2\cdot10^{-10}$',r'$3\cdot10^{-10}$','no'],
 ['0,3','0,2','0,5','sì']], [1.8,2.0,2.5,1.8]),
 p(r'Il criterio evita la divisione nelle celle escluse. Quelle celle rimangono mancanti, con una causa documentata.')+
 info(r'Abbassare la soglia per ottenere più valori finiti non garantisce un risultato più informativo.'),
 r'La maschera deve essere una scelta esplicita del calcolo, applicata in modo riproducibile.',
 code('R0 <- c(.2,0,1e-10,.3)\nN0 <- c(.4,0,2e-10,.2)\nok0 <- N0+R0>1e-6\nItoy <- rep(NA_real_,4)\nItoy[ok0] <- (N0[ok0]-R0[ok0])/\n              (N0[ok0]+R0[ok0])','R · maschera prima del rapporto'),notebook=14,source=[25])

slide(87,'La maschera dell’indice combina le condizioni',
 eq(r"""m=m_{\mathrm{geometria}}\,
          m_{\mathrm{qualità}}\,
          m_{\mathrm{valori}}\,
          m_{\mathrm{denominatore}}""")+
 info(r'Gli indicatori valgono zero o uno. Il prodotto corrisponde alla congiunzione delle condizioni necessarie.'),
 p(r'Distinguiamo valore non finito, qualità non ammessa e somma insufficiente. La maschera finale identifica dove l’indice è utilizzabile.')+
 sm(r'Nel caso sintetico principale tutte le bande sono valide; il notebook N14 costruisce i casi problematici.'),
 r'Le cause di esclusione devono essere conservate prima della loro combinazione.',
 code('okI <- is.finite(R_band) &\n is.finite(NIR) & (R_band+NIR>1e-6)\nIval <- rep(NA_real_,length(NIR))\nIval[okI] <- (NIR[okI]-R_band[okI])/\n              (NIR[okI]+R_band[okI])','R · dominio valido dell’indice'),notebook=14,source=[25])

slide(88,'Una scala leggibile per l’indice',
 fig('28_indice_normalizzato',r'Indice delle bande sintetiche sulla griglia locale. La legenda dichiara la natura adimensionale e l’intervallo rappresentato.'),
 p(r'Il colore mostra il contrasto fra le bande. Nel caso costruito non identifica automaticamente vegetazione, litologia o qualità ambientale.')+
 info(r'Per confrontare due carte usiamo scale cromatiche coerenti e riportiamo le differenze nelle maschere.')+
 p(r'Le bande originali e i parametri del calcolo accompagnano l’esportazione dell’indice.'),
 r'La carta deve distinguere il valore calcolato dalle interpretazioni che richiederebbero ulteriori dati.',notebook=13,source=[23,25])

slide(89,'I controlli devono riconoscere dati incoerenti',
 table(['Prova','Aspettativa'],[
 [r'$N=R>0$','Indice zero'],
 [r'$R=0,\ N>0$','Indice uno'],
 [r'$N=0,\ R>0$','Indice meno uno'],
 ['Entrambe le bande nulle','Cella esclusa'],
 ['Bande non negative e somma positiva','Indice fra −1 e 1']], [4.4,4.6]),
 p(r'Valori fuori dall’intervallo teorico richiedono di esaminare le condizioni sulle bande. Non li correggiamo automaticamente con un taglio arbitrario.')+
 info(r'Anche un indice nell’intervallo può essere sbagliato se le bande sono disallineate o hanno unità incompatibili.'),
 r'I controlli numerici verificano condizioni precise e non sostituiscono l’esame dei metadati.',
 code('stopifnot(sum(is.na(Itoy))==2,\n abs(Itoy[1]-1/3)<1e-12,\n abs(Itoy[4]+0.2)<1e-12)','R · casi di risultato noto'),notebook=14,source=[23,24,25])

slide(90,'Consegna: indice e condizioni',
 experiment('indici','Esperimento online · bande e indice')+
 table(['Attività','Evidenza'],[
 ['N13: bande sintetiche','Formule, geometria e valori'],
 ['N14: denominatore','Soglia e celle escluse'],
 ['Controllo algebrico','Casi noti e fattore comune'],
 ['Controllo geografico','Corrispondenza delle celle'],
 ['Consegna','Indice, maschera e provenienza']], [4.3,4.7]),
 p(r'La relazione deve rendere chiaro che cosa rappresenta il rapporto e quali condizioni lo rendono utilizzabile.')+
 info(r'Le sintesi territoriali successive conserveranno la maschera, il dominio e i pesi: il passaggio a una tabella non elimina la struttura spaziale.'),
 r'Un indice riproducibile include le condizioni che permettono di calcolarlo e interpretarlo.',notebook=14,source=[23,24,25,30])

slide(91,'Le zone cambiano l’unità della tabella',
 fig('32_zone',r'Zone didattiche A e B sullo stesso terreno: 360 celle per zona, ciascuna di area piana 0,09 ha.'),
 p(r'Una sintesi zonale produce una riga per regione. I valori riassumono insiemi di celle definiti da una regola di appartenenza.')+
 info(r'A e B sono convenzioni del caso sintetico. Non rappresentano gruppi sperimentali assegnati casualmente né unità geologiche osservate.')+
 p(r'Conserviamo numerosità, area e copertura insieme alla statistica.'),
 r'Passare dalle celle alle zone cambia l’unità statistica e il significato della riga.',notebook=15,source=[26])

slide(92,'Media e dispersione nella stessa zona',
 fig('33_sintesi_zonali',r'Sintesi delle quote nelle due zone: livello, dispersione e numerosità devono essere letti insieme.'),
 p(r'La media descrive il livello delle quote. La dispersione descrive la variabilità interna; la copertura identifica il dominio disponibile.')+
 info(r'La differenza fra le zone riflette la loro collocazione sul terreno sintetico. Non viene interpretata come effetto causale dell’etichetta.'),
 r'Una tabella zonale deve conservare gli elementi necessari a ricostruire il bersaglio della sintesi.',
 code('zm <- aggregate(quota_m~unita,d,mean)\nzn <- table(d$unita)\nstopifnot(sum(zn)==720)\nzm','R · livello e conteggi'),notebook=15,source=[26])

slide(93,'La media del territorio richiede pesi coerenti',
 fig('34_pesi_aree',r'Dopo la maschera restano 336 celle in A e 360 in B. Pesare per area osservata ricostruisce la media delle 696 celle disponibili.')+
 eq(r"""\overline z_A=\frac{\sum_b A_b\,\overline z_b}{\sum_b A_b}"""),
 p(r'Con zone della stessa area e copertura completa, media semplice delle medie e media per area coincidono. Non è una proprietà generale.')+
 info(r'La formula richiede che le medie zonali rappresentino le aree assegnate. Una copertura incompleta può richiedere un trattamento aggiuntivo.')+
 p(r'La definizione dei pesi segue la domanda scientifica.'),
 r'Il peso di una zona deve essere dichiarato insieme alla popolazione o al territorio che rappresenta.',notebook=15,source=[9,26])

slide(94,'La copertura può differire fra le zone',
 table(['Zona','Celle disponibili','Copertura'],[
 ['A dopo la maschera','336 su 360',r'93,33\%'],
 ['B dopo la maschera','360 su 360',r'100\%'],
 ['Intero dominio','696 su 720',r'96,67\%']], [3.0,3.2,2.4]),
 p(r'La finestra mancante cade interamente nella zona A. La stessa percentuale globale nasconde quindi una distribuzione geografica asimmetrica delle esclusioni.')+
 info(r'Confrontiamo medie zonali e coperture prima di interpretare la differenza fra A e B.'),
 r'La copertura globale deve essere accompagnata dalla sua distribuzione nel territorio.',
 code('okZ <- with(d,!(riga %in% 4:7 &\n                 colonna %in% 9:14))\ntable(d$unita[okZ])/table(d$unita)','R · copertura per zona'),notebook=15,source=[7,26])

slide(95,'Molti pixel non sono molte repliche indipendenti',
 table(['Conteggio','Significato'],[
 ['720 celle','Dimensione della griglia'],
 ['64,8 ettari','Area piana del dominio'],
 ['2 zone','Unità della tabella aggregata'],
 ['12 blocchi didattici','Unità dello schema di ricampionamento'],
 ['Repliche indipendenti','Proprietà del disegno o del modello']], [4.2,4.8]),
 p(r'La continuità della superficie crea relazioni fra celle vicine. Un test che tratta ogni pixel come una replica indipendente richiederebbe una giustificazione specifica.')+
 info(r'La differenza descrittiva fra le quote di A e B è calcolabile. L’inferenza su un processo o su altri territori richiede ipotesi ulteriori.')+
 p(r'Le categorie del conteggio non devono essere confuse fra loro.'),
 r'La numerosità del file non determina automaticamente la quantità di informazione indipendente.',source=[26,27,28])

slide(96,'Le differenze a distanza descrivono due scale',
 fig('35_differenze30_300',r'Differenze longitudinali a 30 m e 300 m: 696 e 480 coppie rispettivamente, costruite nella stessa superficie.'),
 p(r'Le coppie possono condividere celle e risentono della tendenza del terreno. Il confronto descrive come cambia il campo a due separazioni.')+
 info(r'Non presentiamo i contributi come repliche indipendenti né il confronto come un test causale.'),
 r'La distanza delle coppie e il loro riuso delle celle devono accompagnare la statistica.',
 code('d30 <- as.vector(Z[,2:30]-Z[,1:29])\nd300 <- as.vector(Z[,11:30]-Z[,1:20])\nstopifnot(length(d30)==696,\n          length(d300)==480)\nc(mean(abs(d30)),mean(abs(d300)))','R · due separazioni spaziali'),notebook=16,source=[27])

slide(97,'La varianza della media include le covarianze',
 eq(r"""\operatorname{Var}(\overline Z)
 =\frac1{n^2}\sum_i\sum_j\operatorname{Cov}(Z_i,Z_j)""")+
 eq(r"""=\frac1{n^2}\left\{\sum_i\operatorname{Var}(Z_i)
       +2\sum_{i<j}\operatorname{Cov}(Z_i,Z_j)\right\}""")+
 info(r'La relazione riguarda variabili aleatorie. Una superficie sintetica completamente nota ha una media finita calcolabile senza errore di campionamento.'),
 p(r'Per discutere l’incertezza su un processo o su territori non osservati serve un modello o un disegno che definisca la variabilità.')+
 p(r'Il rapporto fra numero di celle e precisione non dipende soltanto dalla varianza marginale. Le covarianze possono contribuire in modo sostanziale.'),
 r'L’incertezza va riferita a un bersaglio e a un meccanismo di variazione espliciti.',source=[27])

slide(98,'Il ricampionamento a blocchi dichiara nuove unità',
 fig('36_blocchi12',r'Dodici blocchi contigui: 6 righe e 10 colonne ciascuno, 60 celle e 5,4 ha di area piana per blocco.'),
 p(r'Calcoliamo la media di ciascun blocco. Ricampioniamo poi dodici medie con reinserimento per ottenere una nuova media complessiva.')+
 info(r'I blocchi sono completi ed equiponderati: la media delle dodici medie coincide con quella delle 720 quote.'),
 r'Lo schema di ricampionamento deve essere descritto nella geometria e nei pesi.',
 code('stopifnot(length(block_means)==12,\n abs(mean(block_means)-mean(Z))<1e-10)\nmean(block_means)','R · controllare il bersaglio'),notebook=17,source=[28])

panorama(99,'Due distribuzioni da ricampionamento',
 '37_bootstrap300_1999',
 r'Dodici medie di blocco ricampionate con reinserimento. La serie di 300 repliche usa i numeri uniformi comuni del laboratorio originale; quella di 1999 usa il seme documentato della figura originale. I quantili descrivono queste distribuzioni condizionate allo schema. Il numero di repliche cambia la precisione Monte Carlo, non giustifica le ipotesi inferenziali.',
 r'Aumentare le repliche rende più preciso il calcolo dello schema scelto, non rende automaticamente valido lo schema.',notebook=17,source=[28])

slide(100,'Il bersaglio guida la scelta dei blocchi',
 eq(r"""\overline Z^*=\frac1{12}\sum_{b=1}^{12}\overline Z_{J_b},
 \qquad J_b\overset{\mathrm{iid}}{\sim}\operatorname{Unif}\{1,\ldots,12\}""")+
 info(r'L’indipendenza riguarda le estrazioni degli indici nello schema bootstrap. Non dimostra che i dodici blocchi del terreno siano indipendenti o scambiabili.'),
 p(r'Blocchi vicini possono restare dipendenti. Un gradiente può rendere le loro distribuzioni diverse.')+
 p(r'Nel caso didattico i quantili sono un’analisi di sensibilità allo schema, non un intervallo con copertura garantita per una popolazione geografica non definita.'),
 r'Le ipotesi del ricampionamento devono essere motivate rispetto a dipendenza, tendenza e popolazione.',notebook=17,source=[28])

slide(101,'Cambia l’unità, cambia il risultato',
 fig('38_bootstrap_confronto',r'Confronto fra schemi di ricampionamento. Le distribuzioni riflettono la scelta delle unità e delle ipotesi.'),
 p(r'Ricampionare singole celle rompe le relazioni locali. Ricampionare blocchi conserva parte della struttura, ma introduce scelte su forma, dimensione e disposizione.')+
 info(r'Un intervallo più ampio non è automaticamente corretto. La validità richiede che il meccanismo rappresenti l’incertezza del compito.')+
 p(r'I registri conservano parametri, semi e quantili per rendere verificabile la sensibilità.'),
 r'Il confronto fra schemi serve a esaminare le assunzioni, non a scegliere il risultato più conveniente.',notebook=17,source=[27,28])

slide(102,'Laboratorio: collegare sintesi, dominio e ipotesi',
 experiment('zone','Esperimento online · sintesi zonali')+
 table(['Attività','Evidenza'],[
 ['N15: zone','Medie, dispersione, conteggi e copertura'],
 ['N16: distanze','Coppie a 30 e 300 m'],
 ['N17: blocchi','Geometria e regola di ricampionamento'],
 ['Confronto','Sensibilità alle unità scelte'],
 ['Conclusione','Bersaglio e limiti dell’inferenza']], [4.1,4.9]),
 p(r'La tabella finale mantiene il legame con la mappa. Ogni media indica quali celle rappresenta e con quali pesi.')+
 info(r'Il processo di esportazione conserverà queste decisioni insieme ai raster e ai risultati numerici.'),
 r'Una sintesi territoriale resta scientificamente leggibile quando conserva dominio, unità e assunzioni.',notebook=17,source=[26,27,28,30])
