soglie <- c(1e-12,1e-6,.1)
data.frame(soglia=soglie,ammessi=vapply(soglie,function(t) sum(den>t),integer(1)))
