# Percentuali: grammi su 100 g
n_mg <- microsonda$MgO / 40.304
n_fe <- microsonda$FeO / 71.844
x_mg <- n_mg / (n_mg + n_fe)
head(x_mg)
# Nel CSV mg_num e una frazione
max(abs(x_mg-microsonda$mg_num))
mg_percento <- 100 * x_mg
