# defs.R

printf <- function (...) {
    cat(sprintf(...))
}

eprintf <- function (...) {
    cat(sprintf(...), file=stderr())
    flush.console ()
}

concat <- function (x,y) {
    paste (x, y, sep="")
}
