#!/usr/local/bin/Rscript

vecsave <- function (xx, output)
{
    N <- length (xx)
    fh <- file (output, "w")
    if (!is.null(names(xx))) {
        labels <- names(xx)
    } else if (!is.null(dimnames(xx))) {
        labels <- dimnames(xx)[[1]]
    } else {
        labels <- NULL
    }
    
    if (is.null(labels)) {
        for (n in 1:N)
        {
            cat (sprintf('% .6f\n', xx[[n]]), file = fh)
        }
    } else {
        for (n in 1:N)
        {
            cat (sprintf('%-12s\t% .6f\n', labels[[n]], xx[[n]]), file = fh)
        }
    }
    close (fh)
}

main <- function ()
{
    xx <- c(1,2,3,4,5)
    names(xx) <- c('this', 'is', 'a', 'pencil', '.')
    args <- commandArgs (trailingOnly=T)
    output <- args[1]

    vecsave (xx, output)
    
}


if (!interactive() && sys.nframe() == 0)
{
    main ()
}

