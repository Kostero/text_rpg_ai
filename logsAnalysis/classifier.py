from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import os

path = os.path.join(os.path.dirname(__file__), 'response_bayes_classifier.pkl')
clf, count_vect, tf_transformer = joblib.load(path)

def is_response_positive(sentence):
    X_count = count_vect.transform([sentence])
    X_tf = tf_transformer.transform(X_count)
    return clf.predict(X_tf)[0]