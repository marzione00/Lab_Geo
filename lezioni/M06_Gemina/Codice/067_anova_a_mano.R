y67 <- c(1,3,4,6)
g67 <- factor(c("A","A","B","B"))
m67 <- ave(y67,g67,FUN=mean)
W67 <- sum((y67-m67)^2)  # Entro: 4
B67 <- sum((m67-mean(y67))^2) # 9
F67 <- (B67/1)/(W67/2)
F67
pf(F67,1,2,lower.tail=FALSE)
anova(lm(y67~g67))  # Stesso F
