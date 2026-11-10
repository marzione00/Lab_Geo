d <- read.csv('dati/progetti/rock.csv')
stopifnot(nrow(d)==48,
 all(table(d$core_id)==4),
 all(d$permeability_md>0),
 all(d$area_pixels<=256^2))
d$area_pct <- 100*d$area_pixels/256^2
stopifnot(all(tapply(d$permeability_md,
 d$core_id,function(x)length(unique(x)))==1))
head(d)
