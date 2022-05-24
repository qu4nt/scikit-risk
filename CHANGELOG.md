**CONSTRUIR a partir de ejemplo en sckit-bio**

# scikit-bio changelog

## Version 0.5.8-dev

### Features

* Added NCBI taxonomy database dump format (`taxdump`) ([#1810](https://github.com/biocore/scikit-bio/pull/1810)).
* Added `TreeNode.from_taxdump` for converting taxdump into a tree ([#1810](https://github.com/biocore/scikit-bio/pull/1810)).

## Version 0.5.7

### Features

* Introduce support for Python 3.10 ([#1801](https://github.com/biocore/scikit-bio/pull/1801)).
* Tentative support for Apple M1 ([#1709](https://github.com/biocore/scikit-bio/pull/1709)).
* Added support for reading and writing a binary distance matrix object format. ([#1716](https://github.com/biocore/scikit-bio/pull/1716))
* Added support for `np.float32` with `DissimilarityMatrix` objects.
* Added support for method and number_of_dimensions to permdisp reducing the runtime by 100x at 4000 samples, [issue #1769](https://github.com/biocore/scikit-bio/pull/1769).
* OrdinationResults object is now accepted as input for permdisp.
