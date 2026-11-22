a16 <- lab_condizionamento(
  prior=.4, pa=.8, pb=.2)
b16 <- lab_condizionamento(
  prior=.1, pa=.8, pb=.2)
a16$indicatori
b16$indicatori
# Uguale probabilita' nei due gruppi
c16 <- lab_condizionamento(
  prior=.4, pa=.2, pb=.2)
c16$indicatori
