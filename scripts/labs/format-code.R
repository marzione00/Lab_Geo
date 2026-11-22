suppressPackageStartupMessages(library(jsonlite))
# deparse() may break a line inside [ ], for example `z[,` followed by `1]`. Such breaks, also inside a call
# nested in [ ], are joined back; a joined line longer than the cutoff is wrapped again after a comma of a call
# or a binary +, never inside [ ]; the outermost position that fits is preferred.
# The parsed program is unchanged: each result is compared with the original expression.
rejoin_brackets <- function(text, width = 88L) {
  lines <- strsplit(text, '\n', fixed = TRUE)[[1]]
  scan <- function(s, stack) {
    ch <- strsplit(s, '')[[1]]; quote <- ''; i <- 1L; cuts <- integer(0); depth <- integer(0)
    while (i <= length(ch)) {
      x <- ch[i]
      if (nzchar(quote)) { if (x == '\\') i <- i + 1L else if (x == quote) quote <- '' }
      else if (x %in% c('"', "'", '`')) quote <- x
      else if (x %in% c('(', '[', '{')) stack <- c(stack, x)
      else if (x %in% c(')', ']', '}')) stack <- head(stack, -1L)
      else if (i < length(ch) && ch[i + 1L] == ' ' && !'[' %in% stack &&
        ((x == ',' && length(stack) && tail(stack, 1L) == '(') || (x == '+' && i > 1L && ch[i - 1L] == ' '))) {
        cuts <- c(cuts, i); depth <- c(depth, length(stack))
      }
      i <- i + 1L
    }
    list(stack = stack, cuts = cuts, depth = depth)
  }
  out <- character(0); stack <- character(0); changed <- logical(0)
  for (line in lines) {
    open <- which(stack == '[')
    if (length(out) && length(open) && !any(stack[-seq_len(max(open))] == '{')) {
      out[length(out)] <- paste0(sub('\\s+$', '', out[length(out)]), ' ', sub('^\\s+', '', line))
      changed[length(out)] <- TRUE
    } else {
      out <- c(out, line); changed <- c(changed, FALSE)
    }
    stack <- scan(line, stack)$stack
  }
  stack <- character(0); wrapped <- character(0)
  for (k in seq_along(out)) {
    line <- out[k]; indent <- sub('^(\\s*).*$', '\\1', line)
    while (changed[k] && nchar(line) > width) {
      found <- scan(line, stack); cuts <- found$cuts
      if (!length(cuts)) break
      # Prefer the outermost position that fits, so that each continuation starts a whole argument or layer.
      fit <- cuts < width
      cut <- if (any(fit)) max(cuts[fit & found$depth == min(found$depth[fit])]) else min(cuts)
      if (cut >= nchar(line) - 1L) break
      head_part <- substr(line, 1L, cut)
      wrapped <- c(wrapped, head_part)
      stack <- scan(head_part, stack)$stack
      line <- paste0(indent, '    ', substr(line, cut + 2L, nchar(line)))
    }
    wrapped <- c(wrapped, line)
    stack <- scan(line, stack)$stack
  }
  paste(wrapped, collapse = '\n')
}
same_program <- function(a, b) identical(lapply(parse(text = a, keep.source = FALSE), deparse, width.cutoff = 500L),
  lapply(parse(text = b, keep.source = FALSE), deparse, width.cutoff = 500L))
x<-fromJSON('content/experiments.json',simplifyVector=FALSE);common<-paste(readLines('R/lab-common.R',warn=FALSE),collapse='\n')
for(i in seq_along(x$activities)){
 a<-x$activities[[i]];expr<-parse(text=a$code);code<-paste(vapply(expr,function(e)rejoin_brackets(paste(deparse(e,width.cutoff=88L),collapse='\n')),character(1)),collapse='\n\n');if(!same_program(code,a$code))stop('Formattazione non equivalente: ',a$id);a$code<-code;x$activities[[i]]<-a
 p<-setNames(lapply(a$controls,function(c)c$value),sapply(a$controls,function(c)c$key));param<-paste(deparse(p,width.cutoff=85L),collapse='\n');script<-paste0('# GeoStat Lab · ',a$title,'\n# ',a$goal,'\n# Dati sintetici; parametri e ambiente dichiarati.\n# Dipendenze: install.packages(c("ggplot2", "jsonlite", "svglite"))\n# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0\n# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)\n\n',common,'\n\np <- ',param,'\nset.seed(p$seed)\n\n',code,'\n\nprint(metrics, row.names = FALSE)\nif (!interactive()) grDevices::cairo_pdf("figure_esperimento.pdf", width=9, height=5.5)\nfor (g in plots) print(g)\nif (!interactive()) grDevices::dev.off()\n# write.csv(data, "dati_esperimento.csv", row.names = FALSE)\n# ggsave("figura.svg", plots[[1]], width = 9, height = 5.5)\n');writeLines(script,a$source,useBytes=TRUE)
}
write_json(x,'content/experiments.json',auto_unbox=TRUE,pretty=TRUE,na='null',digits=12);write_json(x$activities,'content/experiments-draft.json',auto_unbox=TRUE,pretty=TRUE,na='null',digits=12)
cat(length(x$activities),'programmi R formattati\n')
