# Totali e copertura per anno.
anno <- format(demo$data, "%Y")
giorni <- table(anno)
totali <- tapply(demo$pioggia,
                 anno, sum)
cbind(giorni = giorni, mm = totali)
