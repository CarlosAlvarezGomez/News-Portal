import torch

# Converts a non-binary tensor to a binary tensor by converting every non-zero
# number into a 1.
def convert_to_binary(tags):
  n = tags.size()[0]
  return (torch.eq(tags, 0).type(torch.int32)-1)*(-1)

# Compressed the output of the propaganda classifier into a format that takes up
# less memory. For the article, the compressed version of the article is a list
# of string in which all the '<s>' symbols have been removed and all the '</s>'
# symbols are replaced with '/s'. For the tags, instead of storing the label for
# each word, this assumes the first token does not contain propaganda, and it
# stores the indices in the compressed article in which we switch from
# not-propaganda to propaganda, or from propaganda to not-propaganda.
def compress(article, tags):
  new_tags = convert_to_binary(tags)
  compressed_article = []
  compressed_tags = []
  current_label = 0
  offset = 0

  for i, (term, tag) in enumerate(zip(article, new_tags)):
    if term != '<s>' and term != '</s>':
      compressed_article.append(term)
      if tag != current_label:
        compressed_tags.append(i-offset)
        current_label = tag
    elif term == '</s>':
      compressed_article.append('/s')
    else:
      offset += 1

  return compressed_article, compressed_tags

# Converts a set of tags in form described above into a binary set of
# non-compressed tags
def decompress(tags, length):
  t = torch.zeros(length)
  if (len(tags) % 2) != 0:
    tags.append(length+1)

  for i in range(len(tags)/2):
    for j in range(tags[2*i],tags[2*i+1]):
      t[j] = 1

  return t
  
article = '<s> Hello , my name is Bob! </s>'.split(' ')
tags = torch.tensor([3, 0, 0, 1, 1, 0, 0, 4])

art, t = compress(article, tags)

print(art)
print(t)