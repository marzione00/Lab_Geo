"""Diagrammi rivisti dopo la lettura delle singole pagine; palette e font del corso."""
from tikz_base import scrivi,n,a,rect,linea

def flow(mod,id,labels):
    b=''
    for k,(head,sub) in enumerate(labels):
        y=.25+k*1.85;col='Classical' if k!=1 else 'Quantum'
        b+=rect(.25,y,7.15,y+1.35,col)
        b+=n(3.7,y+.36,r'\textbf{'+head+'}',w=6.5,size=12,color=col)
        b+=n(3.7,y+.95,sub,w=6.5,size=11.3)
        if k<len(labels)-1:b+=a(3.7,y+1.4,3.7,y+1.72,col)
    return scrivi(mod,id,b)

def genera(mod):
    if mod=='M08':
        genera_m08()
        return
    if mod=='M07':
        genera_m07()
        return
    if mod=='M06':
        genera_m06()
        return
    if mod=='M05':
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]/'tikz/M05'
        for src,dst,old,new in [('D02','R6_D02','provino $i$ nella stazione $g$','misura del provino $i$, sito $g$'),('D24','R6_D24','Quote fissate per gruppo','Quote fissate')]:
            (root/(dst+'.tex')).write_text((root/(src+'.tex')).read_text().replace(old,new))
        return
    if mod=='M03':
        genera_m03()
        return
    if mod=='M02':
        genera_m02()
        return
    if mod=='M01':
        b=(__import__('pathlib').Path(__file__).resolve().parents[1]/'tikz/M01/D09.tex').read_text()
        b=b.split('\n',1)[1].rsplit(r'\end{tikzpicture}',1)[0]
        b=b.replace(r'\draw[Muted,line width=.8pt] (2.2,4.6)--(7,4.6);','')
        scrivi(mod,'R6_D09',b)
    if mod!='T00':return
    flows={
      'R6_D01':[('Algoritmo','Operazioni e dipendenze'),('Programma','Istruzioni nel linguaggio scelto'),('Runtime','Esecuzione delle istruzioni')],
      'R6_D03':[('File CSV','Dati conservati sul disco'),('Tabella in memoria','Oggetto disponibile nella sessione'),('Scrittura','Risultato salvato in un nuovo file')],
      'R6_D06':[('File di testo','Caratteri e separatori'),('Lettura','Codifica, separatori e tipi'),('Tabella','Valori organizzati in righe e colonne')],
      'R6_D08':[('Sintassi','Le istruzioni sono interpretabili?'),('Esecuzione','Le operazioni sono definite?'),('Metodo','Il risultato risponde alla domanda?')],
      'R6_D09':[('Ambiente','R e pacchetti disponibili'),('Progetto','Dati e codice nella cartella completa'),('Verifica','Laboratorio e controllo dell’esito')],
      'R6_D12':[('Sessione temporanea','Calcolo e produzione dei risultati'),('Salvataggio','Copia su disco persistente'),('Verifica','Riapertura dei file salvati')]
    }
    for id,labels in flows.items():flow(mod,id,labels)
    b=rect(.25,.3,7.15,2.8)+n(3.7,.75,r'\textbf{Lista Python}',w=6.5,color='Classical')
    b+=n(1.85,1.55,'[1, 2]',w=2.5,size=13)+a(3.1,1.55,3.8,1.55)+n(5.45,1.55,'[1, 2, 1, 2]',w=3,size=13)
    b+=n(3.7,2.35,'× 2 ripete gli elementi',w=6.5,size=11.5)
    b+=rect(.25,3.25,7.15,5.75,'Quantum')+n(3.7,3.7,r'\textbf{Array NumPy}',w=6.5,color='Quantum')
    b+=n(1.85,4.5,'[1, 2]',w=2.5,size=13)+a(3.1,4.5,3.8,4.5,'Quantum')+n(5.45,4.5,'[2, 4]',w=3,size=13)
    b+=n(3.7,5.3,'× 2 raddoppia ogni valore',w=6.5,size=11.5)
    scrivi(mod,'R6_D04',b)
    b=n(3.7,.45,r'\textbf{Condizione: }$V\geq45\ \mathrm{cm}^3$',w=7,size=12.5)
    rows=[('C01 · A1 · 107,2 g · 40 cm³','escluso','Muted'),('C02 · A1 · 121,95 g · 45 cm³','incluso','Classical'),('C03 · A1 · 132,5 g · 50 cm³','incluso','Classical')]
    for k,(label,status,col) in enumerate(rows):
        y=1.1+k*1.45;b+=rect(.25,y,7.15,y+1.18,col,4 if k==0 else 10)
        b+=n(3.7,y+.32,label,w=6.7,size=11,color=col)+n(3.7,y+.84,status,w=6.7,size=11,color=col)
    b+=n(3.7,5.85,r'$A=\{2,3\}$: due righe complete',w=7,size=12)
    scrivi(mod,'R6_D07',b)

def genera_m02():
    b=n(3.7,.35,r'\textbf{Righe ordinate per data}',w=7,size=12,color='Classical')
    for x,t,w in [(.8,'ID',1),(2.9,'Alterazione',2.4),(5.8,'Data',2.5)]:b+=n(x,1.1,t,w=w,size=11.5)
    b+=linea(.25,1.48,7.15,1.48)
    for k,row in enumerate([('C02','bassa','2026-04-02'),('C01','alta','2026-04-08'),('C03','media','2026-04-12')]):
        y=1.95+k*.8
        if k==1:b+=rect(.25,y-.32,7.15,y+.32,'Quantum',5)
        for x,t,w in zip([.8,2.9,5.8],row,[1,2.4,2.5]):b+=n(x,y,t,w=w,size=11.5)
    b+=n(3.7,4.6,'Ordine delle categorie',w=7,size=12,color='Quantum')+n(3.7,5.35,r'bassa $<$ media $<$ alta',w=7,size=12)
    scrivi('M02','R6_D02',b)
    b=n(1.2,.35,r'\textbf{Testo}',w=1.6,size=12,color='Classical')+n(4.9,.35,r'\textbf{Esito}',w=4.4,size=12,color='Quantum')
    for k,(txt,out) in enumerate([('5,4','5.4 · numero'),('ND','NA · assente'),('abc','NA · errore di formato'),('$<0{,}05$','Limite 0,05 · censura')]):
        y=.9+k*1.25;col='Classical' if k==0 else 'Quantum'
        b+=rect(.25,y,7.15,y+1.05,col,5)+n(1.2,y+.52,txt,w=1.6,size=12)+a(2.2,y+.52,2.85,y+.52,col)+n(5,y+.52,out,w=4,size=11.5)
    scrivi('M02','R6_D03',b)

def genera_m03():
    z=lambda v:.6+(v+1)*.65
    b=n(3.7,.3,'Soglie teoriche e valori osservati',w=7,size=12)
    b+=linea(.3,3,7.05,3)
    for v,lab in [(-1,'$L=-1$'),(7,'$U=7$')]:
        b+=rf'\draw[Measure,dashed,line width=.8pt] ({z(v)},1.6)--({z(v)},4.1);'
        b+=n(z(v),1.1,lab,size=11.5,color='Measure')
    b+=rect(z(2),2.3,z(4),3.7)+linea(z(3),2.3,z(3),3.7,'Classical')
    b+=linea(z(.5),3,z(2),3,'Classical')+linea(z(4),3,z(6),3,'Classical')
    for v in [.5,6]:b+=linea(z(v),2.65,z(v),3.35,'Classical')+n(z(v),4.3,str(v).replace('.',','),size=11.5)
    b+=n(z(3),4.95,r'$Q_1=2,\quad Q_3=4$',w=4,size=11.5)
    b+=n(z(3),1.85,'Mediana 3',size=11.5)+n(z(8),3,r'$\circ$',size=17,color='Quantum')+n(z(8),4.3,'8',size=11.5,color='Quantum')
    b+=n(3.7,5.85,'Baffi: 0,5 e 6; soglie: −1 e 7',w=7,size=11.5)
    scrivi('M03','R6_D06',b)
    b=rect(.3,.3,7.1,2.1)+n(3.7,.75,r'\textbf{Parametri dell’addestramento}',w=6.5,size=11.5,color='Classical')
    b+=n(3.7,1.5,r'$\bar x_{\rm train}=5\ \mu\mathrm m,\quad s_{\rm train}=2\ \mu\mathrm m$',w=6.5,size=12)
    b+=a(3.7,2.25,3.7,3,'Quantum')+rect(.3,3.15,7.1,5.7,'Quantum')
    b+=n(3.7,3.65,r'Nuova misura: $x=6\ \mu\mathrm m$',w=6.5,size=12)
    b+=n(3.7,4.5,r'$z=(6-5)/2=0{,}5$',w=6.5,size=13,color='Quantum')
    b+=n(3.7,5.25,'Media e scala restano fissate',w=6.5,size=11.5)
    scrivi('M03','R6_D08',b)

def genera_m06():
    # Tre disegni distinti; i contorni segnalano le unità legate.
    b=''
    for k,(lab,col) in enumerate([('Indipendenti','Classical'),('Appaiati','Quantum'),('Raggruppati','Measure')]):
        y=.25+2*k;b+=n(1.4,y+.6,lab,w=2.7,color=col,size=11.5)
        if k==0:
            for x,v in [(3.2,'A'),(4.4,'B'),(5.6,'C'),(6.8,'D')]:
                b+=rf'\draw[draw={col},fill={col}!8] ({x},{y+.6}) circle (.28);'+n(x,y+.6,v,size=11)
        elif k==1:
            for j in range(3):
                x=3.2+j*1.4;b+=rect(x-.45,y-.05,x+.45,y+1.25,col)
                b+=n(x,y+.25,f'{j+1}a',size=11)+n(x,y+.95,f'{j+1}b',size=11)
        else:
            for j in range(2):
                x=4+j*2.2;b+=rect(x-.8,y-.05,x+.8,y+1.3,col)+n(x,y+.2,f'Sito {j+1}',size=11,color=col)
                for dx in [-.35,0,.35]:b+=rf'\fill[{col}] ({x+dx},{y+.85}) circle (.07);'
    scrivi('M06','R6_D01',b)
    b=n(1,.2,'Valore',w=2,size=11.5)+n(3.25,.2,'Originale',w=2.4,size=11.5,color='Classical')+n(5.9,.2,'Permutata',w=2.8,size=11.5,color='Quantum')
    for j,(v,old,new) in enumerate([(4,'R','S'),(6,'R','R'),(5,'S','R'),(8,'S','S')]):
        y=1+j*.95;b+=n(1,y,str(v),size=13)+n(3.25,y,old,color='Classical',size=13)+a(4,y,4.8,y)+n(5.9,y,new,color='Quantum',size=13)
    b+=n(3.25,5.0,r'$T_{\rm obs}=1{,}5$',w=3,size=12,color='Classical')+n(5.9,5.0,r'$T^\pi=0{,}5$',w=2.6,size=12,color='Quantum')
    b+=n(3.7,5.8,'Valori e numerosità restano fissi',w=7,size=11.5)
    scrivi('M06','R6_D02',b)
    import math
    xx=lambda v:3.7+.85*v
    yy=lambda v:4.2-2.6*math.exp(-v*v/2)
    b=n(3.7,.25,r'$T\sim N(0,1)$ sotto $H_0$',w=7,size=12)
    for lo,hi in [(-3.5,-2),(2,3.5)]:
        pts=[(lo+(hi-lo)*j/60) for j in range(61)]
        coords=' -- '.join(f'({xx(v):.4f},{yy(v):.4f})' for v in pts)
        b+=rf'\path[fill=Quantum!28] ({xx(lo)},4.2) -- '+coords+rf' -- ({xx(hi)},4.2) -- cycle;'
    pts=[-3.5+7*j/200 for j in range(201)]
    coords=' '.join(f'({xx(v):.4f},{yy(v):.4f})' for v in pts)
    b+=r'\draw[Classical,line width=1pt] plot[smooth] coordinates {'+coords+'};'
    b+=linea(.45,4.2,7,4.2,'Muted')
    for v in [-2,0,2]:
        b+=linea(xx(v),4.1,xx(v),4.3,'Muted')+n(xx(v),4.8,str(v),size=12)
    b+=n(3.7,5.65,r'$p=P(|T|\geq2)\simeq0{,}0455$',w=7,size=12,color='Quantum')
    scrivi('M06','R6_D03',b)
    # ANOVA: (3,5) e (6,8), medie 4 e 7, media globale 5,5.
    y=lambda v:4.6-(v-3)*.6
    b=n(3.7,.2,r'Scarti entro e fra gruppi',w=7,size=12)
    b+=rf'\draw[Muted,dashed] (.45,{y(5.5)})--(7.1,{y(5.5)});'
    b+=n(6.7,y(5.5)-.45,r'$\bar x=5{,}5$',w=1.7,size=11)
    for x,mu,values,lab in [(1.7,4,[3,5],'A'),(4.6,7,[6,8],'B')]:
        b+=n(x,5.15,lab,color='Classical',size=12)
        for j,v in enumerate(values):
            xp=x-.3+j*.6
            b+=linea(xp,y(v),xp,y(mu),'Classical')
            b+=rf'\fill[Classical] ({xp},{y(v)}) circle (.08);'
            b+=n(xp+(-.35 if j==0 else .35),y(v),str(v),size=11)
        b+=linea(x-.65,y(mu),x+.65,y(mu),'Classical')+linea(x+.8,y(mu),x+.8,y(5.5),'Quantum')
        b+=n(x,y(mu)+.37,rf'$\bar x_{lab}={mu}$',w=1.7,size=11,color='Classical')
    b+=n(3.7,5.85,r'Entro: $SS_W=4$; fra: $SS_B=9$',w=7,size=12)
    scrivi('M06','R6_D09',b)

def genera_m07():
    b=n(3.7,.25,r'Un passo in x: odds $\times2$',w=7,size=12.5)
    for k,(p0,p1,odds,col) in enumerate([('0,20','1/3',r'0{,}25\ \longrightarrow\ 0{,}50','Classical'),('0,80','8/9',r'4\ \longrightarrow\ 8','Quantum')]):
        y=1+k*2.55;b+=rect(.25,y,7.15,y+2.15,col)
        b+=n(1.8,y+.55,f'p = {p0}',w=2.8,size=13,color=col)+a(3.2,y+.55,4.2,y+.55,col)
        b+=n(5.6,y+.55,r"$p'="+p1+'$',w=2.7,size=13,color=col)
        b+=n(3.7,y+1.45,r'Odds: $'+odds+'$',w=6.7,size=12)
    scrivi('M07','R6_D08',b)

def genera_m08():
    # Coordinate fisiche euclidee: compensazione della scala verticale TikZ.
    def xy(x,y):return 3.2+x,3.5-y/.87
    def point(x,y,col):
        xx,yy=xy(x,y)
        return rf'\fill[{col}] ({xx:.4f},{yy:.4f}) circle (2pt);'
    b=''
    for vx,vy,lo,hi,col in [(.8,.6,-2.8,3.6,'Classical'),(-.6,.8,-1.7,2.6,'Quantum')]:
        b+=a(*xy(lo*vx,lo*vy),*xy(hi*vx,hi*vy),col)
    px,py=xy(1.76,1.32);xx,yy=xy(2,1)
    b+=rf'\draw[Ink,dashed] ({xx},{yy})--({px},{py});'
    b+=point(2,1,'Ink')+point(1.76,1.32,'Classical')
    b+=n(6.45,1.1,r'$\mathbf v_1$',size=13,color='Classical')
    b+=n(1.2,.65,r'$\mathbf v_2$',size=13,color='Quantum')
    b+=n(5.9,2.6,r'$\mathbf z=(2,1)$',w=2.7,size=11.5)
    b+=n(3.7,5.25,r'$\mathbf v_1=(0{,}8;\,0{,}6)$',w=7,size=12)
    b+=n(3.7,5.95,r'Score: $\mathbf z^\top\mathbf v_1=2{,}2$',w=7,size=12,color='Classical')
    scrivi('M08','R6_D04',b)
