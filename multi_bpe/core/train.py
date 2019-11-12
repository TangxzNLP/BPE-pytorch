#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 19:11:50 2019

@author: daniel
"""

import _thread
import time
import re, collections
import torch
import os
import sys

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICE"] = "0"
def get_vocab(filename):
    vocab = collections.defaultdict(int)
    with open(filename, 'r', encoding="utf-8") as fhand:
        for line in fhand:
            words = line.strip().split()
            for word in words:
                vocab[' '.join(list(word)) + ' </w>'] += 1
    return vocab

def get_stats(vocab):
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[symbols[i],symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in v_in:
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]
    return v_out

def get_tokens(vocab):
    tokens = collections.defaultdict(int)
    for word, freq in vocab.items():
        word_tokens = word.split()
        for token in word_tokens:
            tokens[token] += freq
    return tokens

def get_tokens_from_vocab(vocab):
    tokens_frequencies = collections.defaultdict(int)
    vocab_tokenization = {}
    for word, freq in vocab.items():
        word_tokens = word.split()
        for token in word_tokens:
            tokens_frequencies[token] += freq
        vocab_tokenization[''.join(word_tokens)] = word_tokens
    return tokens_frequencies, vocab_tokenization

def measure_token_length(token):
    if token[-4:] == '</w>':
        return len(token[:-4]) + 1
    else:
        return len(token)

def tokenize_word(string, sorted_tokens, unknown_token='</u>'):
    
    if string == '':
        return []
    if sorted_tokens == []:
        return [unknown_token]

    string_tokens = []
    for i in range(len(sorted_tokens)):
        token = sorted_tokens[i]
        token_reg = re.escape(token.replace('.', '[.]'))

        matched_positions = [(m.start(0), m.end(0)) for m in re.finditer(token_reg, string)]
        if len(matched_positions) == 0:
            continue
        substring_end_positions = [matched_position[0] for matched_position in matched_positions]

        substring_start_position = 0
        for substring_end_position in substring_end_positions:
            substring = string[substring_start_position:substring_end_position]
            string_tokens += tokenize_word(string=substring, sorted_tokens=sorted_tokens[i+1:], unknown_token=unknown_token)
            string_tokens += [token]
            substring_start_position = substring_end_position + len(token)
        remaining_substring = string[substring_start_position:]
        string_tokens += tokenize_word(string=remaining_substring, sorted_tokens=sorted_tokens[i+1:], unknown_token=unknown_token)
        break
    return string_tokens

import pickle
def sorttoken(modelpath, datapath, index):
    # record time, begin
    starttime = time.time()
    datapath = datapath+'splited_{}.txt'.format(index)
    print(datapath)
    vocab = get_vocab(datapath)
    print('==========')
    print('Tokens Before BPE')
    tokens = get_tokens(vocab)
    print('==========')
    num_merges = 5000
    print("test")
    for i in range(num_merges):
        pairs = get_stats(vocab)
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)
        print('Best pair: {}'.format(best))
        tokens_frequencies, vocab_tokenization = get_tokens_from_vocab(vocab)
    endtime = time.time()
    print("Running time:\t{}".format(endtime-starttime).join("seconds").join('\n'))

    sorted_tokens_tuple = sorted(tokens_frequencies.items(), key=lambda item: (measure_token_length(item[0]), item[1]), reverse=True)
    sorted_tokens = [token for (token, freq) in sorted_tokens_tuple]
    pklpath = modelpath + 'splited_{}.pkl'.format(index)
    print(pklpath)
    F = open(pklpath,'wb')
    pickle.dump(sorted_tokens_tuple, F)
    F.close()

def split_thread(path, num):
    try:
        for i in range(num):
            _thread.start_new_thread(sorttoken, (path, i))
    except:
        print("Error: unable to start thread")

if __name__ == '__main__':
    #sorttoken('pklmodel/', 0)
    modelpath = sys.argv[1]
    datapath = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    steplength = 1
    for k in range(start, end, steplength):
        sorttoken(modelpath, datapath, k)
    #split_thread("../splited/pklmodel/", 20)       