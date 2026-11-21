p75 <- c(A_B=.003,A_C=.018,
          A_D=.041,B_C=.2)
# Correggere la famiglia dichiarata
adj75 <- p.adjust(p75,"holm")
data.frame(contrasto=names(p75),
           p=unname(p75),
           Holm=unname(adj75))
