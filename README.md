# Twitter-Sentiment-Analysis
Navie Bayes Classification
# PART II: Tweet Sentiment Analysis

Twitter is a popular micro-blogging service where users create status messages (called "tweets"). These tweets
express opinions about different topics.

The purpose of this project is to build an algorithm that can accurately classify Twitter messages as positive ,
neutral or negative. Our hypothesis is that we can obtain high accuracy on classifying sentiment in Twitter messages
using machine learning techniques. I implemented a Naive Bayes classifier and verify its performance on a tweets
dataset. The polarity of the given tweet as ( 0 = negative, 2 = neutral, 4 = positive). By implementing the Naive Bayes
algorithm we can find the sentiment of the tweets as negative, neutral, and positive.

#### Naive Bayes

Naive Bayes is a simple model for classification. It is simple and works well on text
categorization. We adopt multinomial Naive Bayes in our project. It assumes
each feature is conditional independent to other features given the class.
That is, where c is a specific class and t is text we want to classify. P(c) and
P(t) is the prior probabilities of this class and this text. And P(t | c) is the
probability the text appears given this class.

In our case, the value of class c might be POSITIVE or NEGATIVE and t is just a sentence.
The goal is choosing value of c to maximize P(c | t):

Where P(wi | c) is the probability of the i’th feature in text t appears given class c. We need to train parameters of P(c)
and P(wi | c). It is simple for getting these parameters in Naive Bayes model. They are just maximum likelihood
estimation (MLE) of each one.
When making prediction to a new sentence t, we calculate the log likelihood ( log P(c) +∑ilogP(wi|c)) of different
classes, and take the class with highest log likelihood as prediction.
In practice, it needs smoothing to avoid zero probabilities. Otherwise, the likelihood will be 0 if there is an unseen word
when it making prediction.

We simply use add-1 smoothing in our project and it works well.

## Characteristics of Tweets

Twitter messages have many unique attributes, which differentiates our research from previous research:

Length: The maximum length of a Twitter message is 140 characters. From our training set, we calculate that the
average length of a tweet is 14 words or 78 characters. This is very different from the previous sentiment classification

 research that focused on classifying longer bodies of work, such as movie reviews.

 Data availability: Another difference is the magnitude of data availability. With the Twitter API, it is very easy to

 collect millions of tweets for training. In past research, tests only consisted of thousands of training items.

Language model: Twitter users post messages from many different media, including their cell phones. The frequency

 of misspellings and slang in tweets is much higher than in other domains.


Domain: Twitter users post short messages about a variety of topics unlike other sites which are tailored to a specific

 topic. This differs from a large percentage of past research,which focused on specific domains such as movie reviews.

### Results and Discussion

I explored the usage of unigrams, bigrams, unigrams and bigrams, and parts of speech as features.

#### Unigrams

The unigram feature extractor is the simplest way to retrieve features from a tweet. The machine learning
algorithms clearly perform better than our keyword baseline.

#### Bigrams

I used bigrams to help with tweets that contain negated phrases like “\not good" or \not bad."
In our experiments, negation as an explicit feature with unigrams does not improve accuracy, so i was very motivated
to try bigrams.

However, bigrams tend to be very sparse and the overall accuracy drops. Even collapsing the individual words to
equivalence classes does not help.

I used stopwords to get better result. One of the major forms of
pre-processing is to filter out seless data. In natural language
processing, useless words (data), are referred to as stop words.
A stop word is a commonly used word (such as the”, “a”, “an”, “in”) that a search engine has been programmed to
ignore. By doing that it removes most of the punctuations. To get thoose positive and negative emotions I didn’t
remove the “:”, “)”, “-”, “=” and “(” those punctuations.
