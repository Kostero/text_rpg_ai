import numpy as np
import tensorflow as tf
import nltk

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=1.0/np.sqrt(sum(shape)))
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0., shape=shape)
    return tf.Variable(initial)


class AttentionFFLM(object):
    def __init__(self, vocab_size, embed_size, hid_units, activation=tf.nn.relu):
        self.x = tf.placeholder(tf.int32, shape=[None, None])
        self.y = tf.placeholder(tf.int32, shape=[None])

        self.embedding = weight_variable(shape=(vocab_size, embed_size))

        self.get_them = tf.nn.embedding_lookup(self.embedding, self.x)
        self.cut = tf.shape(self.x)[1]

        ##attention stuff
        self.W_ph = weight_variable([embed_size, embed_size])
        self.b_ph = bias_variable([1, embed_size])

        self.h = activation( tf.matmul(tf.reshape(self.get_them, [-1, embed_size]), self.W_ph) + self.b_ph )
        self.h_ = tf.reshape( tf.reshape(self.h, tf.pack([-1, self.cut*embed_size])), tf.shape(self.h))

        self.W_ha = weight_variable([embed_size, 1])
        self.b_ha =bias_variable([1])

        self.att_logits = tf.reshape( tf.tanh(tf.matmul(self.h_, self.W_ha) + self.b_ha), tf.pack([-1, self.cut]) )
        self.alpha = tf.reshape(tf.nn.softmax(self.att_logits), [1,-1])


word2number = dict()
number2word = dict()

with open("data/attention_model/words.txt", 'rb') as f:
        number = 0
        for line in f:
            word = line.strip()

            word2number[word] = number
            number2word[number] = word

            number += 1


net = AttentionFFLM(vocab_size=len(word2number), embed_size=100, hid_units=200)

session = tf.Session()
saver = tf.train.Saver()


saver.restore(session, "./data/attention_model/rpg_model.ckpt")






def compute_weights(sentence):
    words = nltk.word_tokenize(sentence)
    inp = [word2number[w] if w in word2number else word2number["<UNK>"] for w in words]
    alpha = session.run(net.alpha, feed_dict={net.x:[inp]})[0]
    return zip(words, alpha * len(alpha))


