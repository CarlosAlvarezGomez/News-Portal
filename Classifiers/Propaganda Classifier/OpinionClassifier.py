# Imports necessary libraries
import torch
import os
from typing import List, Tuple
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
from nltk import word_tokenize, sent_tokenize
from nltk.classify import MaxentClassifier
import nltk
nltk.download('averaged_perceptron_tagger')

# Credits: Tokenizer code was mostly made by Professor Claire Cardie from Cornell University
train_path = os.path.join(os.getcwd(), "Data", "train")
dev_path = os.path.join(os.getcwd(), "Data", "dev")
test_path = os.path.join(os.getcwd(), "Data", "test")
 
def read_txt(fname):
  with open(fname, encoding='utf-8') as open_article:
    lines = open_article.read()
  return lines

def read_labels(labels : str) -> List[Tuple[int, int]]:
  "processing of labels file"
  labels = labels.split("\n")[:-1]
  labels = [tuple(map(int, l.split("\t")[-2:])) for l in labels]
  return labels

def sort_and_merge_labels(labels : List[Tuple[int, int]]) -> List[Tuple[int, int]]:
  "sort labels, necessary for later splitting"
  if len(labels) == 0:
    return labels
  labels = list(sorted(labels, key = lambda t: t[0]))
  # merge
  curr = labels[0]
  merged = []
  for l in labels[1:]:
      # if distinct, add
      if l[0] > curr[1]:
        merged.append(curr)
        curr = l
      # else merge
      else:
        curr = (curr[0], max(curr[1], l[1]))
  merged.append(curr)
  return merged

def split_with_labels(labels : List[Tuple[int, int]], article : str) -> Tuple[List[str], List[int]]:
  "split text into segments based upon labels"
  if len(labels) == 0:
    return [article], [0]
  segments = []
  binary_class = []
  start = 0
  for l_start, l_end in labels:
    std_seg = article[start:l_start]
    prop_seg = article[l_start:l_end]
    segments.append(std_seg)
    binary_class.append(0)
    segments.append(prop_seg)
    binary_class.append(1)
    start = l_end
  last_seg = article[start:]
  segments.append(last_seg)
  binary_class.append(0)
  return segments, binary_class

def remove_newline_fix_punc_seg(segments):
  " preprocessing necessry for tokenization to be consistent"
  segments = [s.replace("\n", " ").replace(".", " .") for s in segments]
  return segments

def remove_newline_fix_punc_art(article):
  " preprocessing necessry for tokenization to be consistent"
  article = article.replace("\n", " ").replace(".", " .")
  return article

def get_toks(input):
  output = []
  for toks in [list(map(str.lower, word_tokenize(sent))) for sent in sent_tokenize(input)]:
    output += toks
  return output

# This is the function you may need to call
def tokenize_article(article_file):
  "calls all functions above and perform sanity checks"
  article = read_txt(article_file)
  article = remove_newline_fix_punc_art(article)
  art_toks = get_toks(article)
  return art_toks

# This is the function you may need to call
def master_tokenizer(article_file, labels_file):
  "calls all functions above and perform sanity checks"
	# read and get labels
  article = read_txt(article_file)
  labels = read_txt(labels_file)
  labels = read_labels(labels)
  labels = sort_and_merge_labels(labels)
  segments, binary_class = split_with_labels(labels, article)
  article = remove_newline_fix_punc_art(article)
  segments = remove_newline_fix_punc_seg(segments)
  # sanity check
  reconstructed = ""
  for seg, lab in zip(segments, binary_class):
    reconstructed += seg
  assert reconstructed == article
	# tokenize
  seg_toks = []
  new_labels = []
  for seg, label in zip(segments, binary_class):
    new_toks = get_toks(seg)
    seg_toks += new_toks
    new_labels += [label for _ in range(len(new_toks))]
	# sanity check
  art_toks = get_toks(article)
  sanity = True
  if len(art_toks) != len(seg_toks):
    sanity = False
  for i, (at, st, lab) in enumerate(zip(art_toks, seg_toks, new_labels)):
    if at != st:
      sanity = False
      break
  return seg_toks, new_labels, sanity

# list -- file names of each article, sorted alphabetically
train_articles_list = []
dev_articles_list = []

# list -- file names of each corresponding labels file, sorted alphabetically
train_labels_list = []
dev_labels_list = []

for file_name in os.listdir(train_path):
  if file_name[-11:] == '.labels.tsv':
    train_labels_list.append(file_name)
  elif file_name != 'test.task-SLC.labels' and file_name != '.article999001621.labels.tsv.swo':
    train_articles_list.append(file_name)

for file_name in os.listdir(dev_path):
  if file_name[-11:] == '.labels.tsv':
    dev_labels_list.append(file_name)
  else:
    dev_articles_list.append(file_name)

train_articles_list = sorted(train_articles_list)
train_labels_list = sorted(train_labels_list)
dev_articles_list = sorted(dev_articles_list)
dev_labels_list = sorted(dev_labels_list)

# list of lists -- each list is a tokenized article
tokenized_train_articles = []
# list of lists -- each list is the labels corresponding to the article 
tokenized_train_labels = []

# Creates a two lists: one containing each article as a list of strings, and one
# containing the corresponding labels as a list of ints
for i in range(len(train_articles_list)):
  article_file = os.path.join(train_path, train_articles_list[i])
  labels_file = os.path.join(train_path, train_labels_list[i])
  art, lab, _ = master_tokenizer(article_file, labels_file)
  tokenized_train_articles.append(art)
  tokenized_train_labels.append(lab)

# list of lists -- each list is a tokenized article
tokenized_dev_articles = []
# list of lists -- each list is the labels corresponding to the article 
tokenized_dev_labels = []

# Creates a two lists: one containing each article as a list of strings, and one
# containing the corresponding labels as a list of ints
for i in range(len(dev_articles_list)):
  article_file = os.path.join(dev_path, dev_articles_list[i])
  labels_file = os.path.join(dev_path, dev_labels_list[i])
  art, lab, _ = master_tokenizer(article_file, labels_file)
  tokenized_dev_articles.append(art)
  tokenized_dev_labels.append(lab)

# Inputs: an article (list of strings), a list of all possible states ([0, 1]),
# a transition functions, a start function, and an output funtion
def viterbi(sent, states, next, start, output):
  m = len(states)
  s = len(sent)
  (rows, cols) = (m, s)

  probabilities = [[0.0 for i in range(cols)] for j in range(rows)] 
  previousStates = [["" for i in range(cols)] for j in range(rows)] 


  # Goes through each state in the model, calculates the probability of starting
  # there, and stores the results in the first column of the array
  for index in range(m):
    curState = states[index]
    probabilities[index][0] = math.log(start(curState)) + math.log(output(curState, sent, 0))

  # Goes through each of the remaining words in the article
  for curWordIdx in range(1, s):
    curWord = sent[curWordIdx]

    # Goes through each state in the model
    for curStateIdx in range(m):
      curState = states[curStateIdx]
      maxProbability = float('-inf')
      prevMaxState = -1

      # Goes through each state in the model
      for prevStateIdx in range(m):
        prevState = states[prevStateIdx]

        # Calculates the probability that the next state is curState, assuming
        # that probability[prevState][curWordIdx-1] has that highest possible
        # probability of the previous state being prevState
        transition = math.log(next(prevState, curState))
        emission = math.log(output(curState, sent, curWordIdx))
        curProbability = probabilities[prevState][curWordIdx-1] + \
        transition + emission

        # Replaces maxProbability with curProbability if necessary
        if curProbability > maxProbability:
          maxProbability = curProbability
          prevMaxState = prevState

      # Adds a new state and probability to the previousState and  probabilities
      # arrays
      probabilities[curStateIdx][curWordIdx] = maxProbability
      previousStates[curStateIdx][curWordIdx] = prevMaxState

  # Finds the most likely final state by going through all probabilities in the
  # last column of the probabilities matrix
  maxProbability = 0
  finalStateIdx = 0
  for idx in range(m):
    if probabilities[idx][s-1] > maxProbability:
      maxProbability = probabilities[idx][s-1]
      finalStateIdx = idx
  
  # Backtracks through the previous states until it comes up with a complete
  # path
  path = [states[finalStateIdx]]
  prevState = previousStates[finalStateIdx][s-1]
  prevStateIdx = states.index(prevState)
  for idx in range(s-1):
    curWordIdx = s - 1 - idx
    path.insert(0, prevState)
    prevState = previousStates[prevStateIdx][curWordIdx]
    prevStateIdx = states.index(prevState)

  # Returns path if it has a positive probability, and raises an error otherwise
  if maxProbability > float('-inf'):
    return path, maxProbability
  else:
    print("No path found")
    raise NotImplementedError

# Creates a dictionary containing the features for the token at index in a given
# article. This does not add part-of-speech tags because doing that on a token-
# by-token basis was too innefficient. Instead, part-of-speech tags were added
# in the next function
def extractFeatureForToken(index, article):
  maxIndex = len(article)-1
  if (index-4 >= 0):
    prevWord4 = article[index-4]
  else:
    prevWord4 = ""

  if (index-3 >= 0):
    prevWord3 = article[index-3]
  else:
    prevWord3 = ""

  if (index-2 >= 0):
    prevWord2 = article[index-2]
  else:
    prevWord2 = ""

  if (index-1 >= 0):
    prevWord1 = article[index-1]
  else:
    prevWord1 = ""

  if (index+1 <= maxIndex):
    nextWord1 = article[index+1]
  else:
    nextWord1 = ""

  if (index+2 <= maxIndex):
    nextWord2 = article[index+2]
  else:
    nextWord2 = ""
  
  if (index+3 <= maxIndex):
    nextWord3 = article[index+3]
  else:
    nextWord3 = ""
  
  if (index+4 <= maxIndex):
    nextWord4 = article[index+4]
  else:
    nextWord4 = ""
  
  dic = {
      "prevWord4" : prevWord4,
      "prevWord3" : prevWord3,
      "prevWord2" : prevWord2,
      "prevWord1" : prevWord1,
      "word" : article[index],
      "nextWord1" : nextWord1,
      "nextWord2" : nextWord2,
      "nextWord3" : nextWord3,
      "nextWord4" : nextWord4
  }
  return dic

# Extracts a feature dictionary for each token in an article and returns a list
# of all dictionaries. 
def extractFeaturesForArticle(article, labels):
  indices = list(range(len(article)))
  max_index = len(article)-1

  pos = nltk.pos_tag(article)
  featurelist = list(map(lambda x: extractFeatureForToken(x, article),indices))
  for i in indices:
    phrase = ""
    if i-2 >=0:
      featurelist[i]["prevWord2POS"] = pos[i-2][1]
      phrase += (pos[i-2][1])
    else:
      featurelist[i]["prevWord2POS"] = ""
    if i-1 >=0:
      featurelist[i]["prevWord1POS"] = pos[i-1][1]
      featurelist[i]["prevLabel"] = labels[i-1]
      phrase += (pos[i-1][1])
    else:
      featurelist[i]["prevWord1POS"] = ""
      featurelist[i]["prevLabel"] = -1
    phrase += (pos[i][1])
    if i+1 <= max_index:
      featurelist[i]["nextWord1POS"] = pos[i+1][1]
      phrase += (pos[i+1][1])
    else:
      featurelist[i]["nextWord1POS"] = ""
    if i+2 <= max_index:
      featurelist[i]["nextWord2POS"] = pos[i+2][1]
      phrase += (pos[i+2][1])
    else:
      featurelist[i]["nextWord2POS"] = ""
    featurelist[i]["phrase"] = phrase
    featurelist[i]["pos"] = pos[i][1]
  return featurelist

# Extracts all feature dictionaries from a list of articles and returns a list
# containing all dictionaries
def extractFeaturesForAllArticles(articles, labels):

  func = lambda x : extractFeaturesForArticle(articles[x], labels[x])
  listOfLists = list(map(func, list(range(len(articles)))))
  finalList = []
  for lst in listOfLists:
    finalList += lst
  return finalList

# Flattens a list of lists into a single long list
def flattenLabels(list_of_lists):
  long_list = []
  for lst in list_of_lists:
    long_list += lst
  return long_list

# Takes in a list of articles and a list of list of labels and returns a list
# of pair containing feature dictionaries and labels for each token
def master_data_formatter(articles, labels):
  feature_list  = extractFeaturesForAllArticles(articles, labels)
  label_list = flattenLabels(labels)
  return [(feature_list[i], label_list[i]) for i in range(len(label_list))]

# Formats the data using the helper function
training_data = master_data_formatter(tokenized_train_articles, tokenized_train_labels)

print(training_data[0])
input()
# Creates and trains the classifier
classifier = MaxentClassifier.train(training_data, max_iter=15)

# Checks if the classifier works by using validation data
# predictions = list(map(classifier.classify,validation_features))
# accuracy = [predictions[i] == validation_labels[i] for i in range(len(predictions))]

################################################################################
# Uses the classifier in the viterbi algorithm
################################################################################

def rounder(number):
  if (round(number) == 0):
    return 0.1**99
  else:
    return 1-0.1**99

def modifyDict(dic, prevLabel):
  # dic["prevLabel"] = prevLabel
  return dic


def useMEMM(article):
  prevLabel = -1
  def modeifyPrevLabel(prevState, nextState):
    prevLabel = prevState
    return viterbi_next(prevState, nextState)
  features = extractFeaturesForArticle(article, [0]*len(article))
  func = lambda x, y, z : rounder(classifier.prob_classify(modifyDict(features[z], prevLabel)).prob(x))
  return (viterbi(article, [0,1], modeifyPrevLabel, viterbi_start, func))[0]

predictions = list(map(useMEMM, valid_articles))

print("Accuracy of viterbi: " + str(weighted_accuracy(valid_labels, predictions)))

for k in range(100):
  classifier = MaxentClassifier.train(training_data, max_iter=k)
  predictions = list(map(useMEMM, valid_articles))
  print("Accuracy of viterbi after " + str(k) + " iterations: " + str(weighted_accuracy(valid_labels, predictions)))

# ERROR ANALYSIS: MEMM (ARTICLE 0)

print("Correct labels:")
print(valid_labels[0])
print("Output labels from Viterbi:")
print(predictions[0])
count_correct_labels = 0
count_incorrect_labels = 0
incorrect_labels = []
for i in range(len(valid_labels[0])):
  if valid_labels[0][i] == predictions[0][i]:
    count_correct_labels += 1
  else:
    count_incorrect_labels += 1
    incorrect_labels.append("\t" + str(valid_labels[0][i]) + " was changed to " + str(predictions[0][i]))
print("\nNumber of correct labels: %d" % count_correct_labels)
print("Number of incorrect labels: %d" % count_incorrect_labels)
print("Incorrectly labelled:")
for x in incorrect_labels:
  print(x)