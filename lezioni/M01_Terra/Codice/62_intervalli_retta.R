# Intervalli: esempio su demo.
mod <- lm(tmax ~ tmin, data = demo)
nuovo <- data.frame(tmin = 10)
predict(mod, nuovo,
        interval = "confidence")
predict(mod, nuovo,
        interval = "prediction")
