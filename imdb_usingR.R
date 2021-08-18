# load packages
install.packages("rvest")
library(rvest)
install.packages("XML")
library(XML)
install.packages("magrittr")
library(magrittr)
install.packages("tm")
library(tm)
install.packages("wordcloud")
library(wordcloud)
Sys.setenv(JAVA_HOME="")
install.packages("RWeka")
library(RWeka)

# load imdb url

imdbUrl <- "https://www.imdb.com/title/tt7767422/reviews?ref_=tt_urv"
imdbReview <- NULL
html <- read_html(imdbUrl)
imdbReview <- html %>% html_nodes(".show-more__control") %>% html_text()
imdbReview[1]

write.table(imdbReview, "IMDBReview.txt")
getwd()

str(imdbReview)
length(imdbReview)

# corpus
corpusData <- Corpus(VectorSource(imdbReview))
inspect(corpusData[1])

corpusData <- tm_map(corpusData, function(corpusData) iconv(enc2utf8(corpusData), sub = "byte"))

# data cleaning
data <- tm_map(corpusData, tolower)
inspect(data[1])

data <- tm_map(data, removePunctuation)

data <- tm_map(data, removeNumbers)
inspect(data[1])

# remove stopwords
data <- tm_map(data, removeWords, stopwords(kind = "en"))
inspect(data[1])

data <- tm_map(data, stripWhitespace)
inspect(data[1])

# TDM 
tdm <- TermDocumentMatrix(data)
tdm
nonSparseData <- removeSparseTerms(tdm, 0.90)
nonSparseData

tdm <- as.matrix(tdm)
dim(tdm)

wordSum <- rowSums(tdm)
wordSum
max(wordSum)

wordSubset <- subset(wordSum, wordSum > 20)
wordSubset

# plot
barplot(wordSubset, las=2, col = rainbow(30))

# remove useless word 

data <- tm_map(data, stripWhitespace)
tdm <- TermDocumentMatrix(data)
tdm <- as.matrix(tdm)
wordSum <- rowSums(tdm)
wordSubset <- subset(wordSum, wordSum > 10)
barplot(wordSubset, las=2, col = rainbow(30))

# remove useless word 

data <- tm_map(data, stripWhitespace)
tdm <- TermDocumentMatrix(data)
tdm <- as.matrix(tdm)
wordSum <- rowSums(tdm)
wordSubset <- subset(wordSum, wordSum > 5)
barplot(wordSubset, las=2, col = rainbow(30))

# remove useless word 

data <- tm_map(data, stripWhitespace)
tdm <- TermDocumentMatrix(data)
tdm <- as.matrix(tdm)
wordSum <- rowSums(tdm)
wordSubset <- subset(wordSum, wordSum > 5)
barplot(wordSubset, las=2, col = rainbow(30))

# word cloud
windows()
wordcloud(words = names(wordSubset), freq = wordSubset, random.order = F, colors = rainbow(30))

# Bigram
bitoken <- NGramTokenizer(data, Weka_control(min = 2, max = 2))
biWord <- data.frame(table(bitoken))
sortBiword <- biWord[order(biWord$Freq, decreasing = TRUE),]
windows()
wordcloud(sortBiword$bitoken, sortBiword$Freq, colors = rainbow(30))

# sentiment analysis
# load data
positiveWords <- readLines(file.choose())
negativeWords <- readLines(file.choose())
stopwords <- readLines(file.choose())

positiveMatch <- match(names(wordSum), positiveWords)
positiveMatch
positiveMatch <- !is.na(positiveMatch)
freq <- wordSum[positiveMatch]
freq
name <- names(freq)
wordcloud(name, freq = freq, colors = rainbow(30))

negativeMatch <- match(names(wordSum), negativeWords)
negativeMatch
negativeMatch <- !is.na(negativeMatch)
freq <- wordSum[negativeMatch]
freq
name <- names(freq)
wordcloud(name, freq = freq, colors = rainbow(30))


