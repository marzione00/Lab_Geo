x_u <- c(.2,.4,.5,.6,.8,
         1.2,1.8,2,3,3.8)
h_u <- hist(x_u, breaks = c(0,1,4),
            plot = FALSE)
h_u$counts                  # 5 5
h_u$density                 # .5 1/6
plot(h_u, freq = FALSE)
