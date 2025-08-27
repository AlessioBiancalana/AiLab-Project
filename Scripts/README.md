# Textual Matching and Recommendation Engine

Once the uploaded poster has been visually matched to a specific movie in the database, the recommendation process leverages textual similarity to find related titles.

The textual analysis is based on **Term Frequency–Inverse Document Frequency (TF-IDF)**, a statistical method that assigns higher weight to distinctive words within the dataset while reducing the influence of common terms.

Pipeline:
1.	Text Aggregation – For each movie, multiple metadata fields are concatenated into a single textual document:
        •	Plot summary
        •	Genres
        •	Director
        •	Main cast
        •	Studio
    
2.  Weighting – To emphasize more informative fields, specific weights are applied before vectorization:
                
                Field	    Weight
                Plot	    2.5
                Genre	    2.0
                Director	2.0
                Studio	    1.0
                Cast	    0.5
    This ensures that narrative and genre-related terms have greater impact than less distinctive elements.

3.	TF-IDF Vectorization – The aggregated and weighted text is transformed into sparse vectors representing the importance of each term. Stopwords, punctuation, and overly frequent words are removed.

4.	Similarity Computation – Cosine similarity is computed between the TF-IDF vector of the identified movie and all others in the dataset.

5.	Recommendation Output – The system returns the top-k most similar movies, excluding the query movie itself and filtering near-duplicates.
    
    Advantages:
    - Captures semantic proximity without requiring user ratings.
    - Efficient even for large datasets.
    - Naturally supports multilingual metadata if preprocessed accordingly.

    This approach complements visual similarity: for example, two visually similar posters may belong to different genres, and TF-IDF ensures the recommendations stay contextually relevant to the narrative and metadata.

**TF-IDF Overview**

TF-IDF (Term Frequency – Inverse Document Frequency) is a text representation technique that converts documents into numerical vectors, weighting words based on their relative importance.

It consists of two main components:
1.	Term Frequency (TF) – Measures how often a term appears in a document. The more frequent it is, the more representative it is of that document.
2.	Inverse Document Frequency (IDF) – Measures how rare a term is across the entire corpus. Common terms (e.g., “the”, “and”) have low IDF, while rare terms have high IDF.

The basic formula is:
    
$TF-IDF(t,d)=TF(t,d)×IDF(t)
$     

The output is a sparse vector where each dimension corresponds to a vocabulary term, and the value indicates that term’s relevance to the document.

TF-IDF is widely used in information retrieval, search engines, and recommendation systems because it enables efficient comparison of text documents using similarity measures such as cosine similarity.
 
