y <- ts(d$co2_ppm,
        start = c(1985, 1), frequency = 12)
start(y)
end(y)
frequency(y)
head(time(y))
# Il tempo interno e' espresso in anni.
