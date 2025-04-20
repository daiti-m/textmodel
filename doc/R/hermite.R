#!/usr/local/bin/Rscript

suppressMessages(library(gaussquad))

hermgauss <- function (H)
{
    table <- hermite.h.quadrature.rules(H)[[H]]
    list ( x = rev(table$x), w = rev(table$w) )
}

# default Hermite.

hermite.prior <- function (fun, H=20, ...)
{
    z <- 0
    table <- hermgauss (H)
    w <- table$w; x <- table$x

    for (k in 1:H)
    {
        z <- z + w[k] * fun (sqrt(2) * x[k], ...)
    }

    z / sqrt(pi)
}

log.hermite.prior <- function (logfun, H=20, ...)
{
    z <- vector ("numeric", H)
    table <- hermgauss (H)
    w <- table$w; x <- table$x

    for (k in 1:H)
    {
        z[k] <- log(w[k]) + logfun (sqrt(2) * x[k], ...)
    }

    logsumexp (z) - log (pi) / 2
}

# adaptive Hermite.

hermite <- function (f, H=20, ...)
{
    z <- 0
    table <- hermgauss (H)
    w <- table$w; x <- table$x
    
    m <- infer.x (f, ...)
    s <- infer.s (f, m, ...)

    for (k in 1:H)
    {
        yk <- m + sqrt(2) * s * x[k]
        z <- z + w[k] * f (yk, ...) * exp (((yk - m)^2 / (s^2) - yk^2) / 2)
    }
    
    z * s / sqrt(pi)
}

log.hermite <- function (logf, H=20, ...)
{
    table <- attr(log.hermite, "table")
    if (is.null(table)) {
        table <- hermgauss (H)
        attr(log.hermite, "table") <<- table        
    } else {
        if (H != length(table$x)) {
            table <- hermgauss (H)
            attr(log.hermite, "table") <<- table
        }
    }
    z <- vector ("numeric", H)
    w <- table$w; x <- table$x

    m <- infer.x (logf, ...)
    s <- infer.s (logf, m, ...)

    for (k in 1:H)
    {
        yk <- m + sqrt(2) * s * x[k]
        z[k] <- log (w[k]) + logf (yk, ...) + ((yk - m)^2 / (s^2) - yk^2) / 2
    }

    logsumexp (z) + log (s) - log (pi) / 2
}

log.hermite.positive <- function (logf, H=20, ...)
{
    table <- attr(log.hermite.positive, "table")
    if (is.null(table)) {
        table <- hermgauss (H)
        attr(log.hermite.positive, "table") <<- table        
    } else {
        if (H != length(table$x)) {
            table <- hermgauss (H)
            attr(log.hermite.positive, "table") <<- table
        }
    }
    z <- list ()
    w <- table$w; x <- table$x
    
    m <- infer.x (logf, ...)
    s <- infer.s (logf, m, ...)

    for (k in 1:H)
    {
        yk <- m + sqrt(2) * s * x[k]
        if (yk > 0) {
            z <- c(z, log (w[k]) + logf (yk, ...) + ((yk - m)^2 / (s^2) - yk^2) / 2)
        }
    }

    logsumexp (as.numeric(z)) + log (s) - log (pi) / 2
}

log.hermite.negative <- function (logf, H=20, ...)
{
    table <- attr(log.hermite.negative, "table")
    if (is.null(table)) {
        table <- hermgauss (H)
        attr(log.hermite.negative, "table") <<- table        
    } else {
        if (H != length(table$x)) {
            table <- hermgauss (H)
            attr(log.hermite.negative, "table") <<- table
        }
    }
    z <- list ()
    w <- table$w; x <- table$x
    
    m <- infer.x (logf, ...)
    s <- infer.s (logf, m, ...)

    for (k in 1:H)
    {
        yk <- m + sqrt(2) * s * x[k]
        if (yk < 0) {
            z <- c(z, log (w[k]) + logf (yk, ...) + ((yk - m)^2 / (s^2) - yk^2) / 2)
        }
    }

    logsumexp (as.numeric(z)) + log (s) - log (pi) / 2
}

#
#  gradients.
#

log.hermite.gradient <- function (logf, gradf, H=20, K, ...)
{
    table <- attr(log.hermite.gradient, "table")
    if (is.null(table)) {
        table <- hermgauss (H)
        attr(log.hermite.gradient, "table") <<- table        
    } else {
        if (H != length(table$x)) {
            table <- hermgauss (H)
            attr(log.hermite.gradient, "table") <<- table
        }
    }
    z <- vector ("numeric", H)
    g <- matrix (0, H, K)
    w <- table$w; x <- table$x

    m <- infer.x (logf, ...)
    s <- infer.s (logf, m, ...)

    for (k in 1:H)
    {
        yk <- m + sqrt(2) * s * x[k]
        z[k] <- log (w[k]) + logf (yk, ...) + ((yk - m)^2 / (s^2) - yk^2) / 2
        g[k,] <- gradf (yk, ...)
    }
    Z <- logsumexp (z)

    as.vector (exp (z - Z) %*% g)
}

 

#
#  utility functions.
#

infer.x <- function (likfun, ...)
{
    res <- optimize (likfun, interval = c(-10,10), maximum = TRUE, ...)
    res$maximum
}

infer.s <- function (f, x, ...) # estimate sd
{
    sqrt (- 1 / twodiff (f, x, ...))
}

twodiff <- function (f, x, ...)
{
    h <- 1e-4
    (f (x + h, ...) + f (x - h, ...) - 2 * f(x, ...)) / (h * h)
}

logsumexp <- function (x)
{
    y <- max (x)
    y + log (sum(exp(x - y)))
}

#
#  main (for validation)
#

main <- function ()
{
    # example setting

    likfun <- function (x, m, s)
    {
        exp (loglik (x, m, s))
    }

    loglik <- function (x, m, s)
    {
        # likelihood = log N(x|m,s)
        - (x - m)^2 / (2 * s) - log (2 * pi * s) / 2
    }

    analytical <- function (m, s)
    {
        exp (- m^2 / (2 * (s + 1))) / sqrt (2 * pi * (s + 1))
    }

    log.analytical <- function (m, s)
    {
        - m^2 / (2 * (s + 1)) - log (2 * pi * (s + 1)) / 2
    }

    analytical.positive <- function (m, s)
    {
        pnorm (0, mean = m, sd = sqrt(s), lower.tail = F)
    }

    usage <- function ()
    {
        cat ('usage: % hermite.R mu sigma2 [H]\n')
        quit ()
    }
    
    args = commandArgs (trailingOnly=T)
    
    if (length(args) < 2) {
        usage ()
    } else {
        m <- as.numeric (args[1])
        s <- as.numeric (args[2])
        H <- 20
    }

    logp <- log.hermite (loglik, H=10, m=m, s=s)
    logp.negative <- log.hermite.negative (loglik, H=20, m=m, s=s)

    printf('analytical       = % .10f\n', analytical (m, s))
    printf('adaptive hermite = % .10f\n', hermite (likfun, H=10, m=m, s=s))
    printf('prior hermite    = % .10f\n', hermite.prior (likfun, H=10, m=m, s=s))
    printf('log adaptive     = % .10f\n', exp (logp))
#    printf('* positive   = % .10f\n', exp (logp.negative - logp))
#    printf('* analytical = % .10f\n', 1 - analytical.positive (m, s))

}

if (!interactive() & sys.nframe() == 0)
{
    main ()
}
