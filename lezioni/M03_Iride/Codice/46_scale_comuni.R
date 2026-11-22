# Stesso asse per entrambi i gruppi
boxplot(diam ~ g_f,
        ylim = range(diam),
        xlab = "Morfotipo",
        ylab = "Diametro [um]")
table(g_f)                  # 80 e 80
