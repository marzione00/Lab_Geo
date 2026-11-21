p_ord <- provini[c(3, 1, 2), ]
p_ord$ordine <- seq_len(nrow(p_ord))
j_ord <- merge(p_ord, siti,
  by = "sito", all.x = TRUE,
  sort = FALSE)
j_ord <- j_ord[order(j_ord$ordine), ]
stopifnot(identical(j_ord$id,
                    p_ord$id))
