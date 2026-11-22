"""Gemina M06, slide 20–46: evidenza, potenza e confronto di Welch.

Tutte le figure sono TikZ editabile. I calcoli di riferimento sono in
evidence_proof/calcoli_figure.R; i CSV conservano le coordinate numeriche.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent
FIG = ROOT / 'evidence_proof' / 'coordinate'
SLIDES, CODES = {}, {}
E = 'II · INTERPRETARE L’EVIDENZA'
W = 'III · CONFRONTARE DUE GRUPPI'

def S(n,title,section,left,right,recall):
    SLIDES[n]=dict(title=title,section=section,left=left,right=right,recall=recall)

def code(n,name,text):
    CODES[f'{n:03}_{name}.R']=text.strip()+'\n'

def rows(name):
    return list(csv.DictReader((FIG/(name+'.csv')).open()))

def stats(name):
    return {r['nome']:float(r['valore']) for r in rows(name)}

def fmt(v,d=3):
    return f'{v:.{d}f}'.replace('.','{,}')

def coords(points):
    return ' '.join(f'({x:.5f},{y:.5f})' for x,y in points)

def axes(xmin,xmax,ymax,xticks,yticks,xlab,ylab,h=2.4):
    xx=lambda v:.75+8.0*(v-xmin)/(xmax-xmin)
    yy=lambda v:h*v/ymax
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for v in yticks:
        out += [rf'\draw[Rule](.75,{yy(v):.4f})--(8.75,{yy(v):.4f});',
                rf'\node[pNote,anchor=east] at(.60,{yy(v):.4f}){{$ {v:g} $}};']
    out += [r'\draw[pAxis](.75,0)--(8.98,0);',rf'\draw[pAxis](.75,0)--(.75,{h+.16});']
    for v in xticks:
        out += [rf'\draw[Muted]({xx(v):.4f},0)--({xx(v):.4f},-.07);',
                rf'\node[pNote,below] at({xx(v):.4f},-.08){{$ {v:g} $}};']
    out += [rf'\node[pNote] at(4.75,-.61){{{xlab}}};',
            rf'\node[pNote,rotate=90] at(-.18,{h/2}){{{ylab}}};']
    return out,xx,yy

def curve(out,rr,xkey,ykey,xx,yy,color='GeoA',extra=''):
    out += [rf'\draw[{color},line width=1.1pt,{extra}] plot coordinates{{'+coords([(xx(float(r[xkey])),yy(float(r[ykey]))) for r in rr])+r'};']

def end(out):
    return '\n'.join(out+[r'\end{tikzpicture}'])

def tail(out,rr,xkey,ykey,xx,yy,cut,side,color='GeoB'):
    subset=[r for r in rr if (float(r[xkey])>=cut if side=='right' else float(r[xkey])<=cut)]
    pp=[(xx(float(r[xkey])),yy(float(r[ykey]))) for r in subset]
    out += [rf'\fill[{color}!45] '+f'({pp[0][0]:.5f},0)--'+ ' plot coordinates{'+coords(pp)+'}'+f'--({pp[-1][0]:.5f},0)--cycle;']

def table(headers,data,widths,h=.60):
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    width=sum(widths)
    out += [rf'\fill[GeoTint](0,0)rectangle({width},{h});']
    for i,row in enumerate([headers]+data):
        x=0
        for text,w in zip(row,widths):
            out += [rf'\node[pLabel,anchor=west] at({x+.10},{h/2-i*h}){{{text}}};']
            x+=w
        out += [rf'\draw[Rule](0,{-i*h})--({width},{-i*h});']
    return end(out)

PV=stats('pvalue')
FS=stats('fossili_stats')
PL=stats('pianificazione')
WB=stats('welch_browser_stats')
rr=rows('riferimenti')

# 20: area delle due code, riferimento esatto t con 20 gradi di libertà.
o,xx,yy=axes(-6,6,.42,[-4,-2,0,2,4],[0,.2,.4],'statistica $t$','densità')
tail(o,rr,'x','t20',xx,yy,-2,'left'); tail(o,rr,'x','t20',xx,yy,2,'right')
curve(o,rr,'x','t20',xx,yy)
for x in [-2,2]:
    o += [rf'\draw[GeoB,dashed]({xx(x)},0)--({xx(x)},2.42);']
o += [r'\node[pNote,text=GeoB] at(7.4,2.15){$|t|\geq 2$};']
code(20,'p_bilaterale',r'''
# Riferimento t con 20 gradi di liberta'
t20 <- 2
nu20 <- 20
p20 <- 2 * pt(-abs(t20), df = nu20)
p20  # Circa 0.0593
''')
S(20,'Il p-value è un’area nel riferimento',E,r'''
\PLabel{Due code per una differenza bilaterale}
'''+end(o)+r'''
\[
p=\Pr_{H_0}\!\left(|T|\geq|t_{\mathrm{obs}}|\right).
\]
\PSmall{La probabilità usa il modello nullo, il disegno e la regola di estremità dichiarati. Il grafico mostra $T\sim t_{20}$ e $t_{\mathrm{obs}}=2$.}
''',r'''
\PCode{R · probabilità nelle due code}{020_p_bilaterale.R}
\PBody{\texttt{pt()} è la funzione di ripartizione della distribuzione $t$. La simmetria permette di raddoppiare la coda a sinistra di $-|t_{\mathrm{obs}}|$.}
\PInfo{Qui $p\simeq0{,}0593$. L’area è calcolata sull’intera distribuzione; il disegno visualizza soltanto l’intervallo da $-6$ a $6$.}
''','Il p-value confronta la statistica osservata con risultati almeno altrettanto estremi sotto il riferimento nullo.')

o,xx,yy=axes(-6,6,.42,[-4,-2,0,2,4],[0,.2,.4],'statistica standardizzata','densità')
curve(o,rr,'x','t5',xx,yy,'GeoB')
curve(o,rr,'x','t20',xx,yy,'GeoA')
curve(o,rr,'x','normale',xx,yy,'GeoC','dashed')
o += [r'\node[pNote,anchor=west,text=GeoB] at(6.4,2.35){$t_5$};',r'\node[pNote,anchor=west,text=GeoA] at(6.4,1.95){$t_{20}$};',r'\node[pNote,anchor=west,text=GeoC] at(6.4,1.55){$\mathcal N(0,1)$};']
code(21,'gradi_liberta',r'''
# Stessa statistica, riferimenti diversi
2 * pt(-2, df = 5)
2 * pt(-2, df = 20)
2 * pnorm(-2)
# La scelta del riferimento va motivata.
''')
S(21,'La statistica richiede un riferimento',E,r'''
\PLabel{Le code dipendono dai gradi di libertà}
'''+end(o)+rf'''
\[
p_{{t_5}}={fmt(PV['p5'],4)},\quad
p_{{t_{{20}}}}={fmt(PV['p20'],4)},\quad
p_Z={fmt(PV['pz'],4)}.
\]
\PSmall{{Tutti e tre i valori usano $|t_{{\mathrm{{obs}}}}|=2$. La normale standard è il limite della famiglia $t_\nu$ per $\nu\to\infty$.}}
''',r'''
\PCode{R · la stessa distanza dal centro}{021_gradi_liberta.R}
\PSmall{Pochi gradi di libertà corrispondono a code più pesanti: una stessa statistica ha probabilità di coda differenti.}
\PInfo{I gradi di libertà derivano dal modello e dalla stima della variabilità.}
''','Un valore della statistica, senza modello e gradi di libertà, non determina il p-value.')

code(22,'direzione',r'''
t22 <- 2
nu22 <- 20
# Alternativa: Delta > 0, scelta prima
pt(t22, nu22, lower.tail = FALSE)
# Alternativa: Delta diverso da zero
2 * pt(-abs(t22), nu22)
''')
S(22,'Scegliere prima la direzione',E,r'''
\PLabel{Due domande sullo stesso contrasto}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.3cm] (q) at(1.9,2.0){Domanda scientifica\\$\Delta=\mu_B-\mu_A$};
\node[pFlow,text width=3.2cm,fill=GeoA!8] (b) at(7.2,3.0){$H_1:\Delta\ne0$\\due direzioni};
\node[pFlow,text width=3.2cm,fill=GeoB!8] (u) at(7.2,1.0){$H_1:\Delta>0$\\direzione prefissata};
\draw[pEdge](q.east)--++(.55,0)|-(b.west);
\draw[pEdge](q.east)--++(.55,0)|-(u.west);
\end{tikzpicture}
\[
p_{\mathrm{due}}=2\Pr(T\leq-|t_{\mathrm{obs}}|),\qquad
p_{\mathrm{destra}}=\Pr(T\geq t_{\mathrm{obs}}).
\]
\PSmall{Formule per un riferimento continuo simmetrico. Per un’alternativa a destra, un effetto osservato negativo non è evidenza nella direzione prevista.}
''',r'''
\PCode{R · alternativa dichiarata}{022_direzione.R}
\PBody{Per $t_{\mathrm{obs}}=2$ e $\nu=20$, la coda destra vale circa $0{,}0296$. Il valore bilaterale è circa $0{,}0593$.}
\PInfo{Scegliere la direzione dopo aver visto il segno cambia la procedura. La calibrazione del test deve tenere conto di tale scelta.}
''','La direzione dell’alternativa deriva dalla domanda e si definisce prima di osservare il risultato.')

S(23,'Le probabilità condizionate hanno un verso',E,r'''
\PLabel{Quale quantità è nota e quale è calcolata?}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.0cm] (h) at(1.8,3.1){Modello $H_0$\\e disegno assunti};
\node[pFlow,text width=3.7cm,fill=GeoA!8] (d) at(7.0,3.1){Risultati almeno\\altrettanto estremi};
\draw[pEdge](h)--node[pNote,above]{probabilità}(d);
\node[pFlow,text width=3.0cm] (obs) at(1.8,1.05){Dati osservati};
\node[pFlow,text width=3.7cm,fill=GeoC!8] (post) at(7.0,1.05){Probabilità delle ipotesi\\dato un modello bayesiano};
\draw[pEdge,draw=GeoC](obs)--node[pNote,above]{altra analisi}(post);
\end{tikzpicture}
\[
\Pr(\text{estremità}\mid H_0)\ne\Pr(H_0\mid\text{dati}).
\]
''',r'''
\PLabel{Un’interpretazione corretta}
\PBody{«Se il modello nullo e le ipotesi del test valgono, una statistica almeno altrettanto estrema ha probabilità $p$.»}
\vspace{2mm}
\PLabel{Due conclusioni da correggere}
\PSmall{«$p=0{,}03$: l’ipotesi nulla ha probabilità $3\%$.»\\
«$p=0{,}03$: il risultato è dovuto al caso con probabilità $3\%$.»}
\PInfo{Il p-value non assegna probabilità alle ipotesi e non misura la quota di effetto attribuibile al caso.}
''','Condizionare su un’ipotesi e assegnare una probabilità a quell’ipotesi sono operazioni differenti.')

code(24,'soglie_vicine',r'''
p24 <- c(0.049, 0.051)
t24 <- qt(1 - p24 / 2, df = 20)
data.frame(p = p24, t = t24,
  rifiuto = p24 <= 0.05)
''')
S(24,'Due valori vicini alla soglia',E,r'''
\PLabel{La decisione cambia al confine; l’evidenza è vicina}
'''+table([r'$p$',r'$|t|$ con $\nu=20$',r'Decisione a $\alpha=0{,}05$'],[
['$0{,}049$',f"${fmt(PV['q49'],4)}$",'Rifiuto'],['$0{,}051$',f"${fmt(PV['q51'],4)}$",'Mancato rifiuto']],[1.6,2.9,4.7],.82)+r'''
\vspace{3mm}
\PBody{La regola di decisione è discreta. La distanza fra i due p-value rimane piccola e non giustifica descrizioni scientifiche opposte.}
\[
\text{riportare:}\quad\widehat\Delta,\quad IC,\quad p,\quad n,\quad\text{metodo}.
\]
''',r'''
\PCode{R · due punti attorno al confine}{024_soglie_vicine.R}
\PBody{\texttt{qt()} inverte la funzione di ripartizione. Ricostruisce qui le statistiche bilaterali corrispondenti ai due p-value.}
\PInfo{Usare «significativo» e «non significativo» come descrizioni complete nasconde l’entità dell’effetto e la precisione.}
''','Una soglia rende operativa una decisione; il resoconto conserva stima, intervallo e valore numerico del p-value.')

code(25,'effetto_precisione',r'''
# Intervalli illustrativi: stima e SE
d25 <- c(0.2, 0.2, 1.0, 1.0)
se25 <- c(0.05, 0.4, 0.2, 0.8)
data.frame(stima = d25,
  minimo = d25 - 1.96 * se25,
  massimo = d25 + 1.96 * se25)
''')
o=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
x=lambda v:2.0+(v+.8)*2.15
o += [rf'\draw[Muted,dashed]({x(0)},.1)--({x(0)},3.7);']
for i,(lab,est,se) in enumerate([('Piccolo, preciso',.2,.05),('Piccolo, incerto',.2,.4),('Grande, preciso',1,.2),('Grande, incerto',1,.8)]):
    y=3.4-i*.88;lo=est-1.96*se;hi=est+1.96*se
    o += [rf'\node[pNote,anchor=east] at(2.0,{y}){{{lab}}};',rf'\draw[GeoA,line width=1.4pt]({x(lo)},{y})--({x(hi)},{y});',rf'\fill[GeoA]({x(est)},{y})circle(2pt);']
o += [r'\draw[pAxis](2,-.1)--(9.45,-.1);']
for v in [0,1,2]:o += [rf'\node[pNote,below] at({x(v)},-.15){{$ {v} $}};']
o += [r'\node[pNote] at(5.7,-.77){contrasto, unità convenzionali};']
S(25,'Effetto e precisione sono due informazioni',E,r'''
\PLabel{Quattro intervalli costruiti per illustrare la lettura}
'''+end(o)+r'''
\PSmall{Punti: stime. Segmenti: $\widehat\Delta\pm1{,}96\,SE$. Sono esempi didattici, senza dati osservati sottostanti. «Piccolo» e «grande» richiedono un contesto scientifico.}
''',r'''
\PCode{R · cambiare stima e incertezza}{025_effetto_precisione.R}
\PBody{Un effetto vicino a zero può essere stimato con grande precisione. Un effetto numericamente ampio può avere un intervallo molto largo.}
\PInfo{La precisione riguarda l’incertezza della stima. La rilevanza riguarda le conseguenze scientifiche della differenza.}
''','Leggere insieme posizione e ampiezza dell’intervallo permette di distinguere entità dell’effetto e incertezza.')

code(26,'margine_scientifico',r'''
# Margine stabilito prima dei risultati
delta_min26 <- 0.5
ic26 <- c(0.10, 0.30)
# Tutto l'IC illustrativo e' nel margine?
all(ic26 > -delta_min26 &
    ic26 < delta_min26)
''')
S(26,'La rilevanza richiede un criterio scientifico',E,r'''
\PLabel{Una differenza minima da motivare nel problema}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA!10](3.25,.4)rectangle(6.75,3.1);
\draw[Muted,dashed](5,.25)--(5,3.3);
\draw[pAxis](.8,.3)--(9.2,.3);
\foreach \x/\v in {1.5/-1,3.25/-0.5,5/0,6.75/0.5,8.5/1}{\node[pNote,below] at(\x,.2){$\v$};}
\draw[GeoA,line width=1.6pt](5.35,1.3)--(6.05,1.3);
\fill[GeoA](5.7,1.3)circle(2.2pt);
\node[pLabel] at(5,2.6){$[-\delta_*,\delta_*]$};
\node[pNote] at(5,-.65){contrasto, unità convenzionali};
\end{tikzpicture}
\PBody{Esempio: $\delta_*=0{,}5$ e intervallo $[0{,}10;0{,}30]$. Lo zero è escluso, ma l’intero intervallo rimane entro il margine scientifico dichiarato.}
''',r'''
\PCode{R · collocare un intervallo}{026_margine_scientifico.R}
\PSmall{Il margine deriva dal problema scientifico e ha le stesse unità di $\Delta$.}
\PInfo{Questo controllo descrive la posizione dell’intervallo. L’equivalenza richiede una procedura inferenziale specifica.}
''','Il criterio di rilevanza si definisce con conoscenze del problema; un p-value piccolo non ne stabilisce l’entità.')

S(27,'Un mancato rifiuto conserva più possibilità',E,r'''
\PLabel{Intervalli diversi possono entrambi contenere zero}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA!10](3.75,.1)rectangle(6.25,3.6);
\draw[Muted,dashed](5,.05)--(5,3.6);
\draw[GeoA,line width=1.6pt](4.4,2.7)--(5.6,2.7);
\fill[GeoA](5,2.7)circle(2pt);
\node[pNote,anchor=east] at(3.3,2.7){stima precisa};
\draw[GeoB,line width=1.6pt](1.3,1.4)--(8.7,1.4);
\fill[GeoB](5,1.4)circle(2pt);
\node[pNote,anchor=west] at(1.3,.75){stima poco precisa};
\draw[pAxis](.8,0)--(9.2,0);
\node[pNote,below] at(3.75,-.1){$-\delta_*$};
\node[pNote,below] at(5,-.1){$0$};
\node[pNote,below] at(6.25,-.1){$\delta_*$};
\end{tikzpicture}
\PBody{Un intervallo ampio può comprendere sia differenze trascurabili sia differenze scientificamente importanti.}
''',r'''
\PLabel{Formulazioni utili}
\PBody{«I dati non consentono di escludere differenze comprese fra questi limiti.»}
\vspace{2mm}
\PBody{«La stima è vicina a zero, ma l’incertezza è ampia rispetto al margine di interesse.»}
\PInfo{Per sostenere l’equivalenza occorre mostrare, con una procedura appropriata e margini prefissati, che le differenze incompatibili con l’equivalenza sono escluse.}
''','Non rifiutare una differenza nulla non dimostra uguaglianza, assenza di effetto o equivalenza scientifica.')

S(28,'Gli errori si definiscono nelle ripetizioni',E,r'''
\PLabel{Stato della popolazione e decisione della procedura}
'''+table(['Decisione','$H_0$ vera','$H_0$ falsa'],[
['Rifiutare $H_0$','Errore di I tipo','Rifiuto corretto'],
['Non rifiutare',r'Mancato rifiuto\\corretto','Errore di II tipo']],[2.5,3.2,3.65],.95)+r'''
\[
\Pr_{H_0}(\text{rifiuto})\leq\alpha,
\qquad\operatorname{Potenza}(\Delta)=1-\beta(\Delta).
\]
\PSmall{La seconda probabilità dipende dall’alternativa vera, dalla variabilità, dalla numerosità e dal disegno.}
''',r'''
\PLabel{Che cosa controlla il livello?}
\PBody{Con $\alpha=0{,}05$, una procedura valida rifiuta al massimo nel $5\%$ delle ripetizioni compatibili con $H_0$, alle condizioni dichiarate.}
\PInfo{Il livello non è la probabilità che la singola conclusione riportata sia errata. Anche una decisione corretta deve essere accompagnata dalla stima dell’effetto.}
''','Livello e potenza descrivono le prestazioni della procedura su campioni ripetuti, con stati della popolazione specificati.')

o,xx,yy=axes(0,1,1,[0,.25,.5,.75,1],[0,.5,1],'soglia $u$',r'frequenza $p\leq u$',h=2.65)
o += [rf'\draw[GeoC,dashed,line width=1pt]({xx(0)},0)--({xx(1)},{yy(1)});']
curve(o,rows('calibrazione'),'u','F',xx,yy,'GeoA')
o += [r'\node[pNote,text=GeoA] at(6.6,.6){5\,000 campioni};']
code(29,'calibrazione',r'''
set.seed(6029)
# Z standard normale sotto H0
z29 <- rnorm(5000)
p29 <- 2 * pnorm(-abs(z29))
mean(p29 <= 0.05)
# Frequenza Monte Carlo, non identita'
''')
S(29,'Un p-value valido è calibrato sotto $H_0$',E,r'''
\PLabel{Un riferimento continuo esatto produce p uniformi}
'''+end(o)+r'''
\[
\Pr_{H_0}(p\leq u)\leq u,\qquad 0\leq u\leq1.
\]
\PSmall{Nel caso continuo esatto vale l’uguaglianza. Con statistiche discrete il test può essere conservativo. La curva empirica oscilla attorno alla diagonale.}
''',r'''
\PCode{R · ripetere un riferimento nullo}{029_calibrazione.R}
\PBody{Qui ogni $Z$ simulato rappresenta una statistica sotto $H_0$. Il modello normale noto rende il p-value continuo ed esatto.}
\PInfo{Una verifica di calibrazione riguarda il procedimento completo, comprese selezioni del modello, filtri e regole di arresto.}
''','La calibrazione confronta la frequenza dei p-value piccoli sotto $H_0$ con la soglia usata per decidere.')

pr=rows('potenza_normale');pn=stats('potenza_normale_stats')
o,xx,yy=axes(-6,6,.42,[-4,-2,0,2,4],[0,.2,.4],'statistica $Z$','densità',h=2.5)
tail(o,pr,'x','H1',xx,yy,-pn['critico'],'left','GeoB');tail(o,pr,'x','H1',xx,yy,pn['critico'],'right','GeoB')
curve(o,pr,'x','H0',xx,yy,'GeoA');curve(o,pr,'x','H1',xx,yy,'GeoB')
for z in [-pn['critico'],pn['critico']]:o += [rf'\draw[Muted,dashed]({xx(z)},0)--({xx(z)},2.5);']
o += [r'\node[pNote,text=GeoA] at(1.85,2.2){$H_0$};',r'\node[pNote,text=GeoB] at(7.6,2.2){$\Delta=0{,}5$};']
code(30,'potenza_normale',r'''
# Due gruppi, sigma noto = 1
se30 <- sqrt(2 / 30)
eta30 <- 0.5 / se30
c30 <- qnorm(0.975)
pnorm(-c30, mean = eta30) +
  pnorm(c30, eta30, lower.tail = FALSE)
''')
S(30,'La potenza dipende dall’effetto vero',E,r'''
\PLabel{Esempio normale: varianze note e due gruppi indipendenti}
'''+end(o)+r'''
\[
Z\sim\mathcal N\!\left(\frac{\Delta}{\sigma\sqrt{2/n}},1\right).
\]
\PSmall{Nel disegno $n=30$ per gruppo, $\sigma=1$, $\alpha=0{,}05$. L’area arancione oltre le due soglie è la potenza per $\Delta=0{,}5$.}
''',r'''
\PCode{R · area di rifiuto sotto l’alternativa}{030_potenza_normale.R}
\PSmall{La soglia viene fissata sotto $H_0$. La potenza usa poi la distribuzione dell’effetto vero specificato.}
\PInfo{Questo esempio assume varianza nota. Il laboratorio usa il test $t$ con dispersione comune.}
''','La stessa regola di rifiuto ha potenze diverse al variare dell’effetto vero e dell’errore standard.')

o,xx,yy=axes(0,300,1,[0,50,100,200,300],[0,.5,.8,1],'$n$ per gruppo','potenza',h=2.65)
curve(o,rows('potenza_t'),'n','d05',xx,yy)
o += [rf'\fill[GeoB]({xx(30)},{yy(PL["p30"])})circle(2.2pt);',r'\node[pNote,text=GeoB,anchor=west] at(2.1,1.0){$n=30$: circa $0{,}478$};']
code(31,'potenza_t',r'''
# n indica la numerosita' di ogni gruppo
pt31 <- power.t.test(n = 30,
  delta = 0.5, sd = 1, sig.level = 0.05,
  type = "two.sample",
  alternative = "two.sided",
  strict = TRUE)
pt31$power
''')
S(31,'La potenza teorica del laboratorio',E,r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m06-potenza}{Laboratorio · m06-potenza}
'''+end(o)+r'''
\PSmall{Due gruppi normali indipendenti, uguale numerosità, deviazione standard comune $\sigma=1$, differenza $\Delta=0{,}5$, test bilaterale con $\alpha=0{,}05$.}
''',r'''
\PCode{R · potenza con varianza stimata}{031_potenza_t.R}
\PSmall{\texttt{strict=TRUE} include rifiuti in entrambe le code. Il calcolo usa la distribuzione $t$ non centrale.}
\PInfo{La curva è teorica: il seme non la modifica. Il modello assume una dispersione comune.}
''','Nel laboratorio n è il numero di osservazioni per gruppo; la potenza è teorica e assume una dispersione comune.')

o,xx,yy=axes(0,300,1,[0,50,100,200,300],[0,.5,.8,1],'$n$ per gruppo','potenza',h=2.65)
for key,col in [('d02','GeoC'),('d05','GeoA'),('d08','GeoB')]:curve(o,rows('potenza_t'),'n',key,xx,yy,col)
o += [r'\node[pNote,text=GeoB] at(3.2,2.92){$\Delta=0{,}8$};',r'\node[pNote,text=GeoA] at(6.0,2.45){$0{,}5$};',r'\node[pNote,text=GeoC] at(7.7,1.45){$0{,}2$};']
code(32,'effetti_potenza',r'''
# Sensibilita' a tre effetti prefissati
sapply(c(0.2, 0.5, 0.8), function(d) {
  power.t.test(n = 60, delta = d,
    sd = 1, sig.level = 0.05,
    type = "two.sample",
    strict = TRUE)$power
})
''')
S(32,'Gli effetti piccoli richiedono più informazione',E,r'''
\PLabel{Stesso modello, tre differenze da rilevare}
'''+end(o)+r'''
\PBody{Con dispersione e livello fissati, aumentare $n$ rende più probabile riconoscere una differenza presente. Rilevare una differenza minore richiede più osservazioni.}
''',r'''
\PCode{R · confronto a n fissato}{032_effetti_potenza.R}
\PSmall{Valutare una gamma plausibile di effetti e dispersioni riduce il rischio di pianificare un campione insufficiente.}
\PInfo{Ricalcolare la potenza sull’effetto stimato dagli stessi dati non sostituisce l’intervallo di confidenza.}
''','La pianificazione parte da effetti scientificamente interessanti e da ipotesi plausibili sulla variabilità.')

code(33,'n_approssimato',r'''
alpha33 <- 0.05
pot33 <- 0.80
sigma33 <- 1
delta33 <- 0.5
n33 <- 2 * sigma33^2 *
  (qnorm(1 - alpha33 / 2) +
   qnorm(pot33))^2 / delta33^2
ceiling(n33)  # 63 per gruppo
''')
S(33,'Una formula per pianificare la numerosità',E,r'''
\PLabel{Approssimazione normale per due gruppi bilanciati}
\[
n\simeq
\frac{2\sigma^2\bigl(z_{1-\alpha/2}+z_{1-\beta}\bigr)^2}
{\Delta_*^2}.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.4cm] (a) at(1.45,1.1){Variabilità\\$\sigma$};
\node[pFlow,text width=2.4cm] (b) at(4.75,1.1){Effetto minimo\\$\Delta_*$};
\node[pFlow,text width=2.4cm] (c) at(8.05,1.1){Livello e potenza\\$\alpha,\ 1-\beta$};
\draw[Rule] (.3,.25)--(9.2,.25);
\end{tikzpicture}
\PSmall{$n$: unità indipendenti per gruppo. $\sigma$: deviazione standard comune. $z_q$: quantile della normale standard. L’approssimazione trascura la piccola coda opposta sotto l’alternativa.}
''',r'''
\PCode{R · numerosità approssimata}{033_n_approssimato.R}
\PSmall{Raddoppiare la deviazione standard moltiplica il fabbisogno per quattro. Dimezzare l’effetto minimo ha lo stesso effetto.}
\PInfo{Perdite di osservazioni, dipendenza, campioni sbilanciati e varianze differenti richiedono una pianificazione coerente con quel disegno.}
''','La numerosità è un risultato delle ipotesi su effetto, variabilità, disegno, livello e potenza desiderata.')

code(34,'n_test_t',r'''
# Livello predefinito: 0.05
r34 <- power.t.test(delta = 0.5,
  sd = 1, power = 0.8,
  type = "two.sample", strict = TRUE)
ceiling(r34$n)  # 64 per gruppo
''')
S(34,'Verificare l’arrotondamento di n',E,r'''
\PLabel{Il calcolo t tiene conto della varianza stimata}
'''+table(['Calcolo','$n$ teorico','$n$ intero'],[
['Approssimazione normale',f"${fmt(PL['n_normale'],2)}$",'$63$'],
['Test $t$, varianza comune',f"${fmt(PL['n_t'],2)}$",'$64$']],[4.9,2.15,2.15],.88)+r'''
\vspace{3mm}
\[
\operatorname{Potenza}(n=64,\Delta=0{,}5)\simeq0{,}8015.
\]
\PBody{Si arrotonda per eccesso e si ricalcola la potenza. Il progetto richiede quindi $128$ osservazioni indipendenti complessive.}
''',r'''
\PCode{R · numerosità intera}{034_n_test_t.R}
\PSmall{Il calcolo assume campioni normali indipendenti, uguale numerosità e deviazione standard comune pari a uno.}
\PInfo{Differenza minima e variabilità devono essere motivate con informazioni adeguate al futuro studio.}
''','Il numero di osservazioni deve essere intero; dopo l’arrotondamento controllare la potenza e il costo complessivo.')

o,xx,yy=axes(0,100,.3,[0,20,40,60,80,100],[0,.05,.15,.25],'osservazioni accumulate','frequenza di rifiuto',h=2.6)
curve(o,rows('arresto'),'n','qualsiasi',xx,yy,'GeoB')
curve(o,rows('arresto'),'n','finale',xx,yy,'GeoA')
o += [r'\node[pNote,text=GeoB,anchor=west] at(2.1,2.25){almeno un superamento};',r'\node[pNote,text=GeoA,anchor=west] at(3.0,.82){un solo controllo finale};']
code(35,'regola_arresto',r'''
set.seed(6035)
x35 <- rnorm(100)  # H0: media zero
n35 <- seq(10, 100, 10)
z35 <- cumsum(x35)[n35] / sqrt(n35)
any(abs(z35) > qnorm(0.975))
# Un percorso; la figura ne ripete 5000.
''')
S(35,'La regola di arresto fa parte del test',E,r'''
\PLabel{Controllare ripetutamente cambia la probabilità di rifiuto}
'''+end(o)+r'''
\PSmall{Simulazione: $5\,000$ sequenze di $100$ osservazioni $\mathcal N(0,1)$. Test $z$ bilaterale con varianza nota; controlli ogni $10$ osservazioni, sempre alla soglia nominale $0{,}05$.}
''',r'''
\PCode{R · seguire un campione progressivo}{035_regola_arresto.R}
\PBody{Fermarsi appena $p<0{,}05$ offre più occasioni di rifiutare. La regola risultante non mantiene il livello del singolo controllo.}
\PInfo{Fissare l’analisi finale in anticipo oppure usare un disegno sequenziale che controlli esplicitamente l’errore.}
''','La calibrazione riguarda anche quando si guarda il risultato e quando si decide di interrompere la raccolta.')

code(36,'piano_analisi',r'''
# Schema da completare prima dei dati
piano36 <- list(contrasto = "B - A",
  alternativa = "two.sided",
  alpha = 0.05, effetto_minimo = 0.5,
  n_per_gruppo = 64,
  analisi = "una volta, a n fissato")
str(piano36)
''')
S(36,'Dalla domanda a un piano di analisi',E,r'''
\PLabel{Decisioni da documentare prima del risultato}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.1,3.4){Contrasto, unità\\e margine scientifico};
\node[pFlow,text width=3.7cm] (b) at(7.3,3.4){Campionamento\\e osservazioni indipendenti};
\node[pFlow,text width=3.7cm] (c) at(2.1,1.45){Metodo, alternativa\\e livello $\alpha$};
\node[pFlow,text width=3.7cm] (d) at(7.3,1.45){Numerosità, esclusioni\\e regola di arresto};
\draw[pEdge](a)--(b);
\draw[pEdge](a)--(c);
\draw[pEdge](b)--(d);
\end{tikzpicture}
\PBody{Gli esiti dell’analisi possono portare a nuove domande. Le analisi esplorative si descrivono come tali e conservano le scelte effettivamente compiute.}
''',r'''
\PCode{R · conservare le scelte}{036_piano_analisi.R}
\PSmall{Questo elenco registra soltanto alcune voci. Il metodo scelto deve essere compatibile con disegno e modello usati nella pianificazione.}
\PInfo{La lista R documenta il piano. Non corregge automaticamente p-value, selezioni o arresti non previsti.}
''','Un piano esplicito rende interpretabili sia le decisioni confermative sia le successive analisi esplorative.')

# 37–46: Welch, con caso ricorrente dei 160 fossili sintetici.
code(37,'dati_fossili',r'''
f37 <- read.csv("Dati/fossili_simulati.csv")
a37 <- f37$diametro_tot_um[
  f37$morfotipo == "Rounded"]
b37 <- f37$diametro_tot_um[
  f37$morfotipo == "Spiky"]
c(A = length(a37), B = length(b37))
''')
S(37,'La varianza di una differenza di medie',W,r'''
\PLabel{Due campioni indipendenti; contrasto B meno A}
\[
\begin{aligned}
\operatorname{Var}(\bar X_B-\bar X_A)
&=\operatorname{Var}(\bar X_B)+\operatorname{Var}(\bar X_A)\\
&=\frac{\sigma_B^2}{n_B}+\frac{\sigma_A^2}{n_A}.
\end{aligned}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.1cm,fill=GeoA!8] (a) at(1.9,1.6){Rounded, $n_A=80$\\$\bar X_A$};
\node[pFlow,text width=3.1cm,fill=GeoB!8] (b) at(7.3,1.6){Spiky, $n_B=80$\\$\bar X_B$};
\node[pNote] at(4.6,.4){indipendenza fra e dentro i gruppi};
\end{tikzpicture}
\PSmall{In generale compare anche $-2\operatorname{Cov}(\bar X_A,\bar X_B)$. L’indipendenza azzera questo termine. Le varianze devono essere finite.}
''',r'''
\PCode{R · due vettori, stesso significato}{037_dati_fossili.R}
\PSmall{Nei dati sintetici del corso confrontiamo il diametro totale, in micrometri: Spiky meno Rounded.}
\PInfo{Sotto indipendenza le varianze si sommano: il segno meno viene elevato al quadrato.}
''','L’indipendenza giustifica la somma delle varianze; in un disegno appaiato occorre considerare la covarianza.')

code(38,'errore_standard',r'''
# Contributi delle due varianze stimate
va38 <- var(a37) / length(a37)
vb38 <- var(b37) / length(b37)
se38 <- sqrt(va38 + vb38)
c(A = va38, B = vb38, SE = se38)
''')
S(38,'Ogni gruppo contribuisce all’incertezza',W,r'''
\PLabel{La dispersione di ciascun gruppo è stimata separatamente}
\[
SE_W=\sqrt{\frac{s_A^2}{n_A}+\frac{s_B^2}{n_B}}.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA!80](.5,.9)rectangle(5.22,1.9);
\fill[GeoB!85](5.22,.9)rectangle(9.2,1.9);
\node[pLabel,text=white] at(2.86,1.4){$s_A^2/n_A=0{,}01251$};
\node[pLabel,text=white] at(7.21,1.4){$s_B^2/n_B=0{,}01057$};
\node[pNote] at(4.85,.3){somma $0{,}02308\ \mu\mathrm m^2$};
\end{tikzpicture}
\[
SE_W=\sqrt{0{,}02308}\simeq0{,}15192\ \mu\mathrm m.
\]
\PSmall{$s_A^2,s_B^2$: varianze campionarie; $n_A,n_B$: unità indipendenti. I due termini sono rappresentati in proporzione al loro contributo.}
''',r'''
\PCode{R · costruire l’errore standard}{038_errore_standard.R}
\PBody{\texttt{var()} restituisce la varianza campionaria con denominatore $n-1$. Ogni varianza viene divisa per la propria numerosità.}
\PInfo{Le varianze hanno unità $\mu\mathrm m^2$. La radice riporta l’errore standard nelle stesse unità della differenza.}
''','Welch usa una stima separata della variabilità in ciascun gruppo; l’errore standard conserva le unità del contrasto.')

code(39,'statistica_welch',r'''
d39 <- mean(b37) - mean(a37)
d0_39 <- 0  # Contrasto sotto H0
t39 <- (d39 - d0_39) / se38
c(stima = d39, SE = se38, t = t39)
''')
S(39,'Esprimere la distanza in errori standard',W,r'''
\PLabel{La statistica di Welch}
\[
t_W=\frac{\widehat\Delta-\Delta_0}{SE_W},
\qquad \widehat\Delta=\bar x_B-\bar x_A.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.65,.8)--(9.1,.8);
\foreach \x/\v in {1/0,3/1,5/2,7/3,9/4}{\draw[Muted](\x,.8)--(\x,.67);\node[pNote,below] at(\x,.6){$\v$};}
\draw[GeoB,line width=1.5pt,-{Latex}](1,1.65)--(8.662,1.65);
\fill[GeoB](8.662,.8)circle(2.3pt);
\node[pLabel] at(5,2.25){$t_W\simeq3{,}831$};
\node[pNote] at(5,-.1){distanza da $\Delta_0=0$ in unità di $SE_W$};
\end{tikzpicture}
\PSmall{Fossili sintetici: $\widehat\Delta\simeq0{,}58203\ \mu\mathrm m$ e $SE_W\simeq0{,}15192\ \mu\mathrm m$.}
''',r'''
\PCode{R · standardizzare la differenza}{039_statistica_welch.R}
\PBody{La divisione elimina le unità fisiche. Il segno positivo indica una media campionaria maggiore per Spiky.}
\PInfo{La statistica misura una distanza dal contrasto nullo rispetto all’incertezza stimata. Non è una misura dell’importanza geologica.}
''','La statistica t esprime la distanza dal valore nullo in errori standard; segno e unità dell’effetto vanno riportati separatamente.')

code(40,'gradi_welch',r'''
na40 <- length(a37)
nb40 <- length(b37)
nu40 <- (va38 + vb38)^2 /
  (va38^2 / (na40 - 1) +
   vb38^2 / (nb40 - 1))
nu40  # Circa 156.89; puo' non essere intero
''')
o,xx,yy=axes(.5,4,65,[.5,1,2,3,4],[30,45,60],'rapporto $s_B/s_A$','gradi di libertà',h=1.6)
curve(o,rows('welch_df'),'ratio','df',xx,yy)
S(40,'I gradi di libertà di Welch',W,r'''
\PLabel{Approssimazione di Welch–Satterthwaite}
\[
\nu=\frac{(v_A+v_B)^2}
{v_A^2/(n_A-1)+v_B^2/(n_B-1)},\qquad
v_g=\frac{s_g^2}{n_g}.
\]
'''+end(o)+r'''
\PSmall{Curva illustrativa con $n_A=n_B=30$: varia il rapporto fra le deviazioni standard campionarie. Contributi più sbilanciati riducono i gradi di libertà.}
''',r'''
\PCode{R · gradi di libertà effettivi}{040_gradi_welch.R}
\PBody{Nel caso dei fossili otteniamo $\nu\simeq156{,}89$. R accetta gradi di libertà non interi nella distribuzione $t$.}
\PInfo{Il riferimento è approssimato anche con popolazioni normali e varianze diverse. Non si impone una varianza comune.}
''','I gradi di libertà di Welch dipendono da numerosità e contributi di variabilità dei due gruppi.')

code(41,'intervallo_welch',r'''
q41 <- qt(0.975, df = nu40)
ic41 <- d39 + c(-1, 1) * q41 * se38
p41 <- 2 * pt(-abs(t39), df = nu40)
c(minimo = ic41[1], massimo = ic41[2],
  p = p41)
''')
S(41,'L’intervallo usa lo stesso riferimento',W,r'''
\PLabel{Intervallo di Welch bilaterale al 95\%}
\[
\widehat\Delta\pm t_{\nu,\,0{,}975}\,SE_W.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.5,.5)--(9.2,.5);
\draw[Muted,dashed](1,.5)--(1,2.6);
\draw[GeoA,line width=1.6pt](3.256,1.6)--(8.057,1.6);
\draw[GeoA,line width=1pt](3.256,1.43)--(3.256,1.77);
\draw[GeoA,line width=1pt](8.057,1.43)--(8.057,1.77);
\fill[GeoA](5.656,1.6)circle(2.4pt);
\node[pNote,above] at(5.656,1.85){$\widehat\Delta=0{,}582$};
\foreach \x/\v in {1/0,3.256/0.282,5.656/0.582,8.057/0.882}{\node[pNote,below] at(\x,.45){$\v$};}
\node[pNote] at(4.85,-.3){Spiky meno Rounded ($\mu\mathrm m$)};
\end{tikzpicture}
\PSmall{Il segmento non contiene zero; il p-value bilaterale vale circa $0{,}000184$. Entrambe le letture usano le medesime ipotesi di Welch.}
''',r'''
\PCode{R · quantile, intervallo e p-value}{041_intervallo_welch.R}
\PBody{L’intervallo conserva l’entità della differenza nelle unità originali e i valori compatibili con il procedimento inferenziale adottato.}
\PInfo{Il livello del $95\%$ riguarda la copertura del metodo nelle ripetizioni, alle condizioni del modello e del disegno.}
''','Per un medesimo test bilaterale e livello, l’esclusione del valore nullo dall’intervallo corrisponde al rifiuto del test.')

code(42,'t_test',r'''
# Il primo argomento definisce B - A.
tt42 <- t.test(b37, a37,
  mu = 0, alternative = "two.sided",
  var.equal = FALSE, conf.level = 0.95)
tt42$estimate
tt42$conf.int
tt42$p.value
''')
S(42,'R restituisce tutti gli elementi del confronto',W,r'''
\PLabel{Leggere l’output senza perdere l’ordine dei gruppi}
'''+table(['Componente','Significato','Fossili'],[
[r'\texttt{estimate}','Medie di B e A',r'$6{,}646;\ 6{,}064$'],
[r'\texttt{statistic}','$t_W$','$3{,}831$'],
[r'\texttt{parameter}',r'$\nu$','$156{,}889$'],
[r'\texttt{conf.int}','IC di B meno A','$[0{,}282;0{,}882]$'],
[r'\texttt{p.value}','Probabilità bilaterale','$0{,}000184$']],[2.35,4.8,2.45],.67)+r'''
\PSmall{L’oggetto contiene le due medie, non soltanto la loro differenza. Il contrasto e l’intervallo seguono l’ordine degli argomenti.}
''',r'''
\PCode{R · t.test sui vettori}{042_t_test.R}
\PSmall{\texttt{var.equal=FALSE} richiede Welch ed è anche il valore predefinito. Specificarlo rende visibile la scelta nel codice.}
\PInfo{Invertire i due vettori cambia il segno del contrasto e ribalta l’intervallo. Nel test bilaterale il p-value resta uguale.}
''','Nell’output controllare sempre il metodo dichiarato, l’ordine dei gruppi, l’intervallo e le unità della variabile.')

o=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
xx=lambda v:.7+(v-3)/6.7*8.3
for r in rows('fossili_punti'):
    y=(1.2 if r['gruppo']=='A' else 2.5)+float(r['offset'])
    col='GeoA' if r['gruppo']=='A' else 'GeoB'
    o += [rf'\fill[{col},opacity=.64]({xx(float(r["valore"])):.4f},{y:.4f})circle(1.2pt);']
o += [r'\draw[pAxis](.6,.4)--(9.2,.4);',r'\node[pNote,anchor=west,text=GeoA] at(.8,1.65){Rounded};',r'\node[pNote,anchor=west,text=GeoB] at(.8,2.95){Spiky};']
for v in [3,4,5,6,7,8,9]:o += [rf'\node[pNote,below] at({xx(v)},.32){{$ {v} $}};']
o += [r'\node[pNote] at(4.85,-.3){diametro totale ($\mu\mathrm m$)};']
code(43,'osservare_gruppi',r'''
# Controllo descrittivo prima del test
by(f37$diametro_tot_um, f37$morfotipo,
  function(x) c(n = length(x),
    media = mean(x), sd = sd(x),
    minimo = min(x), massimo = max(x)))
''')
S(43,'Il controllo del disegno precede il calcolo',W,r'''
\PLabel{Le osservazioni restano visibili}
'''+end(o)+r'''
\PBody{Verificare unità indipendenti, criteri di selezione, errori di misura e valori anomali. Campioni piccoli con forte asimmetria o code pesanti richiedono particolare attenzione.}
''',r'''
\PCode{R · descrivere senza eliminare dati}{043_osservare_gruppi.R}
\PSmall{L’inferenza normale è approssimata da Welch; in grandi campioni può essere sostenuta da risultati asintotici, con varianze finite e condizioni adeguate.}
\PInfo{Un grafico non dimostra indipendenza o rappresentatività. Il test non trasforma un campione osservazionale in un esperimento causale.}
''','La correttezza del comando non verifica il disegno: dipendenza, selezione e qualità delle misure richiedono informazioni sul campionamento.')

code(44,'varianze_separate',r'''
# Nessun obbligo di pretest delle varianze
t.test(b37, a37, var.equal = FALSE)
# Confronto descrittivo delle dispersioni
c(sdA = sd(a37), sdB = sd(b37))
''')
S(44,'Varianze diverse: esplicitare il modello',W,r'''
\PLabel{Una scelta coerente con la domanda e il disegno}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.2cm] (a) at(1.9,2.8){Due medie\\campioni indipendenti};
\node[pFlow,text width=3.5cm,fill=GeoA!8] (w) at(7.0,3.65){Welch\\varianze separate};
\node[pFlow,text width=3.5cm,fill=GeoC!8] (s) at(7.0,1.75){Test $t$ a varianza comune\\ipotesi aggiuntiva};
\draw[pEdge](a.east)--++(.6,0)|-(w.west);
\draw[pEdge](a.east)--++(.6,0)|-(s.west);
\node[pNote,text width=8.7cm] at(4.8,.3){L’uguaglianza delle varianze è un’ipotesi sul modello.\\Un pretest non la certifica e introduce una scelta dipendente dai dati.};
\end{tikzpicture}
''',r'''
\PCode{R · dichiarare il metodo}{044_varianze_separate.R}
\PSmall{Welch confronta medie indipendenti senza imporre dispersioni uguali. Rimangono necessarie le altre condizioni del metodo.}
\PInfo{Anche la differenza di variabilità può avere interesse scientifico e va descritta.}
''','Usare varianze separate evita l’ipotesi di omoscedasticità; non risolve automaticamente dipendenza, selezione o code problematiche.')

code(45,'effetto_standardizzato',r'''
# na40 e nb40: numerosita' gia' calcolate
sp45 <- sqrt(((na40 - 1) * var(a37) +
  (nb40 - 1) * var(b37)) /
  (na40 + nb40 - 2))
d45 <- d39 / sp45
glass45 <- d39 / sd(a37)
c(d_pooled = d45, rispetto_A = glass45)
''')
S(45,'Standardizzare richiede un denominatore',W,r'''
\PLabel{La differenza nelle unità originali rimane il risultato primario}
\[
d=\frac{\widehat\Delta}{s_p},\qquad
s_p=\sqrt{\frac{(n_A-1)s_A^2+(n_B-1)s_B^2}{n_A+n_B-2}}.
\]
'''+table(['Scala','Definizione','Valore'],[
['Originale',r'$\widehat\Delta$',rf"${fmt(FS['delta'])}\ \mu\mathrm m$"],
['SD combinata',r'$\widehat\Delta/s_p$',f"${fmt(FS['d'])}$"],
['SD di A',r'$\widehat\Delta/s_A$',f"${fmt(FS['glassA'])}$"]],[3.1,3.6,2.6],.72)+r'''
\PSmall{Con varianze diverse non esiste una dispersione comune unica. La standardizzazione va motivata e descritta, senza applicare soglie universali di rilevanza.}
''',r'''
\PCode{R · due denominatori dichiarati}{045_effetto_standardizzato.R}
\PSmall{Il rapporto con $s_p$ è descrittivo; il test rimane quello di Welch. Usare $s_A$ esprime l’effetto nella dispersione del gruppo A.}
\PInfo{Il significato dipende dal denominatore e dalla popolazione studiata.}
''','Un effetto standardizzato è interpretabile quando si dichiarano contrasto, denominatore e ragione scientifica della scelta.')

o=[r'\begin{tikzpicture}[x=1cm,y=1cm]'];xx=lambda v:.65+(v+6)/12*8.5
vals=rows('welch_browser')
for i,r in enumerate(vals):
    g=r['gruppo'];y=(1.0 if g=='A' else 2.1)+(i%5-2)*.075;co='GeoA' if g=='A' else 'GeoB'
    o += [rf'\fill[{co}]({xx(float(r["valore"])):.4f},{y})circle(1.4pt);']
o += [r'\draw[pAxis](.6,.3)--(9.3,.3);',r'\node[pNote,text=GeoA,anchor=west] at(.8,1.5){A: $\sigma_A=1$};',r'\node[pNote,text=GeoB,anchor=west] at(.8,2.6){B: $\sigma_B=2$};']
for v in [-6,-3,0,3,6]:o += [rf'\node[pNote,below] at({xx(v)},.25){{$ {v} $}};']
o += [r'\node[pNote] at(4.85,-.4){risposta adimensionale};']
code(46,'browser_welch',r'''
set.seed(17)
a46 <- rnorm(30)
b46 <- rnorm(30, mean = 0.5, sd = 2)
tt46 <- t.test(b46, a46)
mean(b46) - mean(a46)
tt46$conf.int
tt46$p.value
''')
S(46,'Laboratorio: aumentare la dispersione di B',W,r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m06-welch}{Laboratorio · m06-welch}
'''+end(o)+r'''
\PSmall{Impostazioni iniziali: $n=30$ per gruppo, effetto vero $0{,}5$, rapporto fra SD pari a $2$, seme $17$. La stima osservata è circa $0{,}0536$; il suo IC95\% è $[-0{,}919;1{,}026]$.}
''',r'''
\PCode{R · riprodurre il caso iniziale}{046_browser_welch.R}
\PSmall{Il controllo \texttt{ratio} regola $\sigma_B/\sigma_A$: raddoppiarlo quadruplica la varianza relativa. L’effetto vero resta $0{,}5$.}
\PInfo{Predire come cambiano dispersione, errore standard e gradi di libertà. Poi variare il rapporto mantenendo fissi $n$ e seme.}
''','Il rapporto del laboratorio riguarda deviazioni standard: occorre elevarlo al quadrato per ottenere il rapporto delle varianze.')

assert set(SLIDES)==set(range(20,47))
