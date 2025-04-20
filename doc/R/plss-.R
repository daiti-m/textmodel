#!/usr/local/bin/Rscript
#
#    plss.R
#    Probabilistic Latent Semantic Scaling.
#    $Id: plss-.R,v 1.1 2024/04/17 14:25:25 daichi Exp $
#
suppressMessages(library(quanteda))
suppressMessages(library(hash))

source("dicload.R")
source("textload.R")
source("vecload.R")
source("vecsave.R")

### body

usage <- function ()
{
    cat ('usage: % plss.R file.txt posneg.txt wordvector.rds [output]\n')
    cat ('$Id: plss-.R,v 1.1 2024/04/17 14:25:25 daichi Exp $\n')
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
        wordvec <- vecload (args[3])
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
    freq <- colSums(data)
    freq / sum(freq)
}

plss <- function (text, posneg, wordvec)
{
    eprintf ('preparing data.. ')
    # prepare data
    toks <- (text %>% tokens (what="fasterword")
                  %>% tokens_select (pattern=keys(wordvec),
                                     selection="keep", valuetype="fixed"))
    N <- length(toks)
    data <- dfm_sort (dfm (toks))
    features <- featnames (data)
    # prepare unigram
    lp <- log (unigram (data, features))
    # prepare beta
    beta <- posneg.beta (posneg, wordvec)
    # body
    eprintf ('done.\n')
    eprintf ('documents = %d, vocabulary = %d\n', dim(data)[1], dim(data)[2])
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
    N <- dim(data)[1]
    theta <- vector ("numeric", N)
    interval <- 10

    for (n in 1:N)
    {
        doc <- data[n,]
        theta[n] <- opt.theta (data[n,], lp, phi)
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
    eprintf ('phi written to %s.\n', file)
}

doclik <- function (theta, doc, lp, phi)
{
    Z <- logsumexp (lp + theta * phi)
    lik <- - (theta * theta) / 2
    res <- dfm_weight (doc, weights = lp + phi * theta - Z)
    lik + sum (res@x)
}

docgrad <- function (theta, doc, lp, phi)
{
    lv <- lp + phi * theta
    ev <- sum (phi * (lv - logsumexp(lv)))
    res <- dfm_weight (doc, weights = phi)
    grad <- - theta
    grad + sum (res@x) - sum (doc@x) * ev
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

