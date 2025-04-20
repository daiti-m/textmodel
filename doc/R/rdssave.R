#!/usr/local/bin/Rscript

source("vecload.R")

usage <- function ()
{
    cat('usage: % rdssave.R wordvec.txt output.rds\n')
    quit('no')
}

if (!interactive() & sys.nframe() == 0)
{
    args <- commandArgs (trailingOnly=T)
    if (length(args) < 2) {
        usage ()
    } else {
        wordvec <- vecload (args[1], isheader=F)
        cat (sprintf('saving to %s.. ', args[2]))
        saveRDS (wordvec, file = args[2])
        cat ('done.\n')
    }
}
