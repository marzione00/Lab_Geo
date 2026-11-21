from pathlib import Path
import csv, math
ROOT=Path(__file__).resolve().parent
SLIDES={}; CODES={}

def load(name):
    with (ROOT/"root_proof/coordinate"/name).open() as f:
        return list(csv.DictReader(f))
def val(lab,key,scenario="base"):
    for r in load("Valori_riferimento_22_scenari.csv"):
        if (r["laboratorio"],r["scenario"],r["metrica"])==(lab,scenario,key):
            return float(r["valore"])
    raise KeyError((lab,key,scenario))
def it(v,n=3):
    return f"{v:.{n}f}".replace(".","{,}")
def S(n,title,left,right,recall):
    SLIDES[n]=dict(title=title,section="V · APPLICAZIONI E VERIFICA",
                   left=left,right=right,recall=recall)
def code(n,name,s):
    CODES[f"{n:03}_{name}.R"]=s.strip()+"\n"
def link(slug,title):
    return rf"\PLab{{https://marzione00.github.io/Lab_Geo/\#laboratorio/m06-{slug}}}{{{title}}}"+"\n"
def table_diagram(headers,data,widths=(3.8,2.5,2.5),height=.8):
    starts=[.25]
    for w in widths[:-1]: starts.append(starts[-1]+w)
    total=sum(widths)
    top=(len(data)+1)*height
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         rf"\fill[Navy](.25,{top-height:.3f}) rectangle({total+.25:.3f},{top:.3f});"]
    for x,w,h in zip(starts,widths,headers):
        out.append(rf"\node[pLabel,text=white,text width={w-.15:.3f}cm] at({x+w/2:.3f},{top-height/2:.3f}){{{h}}};")
    for k,row in enumerate(data):
        yy=top-height*(k+1.5)
        if k%2==0:out.append(rf"\fill[GeoTint](.25,{yy-height/2:.3f}) rectangle({total+.25:.3f},{yy+height/2:.3f});")
        for x,w,v in zip(starts,widths,row):
            out.append(rf"\node[pLabel,text width={w-.15:.3f}cm] at({x+w/2:.3f},{yy:.3f}){{{v}}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)
def ci_compare(entries,xmin=-1.2,xmax=1.3,axislabel="Contrasto B meno A"):
    def xx(v):return 2.1+6.8*(v-xmin)/(xmax-xmin)
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](2.0,.5)--(9.2,.5);",
         rf"\draw[Muted,dashed]({xx(0):.4f},.5)--({xx(0):.4f},3.8);"]
    for tick in [xmin,0,xmax]:
        out.append(rf"\node[pNote] at({xx(tick):.4f},.1){{$ {it(tick,1)} $}};")
    for j,(label,point,lo,hi,col) in enumerate(entries):
        yy=3.1-j*1.35
        out.append(rf"\node[pNote,anchor=east,text width=1.75cm] at(1.85,{yy:.3f}){{{label}}};")
        out.append(rf"\draw[{col},line width=1.6pt]({xx(lo):.4f},{yy:.3f})--({xx(hi):.4f},{yy:.3f});")
        out.append(rf"\fill[{col}]({xx(point):.4f},{yy:.3f}) circle(2.6pt);")
    out +=[rf"\node[pNote] at(5.5,-.5){{{axislabel}; IC 95\%}};",r"\end{tikzpicture}"]
    return "\n".join(out)
def t_plot():
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](.6,.5)--(9.2,.5);"]
    for scenario,col,df in [("base","GeoA",20),("variante","GeoB",5)]:
        data=load(f"lab_pvalue_{scenario}.csv")[::3]
        coords=" ".join(f"({.75+(float(r['x'])+6)*.68:.4f},{.5+float(r['y'])*7.8:.4f})" for r in data)
        out.append(rf"\draw[{col},line width=1.2pt] plot coordinates{{{coords}}};")
    for t in [-2,2]:
        x=.75+(t+6)*.68
        out.append(rf"\draw[Muted,dashed]({x:.4f},.5)--({x:.4f},3.7);")
    for t in [-4,-2,0,2,4]:
        x=.75+(t+6)*.68
        out.append(rf"\node[pNote] at({x:.4f},.12){{$ {t} $}};")
    out +=[r"\node[pNote,text=GeoA] at(2.6,4.05){$\nu=20$};",
           r"\node[pNote,text=GeoB] at(7.0,4.05){$\nu=5$};",
           r"\node[pNote] at(4.8,-.37){Statistica $t$; linee a $\pm2$};",
           r"\end{tikzpicture}"]
    return "\n".join(out)

code(78,"lab_contrasto",'''
source("setup.R", encoding="UTF-8")
# Cambia solo la differenza vera.
z78 <- lab_contrasto(delta=1)
w78 <- lab_contrasto(delta=0)
rbind(delta1=z78$metrics,
      delta0=w78$metrics)
''')
entries=[]
for scenario,label,col in [("base",r"$\Delta=1$","GeoB"),("variante",r"$\Delta=0$","GeoA")]:
    entries.append((label,val("contrasto","Differenza stimata",scenario),
      val("contrasto","Limite inferiore",scenario),
      val("contrasto","Limite superiore",scenario),col))
S(78,"Laboratorio · effetto vero e stima osservata",
  link("contrasto","Apri il laboratorio: contrasto")+
  ci_compare(entries,xmin=-1,xmax=1.2)+r"""
\PSmall{Fissare $n=30$ per gruppo e seme 17. Cambiare $\Delta$ da 1 a 0. Il generatore ha deviazione standard 1 in entrambi i gruppi.}
\PBody{Prima di eseguire: come cambieranno punto e intervallo?}
""",r"""
\PCode{R · una modifica controllata}{078_lab_contrasto.R}
\PSmall{Le funzioni del progetto restituiscono \texttt{data}, \texttt{metrics} e \texttt{parametri}. Le metriche restano non arrotondate.}
\PInfo{A parità di estrazioni, lo spostamento di B trasla stima e limiti della stessa quantità; la larghezza dell’intervallo resta uguale.}
""","Distinguere il parametro impostato, la stima ottenuta dal campione e l’incertezza stimata.")

code(79,"lab_permutazione",'''
# Lo stesso campione, piu permutazioni
z79 <- lab_permutazione(B=200)
w79 <- lab_permutazione(B=1000)
rbind(B200=z79$metrics,
      B1000=w79$metrics)
# Nessun nuovo individuo aggiunto.
''')
S(79,"Laboratorio · aumentare le permutazioni",
  link("permutazione","Apri il laboratorio: permutazione")+
  table_diagram(["Quantità","$B=200$","$B=1000$"],[
    ["Osservazioni","40","40"],
    ["Contrasto osservato",rf"$ {it(val('permutazione','Contrasto osservato'))} $",rf"$ {it(val('permutazione','Contrasto osservato','variante'))} $"],
    ["$p_{MC}$",rf"$ {it(val('permutazione','p Monte Carlo bilaterale'))} $",rf"$ {it(val('permutazione','p Monte Carlo bilaterale','variante'))} $"],
    ["Minimo possibile","$1/201$","$1/1001$"]])+
  r"""
\PSmall{Mantenere $\Delta=0{,}6$ e seme 17. Variare soltanto $B$ da 200 a 1000. I primi 200 riordini rimangono gli stessi.}
\PBody{Perché il risultato non deve diminuire ogni volta che aumenta $B$?}
""",r"""
\PCode{R · confrontare la precisione del calcolo}{079_lab_permutazione.R}
\PSmall{La direzione della variazione dipende dalle ulteriori permutazioni estratte. Un valore più stabile richiede più simulazioni.}
\PInfo{Il miglioramento riguarda l’errore Monte Carlo; non riduce l’errore standard dovuto al campionamento dei 40 individui.}
""","Più permutazioni migliorano la risoluzione del calcolo. Più osservazioni cambiano l’informazione del campione.")

code(80,"lab_pvalue",'''
# t e df sono assegnati direttamente.
z80 <- lab_pvalue(t=2,df=20)
w80 <- lab_pvalue(t=2,df=5)
rbind(df20=z80$metrics,
      df5=w80$metrics)
2*pt(-abs(2), df=20)
''')
S(80,"Laboratorio · la statistica e il suo riferimento",
  link("pvalue","Apri il laboratorio: p-value")+t_plot()+r"""
\PSmall{Mantenere $t=2$ e ridurre i gradi di libertà da 20 a 5. Il grafico mostra un tratto della densità; il calcolo con \texttt{pt()} comprende le code complete.}
""",rf"""
\PCode{{R · aree di coda complete}}{{080_lab_pvalue.R}}
\PSmall{{Con $\nu=20$, $p={it(val('pvalue','p bilaterale'),4)}$; con $\nu=5$, $p={it(val('pvalue','p bilaterale','variante'),4)}$.}}
\PInfo{{Lo stesso valore della statistica assume un significato diverso se cambia la distribuzione di riferimento. Il seme non interviene in questo calcolo.}}
""","Un p-value dipende dal valore osservato, dalla regola di estremità e dalla distribuzione di riferimento.")

def power_plot():
    coords=" ".join(f"({.8+float(r['x'])*.027:.4f},{.55+float(r['y'])*3.4:.4f})"
                    for r in load("lab_potenza_base.csv"))
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](.8,.55)--(9.2,.55);",
         r"\draw[pAxis](.8,.55)--(.8,4.3);",
         rf"\draw[Classical,line width=1.4pt] plot coordinates{{{coords}}};"]
    for v in [0,.5,1]:
        out.append(rf"\node[pNote,anchor=east] at(.6,{.55+3.4*v}){{$ {it(v,1)} $}};")
    for n,scenario in [(30,"base"),(120,"variante")]:
        x=.8+n*.027;y=.55+3.4*val("potenza","Potenza alla numerosità scelta",scenario)
        out +=[rf"\draw[Muted,dashed]({x:.4f},.55)--({x:.4f},{y:.4f});",
               rf"\fill[GeoB]({x:.4f},{y:.4f}) circle(3pt);",
               rf"\node[pNote] at({x:.4f},.15){{{n}}};"]
    out +=[r"\node[pNote] at(8.9,.15){300};",
           r"\node[pNote,anchor=west] at(1.1,4.3){Potenza};",
           r"\node[pNote] at(5,-.4){Numerosità per gruppo};",
           r"\end{tikzpicture}"]
    return "\n".join(out)
code(81,"lab_potenza",'''
# Calcolo teorico, sd comune = 1
z81 <- lab_potenza(n=30)
w81 <- lab_potenza(n=120)
rbind(n30=z81$metrics,
      n120=w81$metrics)
# Delta=.5 e alfa=.05 restano fissi.
''')
S(81,"Laboratorio · pianificare la numerosità",
  link("potenza","Apri il laboratorio: potenza")+power_plot()+r"""
\PSmall{Due gruppi normali indipendenti, $\sigma=1$, $\Delta=0{,}5$, $\alpha=0{,}05$. Il parametro $n$ conta osservazioni per gruppo: 120 significa 240 in totale.}
""",rf"""
\PCode{{R · aumentare n per gruppo}}{{081_lab_potenza.R}}
\PSmall{{La potenza passa da $ {it(val('potenza','Potenza alla numerosità scelta'))}$ a $ {it(val('potenza','Potenza alla numerosità scelta','variante'))}$.}}
\PInfo{{Il calcolo usa un test t con varianza comune. Per progettare uno studio occorrono un effetto minimo motivato e una dispersione plausibile.}}
""","La numerosità si pianifica rispetto a un’alternativa rilevante e a ipotesi sul disegno, prima di osservare il risultato.")

code(82,"lab_welch",'''
# Rapporto fra SD: 2 -> 1
z82 <- lab_welch(ratio=2)
w82 <- lab_welch(ratio=1)
rbind(sd2=z82$metrics,
      sd1=w82$metrics)
z82$test$conf.int
w82$test$conf.int
''')
entries=[]
for scenario,label,col in [("base",r"$\sigma_B/\sigma_A=2$","GeoB"),("variante",r"$\sigma_B/\sigma_A=1$","GeoA")]:
    r=load(f"lab_welch_ci_{scenario}.csv")[0]
    entries.append((label,float(r["stima"]),float(r["lo"]),float(r["hi"]),col))
S(82,"Laboratorio · varianze separate nel confronto",
  link("welch","Apri il laboratorio: Welch")+
  ci_compare(entries,xmin=-1.1,xmax=1.1)+r"""
\PSmall{Mantenere $n=30$ per gruppo e seme 17. La differenza vera resta $0{,}5$. Ridurre il parametro \texttt{ratio} da 2 a 1.}
\PBody{Come cambiano SE, gradi di libertà e intervallo?}
""",r"""
\PCode{R · confrontare due dispersioni}{082_lab_welch.R}
\PSmall{\texttt{ratio=2} indica una deviazione standard doppia in B e una varianza quattro volte maggiore.}
\PInfo{La dispersione diversa modifica anche i valori simulati di B. Nel confronto fra le due esecuzioni può cambiare la stima, oltre all’incertezza.}
""","Welch combina le due varianze campionarie senza imporle uguali. Non corregge una dipendenza trascurata nel disegno.")

def paired_bars():
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](.7,.55)--(9.1,.55);",
         r"\draw[pAxis](.7,.55)--(.7,4.3);"]
    for k,(scenario,tau) in enumerate([("base",3),("variante",5)]):
        cx=2.7+4.1*k
        for shift,metric,col in [(-.6,"SE appaiato","GeoA"),(.6,"SE indipendente","GeoB")]:
            v=val("appaiati",metric,scenario);y=.55+v*2.7
            out.append(rf"\fill[{col}!75]({cx+shift-.4:.3f},.55) rectangle({cx+shift+.4:.3f},{y:.4f});")
            out.append(rf"\node[pNote] at({cx+shift:.3f},{y+.28:.4f}){{$ {it(v)} $}};")
        out.append(rf"\node[pNote] at({cx:.3f},.1){{$\tau={tau}$}};")
    out +=[r"\node[pNote,text=GeoA] at(2.7,4.25){SE appaiato};",
           r"\node[pNote,text=GeoB] at(6.8,4.25){SE indipendente};",
           r"\node[pNote] at(4.8,-.4){Stesse 30 coppie; seme 17};",
           r"\end{tikzpicture}"]
    return "\n".join(out)
code(83,"lab_appaiati",'''
# Varia la componente individuale.
z83 <- lab_appaiati(tau=3)
w83 <- lab_appaiati(tau=5)
rbind(tau3=z83$metrics,
      tau5=w83$metrics)
all.equal(z83$differenze,
          w83$differenze)
''')
S(83,"Laboratorio · conservare l’abbinamento",
  link("appaiati","Apri il laboratorio: appaiati")+paired_bars()+r"""
\PSmall{Il valore individuale condiviso $u_i$ compare sia prima sia dopo. Sottraendo, $D_i=0{,}6+\varepsilon_{i,\mathrm{dopo}}-\varepsilon_{i,\mathrm{prima}}$: $u_i$ si cancella.}
""",r"""
\PCode{R · aumentare tau da 3 a 5}{083_lab_appaiati.R}
\PSmall{Il laboratorio confronta due SE; non restituisce un p-value. Entrambe le impostazioni mantengono $\tau>0$.}
\PInfo{A $\tau=0$ il generatore non consuma le stesse estrazioni casuali: a seme fisso possono cambiare anche gli errori successivi.}
""","La componente comune può aumentare la dispersione delle misure senza aumentare quella delle differenze appaiate.")

def ecdf_plot():
    data=load("lab_ranghi_base.csv")
    xmin=math.floor(min(float(r["valore"]) for r in data))-.2
    xmax=math.ceil(max(float(r["valore"]) for r in data))+.2
    def xx(v):return .85+(v-xmin)/(xmax-xmin)*8
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](.85,.55)--(9.1,.55);",
         r"\draw[pAxis](.85,.55)--(.85,4.35);"]
    for g,col in [("A","GeoA"),("B","GeoB")]:
        values=sorted(float(r["valore"]) for r in data if r["gruppo"]==g)
        coords=[(xx(xmin),.55)]
        for j,v in enumerate(values):
            coords.extend([(xx(v),.55+3.4*j/len(values)),(xx(v),.55+3.4*(j+1)/len(values))])
        coords.append((xx(xmax),3.95))
        points=" ".join(f"({x:.4f},{y:.4f})" for x,y in coords)
        out.append(rf"\draw[{col},line width=1.1pt] plot coordinates{{{points}}};")
    for v in [0,.5,1]:
        out.append(rf"\node[pNote,anchor=east] at(.65,{.55+3.4*v}){{$ {it(v,1)} $}};")
    for v in range(math.ceil(xmin),math.floor(xmax)+1,2):
        out.append(rf"\node[pNote] at({xx(v):.4f},.15){{$ {v} $}};")
    out +=[r"\node[pNote,text=GeoA] at(3,4.4){A};",
           r"\node[pNote,text=GeoB] at(6.5,4.4){B};",
           r"\node[pNote] at(5,-.4){Risposta; ordinate: frequenza cumulata};",
           r"\end{tikzpicture}"]
    return "\n".join(out)
code(84,"lab_ranghi",'''
# SD di B: da 1 a 2
z84 <- lab_ranghi(ratio=1)
w84 <- lab_ranghi(ratio=2)
rbind(sd1=z84$metrics,
      sd2=w84$metrics)
# Delta=.5; 35 dati per gruppo.
''')
S(84,"Laboratorio · confrontare gli ordinamenti",
  link("ranghi","Apri il laboratorio: ranghi")+ecdf_plot()+r"""
\PSmall{Curve empiriche per l’impostazione iniziale: 35 dati per gruppo, $\Delta=0{,}5$, rapporto fra SD uguale a 1. Poi portare il rapporto a 2.}
""",rf"""
\PCode{{R · osservare tre quantità}}{{084_lab_ranghi.R}}
\PSmall{{La superiorità empirica passa da $ {it(val('ranghi','P empirica B > A'))}$ a $ {it(val('ranghi','P empirica B > A','variante'))}$. Confrontarla con differenza delle mediane e $p$.}}
\PInfo{{La calibrazione usuale del rank-sum assume distribuzioni uguali sotto $H_0$. Uguaglianza delle mediane o della sola superiorità non basta.}}
""","Medie, mediane e ordinamenti definiscono domande diverse. Il metodo deve corrispondere al parametro e alle condizioni dichiarate.")

def proportions_plot():
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](.8,.55)--(9.2,.55);",
         r"\draw[pAxis](.8,.55)--(.8,4.15);"]
    for x,pro,lab,count,col in [(2.3,.3,"A","15/50","GeoA"),
        (4.95,25/60,"B: base","25/60","GeoB"),
        (7.6,.3,"B: variante","18/60","GeoC")]:
        y=.55+pro*6.3
        out +=[rf"\fill[{col}!75]({x-.55},.55) rectangle({x+.55},{y:.4f});",
               rf"\node[pNote] at({x},{y+.3:.4f}){{$ {count} $}};",
               rf"\node[pNote] at({x},.12){{{lab}}};"]
    for v in [0,.25,.5]:
        out.append(rf"\node[pNote,anchor=east] at(.6,{.55+6.3*v}){{$ {it(v,2)} $}};")
    out +=[r"\node[pNote,anchor=west] at(1.1,4.1){Quota dell’esito 1};",
           r"\end{tikzpicture}"]
    return "\n".join(out)
code(85,"lab_categorie",'''
# A: 15 su 50; B: count su 60
z85 <- lab_categorie(count=25)
w85 <- lab_categorie(count=18)
z85$tabella
z85$attesi
rbind(B25=z85$metrics,
      B18=w85$metrics)
''')
S(85,"Laboratorio · conteggi e proporzioni",
  link("categorie","Apri il laboratorio: categorie")+proportions_plot()+r"""
\PSmall{Il gruppo A resta fissato a 15 esiti 1 su 50. Modificare il conteggio in B da 25 a 18 su 60. Confrontare percentuali e conteggi attesi.}
\PBody{Perché 15 e 18 esiti possono corrispondere alla stessa proporzione?}
""",r"""
\PCode{R · leggere tabella e attesi}{085_lab_categorie.R}
\PSmall{Il chi-quadrato usa \texttt{correct=FALSE}; Fisher condiziona ai margini. Il seme non modifica i conteggi assegnati.}
\PInfo{Con 18/60 e 15/50 le proporzioni osservate coincidono. Questo non dimostra uguaglianza delle proporzioni nelle popolazioni.}
""","Confrontare i conteggi richiede i denominatori. I test sulla tabella presuppongono unità indipendenti e un modello coerente con il campionamento.")

def anova_plot():
    data=load("lab_anova_medie_base.csv")
    ymin=-2.5;ymax=4.8
    def yy(v):return .55+3.4*(v-ymin)/(ymax-ymin)
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](.85,.55)--(9.2,.55);",
         r"\draw[pAxis](.85,.55)--(.85,4.2);"]
    for j,r in enumerate(data):
        x=2+j*2.0;mu=float(r["media"]);sd=float(r["sd"]);col=["GeoA","GeoB","GeoC","Classical"][j]
        out +=[rf"\draw[{col},line width=1.8pt]({x},{yy(mu-sd):.4f})--({x},{yy(mu+sd):.4f});",
               rf"\fill[{col}]({x},{yy(mu):.4f}) circle(3pt);",
               rf"\node[pNote] at({x},.12){{{r['gruppo']}}};"]
    for v in [-2,0,2,4]:
        out.append(rf"\node[pNote,anchor=east] at(.6,{yy(v):.4f}){{$ {v} $}};")
    out +=[r"\node[pNote] at(5,4.45){Punti: medie; segmenti: media $\pm$ SD};",
           r"\node[pNote] at(5,-.4){Quattro gruppi; 30 osservazioni ciascuno};",
           r"\end{tikzpicture}"]
    return "\n".join(out)
code(86,"lab_anova",'''
# Quattro gruppi, SD diverse
z86 <- lab_anova(ratio=2)
w86 <- lab_anova(ratio=1)
rbind(sd_diverse=z86$metrics,
      sd_uguali=w86$metrics)
# Ogni riga contiene due metodi.
''')
S(86,"Laboratorio · un confronto fra quattro medie",
  link("anova","Apri il laboratorio: ANOVA")+anova_plot()+r"""
\PSmall{Impostazione iniziale: medie vere $0,\ 0{,}5,\ 1,\ 1{,}5$; SD $1,\ 4/3,\ 5/3,\ 2$. Portare \texttt{ratio} a 1 e confrontare i due metodi.}
""",r"""
\PCode{R · ANOVA classica e Welch}{086_lab_anova.R}
\PSmall{I segmenti nel grafico descrivono la dispersione dei dati, non intervalli di confidenza delle medie.}
\PInfo{La configurazione iniziale ha varianze diverse. L’ANOVA classica richiede varianza comune; Welch ammette varianze diverse con il proprio riferimento.}
""","Il test globale valuta se tutte le medie sono uguali. Un rifiuto non identifica automaticamente le coppie differenti.")

def fwer_plot():
    pts=" ".join(f"({.8+.08*m:.4f},{.55+3.4*(1-.95**m):.4f})" for m in range(1,101))
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](.8,.55)--(9.2,.55);",
         r"\draw[pAxis](.8,.55)--(.8,4.3);",
         rf"\draw[GeoB,line width=1.4pt] plot coordinates{{{pts}}};"]
    for m in [20,100]:
        x=.8+.08*m;y=.55+3.4*(1-.95**m)
        out +=[rf"\draw[Muted,dashed]({x:.4f},.55)--({x:.4f},{y:.4f});",
               rf"\fill[GeoB]({x:.4f},{y:.4f}) circle(3pt);",
               rf"\node[pNote] at({x:.4f},.15){{{m}}};"]
    for v in [0,.5,1]:
        out.append(rf"\node[pNote,anchor=east] at(.6,{.55+3.4*v}){{$ {it(v,1)} $}};")
    out +=[r"\node[pNote,anchor=west] at(1.1,4.3){FWER grezza, tutte le ipotesi nulle};",
           r"\node[pNote] at(5,-.4){Numero di test indipendenti, $\alpha=0{,}05$};",
           r"\end{tikzpicture}"]
    return "\n".join(out)
code(87,"lab_multipli",'''
# Stesso seme, famiglia piu ampia
z87 <- lab_multipli(m=20)
w87 <- lab_multipli(m=100)
rbind(m20=z87$metrics,
      m100=w87$metrics)
# Conteggi di una singola famiglia.
''')
S(87,"Laboratorio · la famiglia dei confronti",
  link("multipli","Apri il laboratorio: confronti multipli")+fwer_plot()+r"""
\PSmall{Il generatore estrae p-value uniformi indipendenti sotto $H_0$. Portare $m$ da 20 a 100 mantenendo $\alpha=0{,}05$ e seme 17.}
""",r"""
\PCode{R · confrontare grezzi e Holm}{087_lab_multipli.R}
\PSmall{Il grafico mostra $1-(1-\alpha)^m$. Il browser riporta anche i rifiuti osservati prima e dopo Holm in una sola famiglia.}
\PInfo{Un singolo conteggio non stima la FWER. Occorrono molte famiglie simulate per confrontare la frequenza empirica con la probabilità teorica.}
""","La famiglia dei test si definisce prima dell’analisi. Il controllo di Holm riguarda il rischio di almeno un falso rifiuto nella famiglia.")

code(88,"lab_relazione",'''
# L'effetto vero resta Delta=.3.
z88 <- lab_relazione(n=30)
w88 <- lab_relazione(n=120)
rbind(n30=z88$metrics,
      n120=w88$metrics)
z88$data[c("x","lo","hi")]
''')
entries=[]
for scenario,label,col in [("base","$n=30$","GeoB"),("variante","$n=120$","GeoA")]:
    r=load(f"lab_relazione_{scenario}.csv")[0]
    entries.append((label,float(r["x"]),float(r["lo"]),float(r["hi"]),col))
S(88,"Laboratorio · scrivere una conclusione",
  link("relazione","Apri il laboratorio: relazione")+
  ci_compare(entries,xmin=-.8,xmax=.8)+r"""
\PSmall{Due gruppi indipendenti con SD 1, differenza vera $0{,}3$, seme 17. Aumentare $n$ per gruppo da 30 a 120 e scrivere due brevi relazioni.}
""",r"""
\PCode{R · effetto, intervallo e p-value}{088_lab_relazione.R}
\PSmall{Riportare direzione, stima, intervallo, metodo, $p$ e condizioni. Cambiando $n$ cambiano anche i campioni generati.}
\PInfo{Entrambi gli intervalli mostrati comprendono zero. La maggiore precisione del secondo non dimostra equivalenza fra le popolazioni.}
""","Una conclusione precisa separa l’effetto stimato, la sua incertezza e ciò che il disegno consente di affermare.")

SLIDES[89]=dict(title="Scegliere il metodo dalla domanda e dal disegno",
 section="V · APPLICAZIONI E VERIFICA",
 wide=r"""
\PLabel{Una tabella da motivare, non una scelta automatica}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[Navy](0,5.4) rectangle(17.9,6.15);
\node[pLabel,text=white,text width=5.0cm] at(2.7,5.77){Domanda};
\node[pLabel,text=white,text width=5.0cm] at(8.5,5.77){Disegno e condizioni};
\node[pLabel,text=white,text width=5.6cm] at(14.65,5.77){Metodo del modulo};
\foreach \y/\a/\b/\c in {
4.95/{Due medie}/{Gruppi indipendenti}/{Welch; SE con varianze separate},
4.05/{Cambiamento medio}/{Coppie complete indipendenti}/{Test t sulle differenze},
3.15/{Ordinamento fra gruppi}/{Nulla di distribuzioni uguali}/{Rank-sum; interpretazione dichiarata},
2.25/{Associazione fra categorie}/{Conteggi di unità indipendenti}/{Chi-quadrato o Fisher},
1.35/{Uguaglianza di più medie}/{Gruppi indipendenti; valutare varianze}/{ANOVA classica o Welch},
.45/{Una famiglia di ipotesi}/{Test marginali validi}/{Correzione di Holm}}{
\draw[Rule](0,\y-.45)--(17.9,\y-.45);
\node[pLabel,align=left,text width=5cm] at(2.7,\y){\a};
\node[pLabel,align=left,text width=5cm] at(8.5,\y){\b};
\node[pLabel,align=left,text width=5.6cm] at(14.65,\y){\c};
}
\end{tikzpicture}
\PSmall{Dati raggruppati o dipendenti richiedono un trattamento del disegno. La tabella non autorizza ad analizzare ogni riga come indipendente.}
""",recall="La scelta si motiva con parametro, disegno e condizioni. Se questi cambiano, può cambiare anche il significato dell’inferenza.")

code(90,"rivedere_conclusioni",'''
z90 <- lab_relazione(n=30)
# Prima leggere l'effetto e l'IC.
z90$data[c("x","lo","hi")]
# Poi il p-value del riferimento.
z90$metrics
# Scrivere il limite dell'inferenza.
''')
S(90,"Rivedere conclusioni troppo forti",r"""
\PLabel{Tre frasi da correggere}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \y/\tit/\txt in {
4.25/{«p grande: nessuna differenza»}/{Valutare ampiezza e posizione dell’intervallo.},
2.55/{«p piccolo: effetto importante»}/{Confrontare l’effetto con una soglia scientifica.},
.85/{«differenza: causa dimostrata»}/{Esaminare assegnazione, selezione e confondenti.}}{
\node[pFlow,text width=8.4cm,minimum height=1.25cm] at(4.65,\y)
{\textbf{\tit}\\\txt};
}
\end{tikzpicture}
\PSmall{Una relazione deve rendere riconoscibile il passaggio dai risultati alle affermazioni. L’effetto causale richiede un disegno che lo giustifichi.}
""",r"""
\PCode{R · riprendere un risultato completo}{090_rivedere_conclusioni.R}
\PSmall{Nel laboratorio iniziale l’intervallo comprende effetti positivi e negativi. Esplicitare questa incertezza nella frase conclusiva.}
\PInfo{Esercizio: riscrivere le tre frasi senza usare «accettare $H_0$», «nessun effetto» o «causato da» quando il risultato non le sostiene.}
""","La forza della conclusione deve corrispondere all’informazione del campione e alle condizioni del metodo.")

code(91,"differenze_a_mano",'''
# Cinque coppie costruite, unita u.c.
a91 <- c(10,12,9,11,13)
b91 <- c(10.4,12.1,9.7,10.8,13.5)
d91 <- b91-a91
c(media=mean(d91), SE=sd(d91)/sqrt(5))
all.equal(mean(d91),
          mean(b91)-mean(a91))
''')
S(91,"Esercizio · calcolare le differenze a mano",
  r"\PLabel{Cinque coppie costruite, unità convenzionali}"+
  table_diagram(["Coppia","Prima","Dopo","Differenza"],[
    ["1","10","10,4","$+0{,}4$"],["2","12","12,1","$+0{,}1$"],
    ["3","9","9,7","$+0{,}7$"],["4","11","10,8","$-0{,}2$"],
    ["5","13","13,5","$+0{,}5$"]],widths=(2.1,2.1,2.1,2.5),height=.64)+r"""
\[
\bar D=\frac{1{,}5}{5}=0{,}3=\bar y_{\rm dopo}-\bar y_{\rm prima}.
\]
\PSmall{Calcolare $s_D^2$ e $SE(\bar D)$, poi verificare con R. Le coppie devono rimanere le stesse in entrambe le medie.}
""",r"""
\PCode{R · verificare l’identità delle medie}{091_differenze_a_mano.R}
\PSmall{\texttt{all.equal()} confronta risultati numerici tenendo conto degli arrotondamenti in virgola mobile.}
\PInfo{L’identità delle medie non rende uguali i SE appaiato e indipendente. Il primo usa la dispersione delle differenze entro coppia.}
""","La media delle differenze coincide con la differenza delle medie sulle stesse coppie complete; l’incertezza conserva la covarianza entro coppia.")

code(92,"relazione_fossili",'''
f92 <- read.csv(
 "Dati/fossili_simulati.csv")
g92 <- split(f92$diametro_tot_um,
             f92$morfotipo)
t92 <- t.test(g92$Spiky,g92$Rounded)
c(SE=t92$stderr,p=t92$p.value)
t92$conf.int
''')
F=load("fossili_riepilogo.csv")[0]
F={k:float(v) for k,v in F.items()}
S(92,"Una relazione completa sul confronto dei fossili",rf"""
\PLabel{{Domanda, risultato e condizioni}}
\PBody{{Nel dataset sintetico confrontiamo il diametro totale medio di 80 fossili Spiky e 80 Rounded, usando il contrasto Spiky meno Rounded.}}
\vspace{{2mm}}
\PBody{{La differenza stimata è $ {it(F['differenza'])}\ \mu$m; l’intervallo di Welch al 95\% è $[{it(F['inferiore'])};{it(F['superiore'])}]\ \mu$m.}}
\vspace{{2mm}}
\PBody{{Il test bilaterale di differenza nulla restituisce $t={it(F['differenza']/F['se'],2)}$, $\nu={it(F['df'],1)}$ e $p={it(F['p'],6)}$.}}
\vspace{{2mm}}
\PInfo{{Nel modello adottato i risultati forniscono evidenza di una differenza fra medie. L’analisi assume unità indipendenti e condizioni adeguate per l’approssimazione di Welch.}}
""",r"""
\PCode{R · conservare le quantità riportate}{092_relazione_fossili.R}
\PSmall{L’effetto è espresso nell’unità originale; la rilevanza geologica richiede un criterio esterno al test.}
\PInfo{Questi dati sono simulati per la didattica. Il confronto non costituisce evidenza su una popolazione reale di fossili né dimostra un meccanismo causale.}
""","Una relazione conserva domanda, segno, unità, numerosità, stima, intervallo, metodo e limiti dell’interpretazione.")

code(93,"verifica_finale",'''
# Due domande definite in anticipo
f93 <- read.csv(
 "Dati/fossili_simulati.csv")
variabili93 <- c("diametro_tot_um",
                 "diametro_int_um")
summary(f93[variabili93])
# Completare Esercizi/
# 12_verifica_finale.R
''')
S(93,"Verifica finale · due contrasti pianificati",r"""
\PLabel{Applicare il metodo a una famiglia dichiarata}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.8cm] (a) at(2.2,3.7){Diametro totale\\Spiky meno Rounded};
\node[pFlow,text width=3.8cm] (b) at(7.2,3.7){Diametro interno\\Spiky meno Rounded};
\node[pFlow,text width=8.5cm] (fam) at(4.7,1.3){Famiglia di due ipotesi sulle medie\\due stime, due IC marginali, due $p$, correzione di Holm};
\draw[pEdge](a.south)--(2.2,2.3)--(2.2,1.9);
\draw[pEdge](b.south)--(7.2,2.3)--(7.2,1.9);
\end{tikzpicture}
\PSmall{Motivare il disegno, mostrare i dati, calcolare i contrasti e scrivere una relazione di 120–180 parole. Indicare che i due esiti sono misurati sugli stessi fossili.}
""",r"""
\PCode{R · predisporre l’analisi}{093_verifica_finale.R}
\PSmall{Il file dell’esercizio contiene la traccia; la cartella \texttt{Docente/} conserva risultati e criteri di valutazione.}
\PInfo{I due intervalli al 95\% sono marginali: non diventano simultanei correggendo soltanto i p-value con Holm.}
""","La correzione della famiglia riguarda le decisioni sui test. Copertura degli intervalli, dipendenze e interpretazione vanno dichiarate separatamente.")

SLIDES[94]=dict(title="Fonti e materiali per proseguire",
 section="V · APPLICAZIONI E VERIFICA",
 left=r"""
\PLabel{Corso e documentazione dei metodi}
\PBody{\href{https://marzione00.github.io/Lab_Geo/\#modulo-M06}{GeoStat Lab · Gemina M06}. Modulo originale, 20 notebook e 11 esperimenti; dati sintetici e generatori conservati nel progetto.}
\vspace{3mm}
\PSmall{\textbf{R Core Team, pacchetto stats.}\\
\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html}{t.test},
\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/TDist.html}{TDist},
\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/power.t.test.html}{power.t.test},
\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html}{wilcox.test},
\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/chisq.test.html}{chisq.test},
\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/fisher.test.html}{fisher.test},
\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/oneway.test.html}{oneway.test},
\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html}{p.adjust}.}
\vspace{3mm}
\PSmall{\textbf{Phipson e Smyth (2010).}\\
\href{https://gksmyth.github.io/pubs/PermPValuesPreprint.pdf}{Permutation p-values should never be zero}.\\
\textbf{Wasserstein e Lazar (2016).}\\
\href{https://doi.org/10.1080/00031305.2016.1154108}{The ASA’s Statement on p-Values}.}
\vspace{2mm}
\PSmall{Fonti consultate il 19 novembre 2026. Provenienza e riferimenti completi nel progetto.}
""",
 right=r"""
\PLabel{File del modulo}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \y/\a/\b in {
4.4/{Presentazione}/{PDF e sorgente XeLaTeX},
3.1/{Lezione R}/{Frammenti commentati e dati CSV},
1.8/{Quaderno}/{Undici schede di laboratorio},
.5/{Materiali docente}/{Soluzioni, risultati attesi e mappe}}{
\node[pFlow,text width=6.7cm,minimum height=1.0cm] at(3.6,\y){\textbf{\a}\\\b};
}
\end{tikzpicture}
\PInfo{Per compilare il sorgente scegliere \textbf{XeLaTeX} ed eseguire due passaggi. Per R aprire \texttt{Gemina\_M06.Rproj}.}
""",
 recall="Per riprodurre un’analisi servono dati, codice, impostazioni e condizioni del metodo, insieme alla domanda che si vuole studiare.")
