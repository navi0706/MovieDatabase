from bs4 import BeautifulSoup
import re
import nltk

# Import NLTK specific modules
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer

# Download necessary packages for sentiment analysis and preprocessing 
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('vader_lexicon')

# Init sia and lemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
sia = SentimentIntensityAnalyzer()

class SentimentAnalysisNLTK:

    def sentiment_analysis_pipeline(self, review):
        # Pipeline for sentiment analysis

        preprocessed_review = self.review_preprocessing(review)
        classified_review = self.classify_sentence(preprocessed_review)
        return classified_review

    
    def review_preprocessing(self, raw_review):
        # Function to convert a raw review to a string of words

        # Remove HTML from words
        review_text = BeautifulSoup(raw_review, "html.parser").get_text() 
        #Remove non-letters        
        letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
        # Convert to lower case, split into individual words
        words = letters_only.lower().split()                             
        # Convert to set, faster than list when iterating
        stops = set(stopwords.words("english"))                  
        # Remove stop words
        meaningful_words = [w for w in words if not w in stops]   
        # Lematize the words
        # Lematization was more accurate then stemming
        lematized_words = [wordnet_lemmatizer.lemmatize(word) for word in meaningful_words]
        #stemmed_words = [ps.stem(word) for word in meaningful_words]
        # Join the words back into one string separated by space
        return( " ".join(lematized_words))

    def classify_sentence(self, preprocessed_sentence):
        """
        The scoring for each sentence is defined by following threshholds:

        positive sentiment: compound score >= 0.05
        neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
        negative sentiment: compound score <= -0.05

        Deducted from https://github.com/cjhutto/vaderSentiment

        """

        scores = sia.polarity_scores(preprocessed_sentence)
        compound_score = scores["compound"]
        if compound_score >= 0.05:
            return "Positive"
        elif compound_score <= 0.05:
            return "Negative"
        else:
            return "Neutral"
