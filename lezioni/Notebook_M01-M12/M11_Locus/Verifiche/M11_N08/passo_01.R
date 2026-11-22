d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 ovest <- d$x_m<1000;est <- !ovest
 stopifnot(!any(ovest&est),all(ovest|est),sum(ovest)==32L,sum(est)==32L)
 aree <- ifelse(ovest,"Ovest","Est")
 table(aree)
 stopifnot(identical(aree,d$area))
