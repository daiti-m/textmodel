#!/usr/local/bin/Rscript
#
#    betahmc.R
#    optimize beta by a discriminative setting for semi-supervised learning.
#    $Id: betaopt.R,v 1.1 2024/04/17 14:25:15 daichi Exp $
#
suppressMessages(library(quanteda))
source ("plss.R")
source ("hermite.R")

betaopt <- function (data, mu, kappa, pos.index, neg.index, lv, W)
{
    K    <- ncol(W)
    beta <- rnorm(K) * 1e-3

    res <- optim (beta, fn = betalik, gr = betagrad,
                  mu, kappa, data[pos.index], data[neg.index], lv, W,
                  method = 'L-BFGS',
                  control = list (maxit=100, fnscale=-1, pgtol=1e-2, trace=1, REPORT=1))
    res$par
}

#
#  likelihoods.
#

betalik <- function (beta, mu, kappa, data.positive, data.negative, lv, W)
{
    N <- length (data.positive)
    M <- length (data.negative)
    phi <- W %*% beta
    
    if (any(is.na(mu))) {
        lik <- 0
    } else {
        lik <- kappa * dot(mu, beta) / norm(beta)
    }

    for (n in 1:N)
    {
        lik <- lik + doclik.positive (data.positive[[n]], lv, phi)
    }

    for (m in 1:M)
    {
        lik <- lik + doclik.negative (data.negative[[m]], lv, phi)
    }

    lik
}

doclik.positive <- function (doc, lv, phi)
{
    disclik <- function (theta, doc, lv, phi)
    {
        doclik (theta, doc, lv, phi) - log (1 + exp (- theta))
    }
    
    H <- 20
    (log.hermite (disclik, H, doc, lv, phi)
     - log.hermite (doclik, H, doc, lv, phi))
}

doclik.negative <- function (doc, lv, phi)
{
    disclik <- function (theta, doc, lv, phi)
    {
        doclik (theta, doc, lv, phi) - log (1 + exp (theta))
    }
    
    H <- 20
    (log.hermite (disclik, H, doc, lv, phi)
     - log.hermite (doclik, H, doc, lv, phi))
}

doclik.marginal <- function (doc, lv, phi)
{
    H <- 20
    log.hermite (doclik, H, doc, lv, phi)
}

#
#  expectation.
#

doc.etheta <- function (doc, lv, phi)
{
    aux <- function (theta, doc, lv, phi, Z)
    {
        theta * exp (doclik(theta, doc, lv, phi) - Z)
    }
    
    H <- 20
    Z <- log.hermite (doclik, H, doc, lv, phi)
    
    # hermite (aux, H, doc, lv, phi, Z)
    hermite.prior (aux, H, doc, lv, phi, Z)
}

#
#  gradients.
#

betagrad <- function (beta, mu, kappa, data.positive, data.negative, lv, W)
{
    N <- length (data.positive)
    M <- length (data.negative)
    K <- length (beta)
    phi <- W %*% beta

    if (any(is.na(mu))) {
        grad <- vector ("numeric", K)
    } else {
        grad <- kappa * (mu - dot(mu, beta) * beta / dot(beta,beta)) / norm(beta)
    }

    for (n in 1:N)
    {
        grad <- grad + betagrad.doc.positive (data.positive[[n]], lv, phi, W)
    }
    
    for (m in 1:M)
    {
        grad <- grad + betagrad.doc.negative (data.negative[[m]], lv, phi, W)
    }

    grad
}

betagrad.doc.positive <- function (doc, lv, phi, W)
{
    disclik <- function (theta, doc, lv, phi)
    {
        doclik (theta, doc, lv, phi) - log (1 + exp (- theta))
    }
    
    docgrad <- function (theta, doc, lv, phi)
    {
        index <- doc["id",]
        count <- doc["count",]
        L     <- sum(count)

        z <- lv + theta * phi
        pv <- exp (z - logsumexp(z))

        as.vector (theta * (colSums(diag(count) %*% W[index,]) - L * (t(pv) %*% W)))
    }

    H <- 20
    K <- ncol (W)

    (log.hermite.gradient (disclik, docgrad, H, K, doc, lv, phi)
     - log.hermite.gradient (doclik, docgrad, H, K, doc, lv, phi))
}

betagrad.doc.negative <- function (doc, lv, phi, W)
{
    disclik <- function (theta, doc, lv, phi)
    {
        doclik (theta, doc, lv, phi) - log (1 + exp (theta))
    }
    
    docgrad <- function (theta, doc, lv, phi)
    {
        index <- doc["id",]
        count <- doc["count",]
        L     <- sum(count)

        z <- lv + theta * phi
        pv <- exp (z - logsumexp(z))

        as.vector (theta * (colSums(diag(count) %*% W[index,]) - L * (t(pv) %*% W)))
    }

    H <- 20
    K <- ncol (W)

    (log.hermite.gradient (disclik, docgrad, H, K, doc, lv, phi)
     - log.hermite.gradient (doclik, docgrad, H, K, doc, lv, phi))
}

betangrad <- function (beta, mu, kappa, data.positive, data.negative, lv, W)
{
    K <- length (beta)
    eps <- 1e-6

    if (is.na(mu)) {
        grad <- vector ("numeric", K)
    } else {
        grad <- kappa * mu
    }

    for (k in 1:K)
    {
        lik <- betalik (beta, mu, kappa, data.positive, data.negative, lv, W)
        beta[k] <- beta[k] + eps
        liknew <- betalik (beta, mu, kappa, data.positive, data.negative, lv, W)
        beta[k] <- beta[k] - eps
        grad[k] <- (liknew - lik) / eps
    }

    grad
}

#
#  supporting functions.
#

plss.semi <- function (text, pos.index, neg.index, wordvec)
{
    cat ('preparing data.. ')
    # prepare data
    toks <- (text %>% tokens (what="fasterword")
                  %>% tokens_remove (stopwords("en"))
                  %>% tokens_select (pattern=keys(wordvec),
                                     selection="keep", valuetype="fixed"))
    N <- length(toks)
    mat <- dfm_sort (dfm (toks))
    data <- lapply (1:N, function (n) as (mat[n,], "dgTMatrix"))
    features <- featnames (mat)
    cat ('done.\n')
    # prepare unigram
    lv <- log (unigram (data, features))
    # prepare word matrix
    W <- t (rbind (sapply (features,
                           function (word) wordvec[[word]] / norm (wordvec[[word]]))))
    # prepare beta
    # beta <- betadisc (data, pos.index, neg.index, lv, W)
    beta <- betaopt (data, pos.index, neg.index, lv, W)
    print (beta)
    quit ()
    phi <- W %*% beta
    for (n in pos.index)
    {
        printf ('E(theta|data[%d]) = %g\n', n, doc.etheta (data[[n]], lv, phi))
    }
}

tovector <- function (s)
{
    sapply (strsplit(s, ","), as.numeric)
}

usage <- function ()
{
    cat ('usage: % betahmc.R file.txt list.pos list.neg wordvector.rds [output]\n')
    cat ('list.pos,list.neg: ,-separated index, eg: "1,4,5"\n')
    cat ('$Id: betaopt.R,v 1.1 2024/04/17 14:25:15 daichi Exp $\n')
    quit ('no')
}

main <- function ()
{
    args <- commandArgs (trailingOnly=T)
    if (length(args) < 4) {
        usage ()
    } else {
        text <- textload (args[1], sep="^<DOC")
        pos.index <- tovector (args[2])
        neg.index <- tovector (args[3])
        wordvec   <- vecload (args[4])
    }
    
    res <- plss.semi (text, pos.index, neg.index, wordvec)
    
    if (length(args) > 4) {
        save.theta (res$theta, args[5])
    }
}


if (!interactive() & sys.nframe() == 0)
{
    main ()
}
