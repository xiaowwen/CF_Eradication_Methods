This script runs kraken to analyse possible contamination in the sequence reads.
To run do:

python check_contamination_kraken1_paired.py path_to_paired_end_reads path_to_kraken executable.

It outputs a file that can be run locally on a workstation to generate the analysis or submitted 
(with prefacing resource request flags) to a supercomuting cluster

