z_perm <- z[order(casuali$u[1:n])]
stopifnot(identical(sort(z),
                    sort(z_perm)))
