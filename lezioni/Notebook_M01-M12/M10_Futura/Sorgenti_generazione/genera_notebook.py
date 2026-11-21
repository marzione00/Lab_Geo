from pathlib import Path
import json, re, hashlib, csv, textwrap, shutil

HERE = Path(__file__).resolve().parent
BASE = HERE.parent if HERE.name == 'Sorgenti_generazione' else HERE.parent / 'M10/03_Notebook_svolti/M10_Futura'
N=[]
def nb(title,question,objectives,data,steps,variant,error,answer):
    N.append(dict(title=title,question=question,objectives=objectives,data=data,steps=steps,variant=variant,error=error,answer=answer))
def step(title,text,code,reading): return dict(title=title,text=text,code=textwrap.dedent(code).strip(),reading=reading)

CO2='CO₂ storica: 204 mesi da gennaio 1985 a dicembre 2001, concentrazione in ppm. Le medie derivano dalle osservazioni settimanali attribuite al mese della data, secondo la convenzione del corso. Sono dati storici, distinti da una serie mensile ufficiale e da una misura attuale. Il protocollo usa 168 mesi per l’adattamento (1985–1998) e 36 per il test (1999–2001).'
FOS='160 fossili sintetici del corso. Diametri e spessore sono espressi in micrometri. Il diametro interno deriva dal totale meno due volte lo spessore, entro l’arrotondamento del CSV. Il test contiene ogni quinta riga: 32 individui, separati dai 128 usati per stimare. È un protocollo didattico su dati già noti, non una validazione prospettica.'
VAR='Processi sintetici di 300 passi, senza unità fisica. Le colonne x_VAR e y_VAR costituiscono un sistema bivariato. Usiamo i passi 1–250 per stimare e, quando richiesto, 251–260 per una previsione a origine fissa. La prima riga è una condizione iniziale finita: l’esempio non equivale a una nuova serie osservativa.'
LOAD='c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))\ntrain <- c2$train; test <- c2$test; h <- c2$h'
FIT='fit <- stima_sarima(train)'

nb('Fissare l’origine della previsione','Quali osservazioni erano disponibili nel dicembre 1998?',
 ['Controllare il calendario mensile.','Separare adattamento e test prima delle scelte.','Associare origine, bersaglio e orizzonte.'],CO2,[
 step('Il calendario identifica le osservazioni','Una riga corrisponde a un mese. Il controllo usa le date, perché una sequenza di numeri senza calendario non determina l’orizzonte.', '''
 d <- carica_dati("co2_1985_2001.csv")
 d$data <- as.Date(d$data)
 stopifnot(!anyDuplicated(d$data), !anyNA(d$co2_ppm))
 stopifnot(identical(d$data,seq(as.Date("1985-01-01"),as.Date("2001-12-01"),by="month")))
 data.frame(prima=min(d$data),ultima=max(d$data),mesi=nrow(d),
            minimo_settimane=min(d$n_settimane))
 ''','Le 204 righe formano una griglia mensile completa. La copertura settimanale rimane una colonna del dato, anche quando il valore mensile è disponibile.'),
 step('La divisione conserva l’ordine','L’origine fissa è l’ultimo mese del train. Tutti i valori successivi servono soltanto alla verifica del protocollo già definito.',LOAD+'''
 data.frame(insieme=c("Train","Test"),n=c(length(train),length(test)),
   inizio=c("1985-01","1999-01"),fine=c("1998-12","2001-12"))
 stopifnot(length(train)==168L,h==36L,max(time(train))<min(time(test)))
 ''','Nessuna osservazione 1999–2001 entra nel train. Il periodo di test è noto come calendario, mentre i suoi valori restano fuori dalla stima.'),
 step('L’orizzonte misura la distanza dall’origine','La separazione appare sul grafico. L’esposizione del test qui rende visibile il disegno didattico: le scelte di modello devono essere fissate prima del suo uso per confrontare gli errori.','''
 stile_grafico()
 plot(c2$dati$data,c2$dati$co2_ppm,type="n",xlab="Data",ylab="CO2 (ppm)",
      main="Train e test: origine dicembre 1998")
 lines(c2$dati$data[1:168],c2$dati$co2_ppm[1:168],col=palette_geo[1],lwd=2)
 lines(c2$date_test,as.numeric(test),col=palette_geo[2],lwd=2)
 abline(v=as.numeric(as.Date("1999-01-01")),lty=2)
 legend("topleft",c("Train: 168 mesi","Test: 36 mesi"),col=palette_geo[1:2],lty=1,bty="n")
 data.frame(origine="1998-12",bersaglio=as.character(c2$date_test[c(1,12,36)]),h=c(1,12,36))
 ''','I primi 12 mesi e il terzo anno del test rispondono a orizzonti diversi. Conservarli evita di chiamare «previsione a un mese» una sequenza prodotta una sola volta per 36 mesi.')],
 step('Un’origine precedente','Spostare l’origine a dicembre 1997 e misurare quante osservazioni restano nei due segmenti.','''
 tr97 <- window(c2$y,end=c(1997,12)); te97 <- window(c2$y,start=c(1998,1))
 data.frame(origine="1997-12",n_train=length(tr97),n_test=length(te97))
 stopifnot(length(tr97)+length(te97)==204L)
 ''','La variante cambia il problema: aumenta il periodo da prevedere e riduce quello disponibile per l’adattamento. Non confrontare i suoi errori come se il protocollo fosse identico.'),
 'Rimescolare le righe prima dello split, oppure scegliere la data di separazione dopo aver confrontato gli errori sul futuro.',
 'Al dicembre 1998 sono disponibili i 168 mesi del train. Una previsione verificabile conserva la data dell’origine, le date bersaglio e il numero di passi. I risultati su questo archivio storico hanno valore didattico.')

nb('Modelli di riferimento disponibili all’origine','Quale previsione semplice deve superare il modello?',
 ['Calcolare tre riferimenti con il solo train.','Distinguere livello, stagione e deriva.','Verificare la ripetizione stagionale oltre un anno.'],CO2,[
 step('Ultimo valore e stagione',r'Il riferimento ingenuo conserva l’ultimo valore. Il riferimento stagionale ripete l’ultimo anno osservato. Le formule per i primi dodici passi sono $\hat y_{T+h}=y_T$ e $\hat y_{T+h}=y_{T+h-12}$.',LOAD+'''
 ultimo <- rep(as.numeric(tail(train,1)),h)
 stagionale <- rep(as.numeric(tail(train,12)),length.out=h)
 head(data.frame(h=1:h,ultimo=ultimo,stagionale=stagionale),6)
 stopifnot(identical(stagionale[1:12],stagionale[13:24]))
 ''','Dopo dodici passi il riferimento stagionale ripete ancora l’ultimo anno del train. Non consulta il primo anno del test per prevedere il secondo.'),
 step('La deriva usa il cambiamento storico',r'La pendenza deriva dagli estremi del train: $\hat d=(y_T-y_1)/(T-1)$. Questo riferimento è trasparente, ma sensibile agli estremi e a cambiamenti del processo.','''
 deriva <- (as.numeric(tail(train,1))-as.numeric(head(train,1)))/(length(train)-1)
 pred_deriva <- as.numeric(tail(train,1))+seq_len(h)*deriva
 data.frame(ppm_per_mese=deriva,ppm_per_anno=12*deriva)
 tail(data.frame(h=1:h,previsto=pred_deriva),3)
 ''','La deriva esprime ppm per mese. Moltiplicarla per dodici cambia l’unità della pendenza, senza rendere lineare il processo reale.'),
 step('I riferimenti fanno ipotesi differenti','Il confronto grafico riguarda soltanto le traiettorie prodotte all’origine, prima di usarle per calcolare l’errore.','''
 stile_grafico()
 matplot(1:h,cbind(ultimo,stagionale,pred_deriva),type="l",lty=c(2,1,1),
   col=palette_geo[1:3],lwd=2,xlab="Mesi dall'origine",ylab="CO2 prevista (ppm)",
   main="Riferimenti disponibili nel dicembre 1998")
 legend("topleft",c("Ultimo valore","Stagionale","Deriva"),col=palette_geo[1:3],lty=c(2,1,1),bty="n")
 ''','Le curve codificano persistenza, ripetizione stagionale e crescita lineare. Un modello più complesso va giudicato rispetto a un riferimento pertinente alla domanda.')],
 step('Un quarto riferimento','Aggiungere la media del train e confrontarla con l’ultimo valore.','''
 media <- rep(mean(train),h)
 data.frame(metodo=c("Media","Ultimo"),previsione=c(media[1],ultimo[1]))
 stopifnot(all(media==mean(train)))
 ''','La media usa l’intero periodo passato e può essere poco adatta a una serie in crescita. La scelta del riferimento richiede una motivazione, non soltanto facilità di calcolo.'),
 'Usare i valori osservati nel test per aggiornare una baseline e confrontarla con un modello rimasto a origine fissa.',
 'Il riferimento conserva soltanto informazioni disponibili all’origine. Ultimo valore, stagione e deriva offrono confronti complementari da valutare sulle stesse date e sugli stessi orizzonti.')

nb('Stimare il modello sui livelli, non sulle differenze già calcolate','Come si applica correttamente una specifica SARIMA?',
 ['Dichiarare ordini e periodo stagionale.','Stimare sui livelli lasciando le differenze alla funzione.','Controllare convergenza e struttura dei coefficienti.'],CO2,[
 step('La specifica entra nella funzione','Nel modello SARIMA$(0,1,1)(0,1,1)_{12}$, le differenze ordinaria e stagionale sono interne alla stima. In R i coefficienti MA usano la convenzione con il segno più.',LOAD+'''
 fit <- stats::arima(train,order=c(0,1,1),
   seasonal=list(order=c(0,1,1),period=12),
   include.mean=FALSE,method="ML")
 fit
 stopifnot(is.null(fit$code) || fit$code==0L)
 ''','La stima riceve i 168 livelli. La chiamata dichiara due differenze e due termini MA, senza drift. Il numero di coefficienti non misura da solo l’adeguatezza del modello.'),
 step('Coefficienti e precisione numerica',r'Il modello soddisfa $(1-B)(1-B^{12})y_t=(1+\theta B)(1+\Theta B^{12})\varepsilon_t$. Gli errori standard sono quelli dell’approssimazione della stima.','''
 data.frame(termine=names(coef(fit)),stima=as.numeric(coef(fit)),
   errore_standard=sqrt(diag(fit$var.coef)))
 data.frame(varianza_innovazioni=fit$sigma2,logLik=as.numeric(logLik(fit)),
            AIC=AIC(fit),codice_convergenza=fit$code)
 stopifnot(length(coef(fit))==2L,all(is.finite(fit$var.coef)))
 ''','La convergenza è un requisito di calcolo, non una garanzia scientifica. AIC riguarda l’adattamento penalizzato e va distinto dalla prestazione futura.'),
 step('La differenza esplicita serve a capire','Costruiamo la trasformazione separatamente per controllarne l’indice temporale. Questo oggetto serve alla diagnosi, mentre il modello precedente resta stimato sui livelli.','''
 z <- diff(diff(train,lag=12),differences=1)
 data.frame(livelli=length(train),dopo_differenza_12=length(diff(train,lag=12)),
            doppia_differenza=length(z))
 stile_grafico()
 plot(z,type="l",col=palette_geo[1],xlab="Anno",ylab="Differenza (ppm)",
      main="Trasformazione diagnostica: (1-B)(1-B^12)")
 abline(h=0,lty=2)
 ''','La trasformazione esplicita conserva 155 valori. Passarla di nuovo a una chiamata con d=1 e D=1 introdurrebbe altre differenze.')],
 step('Una specifica alternativa dichiarata','Stimare un modello stagionale con il solo termine MA stagionale. Il confronto è esplorativo all’interno del train.','''
 alternativo <- arima(train,order=c(0,1,0),
   seasonal=list(order=c(0,1,1),period=12),include.mean=FALSE,method="ML")
 stopifnot(is.null(alternativo$code)||alternativo$code==0L)
 data.frame(modello=c("MA1 e MA stagionale","Solo MA stagionale"),
            AIC=c(AIC(fit),AIC(alternativo)))
 ''','Le due specifiche condividono differenze, campione e metodo ML. Il confronto AIC è interpretabile in questo contesto, ma il modello scelto richiede ancora diagnostica e validazione.'),
 'Applicare diff due volte ai dati e poi dichiarare ancora d=1 e D=1 in arima.',
 'La specifica SARIMA va applicata ai livelli quando arima gestisce le differenze. Ordini, metodo di stima, componenti deterministiche e convergenza fanno parte del risultato riproducibile.')

nb('Residui: controlli prima della previsione','Quale struttura rimane dopo l’adattamento del modello?',
 ['Separare residui del train ed errori del test.','Leggere ACF e grafici diagnostici.','Interpretare Ljung–Box con gradi di libertà dichiarati.'],CO2,[
 step('I residui appartengono al train','Seguiamo la convenzione del laboratorio originale, che esclude i primi 13 residui legati all’avvio del modello differenziato. Questa scelta resta documentata.',LOAD+'\n'+FIT+'''
 res <- as.numeric(residuals(fit))
 res <- res[seq.int(14,length(res))]
 res <- res[is.finite(res)]
 data.frame(n=length(res),media=mean(res),sd=sd(res),min=min(res),max=max(res))
 stile_grafico()
 plot(res,type="l",col=palette_geo[1],xlab="Indice residuo",ylab="Residuo (ppm)",
      main="Innovazioni stimate nel train")
 abline(h=0,lty=2)
 ''','Il grafico mostra segni, sequenze e osservazioni insolite. Non comprende i 36 errori di previsione finali: quelli richiedono una verifica separata.'),
 step('La dipendenza residua ha una scala','Ljung–Box aggrega autocorrelazioni fino al ritardo dichiarato. Usiamo 24 ritardi e fitdf=2 per i due coefficienti MA stimati.','''
 stile_grafico()
 acf(res,lag.max=36,main="ACF dei residui del train")
 lb <- Box.test(res,lag=24,type="Ljung-Box",fitdf=2)
 data.frame(statistica=as.numeric(lb$statistic),df=as.numeric(lb$parameter),
            p_value=lb$p.value,lag=24,fitdf=2)
 ''','Il test riguarda assenza di autocorrelazione fino a quei ritardi nel riferimento approssimato. Un p-value elevato non dimostra indipendenza, normalità o correttezza della previsione.'),
 step('La forma della distribuzione completa la diagnosi','Il QQ plot esplora l’adeguatezza di un riferimento gaussiano per le innovazioni, importante per l’intervallo predittivo condizionale.','''
 stile_grafico()
 qqnorm(res,pch=19,col=palette_geo[1],main="Residui e quantili gaussiani")
 qqline(res,col=palette_geo[2],lwd=2)
 data.frame(quartile=c("Q1","Mediana","Q3"),valore=as.numeric(quantile(res,c(.25,.5,.75))))
 ''','Scostamenti nelle code invitano a controllare eventi insoliti e sensibilità. I punti non sono una prova formale di gaussianità.')],
 step('Cambiare il ritardo diagnostico','Confrontare 12, 24 e 36 ritardi, conservando la stessa correzione dei coefficienti.','''
 do.call(rbind,lapply(c(12,24,36),function(L) {
   q <- Box.test(res,lag=L,type="Ljung-Box",fitdf=2)
   data.frame(lag=L,df=as.numeric(q$parameter),p_value=q$p.value)
 }))
 ''','La sensibilità al ritardo è informazione diagnostica. Scegliere solo il risultato più favorevole trasformerebbe il controllo in selezione del p-value.'),
 'Chiamare «errori fuori campione» i residui usati nella stima o interpretare un mancato rifiuto come certificazione del modello.',
 'La diagnostica combina successione temporale, autocorrelazione e forma della distribuzione. Consente di riconoscere problemi del modello prima della verifica predittiva, senza sostituirla.')

nb('Valutazione progressiva interna al train','Come si confrontano previsioni senza aprire il test finale?',
 ['Ripetere la stima a origini crescenti.','Confrontare SARIMA e riferimento stagionale.','Conservare origine e orizzonte per ogni errore.'],CO2,[
 step('Il disegno resta dentro il train','Le origini 120, 132 e 144 corrispondono a dicembre 1994, 1995 e 1996. Ogni previsione copre i dodici mesi successivi, tutti anteriori al test finale.',LOAD+'''
 origini <- c(120L,132L,144L)
 data.frame(origine=origini,data_origine=c2$dati$data[origini],
            primo_bersaglio=c2$dati$data[origini+1],
            ultimo_bersaglio=c2$dati$data[origini+12])
 stopifnot(all(origini+12<=length(train)))
 ''','Il disegno separa scelta del modello e test finale. Le tre origini sono poche: la loro sintesi è un confronto didattico, con variabilità che va mostrata.'),
 step('Ogni origine richiede una nuova stima','Per ciascuna origine la funzione riceve soltanto il passato disponibile. I 36 bersagli interni non sono i 36 mesi del test 1999–2001.','''
 dettaglio <- do.call(rbind,lapply(origini,function(o) {
   tr <- ts(as.numeric(train)[1:o],start=c(1985,1),frequency=12)
   obs <- as.numeric(train)[(o+1):(o+12)]
   mod <- stima_sarima(tr)
   pr <- as.numeric(predict(mod,n.ahead=12)$pred)
   sn <- as.numeric(tail(tr,12))
   data.frame(origine=o,h=1:12,osservato=obs,SARIMA=pr,Stagionale=sn)
 }))
 cv <- do.call(rbind,lapply(split(dettaglio,dettaglio$origine),function(d) {
   data.frame(origine=d$origine[1],RMSE_SARIMA=metriche(d$osservato,d$SARIMA)["RMSE"],
              RMSE_Stagionale=metriche(d$osservato,d$Stagionale)["RMSE"])
 }))
 rownames(cv) <- NULL
 cv
 ''','La graduatoria può variare con l’origine. Tutti i metodi devono affrontare gli stessi bersagli per rendere equo il confronto.'),
 step('Il registro rende verificabile la procedura','Salviamo sia la sintesi per origine sia le singole previsioni, così da poter ricalcolare metriche e controllare i confini temporali.','''
 write.csv(dettaglio,percorso_risultati("previsioni_CV.csv"),row.names=FALSE)
 write.csv(cv,percorso_risultati("metriche_CV.csv"),row.names=FALSE)
 stile_grafico()
 matplot(cv$origine,cv[,c("RMSE_SARIMA","RMSE_Stagionale")],type="b",pch=c(19,17),
   lty=1,col=palette_geo[1:2],xlab="Indice origine",ylab="RMSE a 12 mesi (ppm)",
   main="Validazione interna al train")
 legend("topleft",c("SARIMA","Stagionale"),col=palette_geo[1:2],pch=c(19,17),lty=1,bty="n")
 ''','Il grafico mantiene visibile la variabilità fra origini. Una media unica perderebbe questa parte dell’evidenza.')],
 step('Una quarta origine','Aggiungere l’origine 156, con verifica nei mesi 157–168 ancora interni al train.','''
 o <- 156L
 tr <- ts(as.numeric(train)[1:o],start=c(1985,1),frequency=12)
 obs <- as.numeric(train)[157:168]
 pr <- as.numeric(predict(stima_sarima(tr),n.ahead=12)$pred)
 rbind(SARIMA=metriche(obs,pr),Stagionale=metriche(obs,tail(tr,12)))
 ''','Il protocollo esteso aggiunge un confronto possibile senza toccare il test. Dichiarare la variante evita di confonderla con le tre origini del laboratorio originale.'),
 'Stimare una sola volta sui 168 mesi e chiamare «validazione interna» le previsioni retrospettive delle origini precedenti.',
 'La valutazione progressiva ricostruisce ciò che era disponibile a ogni origine. La stima si ripete e il test finale resta separato dalla scelta del modello.')

nb('Previsione e intervallo condizionale','Quale incertezza descrive la fascia attorno alla previsione?',
 ['Calcolare previsione e errore standard per 36 passi.','Costruire intervalli gaussiani puntuali.','Dichiarare quale incertezza resta esclusa.'],CO2,[
 step('Il modello produce media ed errore standard','La specifica resta SARIMA$(0,1,1)(0,1,1)_{12}$ stimata sui livelli del solo train.',LOAD+'\n'+FIT+'''
 fc <- predict(fit,n.ahead=h)
 previsione <- data.frame(data=c2$date_test,h=1:h,
   media=as.numeric(fc$pred),se=as.numeric(fc$se))
 head(previsione,6)
 stopifnot(all(is.finite(previsione$se)),all(previsione$se>=0))
 ''','L’errore standard dipende dall’orizzonte e dal modello. L’implementazione predict.Arima non include l’incertezza della stima dei parametri.'),
 step('Il livello nominale entra nel quantile',r'Usiamo $\hat y_{T+h}\pm z_{0,975}\,\widehat{se}_h$. La lettura gaussiana è condizionata alla specifica stimata e alle sue ipotesi.','''
 previsione$inferiore95 <- previsione$media-qnorm(.975)*previsione$se
 previsione$superiore95 <- previsione$media+qnorm(.975)*previsione$se
 previsione$ampiezza95 <- previsione$superiore95-previsione$inferiore95
 previsione[c(1,12,24,36),]
 write.csv(previsione,percorso_risultati("previsione_condizionale.csv"),row.names=FALSE)
 ''','La fascia è puntuale: 95% nominale per ciascun orizzonte sotto il modello. Non equivale a 95% di probabilità che l’intera traiettoria resti dentro tutte le bande.'),
 step('Il disegno mostra solo ciò che si prevede','Il grafico conserva l’origine e i livelli del train. I valori osservati del test non sono necessari per costruire la previsione.','''
 stile_grafico()
 plot(c2$dati$data[1:168],as.numeric(train),type="l",col="grey45",
   xlim=range(c2$dati$data),ylim=range(train,previsione$inferiore95,previsione$superiore95),
   xlab="Data",ylab="CO2 (ppm)",main="Previsione a origine fissa")
 polygon(c(previsione$data,rev(previsione$data)),
   c(previsione$inferiore95,rev(previsione$superiore95)),
   col=adjustcolor(palette_geo[1],.18),border=NA)
 lines(previsione$data,previsione$media,col=palette_geo[1],lwd=2)
 abline(v=as.numeric(as.Date("1999-01-01")),lty=2)
 ''','La previsione riguarda l’archivio storico e non la CO₂ attuale. Un cambiamento strutturale futuro non è automaticamente rappresentato da queste bande.')],
 step('Dal 95% all’80%','Calcolare l’ampiezza nominale all’80% alle stesse date.','''
 previsione$ampiezza80 <- 2*qnorm(.9)*previsione$se
 previsione[c(1,12,36),c("h","ampiezza80","ampiezza95")]
 stopifnot(all(previsione$ampiezza80<=previsione$ampiezza95))
 ''','Un livello nominale più basso restringe la fascia senza migliorare il modello. Copertura e ampiezza vanno valutate congiuntamente.'),
 'Presentare l’intervallo come garanzia universale, o interpretarlo come intervallo di confidenza di una costante senza distinguere il valore futuro.',
 'La fascia descrive l’incertezza predittiva condizionale del modello gaussiano stimato. Non comprende automaticamente stima dei parametri, scelta del modello, cambiamenti di regime o copertura simultanea della traiettoria.')

nb('Aprire il test e confrontare gli errori','Come si confrontano i metodi sul periodo escluso?',
 ['Usare gli stessi 36 bersagli per tutti i metodi.','Calcolare MAE, RMSE e bias con segno esplicito.','Distinguere valutazione finale e nuova selezione.'],CO2,[
 step('Le previsioni precedono il confronto','I metodi sono quelli del protocollo già dichiarato. Il test viene usato qui per quantificare la prestazione.',LOAD+'\n'+FIT+'''
 pred <- baseline_co2(train,h)[c("Ultimo","Stagionale","Deriva")]
 pred$SARIMA <- as.numeric(predict(fit,n.ahead=h)$pred)
 stopifnot(all(vapply(pred,length,integer(1))==length(test)))
 data.frame(h=1:3,osservato=as.numeric(test)[1:3],
            previsto_SARIMA=pred$SARIMA[1:3])
 ''','Tutti i metodi partono dal dicembre 1998. Nessuno aggiorna la previsione usando i valori del test nei mesi successivi.'),
 step('Tre metriche descrivono aspetti diversi',r'Definiamo $e_h=y_{T+h}-\hat y_{T+h}$, $MAE=\operatorname{media}|e_h|$ e $RMSE=\sqrt{\operatorname{media}(e_h^2)}$. Un bias positivo indica sottostima media.','''
 risultati <- as.data.frame(do.call(rbind,lapply(pred,function(p) metriche(test,p))))
 risultati$modello <- rownames(risultati)
 rownames(risultati) <- NULL
 risultati <- risultati[,c("modello","MAE","RMSE","bias_osservato_meno_previsto")]
 risultati
 write.csv(risultati,percorso_risultati("metriche_test.csv"),row.names=FALSE)
 ''','MAE e RMSE restano in ppm. RMSE pesa maggiormente gli errori ampi, mentre il bias può nascondere compensazioni fra segni.'),
 step('Il calendario localizza gli errori','La prestazione riassuntiva va accompagnata dalla successione degli scarti per riconoscere errori persistenti.','''
 errori <- sapply(pred,function(p) as.numeric(test)-p)
 stile_grafico()
 matplot(1:h,errori,type="l",lty=1,col=palette_geo,lwd=1.7,
   xlab="Mesi dall'origine",ylab="Osservato - previsto (ppm)",main="Errori nel test storico")
 abline(h=0,lty=2)
 legend("topleft",names(pred),col=palette_geo,lty=1,bty="n",cex=.8)
 ''','Le curve rendono visibili scostamenti sistematici e stagionalità residua. Un solo holdout resta una verifica limitata di trasferibilità.')],
 step('MAE e RMSE ordinano allo stesso modo?','Ordinare le tabelle secondo due perdite e confrontare la graduatoria.','''
 data.frame(posizione=seq_len(nrow(risultati)),
   ordine_MAE=risultati$modello[order(risultati$MAE)],
   ordine_RMSE=risultati$modello[order(risultati$RMSE)])
 ''','Una graduatoria diversa può riflettere il peso degli errori grandi. La metrica va scelta in rapporto alla domanda prima di usare il test per decidere.'),
 'Dopo aver visto la graduatoria del test, cambiare ordini finché il modello supera i riferimenti e riportare lo stesso test come indipendente.',
 'Il confronto usa gli stessi bersagli, le stesse unità e un’origine comune. La tabella finale quantifica ciò che accade in questo segmento storico, con il protocollo fissato.')

nb('Orizzonte e copertura descrittiva','Come cambiano errori e copertura con la distanza dall’origine?',
 ['Conservare l’orizzonte di ogni previsione.','Contare le osservazioni dentro l’intervallo.','Distinguere copertura descrittiva e calibrazione della procedura.'],CO2,[
 step('Una riga per bersaglio','Affianchiamo osservato, previsto e intervallo senza perdere l’orizzonte.',LOAD+'\n'+FIT+'''
 fc <- predict(fit,n.ahead=h)
 p <- data.frame(data=c2$date_test,h=1:h,osservato=as.numeric(test),
   previsto=as.numeric(fc$pred),se=as.numeric(fc$se))
 p$inferiore <- p$previsto-qnorm(.975)*p$se
 p$superiore <- p$previsto+qnorm(.975)*p$se
 p$errore <- p$osservato-p$previsto
 p$dentro95 <- p$osservato>=p$inferiore & p$osservato<=p$superiore
 head(p,4)
 ''','Le 36 righe sono orizzonti della stessa origine. Le loro dipendenze impediscono di trattarle automaticamente come 36 prove indipendenti di calibrazione.'),
 step('La copertura si accompagna alla numerosità','Il conteggio è una descrizione del test. Per studiare la calibrazione a un dato orizzonte occorrono molte origini o simulazioni dichiarate.','''
 data.frame(dentro=sum(p$dentro95),totale=nrow(p),quota=mean(p$dentro95),
            ampiezza_media=mean(p$superiore-p$inferiore))
 p$blocco <- factor(rep(c("1-12 mesi","13-24 mesi","25-36 mesi"),each=12),
                   levels=c("1-12 mesi","13-24 mesi","25-36 mesi"))
 do.call(rbind,lapply(split(p,p$blocco),function(d) {
   data.frame(blocco=as.character(d$blocco[1]),n=nrow(d),MAE=mean(abs(d$errore)),
              quota_dentro95=mean(d$dentro95),ampiezza=mean(d$superiore-d$inferiore))
 }))
 ''','Una quota lontana dal 95% può rivelare problemi, ma una quota vicina non basta a certificare la procedura. L’ampiezza contribuisce al giudizio di utilità.'),
 step('Gli errori hanno un andamento','Il riferimento zero mantiene visibile il segno della previsione e le sequenze di sottostima o sovrastima.','''
 stile_grafico()
 plot(p$h,p$errore,type="b",pch=19,col=palette_geo[1],xlab="Mesi dall'origine",
      ylab="Osservato - previsto (ppm)",main="Errore per orizzonte")
 abline(h=0,lty=2)
 write.csv(p,percorso_risultati("errori_intervalli_per_orizzonte.csv"),row.names=FALSE)
 ''','Le differenze fra anni del test vanno riportate, non compensate soltanto in una media globale.')],
 step('Contare la copertura all’80%','Ricalcolare la quota descrittiva per un livello nominale diverso, mantenendo le stesse previsioni.','''
 dentro80 <- abs(p$errore)<=qnorm(.9)*p$se
 data.frame(livello=c(.8,.95),dentro=c(sum(dentro80),sum(p$dentro95)),
   n=nrow(p),quota=c(mean(dentro80),mean(p$dentro95)))
 stopifnot(all(!dentro80 | p$dentro95))
 ''','Le bande sono annidate. Questa proprietà geometrica non dimostra calibrazione statistica.'),
 'Trattare i 36 orizzonti correlati di una singola origine come repliche indipendenti e associare una garanzia al semplice conteggio.',
 'Errori, copertura e ampiezza vanno letti per orizzonte. Il test storico permette una descrizione verificabile, mentre la calibrazione richiede un disegno più esteso.')

nb('Esportare una previsione verificabile','Quali file permettono a un’altra persona di ricostruire la previsione?',
 ['Salvare date, metodi e intervalli.','Conservare il modello e il protocollo.','Rileggere gli output e controllarne l’identità.'],CO2,[
 step('La tabella conserva il bersaglio','Esportiamo valori previsti e osservati con origine e orizzonte, in modo che la tabella si interpreti anche fuori dalla sessione R.',LOAD+'\n'+FIT+'''
 fc <- predict(fit,n.ahead=h)
 tab <- data.frame(origine="1998-12-01",data=as.character(c2$date_test),h=1:h,
   osservato=as.numeric(test),previsto=as.numeric(fc$pred),
   inferiore95=as.numeric(fc$pred-qnorm(.975)*fc$se),
   superiore95=as.numeric(fc$pred+qnorm(.975)*fc$se),unita="ppm")
 write.csv(tab,percorso_risultati("previsioni_test.csv"),row.names=FALSE)
 pr <- baseline_co2(train,h)[c("Ultimo","Stagionale","Deriva")]
 pr$SARIMA <- tab$previsto
 met <- as.data.frame(do.call(rbind,lapply(pr,function(z) metriche(tab$osservato,z))))
 met$modello <- rownames(met); rownames(met) <- NULL
 write.csv(met,percorso_risultati("metriche_test.csv"),row.names=FALSE)
 head(tab,3)
 met
 ''','L’origine non si ricava dal semplice nome del modello. Date e unità devono accompagnare ogni valore.'),
 step('Il modello e la specifica hanno file distinti','L’oggetto RDS conserva l’adattamento. Il testo spiega la procedura a chi non apre R.','''
 saveRDS(fit,percorso_risultati("modello_SARIMA.rds"))
 cv <- do.call(rbind,lapply(c(120L,132L,144L),function(o) {
   tr <- ts(as.numeric(train)[1:o],start=c(1985,1),frequency=12)
   osservato <- as.numeric(train)[o+1:12]
   previsto <- as.numeric(predict(stima_sarima(tr),n.ahead=12)$pred)
   stagionale <- as.numeric(tail(tr,12))
   data.frame(origine=o,RMSE_SARIMA=metriche(osservato,previsto)["RMSE"],
     RMSE_stagionale=metriche(osservato,stagionale)["RMSE"])
 }))
 rownames(cv) <- NULL
 write.csv(cv,percorso_risultati("validazione_interna_train.csv"),row.names=FALSE)
 cv
 protocollo <- c("CO2 storica: aggregazione mensile del corso, ppm.",
   "Train 1985-01/1998-12. Test 1999-01/2001-12.",
   "Origine fissa dicembre 1998, 36 mesi, nessun aggiornamento nel test.",
   "SARIMA(0,1,1)(0,1,1)[12], ML, senza drift.",
   "Intervalli gaussiani puntuali condizionali. Incertezza dei parametri esclusa.",
   paste("Runtime:",R.version.string),capture.output(met))
 writeLines(protocollo,percorso_risultati("protocollo.txt"),useBytes=TRUE)
 cat(paste(protocollo,collapse="\n"))
 ''','Il contenitore RDS dipende da R. CSV e protocollo testuale rendono il risultato accessibile e controllabile anche senza caricare l’oggetto.'),
 step('La rilettura controlla la consegna','Un file scritto con successo può essere incompleto o mal interpretato. Verifichiamo numero di righe, colonne e corrispondenza numerica.','''
 ritorno <- read.csv(percorso_risultati("previsioni_test.csv"),stringsAsFactors=FALSE)
 fit2 <- readRDS(percorso_risultati("modello_SARIMA.rds"))
 stopifnot(nrow(ritorno)==36L,identical(ritorno$data,tab$data),
   isTRUE(all.equal(ritorno$previsto,tab$previsto,tolerance=1e-10)),
   isTRUE(all.equal(as.numeric(predict(fit2,n.ahead=h)$pred),tab$previsto)))
 data.frame(controllo=c("36 righe","Date identiche","Valori riletti","Previsione da RDS"),esito=TRUE)
 ''','Il controllo di ritorno rende verificabile il percorso fino al file consegnato.')],
 step('La metrica si ricalcola dal CSV','Usare soltanto la tabella riletta per ottenere le metriche finali.','''
 metriche(ritorno$osservato,ritorno$previsto)
 write.csv(as.data.frame(t(metriche(ritorno$osservato,ritorno$previsto))),
   percorso_risultati("metriche_da_csv.csv"),row.names=FALSE)
 ''','Chi riceve il CSV può controllare le metriche senza rieseguire la stima. La provenienza dei dati resta comunque necessaria.'),
 'Consegnare soltanto il grafico o un RDS senza calendario, unità e descrizione della specifica.',
 'Una previsione ricostruibile unisce tabella, protocollo, dati originali e codice. La rilettura verifica che l’esportazione conservi effettivamente ciò che si intende comunicare.')

nb('Percorso obbligatorio e approfondimento','Quale domanda affronta il progetto base e quale il sistema VAR?',
 ['Identificare unità osservativa e bersaglio.','Controllare i fossili prima della regressione.','Separare il progetto morfometrico dall’approfondimento temporale.'],FOS+' '+VAR,[
 step('Una domanda per ciascun dataset','Il progetto base riguarda individui, il VAR riguarda una successione bivariata. Una tabella di progetto mantiene esplicita questa differenza.','''
 progetti <- data.frame(percorso=c("Base morfometrico","Approfondimento VAR"),
   unita=c("Fossile sintetico","Passo temporale sintetico"),
   bersaglio=c("Diametro interno","X e Y future"),
   verifica=c("32 individui esclusi","Passi 251-260"))
 progetti
 ''','I due percorsi condividono audit e validazione, ma richiedono split e interpretazioni diversi.'),
 step('L’audit precede il modello','Controlliamo identificativi e vincoli fisici, senza cancellare osservazioni automaticamente.','''
 f <- carica_dati("fossili_simulati.csv")
 audit <- data.frame(controllo=c("ID unici","Diametri completi","Totale positivo","Interno entro totale"),
   esito=c(!anyDuplicated(f$id),!anyNA(f[c("diametro_tot_um","diametro_int_um")]),
     all(f$diametro_tot_um>0),all(f$diametro_int_um>0 & f$diametro_int_um<=f$diametro_tot_um)))
 audit
 stopifnot(all(audit$esito))
 ''','Un esito positivo significa coerenza con i controlli adottati, non assenza di ogni possibile problema.'),
 step('Il legame geometrico limita la spiegazione','Il rapporto fra diametri contiene già il bersaglio. Non è disponibile prima di misurare il diametro interno.','''
 scarto <- f$diametro_int_um-(f$diametro_tot_um-2*f$spessore_um)
 data.frame(n=nrow(f),massimo_scarto_geometrico=max(abs(scarto)))
 stile_grafico()
 plot(f$diametro_tot_um,f$diametro_int_um,pch=19,col=palette_geo[1],
   xlab="Diametro totale (micrometri)",ylab="Diametro interno (micrometri)",
   main="Misure sintetiche geometricamente legate")
 abline(0,1,lty=2)
 ''','Una forte associazione è in parte incorporata nella costruzione geometrica. Non basta per attribuire un meccanismo causale indipendente.')],
 step('Il protocollo è una tabella','Scrivere prima del modello gli elementi minimi della consegna.','''
 piano <- data.frame(voce=c("Domanda","Input disponibile","Bersaglio","Split","Riferimento"),
   scelta=c("Prevedere il diametro interno","Diametro totale","Diametro interno in micrometri",
   "Ogni quinta riga nel test","Media del solo train"))
 write.csv(piano,percorso_risultati("piano_progetto.csv"),row.names=FALSE)
 piano
 ''','Il piano rende riconoscibili cambiamenti effettuati dopo aver visto i risultati.'),
 'Mescolare individui e tempi nella stessa strategia di split, oppure introdurre il rapporto interno/totale come predittore ignoto all’atto della previsione.',
 'Il percorso base verifica una regressione morfometrica su individui sintetici. Il VAR approfondisce la previsione di un sistema temporale. Domande, unità e limiti restano distinti.')

nb('Dichiarare prima il confronto predittivo','La regressione migliora la previsione rispetto alla media del train?',
 ['Riprodurre lo split dichiarato.','Stimare usando soltanto il train.','Confrontare modello e riferimento sugli stessi individui.'],FOS,[
 step('Gli identificativi fissano la separazione','Il laboratorio conserva ogni quinta riga nel test. Questo disegno deterministico dipende dall’ordine del file e non equivale a un campionamento casuale.','''
 f <- carica_dati("fossili_simulati.csv")
 s <- prepara_fossili(f); tr <- s$train; te <- s$test
 data.frame(insieme=c("Train","Test"),n=c(nrow(tr),nrow(te)))
 stopifnot(nrow(tr)==128L,nrow(te)==32L,!any(tr$id %in% te$id))
 table(insieme=ifelse(f$id %in% te$id,"Test","Train"),morfotipo=f$morfotipo)
 ''','La tabella dei morfotipi descrive la composizione degli insiemi. Le prestazioni restano legate a questa divisione didattica.'),
 step('Stima e riferimento usano la stessa informazione','La regressione usa soltanto il diametro totale. Il riferimento è costante e pari alla media dei diametri interni del train.','''
 mod <- lm(diametro_int_um~diametro_tot_um,data=tr)
 prev <- as.numeric(predict(mod,newdata=te))
 base <- rep(mean(tr$diametro_int_um),nrow(te))
 data.frame(termine=names(coef(mod)),stima=as.numeric(coef(mod)))
 head(data.frame(id=te$id,osservato=te$diametro_int_um,regressione=prev,baseline=base),4)
 ''','Il valore della baseline non deve usare i diametri interni del test. Una stima corretta dei parametri non implica automaticamente un buon risultato sui nuovi casi.'),
 step('Il confronto conserva unità e campione','Calcoliamo perdite sui medesimi 32 individui e salviamo la tabella.','''
 confronto <- rbind(Media_train=metriche(te$diametro_int_um,base),
                     Regressione=metriche(te$diametro_int_um,prev))
 confronto
 write.csv(confronto,percorso_risultati("metriche_fossili.csv"))
 ''','Le metriche sono in micrometri. Il confronto quantifica il contributo predittivo del diametro totale entro questa simulazione.')],
 step('La mediana come riferimento','La mediana del train offre un ulteriore riferimento costante, naturale per una perdita assoluta.','''
 med <- rep(median(tr$diametro_int_um),nrow(te))
 rbind(Media=metriche(te$diametro_int_um,base),
       Mediana=metriche(te$diametro_int_um,med))
 ''','La variante amplia la discussione della perdita. Non trasforma il test già esaminato in un nuovo campione indipendente.'),
 'Calcolare la baseline sull’intero dataset o scegliere il predittore dopo aver misurato il suo vantaggio nel test.',
 'Il confronto è interpretabile quando informazioni disponibili, individui del test e metrica restano gli stessi. Il legame geometrico e la natura sintetica delimitano la conclusione.')

nb('Un grafico e una diagnostica utili alla domanda','Quali grafici distinguono adattamento e previsione?',
 ['Disegnare osservato contro previsto nel test.','Esaminare i residui nel train.','Collegare gli assi alla quantità misurata.'],FOS,[
 step('La bisettrice rappresenta una previsione esatta','Ogni punto del test confronta lo stesso individuo previsto e osservato. Assi con uguale scala permettono di leggere la distanza dalla bisettrice.','''
 f <- carica_dati("fossili_simulati.csv"); s <- prepara_fossili(f)
 tr <- s$train; te <- s$test
 mod <- lm(diametro_int_um~diametro_tot_um,data=tr)
 prev <- as.numeric(predict(mod,newdata=te))
 stile_grafico()
 lim <- range(prev,te$diametro_int_um)
 plot(prev,te$diametro_int_um,pch=19,col=palette_geo[1],xlim=lim,ylim=lim,asp=1,
   xlab="Previsto nel test (micrometri)",ylab="Osservato nel test (micrometri)",
   main="32 individui esclusi dalla stima")
 abline(0,1,lty=2)
 ''','La vicinanza alla bisettrice descrive la prestazione sui casi esclusi. Il grafico non mostra di per sé l’incertezza delle previsioni.'),
 step('I residui servono alla diagnosi del train','Una struttura dei residui rispetto ai valori stimati può suggerire un andamento medio incompleto o una variabilità non costante.','''
 stile_grafico()
 plot(fitted(mod),residuals(mod),pch=19,col=palette_geo[2],
   xlab="Stimato nel train (micrometri)",ylab="Residuo nel train (micrometri)",
   main="Diagnostica della regressione")
 abline(h=0,lty=2)
 data.frame(n_train=nobs(mod),sd_residua=sigma(mod),df_residui=df.residual(mod))
 ''','Questi residui appartengono all’insieme che ha determinato i coefficienti. Non vanno usati al posto degli errori del test.'),
 step('Il contesto del gruppo aiuta a leggere','I morfotipi sono metadati della simulazione. Li usiamo qui per descrivere gli errori, senza cambiare il modello già valutato.','''
 errori <- data.frame(id=te$id,morfotipo=te$morfotipo,errore=te$diametro_int_um-prev)
 aggregate(errore~morfotipo,data=errori,FUN=mean)
 aggregate(abs(errore)~morfotipo,data=errori,FUN=mean)
 write.csv(errori,percorso_risultati("errori_per_individuo.csv"),row.names=FALSE)
 ''','La descrizione per gruppo può orientare una successiva indagine. Un modello modificato dopo questo esame richiederebbe una nuova valutazione.')],
 step('Il QQ plot dei residui','Esplorare la forma degli scarti del train.','''
 stile_grafico()
 qqnorm(residuals(mod),pch=19,col=palette_geo[1],main="Residui della regressione e riferimento normale")
 qqline(residuals(mod),col=palette_geo[2])
 ''','La forma della distribuzione ha rilievo per gli intervalli del modello. La previsione puntuale e il suo errore restano oggetti distinti.'),
 'Sovrapporre residui di adattamento ed errori di previsione in un solo grafico senza identificare gli insiemi.',
 'Osservato contro previsto documenta il test. Residui contro stimato documenta l’adattamento. Le etichette chiariscono quale informazione sostiene ciascuna conclusione.')

nb('Generare una relazione che riporti i risultati reali','Come si scrive una conclusione collegata agli output calcolati?',
 ['Generare il testo dai risultati dell’analisi.','Esplicitare fonte, split e unità.','Rileggere la relazione senza completare a mano i numeri.'],FOS,[
 step('I risultati vengono prima della frase','Ricalcoliamo il progetto per rendere autonomo questo notebook. La tabella finale alimenterà il testo.','''
 f <- carica_dati("fossili_simulati.csv"); s <- prepara_fossili(f)
 tr <- s$train; te <- s$test
 mod <- lm(diametro_int_um~diametro_tot_um,data=tr)
 prev <- as.numeric(predict(mod,newdata=te))
 base <- rep(mean(tr$diametro_int_um),nrow(te))
 m0 <- metriche(te$diametro_int_um,base); m1 <- metriche(te$diametro_int_um,prev)
 confronto <- data.frame(modello=c("Media_train","Regressione"),
   MAE=c(m0["MAE"],m1["MAE"]),RMSE=c(m0["RMSE"],m1["RMSE"]))
 audit <- data.frame(controllo=c("ID unici","Diametri completi","Totale positivo","Interno entro totale"),
   esito=c(!anyDuplicated(f$id),!anyNA(f[c("diametro_tot_um","diametro_int_um")]),
     all(f$diametro_tot_um>0),all(f$diametro_int_um>0 & f$diametro_int_um<=f$diametro_tot_um)))
 stopifnot(all(audit$esito))
 confronto
 ''','La relazione deve restare coerente se dati o specifica cambiano. Evitiamo valori numerici copiati separatamente dal codice.'),
 step('La conclusione mantiene i limiti','La differenza di RMSE è descritta nelle unità originali. Il risultato resta condizionato al dataset sintetico e al singolo holdout.','''
 rapporto <- c("PROGETTO MORFOMETRICO: DATI SINTETICI",
   "Domanda: prevedere il diametro interno a partire dal totale.",
   sprintf("Train: %d individui; test: %d, ogni quinta riga.",nrow(tr),nrow(te)),
   sprintf("Retta stimata: interno = %.4f + %.4f * totale (micrometri).",coef(mod)[1],coef(mod)[2]),
   sprintf("RMSE media train: %.4f micrometri; regressione: %.4f.",m0["RMSE"],m1["RMSE"]),
   sprintf("Differenza RMSE riferimento meno modello: %.4f micrometri.",m0["RMSE"]-m1["RMSE"]),
   "Limiti: dati simulati, misure geometricamente legate, un solo holdout noto.",
   "La previsione non dimostra causalita fisica; servono nuovi dati e un protocollo prospettico.")
 cat(paste(rapporto,collapse="\n"))
 ''','La frase riporta il risultato effettivo, anche se un’altra specifica non migliorasse il riferimento. La parte argomentativa non deve trasformare un caso sintetico in evidenza sul territorio.'),
 step('Testo e tabelle si verificano insieme','Conserviamo coefficienti, previsioni e relazione per ricostruire tutti i numeri riportati.','''
 writeLines(rapporto,percorso_risultati("relazione_progetto_base.txt"),useBytes=TRUE)
 write.csv(audit,percorso_risultati("audit_progetto.csv"),row.names=FALSE)
 write.csv(confronto,percorso_risultati("metriche_progetto.csv"),row.names=FALSE)
 write.csv(data.frame(id=te$id,osservato=te$diametro_int_um,previsto=prev),
   percorso_risultati("previsioni_fossili.csv"),row.names=FALSE)
 saveRDS(mod,percorso_risultati("modello_fossili.rds"))
 stopifnot(identical(readLines(percorso_risultati("relazione_progetto_base.txt"),warn=FALSE),rapporto))
 data.frame(righe_relazione=length(rapporto),previsioni=nrow(te),rilettura_identica=TRUE)
 ''','La rilettura controlla la consegna, mentre il giudizio sui limiti richiede comunque un’interpretazione scientifica.')],
 step('Un riepilogo alternativo','Scrivere un confronto basato su MAE, conservando il nome della metrica.','''
 sprintf("MAE sul medesimo test: riferimento %.4f, regressione %.4f micrometri.",m0["MAE"],m1["MAE"])
 ''','Cambiare la metrica cambia la perdita descritta. La frase deve nominarla esplicitamente.'),
 'Scrivere una conclusione favorevole al modello prima del calcolo oppure chiamare «reali» dati costruiti per la didattica.',
 'Una relazione verificabile deriva i numeri dai risultati e collega domanda, unità, disegno e limiti. La parte interpretativa resta proporzionata alla natura dei dati.')

nb('Approfondimento: un VAR(1) come due regressioni','Come si rappresenta la memoria reciproca di due serie?',
 ['Costruire ritardi senza disallineare le righe.','Stimare le due equazioni sullo stesso campione.','Leggere la matrice dei coefficienti.'],VAR,[
 step('I ritardi mantengono le coppie','Per ogni istante da 2 a 250, i predittori sono X e Y dell’istante precedente. La trasformazione produce 249 coppie complete.','''
 p <- carica_dati("processi_simulati.csv")
 v <- p[1:250,c("x_VAR","y_VAR")]
 lagged <- data.frame(x=v$x_VAR[-1],y=v$y_VAR[-1],
   x_lag=head(v$x_VAR,-1),y_lag=head(v$y_VAR,-1))
 head(lagged,4)
 stopifnot(nrow(lagged)==249L,lagged$x_lag[1]==v$x_VAR[1],lagged$x[1]==v$x_VAR[2])
 ''','Il ritardo costa una riga. Usare serie con lunghezze uguali non basta: ogni risposta deve essere associata ai suoi predittori passati.'),
 step('Due equazioni formano il sistema',r'Il VAR(1) scrive $\boldsymbol z_t=\boldsymbol c+A\boldsymbol z_{t-1}+\boldsymbol\varepsilon_t$. Entrambe le regressioni usano il medesimo insieme di predittori.','''
 fit_x <- lm(x~x_lag+y_lag,data=lagged)
 fit_y <- lm(y~x_lag+y_lag,data=lagged)
 coefficienti <- rbind(X=coef(fit_x),Y=coef(fit_y))
 coefficienti
 ''','La riga X descrive la prima equazione, la riga Y la seconda. I coefficienti incrociati riguardano un contributo predittivo condizionato agli altri regressori.'),
 step('La matrice conserva la direzione','La riga identifica la risposta e la colonna la variabile ritardata. Questa convenzione è essenziale per la previsione ricorsiva.','''
 A <- rbind(coef(fit_x)[c("x_lag","y_lag")],coef(fit_y)[c("x_lag","y_lag")])
 rownames(A) <- c("X","Y")
 intercetta <- c(coef(fit_x)[1],coef(fit_y)[1])
 A
 z250 <- as.numeric(v[250,])
 primo <- as.numeric(intercetta+A%*%z250)
 data.frame(variabile=c("X","Y"),prevista_passo251=primo)
 ''','L’operazione matrice per stato usa il valore al passo 250 per produrre il 251. Il futuro osservato non entra in questa operazione.')],
 step('Il modello senza contributi incrociati','Stimare separatamente due AR(1) per comprendere le restrizioni imposte.','''
 rid_x <- lm(x~x_lag,data=lagged); rid_y <- lm(y~y_lag,data=lagged)
 data.frame(equazione=c("X","Y"),AIC_VAR=c(AIC(fit_x),AIC(fit_y)),
   AIC_solo_memoria_propria=c(AIC(rid_x),AIC(rid_y)))
 ''','L’esercizio riguarda l’adattamento nel train. Un vantaggio AIC non prova né causalità né superiorità predittiva su dati esclusi.'),
 'Trasporre la matrice dei coefficienti o allineare X del tempo t con Y del tempo t anziché con il ritardo dichiarato.',
 'Il VAR(1) coordina due regressioni con i medesimi predittori ritardati. La matrice A rende esplicite memoria propria e dipendenza incrociata, da verificare prima dell’uso predittivo.')

nb('Stabilità e residui del sistema','La dinamica stimata si attenua e quali scarti rimangono?',
 ['Calcolare gli autovalori della matrice VAR.','Confrontare i moduli con uno.','Esaminare residui contemporanei e temporali.'],VAR,[
 step('La stabilità riguarda la matrice','Per un VAR(1) la dinamica è stabile quando tutti gli autovalori di A hanno modulo inferiore a uno. La condizione riguarda il modello stimato.','''
 p <- carica_dati("processi_simulati.csv")
 mod <- stima_var(p)
 ev <- eigen(mod$A,only.values=TRUE)$values
 data.frame(parte_reale=Re(ev),parte_immaginaria=Im(ev),modulo=Mod(ev))
 data.frame(stabile=all(Mod(ev)<1))
 ''','Una singola stima stabile non dimostra che ogni meccanismo reale sia stabile. Nel dataset sintetico conosciamo il contesto di simulazione, ma restano variabilità campionaria e avvio finito.'),
 step('Gli scarti possono condividere uno shock','La correlazione contemporanea fra residui X e Y è diversa dall’autocorrelazione nel tempo.','''
 rx <- residuals(mod$fit_x); ry <- residuals(mod$fit_y)
 cov(cbind(X=rx,Y=ry))
 cor(rx,ry)
 stile_grafico()
 plot(rx,ry,pch=19,col=palette_geo[1],xlab="Residuo X",ylab="Residuo Y",
      main="Scarti contemporanei del sistema")
 abline(h=0,v=0,lty=2,col="grey60")
 ''','Una covarianza contemporanea richiede attenzione nell’incertezza congiunta. Non identifica da sola la direzione di una relazione fisica.'),
 step('La successione verifica memoria residua','Le ACF delle due equazioni conservano la scala dei ritardi.','''
 stile_grafico(); acf(rx,lag.max=20,main="VAR: ACF residui equazione X")
 stile_grafico(); acf(ry,lag.max=20,main="VAR: ACF residui equazione Y")
 data.frame(equazione=c("X","Y"),n=c(length(rx),length(ry)),
            media=c(mean(rx),mean(ry)),sd=c(sd(rx),sd(ry)))
 ''','Residui con memoria suggeriscono una specifica incompleta. Grafici e test devono considerare la struttura del sistema e la stima dei parametri.')],
 step('Propagare una perturbazione nota','Conservare la matrice stimata e osservare come evolve uno scostamento iniziale unitario in X, senza aggiungere innovazioni.','''
 stato <- c(1,0)
 risposta <- matrix(NA_real_,21,2)
 risposta[1,] <- stato
 for(k in 1:20) { stato <- as.numeric(mod$A%*%stato); risposta[k+1,] <- stato }
 head(data.frame(h=0:20,X=risposta[,1],Y=risposta[,2]),6)
 stile_grafico()
 matplot(0:20,risposta,type="l",lty=1,col=palette_geo[1:2],
   xlab="Passi",ylab="Scostamento dal riferimento",main="Propagazione deterministica con A stimata")
 abline(h=0,lty=2)
 ''','Questa è una perturbazione dello stato, non un impulso strutturale identificato. Confronta la dinamica della matrice senza introdurre un’interpretazione causale.'),
 'Controllare separatamente i coefficienti diagonali e trascurare gli autovalori dell’intera matrice.',
 'La stabilità dipende dal sistema complessivo. La diagnosi dei residui completa la verifica e mantiene distinta la dipendenza contemporanea dalla memoria temporale.')

nb('Granger: confronto condizionato, non causalità fisica','Il passato di X aggiunge informazione predittiva per Y?',
 ['Confrontare modelli annidati sullo stesso campione.','Conservare entrambe le direzioni.','Correggere la famiglia di due confronti dichiarati.'],VAR,[
 step('L’ipotesi riguarda coefficienti ritardati','Nel VAR(1), la domanda X verso Y confronta Y spiegata dal proprio passato con Y spiegata anche da X ritardata.','''
 p <- carica_dati("processi_simulati.csv"); mod <- stima_var(p)
 ridotto_y <- lm(y~y_lag,data=mod$lagged)
 ridotto_x <- lm(x~x_lag,data=mod$lagged)
 g_xy <- anova(ridotto_y,mod$fit_y)
 g_yx <- anova(ridotto_x,mod$fit_x)
 g_xy
 g_yx
 ''','Le regressioni sono annidate e hanno le stesse 249 righe. L’inferenza F usa le ipotesi del modello lineare sulle innovazioni, da confrontare con la diagnostica.'),
 step('Le due direzioni costituiscono una famiglia','Conserviamo p-value grezzi e correzione Holm per i due confronti pianificati.','''
 p_g <- c(g_xy$`Pr(>F)`[2],g_yx$`Pr(>F)`[2])
 tab <- data.frame(direzione=c("X aiuta Y al lag 1","Y aiuta X al lag 1"),
   p_non_corretto=p_g,p_Holm_due_confronti=p.adjust(p_g,method="holm"))
 tab
 write.csv(tab,percorso_risultati("Granger_due_direzioni.csv"),row.names=FALSE)
 ''','Il numero di confronti si riferisce alla famiglia dichiarata. Cercare molti ritardi o molte variabili e correggere soltanto i due risultati selezionati cambierebbe il problema.'),
 step('Il test resta legato alla specifica','Affianchiamo la stima del coefficiente incrociato alla sua incertezza. Un effetto statisticamente rilevabile va ancora valutato per scala e utilità.','''
 sx <- summary(mod$fit_x)$coefficients
 sy <- summary(mod$fit_y)$coefficients
 data.frame(direzione=c("X verso Y","Y verso X"),
   coefficiente=c(sy["x_lag","Estimate"],sx["y_lag","Estimate"]),
   errore_standard=c(sy["x_lag","Std. Error"],sx["y_lag","Std. Error"]))
 ''','Il contributo è condizionato alle variabili incluse, al lag 1 e al periodo stimato. Cause comuni e variabili omesse restano possibili in un’applicazione osservativa.')],
 step('Leggere la correzione','Confrontare le decisioni al livello nominale del 5% senza eliminare i valori grezzi.','''
 data.frame(tab,rifiuto_grezzo=tab$p_non_corretto<.05,
            rifiuto_Holm=tab$p_Holm_due_confronti<.05)
 stopifnot(all(tab$p_Holm_due_confronti>=tab$p_non_corretto))
 ''','La correzione può conservare o modificare le decisioni. Anche un rifiuto corretto resta evidenza su una restrizione predittiva del modello.'),
 'Scrivere «X causa fisicamente Y» perché il p-value del confronto di Granger è piccolo.',
 'Il confronto valuta se un passato aggiunge informazione nel modello specificato. L’interpretazione fisica richiede un disegno e assunzioni ulteriori, oltre al solo risultato statistico.')

nb('Previsione ricorsiva senza osservazioni future','Come si prosegue il sistema dopo il passo 250?',
 ['Avviare la ricorsione dall’ultimo stato osservato.','Usare gli stati previsti nei passi successivi.','Confrontare con il riferimento dell’ultimo valore.'],VAR,[
 step('La prima previsione usa lo stato osservato','Dopo l’origine non si sostituiscono le previsioni con i valori futuri osservati.','''
 p <- carica_dati("processi_simulati.csv"); mod <- stima_var(p)
 h <- 10L
 stato <- as.numeric(tail(mod$v,1))
 prev <- matrix(NA_real_,h,2,dimnames=list(NULL,c("X","Y")))
 for(k in seq_len(h)) {
   stato <- as.numeric(mod$intercetta+mod$A%*%stato)
   prev[k,] <- stato
 }
 data.frame(passo=251:260,prev)
 ''','Le innovazioni future hanno media condizionale zero nel modello. La traiettoria puntuale non riproduce i futuri shock casuali.'),
 step('La verifica apre i dieci bersagli','Solo ora i valori osservati vengono usati per quantificare l’errore a origine fissa.','''
 obs <- as.matrix(p[251:260,c("x_VAR","y_VAR")])
 base <- matrix(rep(as.numeric(tail(mod$v,1)),each=h),ncol=2)
 confronto <- data.frame(variabile=c("X","Y"),
   RMSE_VAR=sqrt(colMeans((obs-prev)^2)),
   RMSE_ultimo=sqrt(colMeans((obs-base)^2)))
 confronto
 ''','Dieci passi da una sola origine sono un esempio limitato. Un risultato favorevole o sfavorevole non rappresenta la prestazione universale del VAR.'),
 step('La figura mantiene lo stesso bersaglio','Disegniamo Y osservata e prevista, etichettando l’orizzonte.','''
 stile_grafico()
 matplot(1:h,cbind(obs[,2],prev[,2],base[,2]),type="b",pch=c(19,1,17),lty=c(1,2,3),
   col=palette_geo[1:3],xlab="Passi dall'origine 250",ylab="Y sintetica",
   main="Previsione ricorsiva a origine fissa")
 legend("topleft",c("Osservato","VAR","Ultimo valore"),col=palette_geo[1:3],
   pch=c(19,1,17),lty=c(1,2,3),bty="n")
 write.csv(data.frame(passo=251:260,X_osservata=obs[,1],Y_osservata=obs[,2],
   X_prevista=prev[,1],Y_prevista=prev[,2]),percorso_risultati("previsioni_VAR.csv"),row.names=FALSE)
 ''','La previsione ricorsiva può attenuarsi mentre la realizzazione futura riceve nuovi shock. Questo comportamento è coerente con la distinzione fra previsione media e dato.')],
 step('Una verifica automatica della ricorsione','Confrontare il ciclo visibile con la funzione di servizio e controllare il secondo passo.','''
 stopifnot(isTRUE(all.equal(prev,prevedi_var(mod,h))),
   isTRUE(all.equal(as.numeric(prev[2,]),as.numeric(mod$intercetta+mod$A%*%prev[1,]))))
 data.frame(controllo=c("Funzione e ciclo coincidono","Secondo passo usa il primo previsto"),esito=TRUE)
 ''','Il caso calcolabile verifica il codice. Non dimostra che il modello descriva ogni aspetto del processo.'),
 'Inserire X o Y osservata al passo 251 per calcolare il passo 252, continuando a chiamare il risultato «origine fissa 250».',
 'La ricorsione mantiene l’origine: ogni stato futuro deriva dallo stato previsto precedente. L’apertura dei bersagli serve esclusivamente al confronto finale.')

nb('Consegnare e verificare','Quali elementi rendono completa la consegna dell’approfondimento?',
 ['Conservare modello, previsioni e confronti.','Separare i risultati predittivi dai test.','Rileggere i file esportati.'],VAR,[
 step('La tabella collega origine e valori','Ricostruiamo il VAR per un’esecuzione autonoma e salviamo i dieci bersagli con le rispettive previsioni.','''
 p <- carica_dati("processi_simulati.csv"); mod <- stima_var(p)
 pr <- prevedi_var(mod,10)
 obs <- as.matrix(p[251:260,c("x_VAR","y_VAR")])
 tab <- data.frame(origine=250L,passo=251:260,h=1:10,
   X_osservata=obs[,1],Y_osservata=obs[,2],X_prevista=pr[,1],Y_prevista=pr[,2])
 write.csv(tab,percorso_risultati("consegna_VAR.csv"),row.names=FALSE)
 saveRDS(mod,percorso_risultati("modello_VAR.rds"))
 head(tab,3)
 ''','La consegna dichiara che X e Y sono senza unità fisica. Il file del modello non sostituisce la tabella leggibile.'),
 step('Metriche e test rispondono a domande diverse','La prima tabella valuta previsioni fuori dal train. La seconda valuta restrizioni nelle regressioni stimate.','''
 ultimo <- matrix(rep(as.numeric(tail(mod$v,1)),each=10),ncol=2)
 metriche_var <- data.frame(variabile=c("X","Y"),
   RMSE_VAR=sqrt(colMeans((obs-pr)^2)),
   RMSE_ultimo=sqrt(colMeans((obs-ultimo)^2)))
 gy <- anova(lm(y~y_lag,data=mod$lagged),mod$fit_y)
 gx <- anova(lm(x~x_lag,data=mod$lagged),mod$fit_x)
 pval <- c(gy$`Pr(>F)`[2],gx$`Pr(>F)`[2])
 granger <- data.frame(direzione=c("X verso Y","Y verso X"),p=pval,
                        p_Holm=p.adjust(pval,"holm"))
 write.csv(metriche_var,percorso_risultati("metriche_VAR.csv"))
 write.csv(granger,percorso_risultati("Granger.csv"),row.names=FALSE)
 metriche_var
 granger
 ''','Un test significativo non garantisce un guadagno predittivo in ogni futuro. Una buona previsione non identifica automaticamente una causa fisica.'),
 step('La verifica della consegna usa i file riletti','Una breve scheda documenta input, parametri e limiti insieme ai controlli automatici.','''
 ritorno <- read.csv(percorso_risultati("consegna_VAR.csv"))
 mod2 <- readRDS(percorso_risultati("modello_VAR.rds"))
 stopifnot(identical(ritorno$passo,251:260),
   isTRUE(all.equal(ritorno$X_prevista,pr[,1],check.attributes=FALSE,tolerance=1e-10)),
   isTRUE(all.equal(prevedi_var(mod2,10),pr)))
 scheda <- c("VAR(1) didattico su processi sintetici.",
   "Train: passi 1-250. Test: passi 251-260. Origine fissa 250.",
   "Due regressioni OLS con intercetta e ritardi X,Y.",
   "Granger: due direzioni pianificate, correzione Holm.",
   "Limiti: simulazione, singola origine, nessuna attribuzione causale fisica.")
 writeLines(scheda,percorso_risultati("scheda_modello.txt"),useBytes=TRUE)
 cat(paste(scheda,collapse="\n"))
 ''','La scheda delimita il significato del risultato. La prova di rilettura controlla il trasferimento delle informazioni.')],
 step('Inventario degli output','Elencare soltanto i file del notebook corrente e la loro dimensione.','''
 files <- list.files(dirname(percorso_risultati("scheda_modello.txt")),full.names=TRUE)
 data.frame(file=basename(files),bytes=file.info(files)$size)
 ''','L’inventario aiuta a riconoscere output mancanti. Per un archivio completo va affiancato al manifesto delle impronte del pacchetto.'),
 'Riportare solo il p-value più favorevole oppure confondere la scheda del progetto base con quella del VAR.',
 'Una consegna completa collega tabella, modello, metriche e limiti. La rilettura e la ricostruzione della previsione verificano il risultato trasferito.')

nb('Laboratorio applicativo: audit prima del modello','Che cosa succede se un individuo compare due volte?',
 ['Riconoscere un duplicato della chiave.','Distinguere duplicazione e nuova misura.','Conservare la segnalazione senza modificare l’originale.'],FOS,[
 step('Una copia mantiene intatto il CSV','Aggiungiamo deliberatamente una riga a un oggetto in memoria. L’esperimento permette di osservare il comportamento del controllo.','''
 f <- carica_dati("fossili_simulati.csv")
 copia <- rbind(f,f[1,])
 data.frame(originale=nrow(f),copia=nrow(copia),duplicati=sum(duplicated(copia$id)))
 copia[duplicated(copia$id),]
 stopifnot(nrow(f)==160L,nrow(copia)==161L)
 ''','Il CSV resta invariato. Una riga duplicata aumenta il peso dell’individuo senza creare una nuova unità indipendente.'),
 step('La chiave identifica il problema','Mostriamo tutte le righe che condividono una chiave, inclusa la prima occorrenza.','''
 flag <- duplicated(copia$id)|duplicated(copia$id,fromLast=TRUE)
 segnalazioni <- data.frame(riga=which(flag),copia[flag,],check.names=FALSE)
 segnalazioni
 write.csv(segnalazioni,percorso_risultati("segnalazioni_duplicati.csv"),row.names=FALSE)
 ''','Il controllo segnala identità ripetute. Stabilire se si tratta di una copia accidentale o di una misura ripetuta richiede metadati e protocollo.'),
 step('La duplicazione cambia i pesi','Confrontiamo le medie senza cancellare automaticamente la riga. Il cambiamento può essere piccolo ma il principio statistico resta rilevante.','''
 data.frame(archivio=c("Originale","Con duplicato"),
   n_righe=c(nrow(f),nrow(copia)),n_ID=c(length(unique(f$id)),length(unique(copia$id))),
   media_interno=c(mean(f$diametro_int_um),mean(copia$diametro_int_um)))
 ''','Il numero di righe non coincide più con il numero di individui. La duplice presenza può anche contaminare uno split se l’identificativo appare in entrambi gli insiemi.')],
 step('Una violazione geometrica separata','Modificare una copia di un diametro per simulare un errore e riconoscerlo.','''
 errore <- f
 errore$diametro_int_um[2] <- errore$diametro_tot_um[2]+1
 fuori <- errore$diametro_int_um>errore$diametro_tot_um
 errore[fuori,c("id","diametro_tot_um","diametro_int_um")]
 stopifnot(sum(fuori)==1L,nrow(carica_dati("fossili_simulati.csv"))==160L)
 ''','La chiave può essere corretta mentre la geometria è incoerente. Controlli diversi affrontano errori diversi.'),
 'Eliminare righe ripetute senza stabilire se rappresentano lo stesso individuo, repliche tecniche o misure in tempi differenti.',
 'L’audit riconosce e documenta la duplicazione prima del modello. I dati originali restano disponibili e le decisioni richiedono una spiegazione del processo di raccolta.')

nb('Laboratorio applicativo: baseline stagionale','Come si costruiscono diciotto mesi usando soltanto l’ultimo anno del train?',
 ['Associare ogni bersaglio al mese di riferimento.','Ripetere il ciclo oltre i primi dodici passi.','Controllare che il test non entri nella formula.'],CO2,[
 step('L’ultimo anno è il riferimento disponibile','Il protocollo usa la stessa origine del caso SARIMA. Costruiamo diciotto mesi senza consultare i valori del test.',LOAD+'''
 h18 <- 18L
 ultimo_anno <- as.numeric(tail(train,12))
 pred18 <- rep(ultimo_anno,length.out=h18)
 data.frame(h=1:h18,data=as.character(c2$date_test[1:h18]),
            mese_riferimento=rep(as.character(c2$dati$data[157:168]),length.out=h18),
            previsto=pred18)
 ''','Gennaio 2000 usa ancora gennaio 1998 nella previsione a origine fissa dicembre 1998. Gennaio 1999 osservato appartiene al futuro di quell’origine.'),
 step('La periodicità diventa un controllo','La regola è verificabile senza conoscere il test: i passi 13–18 ripetono i primi sei valori dell’ultimo anno.','''
 stopifnot(identical(pred18[13:18],ultimo_anno[1:6]),
           identical(pred18[1:12],ultimo_anno))
 data.frame(controllo=c("Primo anno uguale all'ultimo train","Mesi 13-18 ripetono 1-6"),esito=TRUE)
 stile_grafico()
 plot(1:h18,pred18,type="b",pch=19,col=palette_geo[1],xlab="Mesi dall'origine",
   ylab="CO2 prevista (ppm)",main="Baseline stagionale a 18 mesi")
 abline(v=12.5,lty=2)
 ''','La curva conserva la stagione ma non aggiunge crescita. Questa ipotesi va discussa quando la serie ha un trend.'),
 step('Il confronto usa esattamente diciotto bersagli','Calcoliamo le metriche sul sottoinsieme dichiarato. Non confrontiamo direttamente queste metriche con quelle su 36 mesi senza segnalare il cambio di orizzonte.','''
 obs18 <- as.numeric(test)[1:h18]
 fit <- stima_sarima(train)
 ar18 <- as.numeric(predict(fit,n.ahead=h18)$pred)
 rbind(Stagionale=metriche(obs18,pred18),SARIMA=metriche(obs18,ar18))
 write.csv(data.frame(data=c2$date_test[1:h18],osservato=obs18,
   stagionale=pred18,SARIMA=ar18),percorso_risultati("baseline_18_mesi.csv"),row.names=FALSE)
 ''','I due metodi condividono origine e bersagli. Il risultato riguarda questa finestra e non tutti i possibili periodi futuri.')],
 step('Trenta mesi senza accesso al futuro','Estendere la regola e verificare il terzo ciclo parziale.','''
 pred30 <- rep(ultimo_anno,length.out=30)
 stopifnot(identical(pred30[25:30],ultimo_anno[1:6]))
 data.frame(h=25:30,previsto=pred30[25:30])
 ''','L’estensione richiede solo il calendario della previsione. Per aggiornare il riferimento con nuovi valori servirebbe dichiarare una nuova origine.'),
 'Costruire la baseline con y del mese precedente dell’anno del test per gli orizzonti superiori a dodici, senza dichiarare l’aggiornamento.',
 'La baseline stagionale ripete l’ultimo ciclo osservato all’origine. Una tabella di corrispondenza fra mesi rende il calcolo trasparente e impedisce l’uso accidentale di osservazioni future.')

PREP='''# Trova la cartella M10 dal progetto autonomo o dal progetto generale.
.gs_cerca <- normalizePath(getwd(),winslash="/",mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca,
    file.path(.gs_cerca,"M10_Futura"),
    file.path(.gs_cerca,"03_Notebook_svolti","M10_Futura"),
    file.path(.gs_cerca,"M10","03_Notebook_svolti","M10_Futura"))
  .gs_ok <- file.exists(file.path(.gs_candidati,"M10_N01.Rmd")) &
    file.exists(file.path(.gs_candidati,"R","funzioni_notebook.R"))
  if(any(.gs_ok)) { .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]; break }
  .gs_padre <- dirname(.gs_cerca)
  if(.gs_padre==.gs_cerca) stop("Aprire il progetto M10_Futura o quello generale dei notebook.")
  .gs_cerca <- .gs_padre
}
source(file.path(.gs_modulo,"R","funzioni_notebook.R"),local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo,"{ID}")
carica_dati <- .gs_funzioni$carica_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88,digits=6)
if(requireNamespace("knitr",quietly=TRUE)) {
  knitr::opts_chunk$set(echo=TRUE,error=FALSE,warning=TRUE,message=TRUE,
    fig.width=8,fig.height=5,dpi=150,fig.align="center")
}
set.seed({SEED})
'''

def make():
    assert len(N)==20
    rows=[]
    for i,n in enumerate(N,1):
        ident=f'M10_N{i:02d}'
        yaml='---\ntitle: '+json.dumps(n['title'],ensure_ascii=False)+'\nsubtitle: "'+ident+' · Futura"\nlang: it-IT\noutput:\n  html_document:\n    toc: true\n    self_contained: true\n    theme: null\n    highlight: tango\n    mathjax: null\n    pandoc_args: ["--mathml"]\n    css: "R/stile_notebook.css"\n---\n'
        s=yaml+'\n# La domanda\n\n'+n['question']+'\n\n## Obiettivi\n\n'+'\n'.join('- '+o for o in n['objectives'])
        s+='\n\n**Prima di iniziare.** Sono richiesti vettori, tabelle e funzioni R di base. I blocchi vanno eseguiti in ordine. Il notebook è autonomo rispetto agli altri.\n\n**Dati e unità.** '+n['data']
        s+='\n\n## Preparazione\n\nAprire il progetto autonomo di Futura o quello generale del corso. I calcoli usano R base e stats. Gli output del notebook vanno in `Risultati/'+ident+'/`; i CSV originali restano invariati.\n\n```{r preparazione}\n'+PREP.replace('{ID}',ident).replace('{SEED}',str(10000+i))+'```\n'
        chunks=[dict(name='preparazione',code=PREP.replace('{ID}',ident).replace('{SEED}',str(10000+i)))]
        for j,st in enumerate(n['steps'],1):
            s+=f'\n## {j}. {st["title"]}\n\n{st["text"]}\n\n```{{r passo_{j:02d}}}\n{st["code"]}\n```\n\n**Lettura del risultato.** {st["reading"]}\n'
            chunks.append(dict(name=f'passo_{j:02d}',code=st['code']))
        v=n['variant']; s+=f'\n## Variante svolta\n\n**{v["title"]}.** {v["text"]}\n\n```{{r variante}}\n{v["code"]}\n```\n\n{v["reading"]}\n'
        chunks.append(dict(name='variante',code=v['code']))
        s+='\n## Errore da riconoscere\n\n'+n['error']+'\n\n## Risposta alla domanda\n\n'+n['answer']
        s+='\n\n## Riferimento nel corso\n\nQuesto svolgimento sviluppa il laboratorio `'+ident+'` di [GeoStat Lab M10](https://marzione00.github.io/Lab_Geo/#indice). Il [codice originale del laboratorio](https://github.com/marzione00/Lab_Geo/blob/649f7cc577b96bd1044d81e78a2f530813e4f96b/materiali/laboratori/M10/'+ident+'.R) è conservato anche in `R/Originali_corso`. Gli ampliamenti e le varianti sono identificati nella mappa allegata.\n'
        s+='\nDocumentazione dei metodi: [R stats, arima](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/arima.html), [predict.Arima](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.arima.html), [Box.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/box.test.html) e [p.adjust](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html).\n'
        (BASE/f'{ident}.Rmd').write_text(s,encoding='utf-8')
        chunkdir=BASE/'Verifiche'/ident
        chunkdir.mkdir(parents=True,exist_ok=True)
        for c in chunks: (chunkdir/(c['name']+'.R')).write_text(c['code']+'\n',encoding='utf-8')
        rows.append(dict(id=ident,titolo=n['title'],html=f'{ident}.html',rmd=f'{ident}.Rmd',blocchi=len(chunks),sha256_Rmd=hashlib.sha256(s.encode()).hexdigest(),chunks=[c['name'] for c in chunks]))
    (BASE/'Sorgenti_generazione/notebook_contenuti.json').write_text(json.dumps(N,ensure_ascii=False,indent=2),encoding='utf-8')
    (BASE/'Verifiche/piano_esecuzione.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    with (BASE/'INDICE_NOTEBOOK.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['id','titolo','html','rmd','blocchi']);w.writeheader()
        for r in rows:w.writerow({k:r[k] for k in w.fieldnames})
    destinazione = BASE/'Sorgenti_generazione/genera_notebook.py'
    if Path(__file__).resolve() != destinazione.resolve():
        shutil.copy2(__file__,destinazione)
    print(f'Generated {len(rows)} notebooks; {sum(r["blocchi"] for r in rows)} R chunks')
if __name__=='__main__': make()
