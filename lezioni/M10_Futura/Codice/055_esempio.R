pred <- predict(fit,n.ahead=36)
p_hat <- as.numeric(pred$pred)
s_hat <- as.numeric(pred$se)
stopifnot(length(p_hat)==36,
          all(s_hat>0))
