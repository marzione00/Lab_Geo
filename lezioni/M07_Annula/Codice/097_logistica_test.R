# Risposta: TRUE per i fossili Spiky.
g_train <- glm(
  I(morfotipo == "Spiky") ~
    diametro_tot_um +
    rapporto_int_tot,
  data = training,
  family = binomial())
p_test <- predict(g_train,
  newdata = test, type = "response")
y_test <- as.integer(
  test$morfotipo == "Spiky")
mean((p_test - y_test)^2) # Brier.
mean((p_test >= 0.5) == y_test)
