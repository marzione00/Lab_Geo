# Sei medie locali indipendenti
quantile(bs81, c(.025, .975),
         type = 7)
# Student assume normalita delle
# medie di stazione, oltre a iid.
t.test(stazioni$densita)$conf.int
length(stazioni$densita)  # 6
