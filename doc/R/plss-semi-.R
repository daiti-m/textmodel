#!/usr/local/bin/Rscript
#
#    plss-semi.R
#    semi-supervised inference of PLSS.
#    $Id: plss-semi-.R,v 1.1 2024/04/17 14:25:27 daichi Exp $
#

suppressMessages(library(quanteda))
suppressMessages(library(cld3))
source ("defs.R")
source ("opts.R")
source ("plss.R")
source ("betaopt.R")
source ("vecload.R")
library(Matrix)

### constants
default.kappa <- 1

### supporting functions

detect.lang <- function (s)
{
    detect_language (s)
}

stopwords.mod <- function (lang)
{
    if (lang == "ja") {
        stopwords (language=lang, source="marimo")
    } else if (lang == "zh") {
        stopwords (language=lang, source="misc")
    } else {
        stopwords (lang)
    }
}

hashlen <- function (hash)
{
    key <- keys(hash)[[1]]
    length (hash[[key]])
}

ifwordvec <- function (wordvec, word, K)
{
    if (has.key (word, wordvec)) {
        wordvec[[word]] / norm (wordvec[[word]])
    } else {
        numeric (K)
    }
}

tovector <- function (s)
{
    as.vector (sapply (strsplit(s, ","), as.numeric))
}

ijv.to.doc <- function (i,j,v)
{
    docs <- split (j, i)
    count <- split (v, i)
    mapply (function (x,y) {
        doc <- rbind(x, y)
        rownames(doc) <- c("id","count")
        doc
    }, docs, count)
}

## main functions

doc.vec <- function (doc, wordvec, features)
{
    index <- doc["id",]
    count <- doc["count",]
    N     <- length (index)
    K     <- length (wordvec[[features[1]]])
    dvec  <- vector ("numeric", K)
    for (n in 1:N)
    {
        v <- index[n]
        c <- count[n]
        vec <- wordvec[[features[v]]]
        dvec <- dvec + c * vec
    }
    dvec / sum(count)
}

dfm.to.data <- function (mat)
{
    data <- as (mat, "dgTMatrix")
    ijv.to.doc (data@i + 1, data@j + 1, data@x)
}

plss.semi <- function (text, posneg, pos.index, neg.index, wordvec,
                       kappa, iters)
{
    # prepare data
    lang <- detect.lang (text[[1]])
    eprintf ('preparing data of language "%s".. ', lang)
    toks <- (text %>% tokens (what="fasterword",
                              remove_punct=T, remove_numbers=T)
                  %>% tokens_remove (stopwords.mod (lang))
                  %>% tokens_select (pattern=keys(wordvec),
                                     selection="keep", valuetype="fixed"))
    N <- length(toks)
    mat <- dfm_sort (dfm (toks))
    data <- dfm.to.data (mat)
    features <- featnames (mat)
    eprintf ('done.\n')
    # prepare unigram
    lv <- log (unigram (data, features))
    # prepare word matrix
    K <- hashlen (wordvec)
    W <- t (rbind (sapply (features, 
                           function (word) ifwordvec (wordvec, word, K))))
    # prepare beta prior
    if (!is.null(posneg)) {
        beta <- posneg.beta (posneg, wordvec)
    } else {
        beta <- rnorm (K) * 1e-2
    }
    # prepare beta
    if (!is.null (pos.index) && !is.null (neg.index)) {
        eprintf ('optimizing beta from examples..\n')
        beta <- betaopt (data, beta, kappa, pos.index, neg.index, lv, W)
        # beta <- betadisc (data, pos.index, neg.index, lv, W)
    }
    beta <- kappa * beta
    eprintf ('length of data = %d\n', N)
    eprintf ('word dimension = %d\n', ncol(W))
    eprintf ('norm of beta   = %.2f\n', norm(beta))
    # compute theta
    irt (data, features, lv, beta, W)
}

usage <- function ()
{
    printf ('usage: %% plss-semi.R OPTIONS file.txt wordvector.{vec/rds}\n')
    printf ('$Id: plss-semi-.R,v 1.1 2024/04/17 14:25:27 daichi Exp $\n')
    printf ('OPTIONS\n')
    printf (' --output=output        theta output\n')
    printf (' --posneg=file          positive/negative seed words\n')
    printf (' --positives=list.pos   list of ids of positive documents\n')
    printf (' --negatives=list.neg   list of ids of negative documents\n')
    printf (' --docsep=regexp        regular expression of document separator (default "")\n')
    printf (' --noheader             word vector has no header (default F)\n')
    printf (' --kappa=kappa          strength of von Mises-Fisher prior (default %g)\n',
            default.kappa)
    printf (' --iters=iters          MCMC iterations (for HMC)\n')
    printf (' --help                 displays this help\n')
    printf ('list.pos,list.neg: ,-separated index, e.g.: "1,4,5"\n')
    quit ()
}

main <- function ()
{
    res <- getopts ( c(
        "posneg",    "q", 2, "character",
        "positives", "p", 2, "character",
        "negatives", "n", 2, "character",
        "kappa",     "k", 2, "double",
        "iters",     "N", 2, "integer",
        "output",    "o", 2, "character",
        "docsep",    "s", 2, "character",
        "noheader",  "H", 0, "logical",
        "help",      "h", 0, "logical"
    ), usage, 2)
    args <- res$args; opts <- res$opts
    
    posneg <- NULL; pos.index <- NULL; neg.index <- NULL;
    docsep <- ""; isheader <- T

    if (!is.na(opts$help)) {
        usage ()
    } else {
        if (is.na(opts$kappa)) {
            opts$kappa <- default.kappa
        }
        if (!is.na(opts$posneg)) {
            posneg <- dicload (opts$posneg)
        }
        if (!is.na(opts$positives)) {
            pos.index <- tovector (opts$positives)
        }
        if (!is.na(opts$negatives)) {
            neg.index <- tovector (opts$negatives)
        }
        if (!is.na(opts$docsep)) {
            docsep <- opts$docsep
        }
        if (!is.na(opts$noheader)) {
            isheader <- F
        }
        text <- textload (args[1], sep=docsep)
        wordvec <- vecload (args[2], isheader=isheader)
    }

    res <- plss.semi (text, posneg, pos.index, neg.index, wordvec,
                      opts$kappa, opts$iters)

    if (!is.na(opts$output)) {
        save.theta (res$theta, opts$output)
        save.phi   (res$phi, opts$output)
    }

}


if (!interactive() & sys.nframe() == 0)
{
    main ()
}

