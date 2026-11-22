"""Morfometria e rappresentazione del rilievo: pagine 49–76."""
from componenti import *

slide(49,'La morfometria deriva misure dalla geometria',
 table(['Grandezza','Domanda'],[
 ['Quota','Quanto è alta la superficie nel riferimento?'],
 ['Gradiente','Come cambia la quota lungo gli assi?'],
 ['Pendenza','Qual è la massima inclinazione locale?'],
 ['Esposizione','Verso quale azimut scende il terreno?'],
 ['Ombreggiatura','Come appare con una luce scelta?']], [3.8,5.2]),
 p(r'Il valore derivato dipende dalla superficie rappresentata e dalla regola numerica. La risoluzione entra attraverso le distanze fra celle.')+
 info(r'Useremo prima un piano con soluzione nota, poi il terreno sintetico del corso. Questo separa il controllo del codice dall’interpretazione della morfologia.')+
 p(r'La carta finale conserverà algoritmo, unità, passo e trattamento dei margini.'),
 r'Una misura morfometrica è il risultato di dati geometrici e di un procedimento dichiarato.',source=[14,15,16,17])

slide(50,'Il gradiente misura variazioni orientate della quota',
 stencil()+
 eq(r"""\nabla z=\left(\frac{\partial z}{\partial x},
                       \frac{\partial z}{\partial y}\right)"""),
 p(r'La componente lungo Est descrive come cambia la quota muovendosi su quell’asse. La componente lungo Nord usa l’orientamento geografico corrispondente.')+
 info(r'Il segno contiene informazione: una componente positiva indica salita nella direzione positiva dell’asse.')+
 p(r'La norma del gradiente e la sua direzione descrivono proprietà diverse. La pendenza non conserva da sola l’esposizione.'),
 r'Il gradiente deve essere interpretato insieme agli assi e alle loro unità.',source=[14,18])

slide(51,'Le differenze centrate usano due passi',
 eq(r"""g_x=\frac{z_{i,j+1}-z_{i,j-1}}{2\Delta x}""")+
 eq(r"""g_y=\frac{z_{i+1,j}-z_{i-1,j}}{2\Delta y}""")+
 info(r'Matrice locale con righe crescenti verso Nord. Per $\Delta x=\Delta y=30$ m il denominatore è 60 m.'),
 p(r'I due valori confrontati si trovano ai lati del centro. La loro distanza è doppia rispetto al passo della griglia.')+
 sm(r'Conserviamo soltanto le righe e colonne interne, dove entrambi i vicini sono disponibili.'),
 r'Il denominatore è una distanza geometrica, non un parametro da scegliere per adattare il risultato.',
 code('gx <- (Z[2:23,3:30]-\n       Z[2:23,1:28])/60\ngy <- (Z[3:24,2:29]-\n       Z[1:22,2:29])/60','R · derivate nella matrice locale'),notebook=9,source=[14])

slide(52,'Quote e distanze devono avere unità coerenti',
 eq(r"""[g_x]=\frac{[\mathrm{quota}]}{[\mathrm{distanza}]}""")+
 table(['Configurazione','Conseguenza'],[
 ['Quota e assi in metri','Rapporto adimensionale'],
 ['Quota in piedi, assi in metri','Conversione necessaria'],
 ['Assi in gradi','Distanza metrica da ricostruire'],
 ['Passi diversi su x e y','Denominatori distinti'],
 ['Esagerazione verticale','Inclinazione rappresentata modificata']], [4.2,4.8]),
 p(r'La tangente dell’angolo di pendenza è un rapporto fra lunghezze espresse nella stessa unità.')+
 info(r'Il caso guida usa metri per quote e coordinate. Un DEM geografico richiede un algoritmo che tenga conto delle distanze sulla Terra.')+
 p(r'Una trasformazione dei soli valori per migliorare la visualizzazione non deve entrare implicitamente nei calcoli scientifici.'),
 r'L’unità della derivata deriva dalle unità dei dati, che devono essere verificate prima del calcolo.',source=[14,16])

slide(53,'Un piano fornisce una soluzione di riferimento',
 fig('16_piano_noto',r'Piano sintetico $z=900+0{,}12x+0{,}08y$. Il gradiente esatto è noto in tutto il dominio.'),
 p(r'Le derivate sono costanti: 0,12 lungo Est e 0,08 lungo Nord. Il livello iniziale 900 m non cambia l’inclinazione.')+
 info(r'La soluzione analitica è disponibile prima di eseguire il programma. Può quindi riconoscere errori nel passo, nel segno o nell’ordine degli assi.'),
 r'Una verifica utile confronta il codice con un risultato noto indipendentemente.',
 code('P <- outer((0:23)*30,(0:29)*30,\n function(y,x)900+0.12*x+0.08*y)\ng_atteso <- sqrt(0.12^2+0.08^2)\natan(g_atteso)*180/pi','R · piano e pendenza attesa'),notebook=9,source=[15])

slide(54,'Il controllo confronta entrambe le componenti',
 eq(r"""\max|g_x-0{,}12|<10^{-12}""")+
 eq(r"""\max|g_y-0{,}08|<10^{-12}""")+
 info(r'La tolleranza riconosce l’aritmetica in virgola mobile. Il confronto riguarda tutte le celle interne, non soltanto la media.'),
 p(r'Un errore di orientamento può cambiare il segno della componente Nord lasciando invariata la norma del gradiente.')+
 sm(r'Per questo controlliamo le componenti prima dell’angolo di pendenza.'),
 r'Verificare soltanto la norma può nascondere un errore di direzione.',
 code('px <- (P[2:23,3:30]-P[2:23,1:28])/60\npy <- (P[3:24,2:29]-P[1:22,2:29])/60\nstopifnot(max(abs(px-0.12))<1e-12,\n          max(abs(py-0.08))<1e-12)','R · prova numerica indipendente'),notebook=9,source=[15])

slide(55,'Gli errori costruiti mostrano che cosa controllare',
 table(['Errore introdotto','Effetto sul piano'],[
 [r'Usare $\Delta$ invece di $2\Delta$','Componenti raddoppiate'],
 ['Invertire Nord e Sud','Segno della componente Nord invertito'],
 ['Scambiare gli assi','Componenti scambiate'],
 ['Aggiungere una costante alle quote','Gradiente invariato'],
 ['Moltiplicare le quote per un fattore','Gradiente moltiplicato per quel fattore']], [4.7,4.3]),
 p(r'Queste trasformazioni rendono esplicito il comportamento atteso. Una verifica deve fallire quando introduciamo un errore che pretende di riconoscere.')+
 info(r'L’angolo è l’arcotangente della norma: raddoppiare il gradiente non raddoppia esattamente l’angolo.')+
 p(r'Una volta superate le prove note, applichiamo il calcolo al rilievo articolato.'),
 r'Le proprietà geometriche aiutano a progettare controlli che distinguono errori e cambiamenti legittimi.',notebook=9,source=[14,15,16])

slide(56,'La precisione dipende da passo e regolarità',
 fig('11_sensibilita_pendenza',r'Esperimento analitico: RMSE della pendenza alle tre risoluzioni, sullo stesso dominio fisico valido di 28 ha.',height=4.55)+
 eq(r"""\frac{f(x+h)-f(x-h)}{2h}=f'(x)+O(h^2)"""),
 p(r'Un passo più piccolo riduce l’errore di discretizzazione di una superficie regolare, ma le differenze possono amplificare il rumore delle quote.')+
 p(r'Con un DEM già misurato, interpolare a una griglia più fine non equivale a ottenere nuove quote più precise.')+
 sm(r'Il confronto fra scale deve distinguere errore del metodo, risoluzione del dato e variabilità della misura.'),
 r'La scelta del passo è legata sia alla geometria sia alla qualità dell’informazione disponibile.',source=[11,14,15])

panorama(57,'Il gradiente conserva segno e direzione',
 '17_gradienti_xy',
 r'Componenti Est e Nord delle differenze centrate sul raster originale da 30 m. La scala e il segno descrivono la salita lungo ciascun asse; gli assi delle carte mantengono la convenzione locale. I margini esclusi dal calcolo non rappresentano terreno piano.',
 r'Le due componenti devono essere lette insieme prima di ricavare pendenza ed esposizione.',notebook=10,source=[14,17,18])

slide(58,'La pendenza è la norma del gradiente trasformata',
 fig('18_gradiente_pendenza',r'Il rapporto di massima salita $g$ e l’angolo $\alpha$ sono collegati dall’arcotangente.')+
 eq(r"""g=\sqrt{g_x^2+g_y^2},\qquad \alpha=\arctan g"""),
 p(r'Il gradiente indica la direzione della massima salita locale. La sua norma è il rapporto fra incremento verticale e distanza orizzontale.')+
 info(r'L’angolo perde l’informazione sulla direzione. Due versanti opposti possono avere la stessa pendenza.'),
 r'La pendenza sintetizza l’intensità dell’inclinazione, mentre l’esposizione ne descrive la direzione.',
 code('g <- sqrt(gx^2+gy^2)\nslope_deg <- atan(g)*180/pi\nslope_pct <- 100*g','R · due rappresentazioni'),notebook=10,source=[16])

slide(59,'Gradi e percentuale non sono una scala lineare',
 fig('20_gradi_percentuale',r'45° corrispondono al 100\%; oltre 45° la percentuale supera 100 senza contraddizione.')+
 eq(r"""p_{\%}=100\tan\alpha"""),
 p(r'La percentuale misura il dislivello per cento unità di distanza orizzontale. L’angolo misura l’inclinazione geometrica.')+
 info(r'Una soglia espressa in gradi va convertita prima di applicarla a una carta in percentuale.'),
 r'Le unità delle carte di pendenza devono essere esplicite prima di ogni confronto.',
 code('angoli <- c(0,15,30,45,60)\ndata.frame(gradi=angoli,\n percento=100*tan(angoli*pi/180))','R · conversione non lineare'),notebook=10,source=[16])

slide(60,'La carta delle pendenze conserva il metodo',
 fig('19_pendenza_mappa',r'Differenze centrate con quattro vicini; passo 30 m; pendenza in gradi; 22×28 celle interne.'),
 p(r'Le variazioni cromatiche rappresentano la misura derivata secondo il metodo dichiarato. Non sono direttamente la quota o la luminosità del terreno.')+
 info(r'Per confrontare due carte manteniamo uguali unità e scala cromatica, verificando anche algoritmo, risoluzione e maschere.')+
 p(r'Le aree di pendenza elevata possono essere sensibili alla risoluzione e alla rappresentazione delle discontinuità.'),
 r'La legenda rende leggibile la misura; la didascalia rende ricostruibile il procedimento.',notebook=10,source=[17])

slide(61,'Il bordo non ha tutti i vicini richiesti',
 eq(r"""n_{\mathrm{interno}}=(24-2)(30-2)=616""")+
 eq(r"""n_{\mathrm{bordo}}=720-616=104""")+
 info(r'Con la convenzione adottata, le 104 celle esterne ricevono NA nella carta completa delle derivate. La loro quota originale resta disponibile.'),
 p(r'Le differenze centrate richiedono un valore da entrambi i lati. Sul bordo uno dei due manca.')+
 p(r'Un altro algoritmo potrebbe usare differenze unilaterali o valori oltre il dominio. Sarebbe una scelta diversa da dichiarare e verificare.'),
 r'Uno zero di pendenza significa piano: non deve essere usato per codificare una derivata non calcolata.',
 code('stopifnot(identical(dim(gx),c(22L,28L)))\nc(celle_interne=length(gx),\n celle_bordo=length(Z)-length(gx))','R · conteggio del dominio'),notebook=10,source=[17])

panorama(62,'La maschera si estende alle derivate',
 '21_bordo_maschera',
 r'Il confronto separa il bordo esterno dal vicinato delle celle mancanti. Per le derivate del caso mascherato richiediamo centro valido e quattro vicini validi. La carta delle esclusioni documenta il motivo per cui una quota disponibile può non avere una pendenza calcolabile.',
 r'La maschera dell’output deriva sia dalla validità dei dati sia dalle richieste dell’algoritmo.',source=[7,14,17])

slide(63,'L’esposizione indica la discesa',
 azimuth()+
 eq(r"""\theta=\operatorname{atan2}(-g_x,-g_y)\bmod2\pi"""),
 p(r'Assumiamo Est come asse $x$ e Nord come asse $y$. L’azimut cresce in senso orario dal Nord.')+
 info(r'La direzione di discesa è opposta al gradiente. La funzione atan2 distingue i quadranti e richiede l’ordine delle componenti indicato.')+
 sm(r'La conversione in gradi moltiplica per $180/\pi$. I valori prossimi a 0° e 360° rappresentano direzioni vicine.'),
 r'Il segno del gradiente e la convenzione dell’azimut devono essere coerenti.',notebook=11,source=[18])

slide(64,'Su un piano orizzontale la direzione è indeterminata',
 fig('22_aspect',r'Esposizione in gradi, azimut orario dal Nord. La scala cromatica è circolare; il trattamento delle celle piane è esplicito.'),
 p(r'Quando il gradiente è nullo, la superficie non ha una direzione preferita di discesa. Mascheriamo quelle direzioni.')+
 info(r'Alcuni software restituiscono un valore convenzionale. Per esempio terra documenta 90° sui piani: non va interpretato come un’esposizione reale verso Est.'),
 r'La mancanza di una direzione fisica deve essere distinta da un azimut numericamente valido.',
 code('aspect_deg <-\n (atan2(-gx,-gy)*180/pi)%%360\naspect_deg[g<1e-12] <- NA_real_','R · direzioni e celle piane'),notebook=11,source=[18])

slide(65,'Le direzioni richiedono una media circolare',
 fig('23_media_circolare',r'359° e 1° sono prossimi al Nord. La media aritmetica vale 180°; la media circolare riconosce la vicinanza.')+
 eq(r"""\overline\theta=\operatorname{atan2}(\overline S,\overline C),
 \qquad \overline R=\sqrt{\overline C^2+\overline S^2}"""),
 p(r'Calcoliamo le medie di seno e coseno. La risultante $\overline R$ descrive la concentrazione delle direzioni.')+
 info(r'Quando $\overline R$ è quasi zero, la direzione media è instabile o indeterminata. Riportiamo entrambe le quantità.'),
 r'Una sintesi angolare deve riconoscere la circolarità e dichiarare la concentrazione.',
 code('th <- c(359,1)*pi/180\nS <- mean(sin(th)); C <- mean(cos(th))\nmedia_circolare(c(359,1))','R · media e concentrazione'),notebook=11,source=[19])

slide(66,'Il confronto con terra richiede lo stesso algoritmo',
 fig('24_confronto_terra',r'Confronto con un algoritmo dichiarato di terra. Differenze numeriche e differenze di metodo sono valutate separatamente.'),
 p(r'terra usa otto vicini per impostazione predefinita. Per confrontare le nostre differenze centrate specifichiamo quattro vicini e le stesse unità.')+
 info(r'La gestione di bordo, mancanti e piani deve restare esplicita. Una coincidenza sul piano noto non garantisce uguaglianza per tutti i terreni.'),
 r'Un confronto fra software è interpretabile quando le convenzioni e il compito coincidono.',
 code('s_terra <- terra::terrain(r,\n v="slope",neighbors=4,\n unit="degrees")\nterra::global(s_terra,"range",na.rm=TRUE)','R · algoritmo esplicito'),notebook=10,source=[14,15,17])

slide(67,'L’ombreggiatura combina superficie e luce',
 eq(r"""L=\max(0,\mathbf n\cdot\boldsymbol\ell),
       \qquad \|\mathbf n\|=\|\boldsymbol\ell\|=1""")+
 boxes([('a',2.1,3.4,'Geometria del terreno',3.7,'GeoA'),
        ('b',7.3,3.4,'Direzione della luce',3.7,'GeoB'),
        ('c',2.1,.9,'Normale alla superficie',3.7,'GeoA'),
        ('d',7.3,.9,'Intensità locale',3.7,'GeoC')],
       [('a','c',''),('b','d',''),('c','d','')],4.3),
 p(r'Il modello lambertiano locale associa maggiore intensità alle facce orientate verso la sorgente. I contributi negativi vengono posti a zero.')+
 info(r'Il risultato è una rappresentazione dipendente dalla luce scelta. Non è una nuova misura di quota o riflettanza.')+
 p(r'La normalizzazione dei vettori rende l’intensità confrontabile nell’intervallo da zero a uno.'),
 r'La luce è un parametro della rappresentazione che deve accompagnare l’immagine.',source=[20])

slide(68,'Azimut e altezza definiscono il vettore della luce',
 eq(r"""\mathbf n=\frac{(-g_x,-g_y,1)}
                        {\sqrt{1+g_x^2+g_y^2}}""")+
 eq(r"""\boldsymbol\ell=
       (\cos h\sin A,\;\cos h\cos A,\;\sin h)""")+
 info(r'$A$: azimut orario dal Nord. $h$: altezza sopra l’orizzonte. Quote e coordinate devono avere unità coerenti.'),
 p(r'La componente verticale della luce cresce con l’altezza. Le componenti orizzontali ne descrivono la provenienza geografica.')+
 p(r'Su un terreno orizzontale $\mathbf n=(0,0,1)$ e l’intensità è $\sin h$, indipendente dall’azimut.')+
 sm(r'Questo è un controllo analitico utile per riconoscere uno scambio fra altezza e angolo zenitale.'),
 r'Le convenzioni angolari devono essere dichiarate prima di tradurre la geometria in una formula.',source=[20,21])

panorama(69,'Spostare la luce cambia la carta, a quote invariate',
 '25_hillshade_confronto',
 r'Stesso terreno e stesse derivate, azimut 315° e 135°, altezza 45°, esagerazione verticale unitaria. La scala dell’intensità resta fissata fra 0 e 1. Le differenze derivano dalla direzione della luce; non rappresentano un cambiamento della morfologia.',
 r'Confrontare più illuminazioni aiuta a distinguere la forma del terreno dall’effetto della rappresentazione.',notebook=12,source=[21,22])

slide(70,'Il prodotto scalare rende verificabile il calcolo',
 eq(r"""L=\max\left(0,
 \frac{-g_x\ell_x-g_y\ell_y+\ell_z}
      {\sqrt{1+g_x^2+g_y^2}}\right)""")+
 info(r'Il modello usa la normale orientata verso l’alto. Conserviamo righe e colonne della matrice lungo tutta l’operazione.'),
 p(r'Il codice usa radianti nelle funzioni trigonometriche e mantiene le matrici prima dello zero in pmax, preservandone gli attributi.')+
 sm(r'La corrispondenza fra indice della matrice e posizione geografica viene verificata insieme ai valori.'),
 r'La correttezza numerica deve conservare anche l’ordine delle celle.',
 code('A <- 315*pi/180; h <- 45*pi/180\nluce <- c(cos(h)*sin(A),\n cos(h)*cos(A),sin(h))\nL315 <- pmax((-gx*luce[1]-gy*luce[2]+\n luce[3])/sqrt(1+gx^2+gy^2),0)\nstopifnot(identical(dim(L315),dim(gx)))','R · luce da Nord-Ovest'),notebook=12,source=[20,21])

slide(71,'Un profilo mostra l’effetto dell’illuminazione',
 fig('26_illuminazione_profilo',r'Intensità lungo un profilo del terreno al variare della luce. Quote e geometria restano fisse.'),
 p(r'Il massimo della luminosità non deve coincidere con la massima quota. Dipende dall’orientamento della superficie rispetto alla sorgente.')+
 info(r'Una scala cromatica identica permette di leggere il cambiamento senza introdurre un ulteriore effetto di riscalatura.')+
 p(r'Un profilo collega le differenze visive ai valori e alle convenzioni geometriche del calcolo.'),
 r'Il colore di un hillshade descrive l’illuminazione modellata, non l’altitudine.',notebook=12,source=[21,22])

slide(72,'L’ombra locale non include tutti gli ostacoli',
 table(['Nel modello locale','Richiede un modello ulteriore'],[
 ['Normale della cella','Ombre proiettate da rilievi lontani'],
 ['Direzione della sorgente','Occlusione lungo l’orizzonte'],
 ['Intensità da prodotto scalare','Luce diffusa e riflessioni'],
 ['Taglio dei valori negativi','Proprietà radiometriche del materiale']], [4.4,4.6]),
 p(r'Il calcolo locale usa l’orientamento della superficie nella cella. Non esamina automaticamente tutto il percorso dei raggi luminosi nel paesaggio.')+
 info(r'La copertina è un rendering tridimensionale con illuminazione della scena. Le figure di hillshade adottano invece il modello scientifico esplicitato qui.')+
 p(r'La distinzione permette di usare correttamente entrambi i prodotti.'),
 r'Un’immagine di rilievo deve essere interpretata secondo il modello con cui è stata prodotta.',source=[20])

slide(73,'L’esagerazione verticale modifica le normali',
 eq(r"""z^*=kz,\qquad \nabla z^*=k\nabla z""")+
 eq(r"""\alpha^*=\arctan\left(k\sqrt{g_x^2+g_y^2}\right),
       \qquad k>0""")+
 info(r'La trasformazione può accentuare le forme nella visualizzazione. Non rappresenta una nuova misura delle quote.'),
 p(r'Le pendenze apparenti e l’illuminazione cambiano perché cambia l’orientamento delle normali.')+
 p(r'Nel caso principale l’esagerazione è pari a uno. Le eventuali varianti dichiarano il fattore usato e restano distinte dai dati originali.'),
 r'I parametri che modificano la percezione del rilievo devono essere registrati nella didascalia.',source=[21])

slide(74,'I controlli della luce usano casi noti',
 table(['Caso','Risultato atteso'],[
 ['Vettori unitari','Prodotto scalare fra −1 e 1'],
 ['Taglio locale','Intensità compresa fra 0 e 1'],
 ['Terreno orizzontale',r'Intensità $\sin h$'],
 ['Luce zenitale',r'Intensità $1/\sqrt{1+g^2}$'],
 ['Cambio del solo azimut','Quote e pendenze invariate']], [4.2,4.8]),
 p(r'Questi controlli sono indipendenti dalla plausibilità visiva della carta. Una superficie ben ombreggiata potrebbe comunque usare una convenzione angolare errata.')+
 info(r'Verifichiamo anche la dimensione della matrice e l’associazione delle intensità con le coordinate delle celle.'),
 r'Le identità geometriche forniscono controlli riproducibili per la rappresentazione.',
 code('stopifnot(all(L315>=0 & L315<=1))\nL_piano <- sin(45*pi/180)\nstopifnot(\n abs(L_piano-sqrt(0.5))<1e-12)','R · limiti e piano orizzontale'),notebook=12,source=[20,21,22])

slide(75,'Rappresentare la variabile dichiarata',
 table(['Carta','Scala e parametri da leggere'],[
 ['Quota','Metri e riferimento verticale'],
 ['Pendenza','Gradi o percentuale, algoritmo'],
 ['Esposizione','Azimut e convenzione circolare'],
 ['Hillshade','Intensità, azimut, altezza e fattore verticale'],
 ['Composizione grafica','Canali, trasparenze e trasformazioni']], [3.5,5.5]),
 p(r'Le rappresentazioni possono essere sovrapposte per facilitare l’interpretazione. Ogni componente conserva però un significato distinto.')+
 info(r'Quote, curve di livello e più illuminazioni aiutano a verificare una forma suggerita dalla percezione visiva.')+
 p(r'Le didascalie devono consentire di ricostruire il prodotto anche senza vedere il codice.'),
 r'La leggibilità di una carta comprende sia la legenda sia la spiegazione di come è stata costruita.',source=[17,18,20,21,22])

slide(76,'Laboratorio: verificare forma e rappresentazione',
 experiment('pendenza','Esperimento online · gradiente e pendenza')+
 experiment('hillshade','Esperimento online · illuminazione')+
 table(['Attività','Controllo'],[
 ['N09: piano noto','Componenti 0,12 e 0,08'],
 ['N10: pendenza','Gradi, percentuale, bordo'],
 ['N11: esposizione','Azimut, piani e media circolare'],
 ['N12: hillshade','Stesso terreno, luci differenti'],
 ['Consegna','Metodo e dominio valido delle derivate']], [4.1,4.9]),
 p(r'Il percorso collega formule, casi noti e carte del terreno. Ogni immagine deriva da un calcolo verificabile.')+
 info(r'La sezione successiva usa la stessa attenzione alla geometria per confrontare bande spettrali e costruire un indice.'),
 r'La rappresentazione del rilievo è affidabile quando parametri e verifiche rimangono accessibili.',notebook=12,source=[14,15,16,17,18,19,20,21,22,30])
