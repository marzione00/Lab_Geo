aspect_deg <-
 (atan2(-gx,-gy)*180/pi)%%360
aspect_deg[g<1e-12] <- NA_real_
