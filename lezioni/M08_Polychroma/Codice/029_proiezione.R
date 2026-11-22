z_hat <- t_es * v_es
res_es <- z_es - z_hat
z_hat
# Proiezione e residuo sono ortogonali.
sum(res_es * v_es)
