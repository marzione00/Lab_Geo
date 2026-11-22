# Lo stesso comando produce numeri
# anche fuori dal campo osservato.
fuori <- data.frame(diametro_tot_um = 11)
predict(m0, newdata = fuori,
        interval = "prediction")
range(f$diametro_tot_um)
