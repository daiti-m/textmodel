#!/usr/local/bin/Rscript
#
#    opts.R
#    for easy use of getopt(1).
#    $Id: opts.R,v 1.1 2024/04/17 14:25:23 daichi Exp $
#
library("getopt")

getopts <- function (spec, usage, n, ...)
{
    res <- list()
    tokens <- commandArgs (T)
    
    if (length(tokens) < n) {
        usage ()
    }

    if (substr(tokens[1], 1, 1) == "-") {
        res$args <- tail (tokens, n)
        res$opts <- getopt (matrix (spec, byrow=T, ncol=4),
                            head (tokens, -n), ...)
    } else {
        res$args <- head (tokens, n)
        res$opts <- getopt (matrix (spec, byrow=T, ncol=4),
                            tail (tokens, -n), ...)
    }

    # fill unused options by NA
    names <- spec [seq(1,length(spec),by=4)]
    for (name in names) {
        if (is.null(res$opts[[name]])) {
            res$opts[[name]] <- NA
        }
        res$opts$ARGS <- NULL
    }

    res
}

main <- function ()
{
    usage <- function ()
    {
        cat ('usage: % opts.R --iter=iters --output=file train model\n')
        quit ()
    }

    opts <- getopts ( c(
        "alpha",  "a", 1, "double",
        "iters",  "N", 2, "integer",
        "output", "o", 2, "character",
        "help",   "h", 0, "logical"
        ), usage, 2)

    if (!is.na(opts$opts$help)) {
        usage ()
    }

    print (opts$args)
    print (opts$opts)

}


if (!interactive() & sys.nframe() == 0) {
    main ()
}
