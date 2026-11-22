delta <- Z - km$centers[km$cluster, ]
d2_centro <- rowSums(delta^2)
soglia <- quantile(d2_centro, .95)
segnala <- d2_centro > soglia
d[segnala, c("id", v)]
