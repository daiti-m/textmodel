#!/usr/local/bin/Rscript
#
#    dicload.R
#    dictionary load routines from a text file.
#    $Id: dicload.R,v 1.1 2024/04/17 14:25:19 daichi Exp $
#
suppressMessages (require (quanteda,warn.conflicts=F))

is.valid <- function (xx)
{
    yy <- unlist (xx)
    return (yy[yy != ""])
}

dicload <- function (file)
{
    data <- readLines (con = file)
    keys <- list ()
    content <- list ()

    for (line in data)
    {
        if (grepl("^#", line) > 0) {
            next
        }
        fields = unlist(strsplit (line, "\t"))
        if (length(fields) == 2)
        {
            key = fields[1]
            words = is.valid (strsplit (fields[2], "[ ]+"))
            keys <- c(keys, key)
            content <- c(content, list (words))
        }
    }
    names (content) <- keys

    return (dictionary (content))
}

if (!interactive() & sys.nframe() == 0)
{
    args <- commandArgs (trailingOnly=T)
    dict <- dicload (args[1])
    print (dict[1])
    print (dict[2])
}


