trend <- lm(concentrazione~x_m+y_m,
            data=d)
e_trend <- residuals(trend)
c(dati=moran_I(z,A),
  residui=moran_I(e_trend,A))
