d <- read.csv('dati/progetti/foraminiferi.csv')
d$date <- as.Date(d$date)
stopifnot(nrow(d)==36,
 !anyDuplicated(paste(d$trap_year,d$cup_id)),
 all(d$depth_m==170),
 all(d$diam_min_um<=d$diam_mean_um),
 all(d$diam_mean_um<=d$diam_max_um))
head(d)
