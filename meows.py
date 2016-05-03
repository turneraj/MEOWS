#!/usr/bin/env python
# encoding: utf-8

"""
Multi-step Eliminating Operational Workflow for Sequences, colloquially
called **MEOWS**, is a program used to automatically generate a maximum
likelihood phylogeny for its users. As a user, you simply input a FASTA
file that contains one sequence for your locus of interest. MEOWS uses **NCBI's
BLAST** to check the identify of the input sequence, returning the genus to
screen, and then proceeds to download sequence data for every species within
the specified genus for the locus under study. These sequences are then aligned
by creating a subprocess to **MUSCLE**, after which the `muscle_output` is then
subprocessed to **RAxML** to construct a maximum likelihood phylogeny.

Created by A.J. Turner, April 2016.

"""

import argparse
from Bio import Entrez
from Bio import SeqIO
from Bio.Blast import NCBIXML
from Bio.Blast import NCBIWWW
import time
import subprocess
import shlex


def file_info():
    '''input of email, fasta file path, gene name, and path to MUSCLE
    and RAxML executible files from user'''
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True, help="enter --input followed\
    by email address", type=str)
    parser.add_argument("--input", required=True, help="enter --input followed\
    by path of input file (drop to commandline is easiest)", type=str)
    parser.add_argument("--gene", required=True, help="enter --gene followed\
    by name of gene for your sequence", type=str)
    parser.add_argument("--muscle_path", required=True, help="enter \
    --muscle_path and the exact path to MUSCLE executible file", type=str)
    parser.add_argument("--raxml_path", required=True, help="enter --raxml_path\
    followed by the exact path to the RAxML executible file", type=str)
    args = parser.parse_args()
    return args


def get_seq(args):
    seq = open(args.input, 'rU')
    upload = SeqIO.read(seq, "fasta")
    seq.close()
    return upload.seq


def blast_it(fasta):
    '''getting blast hit from ncbi to obtain gi number'''
    #  https://www.biostars.org/p/131113/
    #  http://stackoverflow.com/questions/25362382/
    result = NCBIWWW.qblast("blastn", "nt", fasta, hitlist_size=1)
    save_file = open("my_blast.xml", "w")
    save_file.write(result.read())
    save_file.close()
    blast_xml = open("my_blast.xml")
    blast_record = NCBIXML.read(blast_xml)
    gi = blast_record.alignments[0].title.split("|")[1]
    return gi


def get_genus(gi):
    '''Using the gi number to obtain the name of the genus identified by seq'''
    seq_genus = Entrez.efetch(
        db="nucleotide",
        id=gi,
        rettype="gb",
        retmode="text"
        )
    genus_result = SeqIO.read(seq_genus, "genbank")
    my_genus = genus_result.annotations['organism'].split(" ")[0]
    print('\nYour sequence was identified within the genus:', my_genus)
    return my_genus


def download_seqs(my_genus, args):
    '''Extracting the gi numbers associated with sequence data for all
    species in the same genus, then using those gi numbers to download all
    available sequences.'''
    search = my_genus+" AND "+args.gene
    query = Entrez.esearch(
        db="nucleotide",
        term=search,
        rettype="gb",
        retmode="text"
        )
    result = Entrez.read(query)
    get_ids = result['IdList']
    get_seqs = []
    for my_id in get_ids:
        query = Entrez.efetch(
            db="nucleotide",
            id=my_id,
            rettype='gb',
            retmode='text'
            )
        seq = SeqIO.read(query, 'genbank')
        get_seqs.append(seq)
        time.sleep(1)
    return get_seqs


def write_fasta(get_seqs, my_genus):
    '''writing sequences from text file to fasta file'''
    with open("all_blast_seqs", 'w') as outfile:
        SeqIO.write(get_seqs, outfile, 'fasta')
    print("All", my_genus, "sequences are in the file: all_blast_seqs")


def muscle_align(args):
    '''Using subprocess to align all sequences downloaded via muscle. Coding
    help provided by Mike Henson'''
    fasta_file = "all_blast_seqs"
    output_file = "muscle_output"
    text_command = args.muscle_path+' -in {} -out {}'.format(
        fasta_file,
        output_file
        )
    cmd = shlex.split(text_command)
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
        )
    if process.returncode == 0:
        pass
    else:
        raise (
            'An Error occurred with your subprocess\n{}'.format(process.stderr)
            )


def raxml(args):
    numberOfThreads = "2"
    sequences = "muscle_output"
    model = "GTRGAMMA"
    parsimony_seed = "12345"
    rapid_bootstrap_seed = " 12345"
    num_replicates = "200"
    name = "raxml_analysis"
    text_command = args.raxml_path+' -T {} -f a -s {} -m {} -p {} -x {}\
     -N {} -n {}'.format(
        numberOfThreads,
        sequences,
        model,
        parsimony_seed,
        rapid_bootstrap_seed,
        num_replicates,
        name
        )
    cmd = shlex.split(text_command)
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
        )
    if process.returncode == 0:
        pass
    else:
        raise (
            'An Error occurred with your subprocess\n{}'.format(process.stderr)
            )


def main():
    args = file_info()
    Entrez.email = args.email
    fasta = get_seq(args)
    gi = blast_it(fasta)
    my_genus = get_genus(gi)
    get_seqs = download_seqs(my_genus, args)
    write_fasta(get_seqs, my_genus)
    muscle_align(args)
    print("Your muscle alignment file is: muscle_output\n")
    raxml(args)


if __name__ == '__main__':
    main()
