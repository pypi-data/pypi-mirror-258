#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from collections import defaultdict
import logging

import pandas as pd

from mgnify_pipelines_toolkit.constants.tax_ranks import _SILVA_TAX_RANKS, _PR2_TAX_RANKS

logging.basicConfig(level=logging.DEBUG)

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--taxa", required=True, type=str, help="Path to DADA2 taxa file")
    parser.add_argument("-f", "--fwd", required=True, type=str, help="Path to DADA2 forward map file")
    parser.add_argument("-r", "--rev", required=False, type=str, help="Path to DADA2 reverse map file")
    parser.add_argument("-a", "--amp", required=True, type=str, help="Path to extracted amp_region reads from inference subworkflow")
    parser.add_argument("-hd", "--headers", required=True, type=str, help="Path to fastq headers")
    parser.add_argument("-s", "--sample", required=True, type=str, help="Sample ID")

    args = parser.parse_args()
  
    _TAXA = args.taxa
    _FWD = args.fwd
    _REV = args.rev
    _AMP = args.amp
    _HEADERS = args.headers
    _SAMPLE = args.sample

    return _TAXA, _FWD, _REV, _AMP, _HEADERS, _SAMPLE


def order_df(taxa_df):

    if len(taxa_df.columns) == 8:
        taxa_df = taxa_df.sort_values(_SILVA_TAX_RANKS, ascending=True)
    elif len(taxa_df.columns) == 10:
        taxa_df = taxa_df.sort_values(_PR2_TAX_RANKS, ascending=True)
    else:
        logging.error("Data frame not the right size, something wrong.")
        exit(1)

    return taxa_df

def make_tax_assignment_dict_silva(taxa_df, asv_dict):

    tax_assignment_dict = defaultdict(int)

    for i in range(len(taxa_df)):
        
        sorted_index = taxa_df.index[i]
        asv_count = asv_dict[sorted_index]

        if asv_count == 0:
            continue

        k = taxa_df.loc[sorted_index, "Kingdom"]
        p = taxa_df.loc[sorted_index, "Phylum"]
        c = taxa_df.loc[sorted_index, "Class"]
        o = taxa_df.loc[sorted_index, "Order"]
        f = taxa_df.loc[sorted_index, "Family"]
        g = taxa_df.loc[sorted_index, "Genus"]        
        s = taxa_df.loc[sorted_index, "Species"]

        tax_assignment = ""

        while True:

            if k != "0":
                k = "_".join(k.split(" "))
                if k == "Archaea" or k == "Bacteria":
                    tax_assignment += f"sk__{k}"
                elif k == "Eukaryota":
                    tax_assignment += f"sk__Eukaryota"
                else:
                    tax_assignment += f"sk__Eukaryota\tk__{k}"
            else:
                break

            if p != "0":
                if k == "Archaea" or k == "Bacteria":
                    tax_assignment += f"\tk__"
                p = "_".join(p.split(" "))
                tax_assignment += f"\tp__{p}"
            else:
                break
            if c != "0":
                c = "_".join(c.split(" "))
                tax_assignment += f"\tc__{c}"
            else:
                break
            if o != "0":
                o = "_".join(o.split(" "))
                tax_assignment += f"\to__{o}"
            else:
                break
            if f != "0":
                f = "_".join(f.split(" "))
                tax_assignment += f"\tf__{f}"
            else:
                break
            if g != "0":
                g = "_".join(g.split(" "))
                tax_assignment += f"\tg__{g}"
            else:
                break
            if s != "0":
                s = "_".join(s.split(" "))
                tax_assignment += f"\ts__{s}"
            break

        if tax_assignment == "":
            continue

        tax_assignment_dict[tax_assignment] += asv_count
    
    return tax_assignment_dict

def make_tax_assignment_dict_pr2(taxa_df, asv_dict):

    tax_assignment_dict = defaultdict(int)

    for i in range(len(taxa_df)):
        
        sorted_index = taxa_df.index[i]
        asv_count = asv_dict[sorted_index]

        if asv_count == 0:
            continue

        d = taxa_df.loc[sorted_index, "Domain"]
        sg = taxa_df.loc[sorted_index, "Supergroup"]
        dv = taxa_df.loc[sorted_index, "Division"]
        sdv = taxa_df.loc[sorted_index, "Subdivision"]
        c = taxa_df.loc[sorted_index, "Class"]
        o = taxa_df.loc[sorted_index, "Order"]
        f = taxa_df.loc[sorted_index, "Family"]
        g = taxa_df.loc[sorted_index, "Genus"]
        s = taxa_df.loc[sorted_index, "Species"]         

        tax_assignment = ""

        while True:

            if d != "0":
                d = "_".join(d.split(" "))
                tax_assignment += f"d__{d}"
            else:
                break

            if sg != "0":
                sg = "_".join(sg.split(" "))
                tax_assignment += f"\tsg__{sg}"
            else:
                break
            if dv != "0":
                dv = "_".join(dv.split(" "))
                tax_assignment += f"\tdv__{dv}"

            if sdv != "0":
                sdv = "_".join(sdv.split(" "))
                tax_assignment += f"\tsdv__{sdv}"
            if c != "0":
                c = "_".join(c.split(" "))
                tax_assignment += f"\tc__{c}"
            else:
                break
            if o != "0":
                o = "_".join(o.split(" "))
                tax_assignment += f"\to__{o}"
            else:
                break
            if f != "0":
                f = "_".join(f.split(" "))
                tax_assignment += f"\tf__{f}"
            else:
                break
            if g != "0":
                g = "_".join(g.split(" "))
                tax_assignment += f"\tg__{g}"
            else:
                break
            if s != "0":
                s = "_".join(s.split(" "))
                tax_assignment += f"\ts__{s}"
            break

        if tax_assignment == "":
            continue

        tax_assignment_dict[tax_assignment] += asv_count

    return tax_assignment_dict

def main():

    _TAXA, _FWD, _REV, _AMP, _HEADERS, _SAMPLE = parse_args()
    
    fwd_fr = open(_FWD, "r")
    paired_end = True

    if _REV == None:
        paired_end = False
        rev_fr = [True]
    else:
        rev_fr = open(_REV, "r")

    taxa_df = pd.read_csv(_TAXA, sep="\t", dtype=str)
    taxa_df = taxa_df.fillna("0")
    taxa_df = order_df(taxa_df)
    
    amp_reads = [ read.strip() for read in list(open(_AMP, "r")) ]
    headers = [ read.split(" ")[0][1:] for read in list(open(_HEADERS, "r")) ]
    amp_region = ".".join(_AMP.split(".")[1:3])

    asv_dict = defaultdict(int)

    counter = -1
    for line_fwd in fwd_fr:

        counter += 1
        line_fwd = line_fwd.strip()
        fwd_asvs = line_fwd.split(",")

        if paired_end:
            line_rev = next(rev_fr).strip()
            rev_asvs = line_rev.split(",")        
            asv_intersection = list(set(fwd_asvs).intersection(rev_asvs))
            
            if len(asv_intersection) == 0:
                continue
            
            if len(asv_intersection) == 1 and asv_intersection[0] == "0":
                continue
        else:
            asv_intersection = fwd_asvs

        if headers[counter] in amp_reads:
            asv_dict[int(asv_intersection[0]) - 1] += 1
    
    fwd_fr.close()
    if paired_end:
        rev_fr.close()

    ref_db = ""

    if len(taxa_df.columns) == 8:
        tax_assignment_dict = make_tax_assignment_dict_silva(taxa_df, asv_dict)
        ref_db = "silva"
    elif len(taxa_df.columns) == 10:
        tax_assignment_dict = make_tax_assignment_dict_pr2(taxa_df, asv_dict)
        ref_db = "pr2"

    with open(f"./{_SAMPLE}_{amp_region}_{ref_db}_asv_krona_counts.txt", "w") as fw:
        for tax_assignment, count in tax_assignment_dict.items():
            fw.write(f"{count}\t{tax_assignment}\n")
    

if __name__ == "__main__":
    main()