stopifnot(max(time(train)) <
          min(time(test)))
stopifnot(length(intersect(
  time(train),time(test)))==0)
