# h_h viene dalla slide 32
amp_h <- diff(h_h$breaks)
data.frame(n = h_h$counts,
           densita = h_h$density)
quote_h <- h_h$density * amp_h
quote_h                     # .3 .4 .3
sum(quote_h)                # 1
