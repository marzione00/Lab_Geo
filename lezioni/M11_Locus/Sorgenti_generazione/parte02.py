"""Carte, appartenenze, vicinati e pesi: pagine 32–55."""
from componenti import *

slide(32,'Una carta rende visibile una scelta statistica',
 table(['Elemento della carta','Scelta che comunica'],[
 ['Punti','Luoghi delle osservazioni'],
 ['Poligoni','Unità territoriali e supporti'],
 ['Colore','Valori e scala di confronto'],
 ['Linee','Confini, percorsi o vicinati'],
 ['Superficie continua','Una stima tra i campioni']], [3.2,5.8]),
 p(r'La forma grafica influenza la lettura del risultato. Ogni elemento deve corrispondere a un oggetto definito nell’analisi.')+
 info(r'Un’interpolazione richiede di mostrare anche i siti utilizzati. Senza campioni visibili, la carta nasconde dove la previsione è sostenuta dai dati.')+
 p(r'Manteniamo gli stessi limiti cromatici quando due pannelli devono essere confrontati.'),
 r'La legenda deve spiegare il dato, l’unità e l’eventuale modello dietro la rappresentazione.', notebook=7, source=[10])

slide(33,'Scale cromatiche comparabili, assi proporzionati',
 table(['Controllo','Perché serve'],[
 ['Rapporto 1:1 degli assi','Un metro ha la stessa lunghezza grafica'],
 ['Unità nei titoli degli assi','Evita di confondere gradi e metri'],
 ['Scala cromatica comune','Permette confronti quantitativi'],
 ['Legenda esplicita','Distingue valore, gruppo e previsione'],
 ['Simboli dei campioni','Mostra il supporto osservativo']], [4.0,5.0]),
 p(r'Un rettangolo disegnato come un quadrato altera la percezione delle distanze. Il parametro \texttt{asp=1} conserva le proporzioni nel piano locale.')+
 info(r'La palette rappresenta la concentrazione in u.a. Non indica da sola una soglia ambientale o una classe di rischio.'),
 r'Il confronto visivo richiede scale e unità costanti.',
 code('plot(d$x_m,d$y_m,asp=1,\n xlab="x locale (m)",\n ylab="y locale (m)",pch=19)\nstopifnot(all(is.finite(xy)))','R · geometria della carta'), notebook=7, source=[10])

slide(34,'Aggregare assegna campioni a unità territoriali',
 fig('08_confini_aggregazioni',r'La partizione del dataset separa Ovest ($x<1000$) ed Est ($x\ge1000$): 32 siti per gruppo.'),
 p(r'Per ogni area calcoliamo numerosità e media dei campioni assegnati. I conteggi sono necessari per interpretare le medie.')+
 info(r'Questa soglia descrittiva a 1000 m è diversa dalla separazione a 1250 m usata nel test previsionale. Le due operazioni hanno scopi diversi.'),
 r'Una media territoriale deve indicare quali campioni contiene e con quali pesi.',
 code('ovest <- d$x_m<1000\naggregate(concentrazione~area,\n data=d,FUN=mean)\ntable(d$area)\nstopifnot(sum(ovest)==32L)','R · aggregazione documentata'), notebook=8, source=[11])

slide(35,'Confini diversi producono riassunti diversi',
 fig('09_aggregazioni_alternative',r'Gli stessi siti possono essere raggruppati con partizioni diverse. Cambiano le unità della sintesi.'),
 p(r'Cambiare la scala o la disposizione dei confini può cambiare le medie, la variabilità tra aree e le relazioni osservate.')+
 info(r'Questa sensibilità è legata al problema delle unità areali modificabili. Un risultato riferito a una partizione non diventa automaticamente una proprietà delle singole persone, rocce o misure.')+
 p(r'Il confronto tra partizioni è una verifica di sensibilità; la partizione principale deve essere motivata prima di scegliere la figura più convincente.'),
 r'I confini sono parte dell’analisi e devono essere motivati insieme alle statistiche.', source=[11,24])

slide(36,'Una regola semiaperta evita doppie assegnazioni',
 fig('10_confini_semiaperti',r'Il confine $x=1000$ appartiene a Est. La partizione copre tutti i siti senza intersezioni.'),
 p(r'Le condizioni $x<1000$ e $x\ge1000$ definiscono due insiemi disgiunti e completi. Un punto sul confine riceve un’unica appartenenza.')+
 info(r'Con veri poligoni, il predicato spaziale e la gestione dei bordi devono essere dichiarati. “Dentro” e “interseca” non sono sinonimi.'),
 r'Una partizione richiede copertura completa e assenza di sovrapposizioni.',
 code('ov <- d$x_m<1000\nes <- !ov\nstopifnot(!any(ov & es),\n          all(ov | es))\nc(Ovest=sum(ov),Est=sum(es))','R · verificare la partizione'), notebook=8, source=[11])

slide(37,'Un sito può appartenere a più regioni',
 membership(),
 p(r'Consideriamo A definita da $x\le1250$ e B da $x\ge750$. L’intervallo comune comprende tre colonne della griglia.')+
 info(r'Le appartenenze sono 88, i siti restano 64 e quelli con due appartenenze sono 24. Il join descrive relazioni, non crea nuovi campioni.')+
 p(r'Una regione amministrativa disgiunta e un insieme di aree di influenza sovrapposte richiedono convenzioni differenti.'),
 r'Quando le aree si sovrappongono, il numero delle relazioni può superare il numero dei siti.', notebook=9, source=[11])

slide(38,'Controllare la cardinalità dopo un join',
 fig('11_join_sovrapposto',r'Due regioni sovrapposte generano più righe per gli stessi identificativi.'),
 p(r'Dopo un join confrontiamo righe, ID distinti e molteplicità. Ogni variazione deve avere una spiegazione geometrica o tabellare.')+
 info(r'Fare la media di tutte le righe del join assegnerebbe peso doppio ai siti nell’intersezione. È una scelta statistica, anche se avviene involontariamente.'),
 r'Il controllo delle molteplicità impedisce di confondere relazioni e osservazioni.',
 code('a <- d$id[d$x_m<=1250]\nb <- d$id[d$x_m>=750]\nfreq <- table(c(a,b))\nc(siti=length(freq),\n  relazioni=sum(freq),\n  multipli=sum(freq>1))','R · contare le appartenenze'), notebook=9, source=[11])

slide(39,'Il buffer definisce una domanda locale',
 fig('12_buffer_raggi',r'Centro $(750,750)$ m; raggi 300, 600 e 900 m. I campioni inclusi cambiano con la scala.'),
 p(r'Un buffer include i siti entro una distanza dal centro. La regola del laboratorio comprende anche i punti esattamente sul raggio.')+
 info(r'La media nel buffer riassume i campioni selezionati. Non è automaticamente la media areale del disco.'),
 r'Centro, raggio, metrica e regola del bordo definiscono il contenuto del buffer.',
 code('dist0 <- sqrt((d$x_m-750)^2+\n              (d$y_m-750)^2)\nraggi <- c(300,600,900)\nsapply(raggi,function(r)\n sum(dist0<=r))','R · inclusione nel buffer'), notebook=10, source=[12])

slide(40,'La media locale cambia quando cambia il raggio',
 eq(r'\bar z(r)=\frac{\sum_i z_i\,\mathbf1(d_{i0}\le r)}{\sum_i\mathbf1(d_{i0}\le r)}')+
 table(['Raggio più piccolo','Raggio più grande'],[
 ['Descrizione più locale','Copertura più ampia'],
 ['Possibili pochi campioni','Più campioni, anche lontani'],
 ['Maggiore sensibilità ai singoli siti','Possibile mescolamento di gradienti']], [4.5,4.5]),
 p(r'Aumentando il raggio, il numero dei siti non può diminuire. La media può aumentare o diminuire: dipende dai valori che entrano.')+
 info(r'Una curva di sensibilità deve mostrare insieme media e numerosità. Un punto della curva sostenuto da un solo campione ha un significato diverso.'),
 r'La scala locale va scelta e discussa; il numero più favorevole non è un criterio di selezione.',
 code('data.frame(raggio=raggi,\n n=sapply(raggi,function(r)\n   sum(dist0<=r)),\n media=sapply(raggi,function(r)\n   mean(z[dist0<=r])))','R · numerosità e media'), notebook=10, source=[12])

slide(41,'Un buffer al bordo osserva una parte del disco',
 bufferedge()+
 info(r'Il supporto desiderato e il dominio campionato possono non coincidere. Al bordo del dominio parte del vicinato può essere priva di osservazioni.'),
 p(r'La mancanza di siti oltre il bordo non dimostra che il fenomeno si arresti lì. Può dipendere soltanto dall’estensione del rilievo.')+
 p(r'Quando confrontiamo medie locali, registriamo quanti siti sono disponibili e come sono distribuiti rispetto al centro.')+
 sm(r'Eventuali correzioni di bordo richiedono un modello o un disegno appropriato; non si ottengono aggiungendo valori non osservati.'),
 r'Il confine del campionamento limita l’informazione disponibile sul vicinato.', source=[12,15])

slide(42,'Il disegno grafico non aggiunge osservazioni',
 table(['Operazione','Che cosa produce'],[
 ['Disegnare un punto','Rappresentazione di un campione'],
 ['Colorare un poligono con una media','Riassunto di campioni assegnati'],
 ['Raffinare una griglia grafica','Più posizioni di visualizzazione'],
 ['Interpolare sulla griglia','Previsioni dipendenti da una regola']], [4.2,4.8]),
 p(r'Una carta più liscia può facilitare la lettura, ma non aumenta il numero di misure disponibili. Le incertezze non scompaiono tra due pixel.')+
 info(r'Nel modulo la griglia di interpolazione contiene 45 punti per asse. I 2025 valori rappresentati sono previsioni ottenute dai 64 campioni.')+
 p(r'Se una superficie copre aree lontane dai campioni, la legenda e il commento devono rendere esplicito questo limite.'),
 r'La risoluzione della figura e la risoluzione dell’informazione osservata sono proprietà differenti.', source=[10,27])

slide(43,'Laboratorio: carte e appartenenze verificabili',
 experiment('aggregazione','Esperimento online · aggregazioni e confini')+
 table(['Notebook','Domanda di controllo'],[
 ['N07: punti','Dove sono le misure?'],
 ['N08: partizione','Ogni ID compare in una sola area?'],
 ['N09: sovrapposizione','Quanti ID hanno più appartenenze?'],
 ['N10: buffer','Come cambiano conteggio e media?']], [4.0,5.0]),
 p(r'Per ogni operazione conservare tabella iniziale, regola geometrica e riepilogo dei conteggi. Un grafico senza questi elementi non basta a ricostruire il risultato.')+
 info(r'Una moltiplicazione delle righe può essere corretta. L’errore nasce quando cambia il peso statistico dei siti senza dichiararlo.')+
 p(r'Il passo successivo assegna pesi direttamente alle coppie di siti.'),
 r'Ogni aggregazione deve rendere controllabile il passaggio dalle osservazioni alle unità di sintesi.', notebook=9, source=[10,11,12,32])

slide(44,'Il vicinato è una scelta del modello',
 fig('13_vicini_soglia',r'Una soglia di 260 m collega i vicini ortogonali della griglia; le diagonali restano escluse.'),
 p(r'Definiamo vicini i siti distinti con distanza non superiore a 260 m. La soglia supera il passo di 250 m ed è inferiore alla diagonale di circa 354 m.')+
 info(r'Il grafo così costruito contiene 112 archi non orientati. La matrice simmetrica registra ciascun arco in due celle.')+
 p(r'Soglia e metrica vengono fissate prima di misurare l’associazione.'),
 r'Il significato di vicino deve essere esplicito prima del calcolo dei pesi.', source=[13])

slide(45,'Una soglia può generare vicinati diversi',
 eq(r'A_{ij}=\mathbf1(0<d_{ij}\le r),\qquad A_{ii}=0')+
 table(['Soglia sulla griglia','Conseguenza'],[
 ['$r<250$ m','Nessun vicino distinto'],
 [r'$250\le r<250\sqrt2$ m','Vicini ortogonali'],
 [r'$r\ge250\sqrt2$ m','Entrano anche le diagonali vicine'],
 ['Soglia molto grande','La relazione diventa meno locale']], [4.5,4.5]),
 p(r'La disuguaglianza sul bordo della soglia fa parte della definizione. Con distanze calcolate numericamente, la tolleranza va motivata se necessaria.')+
 info(r'Nelle coordinate locali del caso guida la soglia di 260 m evita ambiguità sul passo di 250 m.'),
 r'Cambiare soglia cambia il grafo e quindi il fenomeno di associazione che si misura.',
 code('A <- 1*(D>0 & D<=260)\nstopifnot(all(diag(A)==0),\n          identical(A,t(A)))\nc(archi=sum(A)/2,S0=sum(A))','R · adiacenza binaria'), notebook=12, source=[13,14])

slide(46,'Vicino più prossimo: esclusione e parità',
 eq(r'j^\star(i)\in\arg\min_{j\ne i}d_{ij}')+
 info(r'Sulla griglia diversi siti sono alla stessa distanza minima. Il laboratorio risolve le parità scegliendo il primo indice nell’ordine degli ID.'),
 p(r'Se non si esclude la diagonale, il vicino più prossimo di ogni sito è il sito stesso. Per evitarlo sostituiamo la diagonale con infinito solo nella matrice di ricerca.')+
 p(r'La regola delle parità è riproducibile ma non aggiunge una preferenza fisica. Se serve includere tutti gli ex aequo, cambia la struttura del vicinato.'),
 r'Il vicino più prossimo richiede una regola per l’autocoincidenza e una per le distanze uguali.',
 code('D_nn <- D\ndiag(D_nn) <- Inf\nj_nn <- apply(D_nn,1,which.min)\nstopifnot(all(j_nn!=seq_len(n)))\nhead(d$id[j_nn])','R · escludere il sito stesso'), notebook=11, source=[13])

slide(47,'Il grado conta quanti vicini ha un sito',
 fig('14_gradi_vicinato',r'Con vicinato ortogonale: 4 angoli con grado 2, 24 bordi con grado 3, 36 interni con grado 4.'),
 p(r'La somma di una riga di A è il grado del sito. I punti al bordo hanno meno collegamenti disponibili.')+
 info(r'La somma dei gradi è 224, cioè due volte il numero degli archi non orientati. Questo conteggio verifica la costruzione del grafo.'),
 r'Il grado distingue la struttura del vicinato dal valore misurato nel sito.',
 code('grado <- rowSums(A)\ntable(grado)\nstopifnot(sum(grado)==224,\n          sum(A)/2==112)','R · contare i collegamenti'), notebook=12, source=[14,15])

slide(48,'Normalizzare per riga costruisce una media',
 weightstar()+eq(r'W_{ij}=\frac{A_{ij}}{\sum_k A_{ik}},\qquad \sum_jW_{ij}=1'),
 p(r'Per un sito con quattro vicini ogni peso è $1/4$. Per un angolo con due vicini ogni peso è $1/2$.')+
 info(r'La normalizzazione rende il ritardo spaziale una media dei vicini. Non elimina la differenza nella copertura geometrica fra centro e bordo.'),
 r'La normalizzazione per riga cambia il significato dei pesi e del ritardo spaziale.',
 code('stopifnot(all(grado>0))\nW <- A/grado\nstopifnot(max(abs(rowSums(W)-1))\n          <1e-12)','R · pesi normalizzati'), notebook=12, source=[14])

slide(49,'Da A a W: stessa rete, pesi differenti',
 fig('15_matrici_A_W',r'Le celle non nulle sono le stesse. La normalizzazione per riga modifica le intensità.'),
 p(r'A è simmetrica perché la distanza lo è. W può essere asimmetrica: un angolo assegna $1/2$ a un vicino che gli assegna $1/3$.')+
 info(r'Due statistiche calcolate con A e W non devono essere interpretate come lo stesso risultato. Il nome “Moran I” richiede di specificare anche i pesi.'),
 r'La simmetria dell’adiacenza non garantisce la simmetria dei pesi normalizzati.',
 code('c(simmetrica_A=isSymmetric(A),\n  simmetrica_W=isSymmetric(W))\nrange(rowSums(W))','R · distinguere le matrici'), notebook=12, source=[14,17])

slide(50,'Un sito isolato richiede una regola esplicita',
 eq(r'\sum_jA_{ij}=0\quad\Longrightarrow\quad A_{ij}/0\ \text{non definito}')+
 table(['Possibile scelta','Conseguenza da dichiarare'],[
 ['Rivedere il vicinato','Cambia la relazione analizzata'],
 ['Escludere il sito','Cambia il campione e può creare altri isolati'],
 ['Assegnare ritardo zero','È una convenzione del metodo'],
 ['Lasciare il valore mancante','Richiede un’analisi coerente dei mancanti']], [4.1,4.9]),
 p(r'Con la soglia principale ogni sito ha almeno due vicini. Questo fatto viene controllato prima di normalizzare.')+
 info(r'Con 200 m tutti i siti sarebbero isolati. Una divisione silenziosa per zero produrrebbe valori non validi.'),
 r'Il trattamento degli isolati entra nella definizione della statistica e del campione.',
 code('A_200 <- 1*(D>0 & D<=200)\nisolati <- rowSums(A_200)==0\nstopifnot(sum(isolati)==64L)\nsum(isolati)','R · un caso limite controllato'), notebook=12, source=[14])

slide(51,'Il ritardo spaziale riassume i vicini',
 fig('16_lag_spaziale',r'Valore nel sito e media dei vicini sono quantità diverse, calcolate con gli stessi ID.')+
 eq(r'(Wz)_i=\sum_jW_{ij}z_j'),
 p(r'Il ritardo spaziale non sposta i dati nel tempo. Costruisce per ogni sito una combinazione dei valori nei siti collegati.')+
 info(r'Con pesi non negativi normalizzati per riga, il risultato è una media. Se tutte le misure sono costanti, il ritardo riproduce quella costante.'),
 r'Il ritardo spaziale dipende dai valori dei vicini e dalla regola con cui sono pesati.',
 code('lag_z <- drop(W%*%z)\nstopifnot(max(abs(W%*%rep(1,n)-1))\n          <1e-12)\nhead(data.frame(id=d$id,z,lag_z))','R · media del vicinato'), notebook=12, source=[15])

slide(52,'Un riordinamento deve coinvolgere valori e pesi',
 eq(r'z^\star=Pz,\qquad W^\star=PWP^\top')+
 eq(r'W^\star z^\star=P(Wz)')+
 info(r'$P$ è una matrice di permutazione. Cambiare ordine a tutte le componenti conserva il risultato associato ai singoli siti.'),
 p(r'Riordinare soltanto i valori distrugge la corrispondenza con le righe della matrice. Il codice resta eseguibile ma risponde a un’altra disposizione spaziale.')+
 p(r'Il controllo per ID evita di usare la posizione nella tabella come identità del campione.'),
 r'La statistica deve restare invariata sotto un riordinamento coerente delle osservazioni.',
 code('ii <- rev(seq_len(n))\nstopifnot(isTRUE(all.equal(\n drop(W[ii,ii]%*%z[ii]),\n lag_z[ii],check.attributes=FALSE)))','R · invarianza all’ordine'), notebook=12, source=[14,17])

slide(53,'Il bordo cambia la geometria del confronto',
 fig('17_effetti_bordo',r'Centro, lato e angolo hanno disponibilità di vicini differenti, anche con pesi di riga unitari.'),
 p(r'La normalizzazione uniforma la somma dei pesi, ma non rende equivalenti il vicinato di un angolo e quello di un sito interno.')+
 info(r'Un sito al bordo confronta i valori osservati da un solo lato. Se il fenomeno ha un gradiente, questa asimmetria geometrica può incidere sul ritardo.')+
 p(r'La diagnosi del vicinato deve quindi includere mappa, gradi e presenza di componenti separate.'),
 r'Una somma dei pesi uguale a uno non implica uguale informazione spaziale.', source=[15])

slide(54,'La sensibilità ai pesi fa parte del risultato',
 table(['Modifica','Che cosa può cambiare'],[
 ['Soglia di distanza','Scala della relazione'],
 ['Numero fisso di vicini','Raggio locale variabile'],
 ['Pesi binari o di riga','Contributo dei siti con gradi diversi'],
 ['Distanza o rete','Nozione fisica di connessione']], [4.1,4.9]),
 p(r'Il risultato principale usa una specifica dichiarata. Le alternative permettono di valutare quanto dipenda dalla scelta del vicinato.')+
 info(r'Cambiare ripetutamente la matrice finché il risultato diventa significativo introduce una selezione che il singolo p-value non rappresenta.')+
 p(r'Conserviamo le alternative come analisi di sensibilità, con motivazioni e risultati completi.'),
 r'La robustezza rispetto ai pesi va studiata senza scegliere la sola configurazione favorevole.', source=[13,14,19])

slide(55,'Laboratorio: dal vicino alla matrice dei pesi',
 experiment('vicinati','Esperimento online · vicinati e matrici')+
 table(['Prova','Esito richiesto'],[
 ['N11: vicino più prossimo','Nessun sito sceglie se stesso'],
 ['Parità','Regola deterministica documentata'],
 ['N12: adiacenza','Diagonale nulla e 112 archi'],
 ['Normalizzazione','64 somme di riga uguali a uno'],
 ['Allineamento','ID coerenti fra misure e matrice']], [4.0,5.0]),
 p(r'La consegna comprende una carta dei collegamenti e una tabella dei gradi. La matrice viene salvata insieme all’ordine degli ID.')+
 info(r'La statistica di associazione userà il grafo appena definito. Ogni cambiamento dei pesi deve restare riconoscibile nei risultati.')+
 p(r'Possiamo ora chiederci se i valori vicini tendano a essere simili rispetto a un riferimento dichiarato.'),
 r'Una matrice dei pesi verificata rende trasparente il passaggio dalla geometria alla statistica.', notebook=12, source=[13,14,15,32])
