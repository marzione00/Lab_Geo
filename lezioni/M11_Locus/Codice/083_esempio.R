strada <- d$y_m<=250
c(n_strada=sum(strada),
 media_strada=mean(z[strada]),
 media_griglia=mean(z),
 media_altrove=mean(z[!strada]))
