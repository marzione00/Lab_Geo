pa <- subset(f,morfotipo=='Rounded')
diff_coppie <- pa$diametro_tot_um-pa$diametro_int_um
ic_coppie <- unname(t.test(diff_coppie)$conf.int)
