# Specifications for Algorithms and Data Structures Developer
#### Programming skills required: advanced
#### Main challenges: design efficient data structures, devise efficient file access, balance memory usage and response time
#### Corpus: all ICS web pages (developer.zip)
#### Index: Your index should be stored in one or more files in the file system (no databases!).

<hr>

## Search interface:

The response to search queries should be  300ms. 
Ideally, it would be  100ms, or less, but you won’t be penalized if it’s higher (as long as it’s kept  300ms).

## Operational constraints:
You must design and implement your programs as if you are dealing with very large amounts of data, so large that you cannot hold the inverted index all in memory. 

### Indexer
Your indexer must offload the inverted index hash map from main memory to a partial index on disk at least 3 times during index construction; those partial indexes should be merged in the end. 
Optionally, after or during merging, they can also be split into separate index files with term ranges. 

### Search Component
Your search component must not load the entire inverted index in main memory. 
Instead, it must read the postings from the index(es) files on disk. The TAs will check that both of these things are happening.

<hr>

# Understanding the Dataset

Your crawlers crawled the many web sites associated with ICS. 
We collected a big chunk of these pages and are providing them to you as a zip file.

**!!! Because we have two CS majors in our group, we need to download the 'DEV file':** [**here**](https://www.ics.uci.edu/~algol/teaching/informatics141cs121w2020/a3files/developer.zip)

The following is an explanation of how the data is organized.

## Folders:
There is one folder per domain. 
Each file inside a folder corresponds to one web page. (note that you would not do this in a real search engine). 

## Files:
The files are stored in JSON format, with the following fields :
- “url” : contains the URL of the page. (ignore the fragment part, if you see it)
- “content” : contains the content of the page, as found during crawling
- "encoding" : an indication of the encoding of the webpage

## Broken or missing HTML:
Real HTML pages found out there are full of bugs! 
Some of the pages in the dataset may not contain any HTML at all and, when they do, it may not be well formed. 
For example, there might be an open <strong> tag but the associated closing </strong> tag might be missing. 
While selecting the parser library for your project, please ensure that it can handle broken HTML.