# load packages
import requests
from bs4 import BeautifulSoup as bs
import re
import matplotlib.pyplot as plt
# pip install wordcloud
from wordcloud import WordCloud, STOPWORDS
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# empty review list
reviews = []
url = "https://www.imdb.com/title/tt0468569/reviews?ref_=ttexrv_sa_3"

response = requests.get(url)
soup = bs(response.content, "html.parser")
review = soup.find_all("div",attrs = {"class", "text show-more__control"})    
print("review :", review)
for j in range(len(review)):
    reviews.append(review[j].text)

print(reviews)

# storing data
with open("review.txt", "w", encoding="utf8") as output:
    output.write(str(reviews))

# read data
with open("review.txt", "r", encoding="utf8") as inpt:
    reviewStr = inpt.read()

reviewStr = re.sub("[^A-Za-z" "]+", " ", reviewStr).lower()

# tokenize
reviewWords = reviewStr.split(" ")

# tfidf
vectorizer = TfidfVectorizer(reviewWords, use_idf= True, ngram_range=(1,3))
X = vectorizer.fit_transform(reviewWords)

with open(r"C:\Users\Megha\Downloads\Datasets NLP\stopwords_en.txt", "r") as sw:
    stopWords = sw.read()

stopWords = stopWords.split("\n")

stopWords.extend(["dark", "knight",""])

words = [w for w in reviewWords if w not in stopWords]

reviewStr = " ".join(words)

# wordcloud

wordCloud = WordCloud(width=2000, height=2000).generate(reviewStr)
plt.imshow(wordCloud)

# positive wordcloud
with open(r"C:\Users\Megha\Downloads\Datasets NLP\positive-words.txt", "r") as sw:
    positiveWord = sw.read()
    
positiveWord = positiveWord.split("\n")
pWords = [w for w in reviewWords if w in positiveWord]
reviewStr = " ".join(pWords)
wordCloud = WordCloud(width=2000, height=2000).generate(reviewStr)
plt.imshow(wordCloud)

# negative wordcloud

with open(r"C:\Users\Megha\Downloads\Datasets NLP\negative-words.txt", "r") as sw:
    negativeWord = sw.read()

negativeWord = negativeWord.split("\n")
nWords = [w for w in reviewWords if w in negativeWord]
reviewStr = " ".join(nWords)
wordCloud = WordCloud(width=2000, height=2000).generate(reviewStr)
plt.imshow(wordCloud)

# bigram
with open("review.txt", "r", encoding="utf8") as inpt:
    reviewStr = inpt.read()

nltk.download('punkt')
wnl = nltk.WordNetLemmatizer()

t = reviewStr.lower()
t
t = t.replace("'", "")
token = nltk.word_tokenize(t)
text = nltk.Text(t)

textContent = ["".join(re.split("[ .,:;!?''""@#$%^&*()<>{}~\n\t\\\-]", word)) for word in token]
sStopword = set(stopWords)
customWord = ["[", "''", ",","``"]
sStopword = sStopword.union(customWord)

textContent = [word for word in textContent if word not in sStopword]

# Lemmatizer

textContent = [wnl.lemmatize(t) for t in textContent]

nltkToken = nltk.word_tokenize(t)
bigramList = list(nltk.bigrams(textContent))

dictionary = [' '.join(t) for t in bigramList]

# freq in bigram
vectorizer = CountVectorizer(ngram_range=(2,2))
bow = vectorizer.fit_transform(dictionary)
vectorizer.vocabulary_.items()

sumWords = bow.sum(axis = 0)
wordFreq = [(word, sumWords[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
wordFreq = sorted(wordFreq, key= lambda x: x[1], reverse = True)

# wordcloud
data = dict(wordFreq)
wc = WordCloud(width=2000, height=2000, stopwords= sStopword).generate_from_frequencies(data)
plt.imshow(wc)
