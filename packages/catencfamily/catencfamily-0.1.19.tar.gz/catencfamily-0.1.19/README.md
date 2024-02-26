# catencfamily

The module provides a way to encode categorical features in multiple but related ways using network analysis. Together, the family of multiple encodings serve as a numerical vector for every level of a categorical feature. The class transforms a group of categorical features into corresponding numerical features which can then be used either in unsupervised learning or in predictive analytics. To assist in unsupervised learning, it has methods to save a categorical feature as network graphs and plot them. The class has methods to extract unit vectors for every level of a categorical feature to help, for example, in understanding relationshsips between various levels. Extracted numerical vectors can directly be used in plotting, for example, in tensorflow's Embedding Projector. Class provides methods to get categories encoded for large datasets; one can, for example, take a sample of data at a time, have categories encoded, then take another sample and have categories similarly encoded. After a number of iterations, take either a mean or median to get final category-wise vectors. As the encodings are calculated using a group of network analysis operations, the family of encodings is extensible. The class provides one way, but a limited one to extend it.

## Installation

<code>pip install catencfamily</code>

### Requirements
<pre><code>
python >= 3.7
pandas
numpy
networkx
cdlib
scikit-learn
matplotlib
pathlib</code></pre>


## License

_MIT License. Any contribution is welcome!
