# Milestone 1: Index construction (DUE 11/11/2022)

## Building the inverted index:
Now that you have been provided the HTML files to index, you may build your inverted index off of them. 
The inverted index is simply a map with the token as a key and a list of its corresponding postings. 
A posting is the representation of the token’s occurrence in a document. 

The posting typically (not limited to) contains the following info:
- The document name/id the token was found in.
- Its tf-idf score for that document (for MS1, add only the term frequency)
- ... (you are encouraged to think of other attributes that you could add to the index)

## Some tips:
- When designing your inverted index, you will think about the structure of your posting first.
- You would normally begin by implementing the code to calculate/fetch the elements which will constitute your posting.
- Use scripts/classes that will perform a function or a set of closely related functions. This helps in keeping track of your progress, debugging, and also dividing work amongst teammates if you’re in a group.
- We strongly recommend you use GitHub as a mechanism to work with your team members on this project, but please make the project private.

## Deliverables
**No late submissions will be accepted for this milestone.**
Submit your **code** and a **report(in PDF format)** with a table containing some analytics about your index. 

The minimum analytics are:  
- The number of indexed documents;
- The number of unique tokens;
- The total size (in KB) of your index on disk.
- Note for the developer option: at this time, you do not need to have the optimized index, but you may save time if you do. 

## Evaluation criteria:
- Did your report show up on time?
- Are the reported numbers plausible?

<hr>

# Milestone 2: Retrieval component (DUE 11/18/2022)

At least the following queries should be used to test your retrieval:

- 1 – cristina lopes

- 2 - machine learning

- 3 - ACM

- 4 - master of software engineering

## Developing the Search component
Once you have built the inverted index, you are ready to test document retrieval with queries. At the very least, the search should be able to deal with boolean queries: AND only. If you wish, you can sort the retrieved documents based on tf-idf scoring (you are not required to do so now, but it will be required for the final search engine). This can be done using the cosine similarity method. Feel free to use a library to compute cosine similarity once you have the term frequencies and inverse document frequencies (although it should be very easy for you to write your own implementation). You may also add other weighting/scoring mechanisms to help refine the search results. 

## Deliverables
**No late submissions will be accepted for this milestone.**
Submit your **code** and a **report (in PDF format)** 

Report contains
- the top 5 URLs for each of the queries above
- a screenshot of your search interface in action (text or web-based)

## Evaluation criteria:
- Did your report show up on time?
- Are the reported URLs plausible?

<hr>

# Milestone 3: Search engine (DUE 12/2/2022)

During this last stretch, you will improve and finalize your search engine. Come up with a set of at least 20 queries that guide you in evaluating how well your search engine performs, both in terms of ranking performance (effectiveness) and in terms of runtime performance (efficiency). At least half of those queries should be chosen because they do poorly on one or both criteria; the other half should do well. Then change your code to make it work better for the queries that perform poorly, while preserving the good performance of the other ones, and while being as general as possible. 

**Note for the developer option**: at the end of the project, you should have the optimized index that allows you to run both the indexer and the search with small memory footprint, smaller than the index size. 

# Deliverables:

- Submit a zip file containing all the programs you wrote for this project as well as a document with your test queries (no need to report the results). 
- Comment on which queries started by doing poorly (i.e. giving you poor results) and explain what you did in your search engine to make them perform better.
- A live demonstration of your search engine during an interview with a TA. You are expected to share your screen and guide the TAs through the code that you wrote, and also to turn on your video.
- Note: Considering the proximity to the date of the final quiz and the need for the online interviews, late submissions are accepted only 3 days after the due date, with a penalty of 25% of the grade.

## Evaluation criteria:
- Does your search engine work as expected of search engines?
- How general are the heuristics that you employed to improve the retrieval?
- Is the search response time under the expected limit?
- Do you demonstrate in-depth knowledge of how your search engine works? 
- Are you able to answer detailed questions pertaining to any aspect of its implementation and justify your choices?
