I'm not very familar with GitHub, but quiz2.pdf will work if you press raw code, or if you press edit! I've copied my explanation here as well, 
because it seems to result in easier reading this way.



Quiz2.pdf
CS329 quiz 2
Final Program:
  I changed the most_similar method (in my code named most_similar1) to find the most similar fables of all fables to the given input alternative fable
  by finding the document with the highest cosine similarity(as opposed to the lowest Euclidean distance). Cosine similarity is much more more practical for
  out data set of the fables because these documents are relatively short, and some are incredibly short with only a few sentences. Euclidean distance
  correlates document similarity score with number of words in a document, so short fables were being frequently matched with alternative fables they were
  not actually the most similar to. Cosine similarity increased my overall correct matches to 33/37. 
  Additionally I added the conditioned that additional weight would be added to capitalized words which were not in a list of common, un-important punctuation/words.
  I experimented with different weights, but the best results yielded from around 0.5 being added to the TF-IDFS score of a given term is its first letter was
  capitalized and it was not in the list of unwanted terms (such as "and" or "him"). This did little to change the method, but conceptually I think it would be
  an effective strategy if the fables were longer. This seems especially effective for this type of data, since many of the important words (like Death or Lion),
  which often even appear in the title they're so important, are capitalized within each fable. In fields where important words/terms are emphasized with capitalization,
  like old English literature or Medicine, then this strategy might also be helpful.
  
  
Attempted methods and experimentations:
  The code we discussed in class for document similarity computation, and the code in the provided initial code and my final program, are based on a unigram model,
  where terms are analyzed single term by single term. I decided to try to execute a bigram that would consider two words in a row and count the number of same 
  pairs of terms between two different documents. This became complicated quickly and hard to integrate or combine with the current TF-IDFS method, mostly
  because so many more inputs were needed. When checking the matched pairs, most pairs were of clearly unimportant terms (especially including punctuation), so I
  made it so that a term pair would only be counted if 1) one of the terms was in the top fifth of terms for TF_IDS for the given document, and 2) if both of
  the terms was not in a list of common, unimportant words/punctuation. Even with those conditions in place, pairs were rarely significant to the document.
  I think this method was ineffective in part because of the shortness of the documents, but also a strategy of checking words in the same sentence (as
  opposed to only within the same pair of consecutive terms) would have been more telling.
  
  I also wrote sublinear and normalize methods to see if they would be better than TF-IDFS as measures of term importance. The sublinear/weighted frequencies
  method did decently okay with 24/37. It still did not do the best likely because the fables are so short, so it is not reasonable to use log when most of the term frequencies, and even
  the highest of the term frequencies, are relatively small. The normalize function did worse, but still decently alright, with 21/37. I experimented with different
  values of alpha, which made a significant difference, ranging from results of 13 to 21 correct matches. Again, I think the documents are too short
  and issues arose especially with fables that were similar to the given alternative fable but not the most similar (consider TheOldLion and TheSickLion, which are
  both similar to TheSickLion2). 
  
  
Results: number of correct matches out of 37
  Euclidean, TF-IDFS with capitals considered: 7 
  Euclidean, TF-IDFS 6
  Euclidean, sublinear: 13
  Euclidean, normalize: 16
  Cosine, TF-IDFS with capitals considered: 33
  Cosine, TF-IDFS: 33
  Cosine, sublinear: 24
  Cosine, normalize: 21
