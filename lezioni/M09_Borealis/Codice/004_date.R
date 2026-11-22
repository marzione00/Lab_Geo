# ISO 8601: anno-mese-giorno.
date_es <- as.Date(c("2001-01-01",
                    "2001-02-01",
                    "2001-03-01"))
class(date_es)
diff(date_es)
# Febbraio e gennaio hanno durate diverse.
