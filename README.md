# LandmarksViewer

Script for converting [OCaml Landmarks](https://github.com/LexiFi/landmarks) profiling result (not aggregated) into HTML with styling to collapse/expand functions summaries and highlight lines with usage in percentage more than given (if given) threshold.
Written during yet another unconsciousness attack hence is very ugly etc.

## Usage

`create_tree.py [-h] -i FILE -o FILE [-t PERCENTAGE]`

Pass in and out files paths with optional threshold to add highlights

Options:
`-h, --help` show this help message and exit
`-i FILE, --in FILE` path to Landmarks summary
`-o FILE, --out FILE` path to html result
`-t PERCENTAGE, --threshold PERCENTAGE` threshold for usage percentage for highliting (0 to 100)

## Prelude

Log file is supposed to look like:

[    3.56G cycles in 1 calls ]     - 100.00% : load(test)
[    3.56G cycles in 1 calls ]     |   - 100.00% : Test.main
[    2.21G cycles in 1 calls ]     |   |   - 62.05% : Test.zzz_1
[    1.10G cycles in 1 calls ]     |   |   - 31.04% : Test.zzz_05
[  221.00M cycles in 1 calls ]     |   |   -  6.21% : Test.zzz_01
