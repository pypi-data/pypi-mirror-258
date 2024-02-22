

!!! note
    To run this notebook in JupyterLab, load [`examples/sample.ipynb`](https://github.com/DerwenAI/pytextrank/blob/main/examples/sample.ipynb)



# Getting Started

First, we'll import the required libraries and add the **PyTextRank** component into the `spaCy` pipeline:


```python
import pytextrank
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank");
```

Let's take a look at this pipeline now...


```python
nlp.pipe_names
```




    ['tok2vec',
     'tagger',
     'parser',
     'attribute_ruler',
     'lemmatizer',
     'ner',
     'textrank']



We can examine the `spaCy` pipeline in much greater detail...


```python
nlp.analyze_pipes(pretty=True)
```

    [1m
    ============================= Pipeline Overview =============================[0m
    
    #   Component         Assigns               Requires   Scores             Retokenizes
    -   ---------------   -------------------   --------   ----------------   -----------
    0   tok2vec           doc.tensor                                          False      
                                                                                         
    1   tagger            token.tag                        tag_acc            False      
                                                                                         
    2   parser            token.dep                        dep_uas            False      
                          token.head                       dep_las                       
                          token.is_sent_start              dep_las_per_type              
                          doc.sents                        sents_p                       
                                                           sents_r                       
                                                           sents_f                       
                                                                                         
    3   attribute_ruler                                                       False      
                                                                                         
    4   lemmatizer        token.lemma                      lemma_acc          False      
                                                                                         
    5   ner               doc.ents                         ents_f             False      
                          token.ent_iob                    ents_p                        
                          token.ent_type                   ents_r                        
                                                           ents_per_type                 
                                                                                         
    6   textrank                                                              False      
    
    [38;5;2m✔ No problems found.[0m





    {'summary': {'tok2vec': {'assigns': ['doc.tensor'],
       'requires': [],
       'scores': [],
       'retokenizes': False},
      'tagger': {'assigns': ['token.tag'],
       'requires': [],
       'scores': ['tag_acc'],
       'retokenizes': False},
      'parser': {'assigns': ['token.dep',
        'token.head',
        'token.is_sent_start',
        'doc.sents'],
       'requires': [],
       'scores': ['dep_uas',
        'dep_las',
        'dep_las_per_type',
        'sents_p',
        'sents_r',
        'sents_f'],
       'retokenizes': False},
      'attribute_ruler': {'assigns': [],
       'requires': [],
       'scores': [],
       'retokenizes': False},
      'lemmatizer': {'assigns': ['token.lemma'],
       'requires': [],
       'scores': ['lemma_acc'],
       'retokenizes': False},
      'ner': {'assigns': ['doc.ents', 'token.ent_iob', 'token.ent_type'],
       'requires': [],
       'scores': ['ents_f', 'ents_p', 'ents_r', 'ents_per_type'],
       'retokenizes': False},
      'textrank': {'assigns': [],
       'requires': [],
       'scores': [],
       'retokenizes': False}},
     'problems': {'tok2vec': [],
      'tagger': [],
      'parser': [],
      'attribute_ruler': [],
      'lemmatizer': [],
      'ner': [],
      'textrank': []},
     'attrs': {'token.is_sent_start': {'assigns': ['parser'], 'requires': []},
      'doc.sents': {'assigns': ['parser'], 'requires': []},
      'token.head': {'assigns': ['parser'], 'requires': []},
      'token.ent_iob': {'assigns': ['ner'], 'requires': []},
      'token.tag': {'assigns': ['tagger'], 'requires': []},
      'token.lemma': {'assigns': ['lemmatizer'], 'requires': []},
      'doc.tensor': {'assigns': ['tok2vec'], 'requires': []},
      'doc.ents': {'assigns': ['ner'], 'requires': []},
      'token.dep': {'assigns': ['parser'], 'requires': []},
      'token.ent_type': {'assigns': ['ner'], 'requires': []}}}



Next, let's load some text from a document:


```python
from icecream import ic
import pathlib

text = pathlib.Path("../dat/mih.txt").read_text()
text
```




    'Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types.\n'



Then run the `spaCy` pipeline...


```python
doc = nlp(text)
len(doc)
```




    92



Now we can access the **PyTextRank** component within the `spaCy` pipeline, and use it to get more information for post-processing of the document.
For example, let's see what the elapsed time in milliseconds was for the *TextRank* processing:


```python
tr = doc._.textrank
ic(tr.elapsed_time);
```

    ic| tr.elapsed_time: 2.915620803833008


Let's examine the top-ranked phrases in the document


```python
for phrase in doc._.phrases:
    ic(phrase.rank, phrase.count, phrase.text)
    ic(phrase.chunks)
```

    ic| phrase.rank: 0.18359439311764025
        phrase.count: 1
        phrase.text: 'mixed types'
    ic| phrase.chunks: [mixed types]
    ic| phrase.rank: 0.1784796193107821
        phrase.count: 3
        phrase.text: 'systems'
    ic| phrase.chunks: [systems, systems, systems]
    ic| phrase.rank: 0.15037838042245094
        phrase.count: 1
        phrase.text: 'minimal generating sets'
    ic| phrase.chunks: [minimal generating sets]
    ic| phrase.rank: 0.14740065982407313
        phrase.count: 1
        phrase.text: 'nonstrict inequations'
    ic| phrase.chunks: [nonstrict inequations]
    ic| phrase.rank: 0.13946027725597837
        phrase.count: 1
        phrase.text: 'strict inequations'
    ic| phrase.chunks: [strict inequations]
    ic| phrase.rank: 0.1195023546245721
        phrase.count: 1
        phrase.text: 'linear Diophantine equations'
    ic| phrase.chunks: [linear Diophantine equations]
    ic| phrase.rank: 0.11450088293222845
        phrase.count: 1
        phrase.text: 'natural numbers'
    ic| phrase.chunks: [natural numbers]
    ic| phrase.rank: 0.10780718173686318
        phrase.count: 3
        phrase.text: 'solutions'
    ic| phrase.chunks: [solutions, solutions, solutions]
    ic| phrase.rank: 0.10529828014583348
        phrase.count: 1
        phrase.text: 'linear constraints'
    ic| phrase.chunks: [linear constraints]
    ic| phrase.rank: 0.1036960590708142
        phrase.count: 1
        phrase.text: 'all the considered types systems'
    ic| phrase.chunks: [all the considered types systems]
    ic| phrase.rank: 0.08812713074893187
        phrase.count: 1
        phrase.text: 'a minimal supporting set'
    ic| phrase.chunks: [a minimal supporting set]
    ic| phrase.rank: 0.08444534702772151
        phrase.count: 1
        phrase.text: 'linear'
    ic| phrase.chunks: [linear]
    ic| phrase.rank: 0.08243620500315359
        phrase.count: 1
        phrase.text: 'a system'
    ic| phrase.chunks: [a system]
    ic| phrase.rank: 0.07944607954086784
        phrase.count: 1
        phrase.text: 'a minimal set'
    ic| phrase.chunks: [a minimal set]
    ic| phrase.rank: 0.0763527926213032
        phrase.count: 1
        phrase.text: 'algorithms'
    ic| phrase.chunks: [algorithms]
    ic| phrase.rank: 0.07593126037016427
        phrase.count: 1
        phrase.text: 'all types'
    ic| phrase.chunks: [all types]
    ic| phrase.rank: 0.07309361902551355
        phrase.count: 1
        phrase.text: 'Diophantine'
    ic| phrase.chunks: [Diophantine]
    ic| phrase.rank: 0.0702090100898443
        phrase.count: 1
        phrase.text: 'construction'
    ic| phrase.chunks: [construction]
    ic| phrase.rank: 0.05800111772673988
        phrase.count: 1
        phrase.text: 'the set'
    ic| phrase.chunks: [the set]
    ic| phrase.rank: 0.054251394765316464
        phrase.count: 1
        phrase.text: 'components'
    ic| phrase.chunks: [components]
    ic| phrase.rank: 0.04516904342912139
        phrase.count: 1
        phrase.text: 'Compatibility'
    ic| phrase.chunks: [Compatibility]
    ic| phrase.rank: 0.04516904342912139
        phrase.count: 1
        phrase.text: 'compatibility'
    ic| phrase.chunks: [compatibility]
    ic| phrase.rank: 0.04435648606848154
        phrase.count: 1
        phrase.text: 'the corresponding algorithms'
    ic| phrase.chunks: [the corresponding algorithms]
    ic| phrase.rank: 0.042273783712246285
        phrase.count: 1
        phrase.text: 'Criteria'
    ic| phrase.chunks: [Criteria]
    ic| phrase.rank: 0.01952542432474353
        phrase.count: 1
        phrase.text: 'These criteria'
    ic| phrase.chunks: [These criteria]


## Stop Words

To show use of the *stop words* feature, first we'll output a baseline...


```python
text = pathlib.Path("../dat/gen.txt").read_text()
doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='words', chunks=[words, words], count=2, rank=0.16404428603296545)
    ic| phrase: Phrase(text='sentences', chunks=[sentences], count=1, rank=0.1287826954552565)
    ic| phrase: Phrase(text='Mihalcea et al',
                       chunks=[Mihalcea et al],
                       count=1,
                       rank=0.11278365769540494)
    ic| phrase: Phrase(text='Barrios et al',
                       chunks=[Barrios et al],
                       count=1,
                       rank=0.10760811592357011)
    ic| phrase: Phrase(text='the remaining words',
                       chunks=[the remaining words],
                       count=1,
                       rank=0.09737893962520337)
    ic| phrase: Phrase(text='text summarization',
                       chunks=[text summarization],
                       count=1,
                       rank=0.08861074217386355)
    ic| phrase: Phrase(text='ranking webpages',
                       chunks=[ranking webpages],
                       count=1,
                       rank=0.07685260919250497)
    ic| phrase: Phrase(text='Okapi BM25 function',
                       chunks=[Okapi BM25 function],
                       count=1,
                       rank=0.0756013984034083)
    ic| phrase: Phrase(text='gensim implements',
                       chunks=[gensim implements],
                       count=1,
                       rank=0.0748386557231912)
    ic| phrase: Phrase(text='every other sentence',
                       chunks=[every other sentence],
                       count=1,
                       rank=0.07031782290622991)


Notice how the top-ranked phrase above is `words` ?
Let's add that phrase to our *stop words* list, to exclude it from the ranked phrases...


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] } })

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='sentences', chunks=[sentences], count=1, rank=0.14407118792073048)
    ic| phrase: Phrase(text='Mihalcea et al',
                       chunks=[Mihalcea et al],
                       count=1,
                       rank=0.12123026637064825)
    ic| phrase: Phrase(text='Barrios et al',
                       chunks=[Barrios et al],
                       count=1,
                       rank=0.11566772028535821)
    ic| phrase: Phrase(text='text summarization',
                       chunks=[text summarization],
                       count=1,
                       rank=0.09524776232834677)
    ic| phrase: Phrase(text='ranking webpages',
                       chunks=[ranking webpages],
                       count=1,
                       rank=0.08260919223940909)
    ic| phrase: Phrase(text='Okapi BM25 function',
                       chunks=[Okapi BM25 function],
                       count=1,
                       rank=0.08125840606728206)
    ic| phrase: Phrase(text='gensim implements',
                       chunks=[gensim implements],
                       count=1,
                       rank=0.08043607214961235)
    ic| phrase: Phrase(text='every other sentence',
                       chunks=[every other sentence],
                       count=1,
                       rank=0.07915141312258998)
    ic| phrase: Phrase(text='original TextRank',
                       chunks=[original TextRank],
                       count=1,
                       rank=0.07013026654397199)
    ic| phrase: Phrase(text='TextRank',
                       chunks=[TextRank, TextRank, TextRank, TextRank, TextRank],
                       count=5,
                       rank=0.06686718957926076)


For each entry, you'll need to add a key that is the *lemma_* and a value that's a list of its *part-of-speech* tags.

Note: [lemma_](https://spacy.io/api/token#attributes) of a token is base form of the token, with no inflectional suffixes. It is usually represented in lower-case form, with the exception of proper nouns and named entities. For eg. words like *ran*, *runs*, *running* will be lemmatized to *run*, *London* will be lemmatized to *London* without lower casing. It is sugggested to check the designated lemma value for a token before setting it in stopword config.      

## Scrubber

Observe how different variations of "sentence", like "every sentence" and "every other sentence", as well as variations of "sentences", occur in phrase list. You can omit such variations by passing a scrubber function in the config.


```python
from spacy.tokens import Span
nlp = spacy.load("en_core_web_sm")


@spacy.registry.misc("prefix_scrubber")
def prefix_scrubber():
	def scrubber_func(span: Span) -> str:
		while len(span) > 1 and span[0].text in ("a", "the", "their", "every", "other", "two"):
			span = span[1:]
		return span.lemma_
	return scrubber_func

nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] }, "scrubber": {"@misc": "prefix_scrubber"}})

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='sentence',
                       chunks=[sentences,
                               every sentence,
                               every other sentence,
                               the two sentences,
                               two sentences,
                               the sentences],
                       count=6,
                       rank=0.14407118792073048)
    ic| phrase: Phrase(text='Mihalcea et al',
                       chunks=[Mihalcea et al],
                       count=1,
                       rank=0.12123026637064825)
    ic| phrase: Phrase(text='Barrios et al',
                       chunks=[Barrios et al],
                       count=1,
                       rank=0.11566772028535821)
    ic| phrase: Phrase(text='text summarization',
                       chunks=[text summarization],
                       count=1,
                       rank=0.09524776232834677)
    ic| phrase: Phrase(text='rank webpage',
                       chunks=[ranking webpages],
                       count=1,
                       rank=0.08260919223940909)
    ic| phrase: Phrase(text='Okapi BM25 function',
                       chunks=[Okapi BM25 function],
                       count=1,
                       rank=0.08125840606728206)
    ic| phrase: Phrase(text='gensim implement',
                       chunks=[gensim implements],
                       count=1,
                       rank=0.08043607214961235)
    ic| phrase: Phrase(text='original TextRank',
                       chunks=[original TextRank],
                       count=1,
                       rank=0.07013026654397199)
    ic| phrase: Phrase(text='TextRank',
                       chunks=[TextRank, TextRank, TextRank, TextRank],
                       count=4,
                       rank=0.06686718957926076)
    ic| phrase: Phrase(text='Olavur Mortensen',
                       chunks=[Olavur Mortensen, Olavur Mortensen],
                       count=2,
                       rank=0.06548020385220721)


Different variations of "sentence(s)" are now represented as part of single entry in phrase list.

As the scrubber takes in `Spans`, we can also use `token.pos_` or any other spaCy `Token` or `Span` attribute in the scrubbing. The variations of "sentences" have different DETs (determiners), so we could achieve a similar result with the folowing scrubber.


```python
@spacy.registry.misc("articles_scrubber")
def articles_scrubber():
    def scrubber_func(span: Span) -> str:
        for token in span:
            if token.pos_ not in ["DET", "PRON"]:
                break
            span = span[1:]
        return span.text
    return scrubber_func
```


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] }, "scrubber": {"@misc": "articles_scrubber"}})

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='sentences',
                       chunks=[sentences, the sentences],
                       count=2,
                       rank=0.14407118792073048)
    ic| phrase: Phrase(text='Mihalcea et al',
                       chunks=[Mihalcea et al],
                       count=1,
                       rank=0.12123026637064825)
    ic| phrase: Phrase(text='Barrios et al',
                       chunks=[Barrios et al],
                       count=1,
                       rank=0.11566772028535821)
    ic| phrase: Phrase(text='text summarization',
                       chunks=[text summarization],
                       count=1,
                       rank=0.09524776232834677)
    ic| phrase: Phrase(text='ranking webpages',
                       chunks=[ranking webpages],
                       count=1,
                       rank=0.08260919223940909)
    ic| phrase: Phrase(text='Okapi BM25 function',
                       chunks=[Okapi BM25 function],
                       count=1,
                       rank=0.08125840606728206)
    ic| phrase: Phrase(text='gensim implements',
                       chunks=[gensim implements],
                       count=1,
                       rank=0.08043607214961235)
    ic| phrase: Phrase(text='other sentence',
                       chunks=[every other sentence],
                       count=1,
                       rank=0.07915141312258998)
    ic| phrase: Phrase(text='original TextRank',
                       chunks=[original TextRank],
                       count=1,
                       rank=0.07013026654397199)
    ic| phrase: Phrase(text='TextRank',
                       chunks=[TextRank, TextRank, TextRank, TextRank, TextRank],
                       count=5,
                       rank=0.06686718957926076)


We could also use `Span` labels to filter out `ents`, for example, or certain types of entities, e.g. "CARDINAL", or "DATE", if need to do so for our use case.


```python
@spacy.registry.misc("entity_scrubber")
def articles_scrubber():
    def scrubber_func(span: Span) -> str:
        if span[0].ent_type_:
            # ignore named entities
            return "INELIGIBLE_PHRASE"
        return span.text
    return scrubber_func
```


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] }, "scrubber": {"@misc": "entity_scrubber"}})

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    if phrase.text != "INELIGIBLE_PHRASE":
        ic(phrase)
```

    ic| phrase: Phrase(text='sentences', chunks=[sentences], count=1, rank=0.14407118792073048)
    ic| phrase: Phrase(text='Barrios et al',
                       chunks=[Barrios et al],
                       count=1,
                       rank=0.11566772028535821)
    ic| phrase: Phrase(text='text summarization',
                       chunks=[text summarization],
                       count=1,
                       rank=0.09524776232834677)
    ic| phrase: Phrase(text='ranking webpages',
                       chunks=[ranking webpages],
                       count=1,
                       rank=0.08260919223940909)
    ic| phrase: Phrase(text='gensim implements',
                       chunks=[gensim implements],
                       count=1,
                       rank=0.08043607214961235)
    ic| phrase: Phrase(text='every other sentence',
                       chunks=[every other sentence],
                       count=1,
                       rank=0.07915141312258998)
    ic| phrase: Phrase(text='original TextRank',
                       chunks=[original TextRank],
                       count=1,
                       rank=0.07013026654397199)
    ic| phrase: Phrase(text='every sentence',
                       chunks=[every sentence],
                       count=1,
                       rank=0.06654363130280233)
    ic| phrase: Phrase(text='the sentences',
                       chunks=[the sentences],
                       count=1,
                       rank=0.06654363130280233)


## GraphViz Export

Let's generate a GraphViz doc `lemma_graph.dot` to visualize the *lemma graph* that **PyTextRank** produced for the most recent document...


```python
tr = doc._.textrank
tr.write_dot(path="lemma_graph.dot")
```


```python
!ls -lth lemma_graph.dot
```

    -rw-rw-r-- 1 ankush ankush 18K Aug  9 15:06 lemma_graph.dot



```python
!pip install graphviz
```

    Requirement already satisfied: graphviz in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (0.20.1)
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip available: [0m[31;49m22.3.1[0m[39;49m -> [0m[32;49m23.2.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m


To render this graph, you must first download `GraphViz` <https://www.graphviz.org/download/>

Then you can render a `DOT` file...


```python
import graphviz as gv

gv.Source.from_file("lemma_graph.dot")
```




    
![svg](sample_files/sample_36_0.svg)
    



Note that the image which gets rendered in a notebook is probably "squished", but other tools can renders these as interesting graphs.

## Altair visualisation

Let's generate an interactive `altair` plot to look at the lemma graph.



```python
!pip install "altair"
```

    Requirement already satisfied: altair in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (5.0.1)
    Requirement already satisfied: numpy in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from altair) (1.25.2)
    Requirement already satisfied: jsonschema>=3.0 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from altair) (4.19.0)
    Requirement already satisfied: toolz in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from altair) (0.12.0)
    Requirement already satisfied: typing-extensions>=4.0.1 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from altair) (4.7.1)
    Requirement already satisfied: pandas>=0.18 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from altair) (2.0.3)
    Requirement already satisfied: jinja2 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from altair) (3.1.2)
    Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from jsonschema>=3.0->altair) (2023.7.1)
    Requirement already satisfied: referencing>=0.28.4 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from jsonschema>=3.0->altair) (0.30.2)
    Requirement already satisfied: attrs>=22.2.0 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from jsonschema>=3.0->altair) (23.1.0)
    Requirement already satisfied: rpds-py>=0.7.1 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from jsonschema>=3.0->altair) (0.9.2)
    Requirement already satisfied: pytz>=2020.1 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from pandas>=0.18->altair) (2023.3)
    Requirement already satisfied: tzdata>=2022.1 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from pandas>=0.18->altair) (2023.3)
    Requirement already satisfied: python-dateutil>=2.8.2 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from pandas>=0.18->altair) (2.8.2)
    Requirement already satisfied: MarkupSafe>=2.0 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from jinja2->altair) (2.1.3)
    Requirement already satisfied: six>=1.5 in /home/ankush/workplace/os_repos/pytextrank/venv/lib/python3.10/site-packages (from python-dateutil>=2.8.2->pandas>=0.18->altair) (1.16.0)
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip available: [0m[31;49m22.3.1[0m[39;49m -> [0m[32;49m23.2.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m



```python
tr = doc._.textrank
tr.plot_keyphrases()
```





<style>
  #altair-viz-fd3323326ed4463e8623cd34817d680c.vega-embed {
    width: 100%;
    display: flex;
  }

  #altair-viz-fd3323326ed4463e8623cd34817d680c.vega-embed details,
  #altair-viz-fd3323326ed4463e8623cd34817d680c.vega-embed details summary {
    position: relative;
  }
</style>
<div id="altair-viz-fd3323326ed4463e8623cd34817d680c"></div>
<script type="text/javascript">
  var VEGA_DEBUG = (typeof VEGA_DEBUG == "undefined") ? {} : VEGA_DEBUG;
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-fd3323326ed4463e8623cd34817d680c") {
      outputDiv = document.getElementById("altair-viz-fd3323326ed4463e8623cd34817d680c");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm/vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm/vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm/vega-lite@5.8.0?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm/vega-embed@6?noext",
    };

    function maybeLoadScript(lib, version) {
      var key = `${lib.replace("-", "")}_version`;
      return (VEGA_DEBUG[key] == version) ?
        Promise.resolve(paths[lib]) :
        new Promise(function(resolve, reject) {
          var s = document.createElement('script');
          document.getElementsByTagName("head")[0].appendChild(s);
          s.async = true;
          s.onload = () => {
            VEGA_DEBUG[key] = version;
            return resolve(paths[lib]);
          };
          s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
          s.src = paths[lib];
        });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else {
      maybeLoadScript("vega", "5")
        .then(() => maybeLoadScript("vega-lite", "5.8.0"))
        .then(() => maybeLoadScript("vega-embed", "6"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 300, "continuousHeight": 300}}, "data": {"name": "data-af1f75241d67f8e6eb41b3c597d2754d"}, "mark": {"type": "bar"}, "encoding": {"color": {"field": "count", "type": "quantitative"}, "tooltip": [{"field": "text", "type": "nominal"}, {"field": "rank", "type": "quantitative"}, {"field": "count", "type": "quantitative"}], "x": {"field": "index", "type": "quantitative"}, "y": {"field": "rank", "type": "quantitative"}}, "title": "Keyphrase profile of the document", "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json", "datasets": {"data-af1f75241d67f8e6eb41b3c597d2754d": [{"index": 0, "text": "sentences", "count": 1, "rank": 0.14407118792073048}, {"index": 1, "text": "INELIGIBLE_PHRASE", "count": 24, "rank": 0.12123026637064825}, {"index": 2, "text": "Barrios et al", "count": 1, "rank": 0.11566772028535821}, {"index": 3, "text": "text summarization", "count": 1, "rank": 0.09524776232834677}, {"index": 4, "text": "ranking webpages", "count": 1, "rank": 0.08260919223940909}, {"index": 5, "text": "gensim implements", "count": 1, "rank": 0.08043607214961235}, {"index": 6, "text": "every other sentence", "count": 1, "rank": 0.07915141312258998}, {"index": 7, "text": "original TextRank", "count": 1, "rank": 0.07013026654397199}, {"index": 8, "text": "every sentence", "count": 1, "rank": 0.06654363130280233}, {"index": 9, "text": "the sentences", "count": 1, "rank": 0.06654363130280233}, {"index": 10, "text": "-", "count": 1, "rank": 0.05078719110471754}, {"index": 11, "text": "the popular PageRank algorithm", "count": 1, "rank": 0.05014935289717139}, {"index": 12, "text": "weighted-graphs", "count": 1, "rank": 0.0490776014231038}, {"index": 13, "text": "vertices", "count": 1, "rank": 0.04869052856977416}, {"index": 14, "text": "the two sentences", "count": 1, "rank": 0.04832294546848499}, {"index": 15, "text": "the summarization module", "count": 1, "rank": 0.04790153287714053}, {"index": 16, "text": "implementations", "count": 1, "rank": 0.04764465733587137}, {"index": 17, "text": "Pre", "count": 1, "rank": 0.04737378445179717}, {"index": 18, "text": "the highest PageRank score", "count": 1, "rank": 0.04658251039208111}, {"index": 19, "text": "an edge", "count": 2, "rank": 0.046189920195636586}, {"index": 20, "text": "the edge", "count": 1, "rank": 0.046189920195636586}, {"index": 21, "text": "the PageRank algorithm", "count": 1, "rank": 0.04464775208293306}, {"index": 22, "text": "his previous post", "count": 1, "rank": 0.04326438090881735}, {"index": 23, "text": "an unsupervised algorithm", "count": 1, "rank": 0.042277900580912416}, {"index": 24, "text": "the remaining words", "count": 1, "rank": 0.04183918269599732}, {"index": 25, "text": "this blog", "count": 1, "rank": 0.03843170565737933}, {"index": 26, "text": "some popular algorithms", "count": 1, "rank": 0.038087584823861424}, {"index": 27, "text": "top", "count": 1, "rank": 0.03691431910843899}, {"index": 28, "text": "the percentage", "count": 1, "rank": 0.035644214361701745}, {"index": 29, "text": "a graph", "count": 1, "rank": 0.03556661207159536}, {"index": 30, "text": "the graph", "count": 1, "rank": 0.03556661207159536}, {"index": 31, "text": "TextRank", "count": 1, "rank": 0.03258550335641341}, {"index": 32, "text": "the text", "count": 1, "rank": 0.03174034167736255}, {"index": 33, "text": "a paper", "count": 2, "rank": 0.030399026739071213}, {"index": 34, "text": "another incubator student", "count": 1, "rank": 0.027890118936814874}, {"index": 35, "text": "The weight", "count": 1, "rank": 0.01951356399645739}, {"index": 36, "text": "the weights", "count": 1, "rank": 0.01951356399645739}, {"index": 37, "text": "the vertices(sentences", "count": 1, "rank": 0.017049993659367196}, {"index": 38, "text": "an improvement", "count": 1, "rank": 0.015050599307603788}, {"index": 39, "text": "It", "count": 3, "rank": 0.0}, {"index": 40, "text": "both", "count": 1, "rank": 0.0}, {"index": 41, "text": "that", "count": 1, "rank": 0.0}, {"index": 42, "text": "them", "count": 1, "rank": 0.0}, {"index": 43, "text": "words", "count": 2, "rank": 0.0}]}}, {"mode": "vega-lite"});
</script>



## Extractive Summarization

Again, working with the most recent document above, we'll summarize based on its top `15` phrases, yielding its top `5` sentences...


```python
for sent in tr.summary(limit_phrases=15, limit_sentences=5):
    ic(sent)
```

    ic| sent: First, a quick description of some popular algorithms & implementations for text summarization that exist today: the summarization module in gensim implements TextRank, an unsupervised algorithm based on weighted-graphs from a paper by Mihalcea et al.
    ic| sent: It is an improvement from a paper by Barrios et al.
    ic| sent: It is built on top of the popular PageRank algorithm that Google used for ranking webpages.
    ic| sent: Create a graph where vertices are sentences.
    ic| sent: In original TextRank the weights of an edge between two sentences is the percentage of words appearing in both of them.


## Using TopicRank

The *TopicRank* enhanced algorithm is simple to use in the `spaCy` pipeline and it supports the other features described above:


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("topicrank");
```

Let's load an example text:


```python
text = pathlib.Path("../dat/cfc.txt").read_text()
text
```




    " Chelsea 'opted against' signing Salomon Rondón on deadline day.\n\nChelsea reportedly opted against signing Salomón Rondón on deadline day despite their long search for a new centre forward. With Olivier Giroud expected to leave, the Blues targeted Edinson Cavani, Dries Mertens and Moussa Dembele – only to end up with none of them. According to Telegraph Sport, Dalian Yifang offered Rondón to Chelsea only for them to prefer keeping Giroud at the club. Manchester United were also linked with the Venezuela international before agreeing a deal for Shanghai Shenhua striker Odion Ighalo. Manager Frank Lampard made no secret of his transfer window frustration, hinting that to secure top four football he ‘needed’ signings. Their draw against Leicester on Saturday means they have won just four of the last 13 Premier League matches."




```python
doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='Salomon Rondón',
                       chunks=[Salomon Rondón, Salomón Rondón, Rondón],
                       count=3,
                       rank=0.07866221348202057)
    ic| phrase: Phrase(text='Chelsea',
                       chunks=[Chelsea, Chelsea, Chelsea],
                       count=3,
                       rank=0.06832817272016853)
    ic| phrase: Phrase(text='Olivier Giroud',
                       chunks=[Olivier Giroud, Giroud],
                       count=2,
                       rank=0.05574966582168716)
    ic| phrase: Phrase(text='deadline day',
                       chunks=[deadline day, deadline day],
                       count=2,
                       rank=0.05008120527495589)
    ic| phrase: Phrase(text='Leicester', chunks=[Leicester], count=1, rank=0.039067778208486274)
    ic| phrase: Phrase(text='club', chunks=[club], count=1, rank=0.037625206033098234)
    ic| phrase: Phrase(text='Edinson Cavani',
                       chunks=[Edinson Cavani],
                       count=1,
                       rank=0.03759951959121995)
    ic| phrase: Phrase(text='draw', chunks=[draw], count=1, rank=0.037353607917351345)
    ic| phrase: Phrase(text='Manchester United',
                       chunks=[Manchester United],
                       count=1,
                       rank=0.035757812045215435)
    ic| phrase: Phrase(text='Dalian Yifang',
                       chunks=[Dalian Yifang],
                       count=1,
                       rank=0.03570018233618092)


## Using Biased TextRank

The *Biased TextRank* enhanced algorithm is simple to use in the `spaCy` pipeline and it supports the other features described above:


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("biasedtextrank");
```


```python
doc = nlp(text)

focus = "Leicester"
doc._.textrank.change_focus(focus,bias=10.0,  default_bias=0.0)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='Leicester',
                       chunks=[Leicester, Leicester],
                       count=2,
                       rank=0.26184834028994514)
    ic| phrase: Phrase(text='Saturday',
                       chunks=[Saturday, Saturday],
                       count=2,
                       rank=0.13938186779355857)
    ic| phrase: Phrase(text='the last 13 Premier League matches',
                       chunks=[the last 13 Premier League matches],
                       count=1,
                       rank=0.12502820319236171)
    ic| phrase: Phrase(text='none', chunks=[none], count=1, rank=1.9498221604845646e-07)
    ic| phrase: Phrase(text='Moussa Dembele',
                       chunks=[Moussa Dembele, Moussa Dembele],
                       count=2,
                       rank=8.640024414329197e-08)
    ic| phrase: Phrase(text='Dries Mertens',
                       chunks=[Dries Mertens, Dries Mertens],
                       count=2,
                       rank=5.152284728493906e-08)
    ic| phrase: Phrase(text='Edinson Cavani',
                       chunks=[Edinson Cavani],
                       count=1,
                       rank=3.076049036231119e-08)
    ic| phrase: Phrase(text='a new centre',
                       chunks=[a new centre],
                       count=1,
                       rank=2.7737546970070932e-08)
    ic| phrase: Phrase(text='the Blues targeted Edinson Cavani',
                       chunks=[the Blues targeted Edinson Cavani],
                       count=1,
                       rank=1.9405864014707633e-08)
    ic| phrase: Phrase(text='deadline day',
                       chunks=[deadline day, deadline day],
                       count=2,
                       rank=1.3752326412669907e-08)


The top-ranked phrases from *Biased TextRank* are closely related to the "focus" item: `Leicester`

## Using PositionRank

The *PositionRank* enhanced algorithm is simple to use in the `spaCy` pipeline and it supports the other features described above:

## Using PositionRank

The *PositionRank* enhanced algorithm is simple to use in the `spaCy` pipeline and it supports the other features described above:


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("positionrank");
```


```python
doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='deadline day',
                       chunks=[deadline day, deadline day],
                       count=2,
                       rank=0.1671249044190727)
    ic| phrase: Phrase(text='Salomon Rondón',
                       chunks=[Salomon Rondón, Salomon Rondón],
                       count=2,
                       rank=0.14836718147498046)
    ic| phrase: Phrase(text='Salomón Rondón',
                       chunks=[Salomón Rondón, Salomón Rondón],
                       count=2,
                       rank=0.14169986334846618)
    ic| phrase: Phrase(text='Chelsea',
                       chunks=[Chelsea, Chelsea, Chelsea, Chelsea],
                       count=4,
                       rank=0.13419811872859874)
    ic| phrase: Phrase(text='Rondón', chunks=[Rondón], count=1, rank=0.12722264594603172)
    ic| phrase: Phrase(text='a new centre',
                       chunks=[a new centre],
                       count=1,
                       rank=0.09181159181129885)
    ic| phrase: Phrase(text='Giroud', chunks=[Giroud, Giroud], count=2, rank=0.0783201596831592)
    ic| phrase: Phrase(text='Olivier Giroud',
                       chunks=[Olivier Giroud, Olivier Giroud],
                       count=2,
                       rank=0.07805316118093475)
    ic| phrase: Phrase(text='none', chunks=[none], count=1, rank=0.07503538984105931)
    ic| phrase: Phrase(text='their long search',
                       chunks=[their long search],
                       count=1,
                       rank=0.07449683199895643)


The top-ranked phrases from *PositionRank* are closely related to the "lead" items: `Chelsea`, `deadline day`, `Salomon Rondón`

## Baseline

Now let's re-run this pipeline with the baseline *TextRank* algorithm to compare results:


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")
doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='Shanghai Shenhua striker Odion Ighalo',
                       chunks=[Shanghai Shenhua striker Odion Ighalo,
                               Shanghai Shenhua striker Odion Ighalo],
                       count=2,
                       rank=0.11863090071749424)
    ic| phrase: Phrase(text='none', chunks=[none], count=1, rank=0.09802416183300769)
    ic| phrase: Phrase(text='Moussa Dembele',
                       chunks=[Moussa Dembele, Moussa Dembele],
                       count=2,
                       rank=0.09341044332809736)
    ic| phrase: Phrase(text='deadline day',
                       chunks=[deadline day, deadline day],
                       count=2,
                       rank=0.09046182507994752)
    ic| phrase: Phrase(text='Dries Mertens',
                       chunks=[Dries Mertens, Dries Mertens],
                       count=2,
                       rank=0.08919649435994934)
    ic| phrase: Phrase(text='Edinson Cavani',
                       chunks=[Edinson Cavani],
                       count=1,
                       rank=0.08418633972470349)
    ic| phrase: Phrase(text='Salomon Rondón',
                       chunks=[Salomon Rondón, Salomon Rondón],
                       count=2,
                       rank=0.08228367707127111)
    ic| phrase: Phrase(text='Salomón Rondón',
                       chunks=[Salomón Rondón, Salomón Rondón],
                       count=2,
                       rank=0.08228367707127111)
    ic| phrase: Phrase(text='Rondón', chunks=[Rondón], count=1, rank=0.0750732870664833)
    ic| phrase: Phrase(text='Dalian Yifang',
                       chunks=[Dalian Yifang, Dalian Yifang],
                       count=2,
                       rank=0.06681675615287698)


The baseline algorithm is picking up named entities, although not emphasizing the order in which these entities were introduced in the text.
