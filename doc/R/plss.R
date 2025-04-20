#!/usr/local/bin/Rscript
#
#    plss.R
#    Probabilistic Latent Semantic Scaling.
#    $Id: plss.R,v 1.2 2024/04/17 14:28:41 daichi Exp $
#
suppressMessages(library(quanteda))
suppressMessages(library(hash))

source("dicload.R")
source("textload.R")
source("vecload.R")
source("vecsave.R")

### main

usage <- function ()
{
    cat ('usage: % plss.R file.txt posneg.txt wordvector.{vec/rds} output\n')
    cat ('$Id: plss.R,v 1.2 2024/04/17 14:28:41 daichi Exp $\n')
    quit ('no')
}

main <- function ()
{
    args <- commandArgs (trailingOnly=T)
    if (length(args) < 3) {
        usage ()
    } else {
        text <- textload (args[1], sep="")
        posneg <- dicload (args[2])
        wordvec <- vecload (args[3], isheader=F)
    }
    
    res <- plss (text, posneg, wordvec)
    
    if (length(args) > 3) {
        save.theta (res$theta, args[4])
        save.phi (res$phi, args[4])
    }
}

posneg.beta <- function (posneg, wordvec)
{
    key <- keys(wordvec)[1]
    K <- length(wordvec[[key]])
    pos <- vector("numeric", K); npos <- 0
    neg <- vector("numeric", K); nneg <- 0
    for (word in posneg[[1]]) # positives
    {
        if (has.key (word, wordvec)) {
            pos <- pos + wordvec[[word]]
            npos <- npos + 1
        }
    }
    for (word in posneg[[2]]) # negatives
    {
        if (has.key (word, wordvec)) {
            neg <- neg + wordvec[[word]]
            nneg <- nneg + 1
        }
    }
    pos <- pos / npos
    neg <- neg / nneg

    (pos - neg) / norm (pos - neg)
}

unigram <- function (data, features)
{
    N <- length (data)
    V <- length (features)
    freq <- vector ("numeric", V)
    
    for (n in 1:N)
    {
        doc <- data[[n]]
        index <- doc["id",]
        count <- doc["count",]
        freq[index] <- freq[index] + count
    }
    freq / sum(freq)
}

plss <- function (text, posneg, wordvec)
{
    eprintf ('preparing data.. ')
    # prepare data
    toks <- (text %>% tokens (what="fasterword")
                  %>% tokens_select (pattern=keys(wordvec),
                                     selection="keep", valuetype="fixed"))
    mat <- dfm_sort (dfm (toks))
    data <- dfm.to.data (mat)
    features <- featnames (mat)
    # prepare unigram
    lp <- log (unigram (data, features))
    # prepare beta
    beta <- posneg.beta (posneg, wordvec)
    # body
    eprintf ('done.\n')
    eprintf ('documents = %d, vocabulary = %d\n', length(data), length(features))
    irt (data, features, lp, beta, wordvec)
}

irt <- function (data, features, lp, beta, wordvec)
{
    # compute theta, phi
    eprintf ('computing theta..\n')

    V <- length(features)
    phi <- vector("numeric", V)
    names(phi) <- features
    
    for (v in 1:V) {
        word <- features[v]
        phi[v] <- wordvec[[word]] %*% beta
    }
    theta <- optimize.theta (data, lp, phi)
    list (phi = phi, theta = theta)
}

optimize.theta <- function (data, lp, phi)
{
    N <- length(data)
    theta <- vector ("numeric", N)
    interval <- 100

    for (n in 1:N)
    {
        doc <- data[[n]]
        theta[n] <- opt.theta (doc, lp, phi)
        if ((n %% interval) == 0) {
            eprintf ('\x1b[Kcomputing %3d/%d..\r', n, N)
        }
        # printf('grad of %d =\n', n)
        # print (docgrad (theta[n], data[[n]], lp, phi, W))
    }
    eprintf ('\x1b[Kcomputing %3d/%d.. done.\n', N, N)

    theta
}

opt.theta <- function (doc, lp, phi)
{
    res <- optim (0, fn = doclik, method = 'L-BFGS',
                  control = list (maxit=100, fnscale=-1),
                  doc = doc , lp = lp, phi = phi)
    # print (res)
    res$par
}

# supporting functions.

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

dfm.to.data <- function (mat)
{
    data <- as (mat, "TsparseMatrix")
    ijv.to.doc (data@i + 1, data@j + 1, data@x)
}

save.theta <- function (theta, output)
{
    file <- concat (output, ".theta")
    vecsave (theta, file)
    eprintf ('theta written to %s.\n', file)
}

save.phi <- function (phi, output)
{
    file <- concat (output, ".phi")
    vecsave (phi, file)
    eprintf ('phi   written to %s.\n', file)
}

doclik <- function (theta, doc, lp, phi)
{
    index <- doc["id",]
    count <- doc["count",]
    Z <- logsumexp (lp + theta * phi)
    lik <- - (theta * theta) / 2
    lik + sum (count * (lp[index] + phi[index] * theta - Z))
}

docgrad <- function (theta, doc, lp, phi)
{
    index <- doc["id",]
    count <- doc["count",]
    lv <- lp + phi * theta
    ev <- sum (phi * (lv - logsumexp(lv)))
    grad <- - theta
    grad + sum (count * phi[index]) - sum (count) * ev
}

logsumexp <- function (x)
{
    y <- max (x)
    y + log (sum(exp(x - y)))
}

norm <- function (x)
{
    sqrt (sum (x * x))
}

dot <- function (x, y)
{
    sum (x * y)
}

if (!interactive() & sys.nframe() == 0)
{
    main ()
}

