from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib

clf, count_vect, tf_transformer = joblib.load('logsAnalysis/response_bayes_classifier.pkl')

def is_response_positive(sentence):
    X_count = count_vect.transform([sentence])
    X_tf = tf_transformer.transform(X_count)
    return clf.predict(X_tf)[0]