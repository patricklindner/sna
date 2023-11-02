#!/bin/bash

#SBATCH --job-name=communitiest    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=p.m.lindner@student.rug.nl     # Where to send mail
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --mem=2gb                     # Job memory request
#SBATCH --output=out.log   # Standard output and error log

echo activating environment

source venv/bin/activate

echo starting girvan newman
python communities.py