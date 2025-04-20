#!/usr/local/bin/Rscript
#
#    textload.R
#    $Id: textload.R,v 1.1 2024/04/17 14:25:35 daichi Exp $
#
#    usage: textload (file, sep="^<DOC") -> <DOC .*> separated
#           textload (file, sep="^$")    -> separated by an empty line
#           textload (file, sep="")      -> each line is a separate text
#

textload <- function (file, sep="")
{
    text <- readLines (con = file)
    data <- list()

    if (sep == "")
    {
        for (line in text) {
            if (length(line) > 0) {
                data <- c(data, line)
            }
        }
    } else {
        words <- list()
        for (line in text) {
            if (grepl (sep, line) > 0) {
                if (length(words) > 0) {
                    data <- c(data, paste(words, collapse="\n"))
                }
                words <- list()
            } else {
                words <- c(words, line)
            }
        }
        if (length(words) > 0) {
            data <- c(data, paste(words, collapse="\n"))
        }
    }

    return (as.character(data))
}

if (!interactive() & sys.nframe() == 0)
{
    args <- commandArgs (trailingOnly=T)
    text <- textload (args[1], sep="")
    cat (sprintf('text length = %d\n', length(text)))
    cat ('text[1] = \n')
    print (text[1])
}

