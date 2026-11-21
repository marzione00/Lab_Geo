sel <- with(d,x_m>=300 & x_m<=600 &
                  y_m>=180 & y_m<=510)
stopifnot(sum(sel)==132)
mean(d$quota_m[sel])
