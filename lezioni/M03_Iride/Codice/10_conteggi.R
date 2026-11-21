# Frequenze assolute per morfotipo
n10 <- table(fossili$morfotipo)
n10
sum(n10)  # 160 individui
barplot(n10, ylab = "N. di fossili",
        col = c("#1D7890", "#C57E42"))
