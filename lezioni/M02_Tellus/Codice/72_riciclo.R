m_test <- c(10, 20, 30, 40)
v_corto <- c(2, 4)
m_test / v_corto       # 5, 5, 15, 10
# La funzione controllata si ferma
tryCatch(
  densita_controllata(m_test,v_corto),
  error = function(e)
    message("Errore atteso: ",
            conditionMessage(e)))
