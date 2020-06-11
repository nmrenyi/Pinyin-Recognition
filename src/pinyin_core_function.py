import numpy as np
from tqdm import trange
from math import log
import re
class Layer(object):
    '''
    Data structure used for viterbi algorithm.
    Each stage in viterbi algorithm(or the Hidden Markov Model) can be considered as a layer here.
    The most important part for the layer is the connect function, which actually do the viterbi algorithm.
    '''

    words_dict = dict() # storing the probability, characters as the key and probability as the value
    vocabulary_size = 0 # the vocabulary size, used in laplace smoothing

    def __init__(self, word_list):
        '''
        Constructer for layer.
        Each layer represents one pinyin in the input sequence,
        so the layer consists of several nodes, whose number are the number of corresponding characters in terms of the layer's pinyin.
        Each node consists of it's probability till now and the sequence till now.
        '''
        self.width = len(word_list)
        self.word_list = [x for x in word_list]
        self.seq = [x for x in word_list]
        self.prob = [0.0 for i in range(self.width)]
        self.smooth = 1
        self.small_prob_smooth = 1e-50
        for i in range(self.width):
            if word_list[i] in self.words_dict:
                self.prob[i] = log(self.words_dict[word_list[i]] / self.vocabulary_size)
            else:
                self.prob[i] = log(1 / self.vocabulary_size)
                # self.prob[i] = log(self.small_prob_smooth) # small prob smooth

    def getProb(self, j, i, layer):
        '''
        returns the conditional probability of word_list[i] given word_list[j]
        '''
        bigram = layer.word_list[j] + self.word_list[i]
        unigram = layer.word_list[j]
        try:
            prev = self.words_dict[unigram]
        except KeyError:
            prev = 0
        try:
            joint = self.words_dict[bigram]
        except KeyError:
            joint = 0

        # add-k smoothing
        result = (joint + self.smooth) / (prev + self.smooth * self.vocabulary_size)
        
        # # small prob smoothing
        # if joint == 0 or prev == 0:
        #     result = self.small_prob_smooth
        # else:
        #     result = joint / prev
        
        return result

    def connect(self, layer):
        '''
        Actual part of viterbi algorithm.
        Use log probability to avoid underflow.
        '''
        for i in range(self.width):
            max_id = 0
            max_prob = float('-inf')
            for j in range(layer.width):
                now_prob = layer.prob[j] + log(self.getProb(j, i, layer))
                if max_prob < now_prob:
                    max_prob = now_prob
                    max_id = j
            self.prob[i] = max_prob
            self.seq[i] = layer.seq[max_id] + self.seq[i]
        return

    def most_probable(self):
        '''
        Return the most probable sequence given the input pinyin sequence.
        '''
        max_index = self.prob.index(max(self.prob))
        return self.seq[max_index]


def get_pinyin_dict():
    '''
    return a dict with pinyin as the key, list of words corresponding to pinyin as the value
    '''
    pinyin2word_path = '../data/pinyin2word.txt'
    with open(file=pinyin2word_path, mode='r', encoding='gbk') as f:
        word_list = f.readlines()

    word_list = [x.strip().split(' ') for x in word_list]
    return {x[0]:x[1:] for x in word_list}


def viterbi(seq, words_dict, pinyin_dict):
    '''
    Return the characters give the input pinyin.
    '''
    if len(seq) == 1: # one word special case
        try:
            candidate_list = pinyin_dict[seq[0]]
        except KeyError:
            RaiseError(seq[0], seq)
        max_prob = float('-inf')
        max_prob_word = ''
        for i in candidate_list:
            if i in words_dict:
                if words_dict[i] > max_prob:
                    max_prob = words_dict[i]
                    max_prob_word = i
        return max_prob_word

    # goes on with viterbi algorithm iteratively
    try:
        last_layer = Layer(pinyin_dict[seq[0]])
    except KeyError:
        RaiseError(seq[0], seq)
    for pinyin in seq[1:]:
        try:
            current_layer = Layer(pinyin_dict[pinyin])
        except KeyError:
            RaiseError(pinyin, seq)
        current_layer.connect(last_layer)
        last_layer = current_layer
    return current_layer.most_probable()


def RaiseError(unrecognized, seq):
    '''
    Encounters unrecognized pinyin, exit with code 0.
    '''
    print('unrecognized pinyin \'%s\' in %s, program exit with code 0' % (unrecognized, seq))
    exit(0)


def test(path, words_dict, pinyin_dict):
    '''
    Test function for collected samples.
    See more at https://docs.qq.com/doc/DYmZVbURWZWhzc0lH
    Returns the sentence correctness ratio and character correctness ratio.
    '''
    print('testing %s' % path) 
    with open(path, encoding='utf8') as f:  # needs utf8 encoding
        lines = f.readlines()
    lines = [x.strip().lower() for x in lines]
    length = len(lines)
    sentence_correct_ratio = 0
    character_correct_ratio = 0
    all_sentence_count = 0
    all_character_count = 0
    sentence_correct_count = 0
    character_correct_count = 0
    for i in trange(0, length, 2):
        pinyin_input = lines[i]
        ground_truth = lines[i + 1]
        # print('testing ', ground_truth)
        predict_result = viterbi(process_seq(pinyin_input), words_dict, pinyin_dict)
        # print('predicted ', predict_result)
        if ground_truth == predict_result:
            sentence_correct_count += 1
        all_sentence_count += 1
        for j in range(len(ground_truth)):
            if ground_truth[j] == predict_result[j]:
                character_correct_count += 1
        all_character_count += len(ground_truth)
    sentence_correct_ratio = sentence_correct_count / all_sentence_count
    character_correct_ratio = character_correct_count / all_character_count
    print('\nsentence correct ratio = %.4f' % sentence_correct_ratio)
    print('character correct ratio = %.4f' % character_correct_ratio)


def process_seq(line):
    '''
    process the input seq for the viterbi algorithm
    '''
    line_list = re.split(r'[ \t\n\b\r]', line.lower().strip())
    seq = list()
    for x in line_list:
        if len(x) != 0:
            seq.append(x)
    return seq
