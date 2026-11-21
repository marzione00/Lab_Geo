# Taglio della stessa gerarchia.
ward <- cutree(h, k=3)
table(ward)
plot(h,labels=FALSE,sub="Ward.D2")
rect.hclust(h,k=3,border=1:3)
# L'albero resta lo stesso.
ward4 <- cutree(h,k=4)
table(tre=ward,quattro=ward4)
