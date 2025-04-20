#!/usr/local/bin/Rscript

suppressMessages(library (hash,warn.conflicts=F))
suppressMessages(library (data.table,warn.conflicts=F))
source ("defs.R")

vecload <- function (file, isheader=T)
{
    eprintf('loading wordvectors from %s.. ', file)
    
    if (grepl("\\.rds$", file) > 0)
    {
        wordvec <- readRDS (file)
    }
    else {
        data <- fread (file, header=isheader, quote="") # for word2vec format
        rows <- nrow (data)
        cols <- ncol (data)

        wordvec <- hash (
            t (data[,1]),
            lapply (1:rows, function (i) as.numeric (data[i,2:cols]))
        )
    }
    
    eprintf ('done.\n')
    return (wordvec)
}

if (!interactive() & sys.nframe() == 0)
{
    args <- commandArgs (trailingOnly=T)
    wordvec <- vecload (args[1])
    print (wordvec[["sun"]])
    print (class(wordvec[["sun"]]))
}
