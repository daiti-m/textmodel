#
# This Julia code is written by Shuichi Miyazawa (miyazawa@ism.ac.jp) @Sokendai.
#
using TextAnalysis
using Languages
using ProgressBars
# using PyCall
# @pyimport nltk.tag as ptag

"""
read documents from a directory with text cleaning process
"""
function read_docs_with_cleaning(dir::String)
    docs = Vector{String}[]
    for f in ProgressBar(readdir(dir))
        s = open(dir*f) do file
            read(file, String)
        end
        clean_s = s |>
            x -> replace(x, "\n"=>" ") |>
            x -> replace(x, "\t"=>" ") |>
            x -> replace(x, "|"=>" ") |>
            x -> replace(x, '\"'=>" ") |>
            x -> replace(x, ">>"=>" ") |>
            x -> replace(x, "\xda"=>" ") |>
            x -> replace(x, "\xd1"=>" ") |>
            x -> replace(x, "\xfe"=>" ") |>
            x -> replace(x, "\xfd"=>" ") |>
            x -> replace(x, "\xe9"=>" ") |>
            x -> replace(x, "\xaa"=>" ") |>
            x -> replace(x, "\xab"=>" ") |>
            x -> replace(x, "\xa7"=>" ") |>
            x -> replace(x, "\xba"=>" ") |>
            x -> replace(x, "\xbb"=>" ") |>
            x -> replace(x, "\xff"=>" ") |>
            x -> replace(x, "\xed"=>" ") |>
            x -> replace(x, "\xc5"=>" ") |>
            x -> replace(x, r"[\s]+"=>" ")
        sentences = sentencize(clean_s) .|> lowercase
        clean_sentences = [sent for sent in sentences if occursin(r"[a-z]", sent)]
        push!(docs, clean_sentences)
    end
    return docs
end

"""
utility
"""
sentencize(text::String) = TextAnalysis.sentence_tokenize(TextAnalysis.Languages.English(), text) .|> String

clean(text::String) = text |>
    remove_case |>
    x -> replace(x, "\n"=>" ") |>
    x -> replace(x, r"[\s]+"=>" ")

function mergewith(combine, d::AbstractDict, others::AbstractDict...)
    for other in others
        for (k,v) in other
            d[k] = haskey(d, k) ? combine(d[k], v) : v
        end
    end
    return d
end

flatten_tokens(doc::Vector{String}) = reduce(vcat, [tokenize(sent) for sent in doc])
flatten_tokens(docs::Vector{Vector{String}}) = reduce(vcat, [flatten_tokens(doc) for doc in docs])

function tokenize_docs(docs::Vector{Vector{String}}, stop_tokens::Vector{String})
    Docs = Vector{Vector{String}}[]
    for doc in ProgressBar(docs)
        Doc = Vector{String}[]
        for sent in doc
            toks = tokenize(sent)
            Sent = String[]
            for tok in toks
                if ~(tok in stop_tokens) & occursin(r"[a-z1-9]", tok)
                    push!(Sent, tok)
                end
            end
            if length(Sent) > 0
                push!(Doc, Sent)
            end
        end
        push!(Docs, Doc)
    end
    return Docs
end

"""
extract infrequent tokens
"""
function infrequent_tokens(text::Union{Vector{String}, Vector{Vector{String}}}, threshold::Int)
    flat_toks = flatten_tokens(text)
    tok_counts = countmap(flat_toks)
    infreq_toks = [k for (k, v) in collect(tok_counts) if v <= threshold]
    return infreq_toks
end

"""
extract unigrams and bigrams
"""
function ext_1_2_grams_from_docs(
  docs::Union{Vector{String}, Vector{Vector{String}}},
  phrases::Union{Nothing, Vector{AbstractDict}}=nothing)
    unigram_arr = Dict{String, Int}[]
    bigram_arr = Dict{Tuple{String, String}, Int}[]
    D = length(docs)
    for doc in docs
        uni, bi = ext_1_2_grams_from_doc(doc, phrases)
        push!(unigram_arr, uni)
        push!(bigram_arr, bi)
    end
    unigrams = reduce((x, y) -> mergewith(+, x, y), unigram_arr)
    bigrams = reduce((x, y) -> mergewith(+, x, y), bigram_arr)
    return unigrams, bigrams
end

function ext_1_2_grams_from_doc(
  text::Union{String, Vector{String}}, phrases::Union{Nothing, Vector{AbstractDict}}=nothing)
    text = typeof(text) == String ? sentencize(text) : text
    unigram_arr = Dict{String, Int}[]
    bigram_arr = Dict{Tuple{String, String}, Int}[]
    for sent in text
        uni, bi = ext_1_2_grams_from_sent(sent, phrases)
        push!(unigram_arr, uni)
        push!(bigram_arr, bi)
    end
    unigrams = reduce((x, y) -> mergewith(+, x, y), unigram_arr)
    bigrams = reduce((x, y) -> mergewith(+, x, y), bigram_arr)
    return unigrams, bigrams
end

function ext_1_2_grams_from_sent(
  sent::String, phrases::Union{Nothing, Vector{AbstractDict}}=nothing)
    if phrases == nothing
        sd = StringDocument(sent)
        unigrams = ngrams(sd, 1)
        bigrams = ngrams(sd, 2)
    else
        toks = tokenize(sent)
        for phr in phrases
            toks = collocate(toks, phr)
        end
        unigrams = TextAnalysis.ngramize(Languages.English(), toks, 1)
        bigrams = TextAnalysis.ngramize(Languages.English(), toks, 2)
    end
    bigrams = split_bigrams(bigrams)
    return unigrams, bigrams
end

split_bigrams(bigrams::Dict{AbstractString, Int}) = Dict(Tuple(String.(split(bi))) => freq for (bi, freq) in collect(bigrams))

"""
Phraser

USAGE:
    include("./phraser.jl");
    dir = <path to directory which contains text files>
    docs = read_docs_with_cleaning(dir);
    phrases = phraser(docs, 3, minfreq=5)
"""
function phraser(docs::Vector{Vector{String}}, niter::Int; threshold::Float64=.5, minfreq::Int=1)
    unigrams, bigrams = ext_1_2_grams_from_docs(docs)
    phrases = compute_phrase(unigrams, bigrams, threshold, minfreq)
    phrases_store = AbstractDict[]
    push!(phrases_store, phrases)
    if niter > 1
        for n in 2:niter
            unigrams, bigrams = ext_1_2_grams_from_docs(docs, phrases_store)
            phrases = compute_phrase(unigrams, bigrams, threshold, minfreq)
            push!(phrases_store, phrases)
        end
    end
    return phrases
end

function compute_phrase(unigram::Dict{String,Int}, bigram::Dict{Tuple{String,String},Int},
  threshold::Float64=0.5, minfreq::Int=1)
    N = sum(unigram.vals)
    phrases = Dict{Tuple{String, String}, Float64}()
    for (bi, freq) in collect(bigram)
        if freq >= minfreq
            v = bi[1]; w = bi[2]
            npmi = (log(N) + log(freq) - log(unigram[v]) - log(unigram[w])) / (log(N) - log(freq))
            if npmi > threshold
                phrases[bi] = npmi
            end
        end
    end
    return phrases
end

function collocate(words::Array{String}, phrases::Dict)
    N = length(words)
    bond = Float64[]
    for n in 1:N-1
        (v, w) = (words[n], words[n+1])
        if haskey(phrases, (v, w))
            push!(bond, phrases[(v, w)])  # NPMI > 0
        else
            push!(bond, 0)
        end
    end
    push!(bond, 0)
    # collocate max-first
    while true
        s = maximum(bond)
        n = argmax(bond)
        if s == 0
            break
        end
        # connect maximum
        bond[n] = -1
        if n > 1
            bond[n-1] = 0
        end
        if n < N-1
            bond[n+1] = 0
        end
    end
    # join words
    return connect(words, bond)
end

function connect(words::Array{String}, bondwords::Array{Float64})
    N = length(words)
    n = 1
    sentence = String[]
    while n <= N
        flag = bondwords[n]
        if flag == 0
            push!(sentence, words[n])
            n += 1
        else
            push!(sentence, words[n]*'_'*words[n+1])
            n += 2
        end
    end
    return sentence
end
