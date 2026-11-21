x_h <- c(1,1,2,3,3,3,4,5,6,6)
b_h <- c(0, 2, 4, 6)
h_h <- hist(x_h, breaks = b_h,
            plot = FALSE)
h_h$counts                  # 3 4 3
sum(h_h$counts)             # 10
