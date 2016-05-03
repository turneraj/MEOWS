Title: README for MEOWS
Version: 0.1(4 May 2016)
Author: A.J. Turner -- created for BIOL 7800 at Louisiana State University
Created: April 2016
Edited: May 2016

MEOWS
=====

Multi-step Eliminating Operational Workflow for Sequences
---------------------------------------------------------

###Overview
Multi-step Eliminating Operational Workflow for Sequences, affectionately
called **MEOWS**, is a program used to automatically generate a maximum
likelihood phylogeny for its users. As a user, you simply input a `fasta`
file that contains one sequence for your locus of interest. MEOWS uses *NCBI's
BLAST* to check the identify of the `input sequence`, returning the genus to
screen, and then proceeds to download sequence data for every species within
the specified genus for the locus under study. These sequences are then aligned
by creating a subprocess to **MUSCLE**, after which the `muscle_output` is then
subprocessed to **RAxML** to construct a maximum likelihood phylogeny.

###Program Requirements
In order to run MEOWS, you will need:
    * Python 3.5
    link to [Python website](https://www.python.org/downloads/release/python-350/)
    * MUSCLE
    link to [MUSCLE website](http://www.drive5.com/muscle/)
    * RAxML
    link to [RAxML website](http://sco.h-its.org/exelixis/web/software/raxml/)

###Acknowledgments
Ideas and coding suggestions for this program were provided by Fernando
Alda and Subir Shakya. Additional coding help was provided by Brant Faircloth,
specifically dealing with the use of subprocess.

###Citations
1. A. Stamatakis: "RAxML Version 8: A tool for Phylogenetic Analysis and
Post-Analysis of Large Phylogenies". In Bioinformatics, 2014, open access.

2. http://stackoverflow.com/questions/25362382 -- Using NCBI BLAST

3. https://www.biostars.org/p/131113/ -- Using NCBI BLAST

4. Cite the people who uploaded the Limia sequence being used in example
