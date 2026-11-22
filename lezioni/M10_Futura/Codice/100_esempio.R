varpred <- previsione_VAR1(
  varfit,ultimo=v[250,],h=10)
stopifnot(all(dim(varpred)==c(10,2)))
head(varpred)
