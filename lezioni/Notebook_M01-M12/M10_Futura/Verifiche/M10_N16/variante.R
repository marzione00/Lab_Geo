data.frame(tab,rifiuto_grezzo=tab$p_non_corretto<.05,
           rifiuto_Holm=tab$p_Holm_due_confronti<.05)
stopifnot(all(tab$p_Holm_due_confronti>=tab$p_non_corretto))
