# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conodictor']

package_data = \
{'': ['*']}

install_requires = \
['bio>=1.3.3,<2.0.0',
 'exitstatus>=2.2.0,<3.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pyfastx>=0.8.4,<0.9.0']

entry_points = \
{'console_scripts': ['conodictor = conodictor.conodictor:main']}

setup_kwargs = {
    'name': 'conodictor',
    'version': '2.3.6',
    'description': 'Prediction and classification of conopeptides',
    'long_description': "[![PyPI](https://img.shields.io/pypi/v/conodictor.svg)](https://pypi.org/project/conodictor)\n[![Wheel](https://img.shields.io/pypi/wheel/conodictor.svg)](https://pypi.org/project/conodictor)\n[![Language](https://img.shields.io/pypi/implementation/conodictor)](https://pypi.org/project/conodictor)\n[![Pyver](https://img.shields.io/pypi/pyversions/conodictor.svg)](https://pypi.org/project/conodictor)\n[![Downloads](https://img.shields.io/pypi/dm/conodictor)](https://pypi.org/project/conodictor)\n[![Docker](https://img.shields.io/docker/pulls/ebedthan/conodictor.svg)]()\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\n\n## ConoDictor: A fast and accurate prediction and classification tool for conopeptides\n\n\n### Important\nIf using conodictor and have issue like [CONODB issue](https://github.com/koualab/conodictor/issues/18), please update to v2.3.6 that provide a fix.\n\nconodictor v2.3.6 introduce the -d option to specify the path to the db folder containing HMM and PSSM files for classification.\n\nThis is a temporary solution while I am working on the next big release. Thanks.\n\n### Introduction\n\nCone snails are among the richest sources of natural peptides with promising pharmacological and therapeutic applications. With the reduced costs of RNAseq, scientists now heavily rely on venom gland transcriptomes for the mining of novel bioactive conopeptides, but the bioinformatic analyses often hamper the discovery process.\n\nConoDictor 2 is a standalone and user-friendly command-line program. We have updated the program originally published as a web server 10 years ago using novel and updated tools and algorithms and improved our classification models with new and higher quality sequences. ConoDictor 2 is now more accurate, faster, multiplatform, and able to deal with a whole cone snail venom gland transcriptome (raw reads or contigs) in a very short time.\n\nThe only input ConoDictor 2 requires is the assembled transcriptome or the raw reads file either in DNA or amino acid: the used alphabet is automatically recognized. ConoDictor 2 runs predictions directly on the proteins file (submitted or dynamically generated) and tries to report the longest conopeptide precursor-like sequence.\n\n### Installation\n\n#### Install from Pip\n\nYou will have first to install [HMMER 3](https://hmmer.org) and [Pftools](https://github.com/sib-swiss/pftools3) to be able to run conodictor.\n\n```bash\npip install conodictor\n```\n\n#### Using containers\n\n#### Docker\n\nAccessible at https://hub.docker.com/u/ebedthan or on [BioContainers](https://github.com/BioContainers/containers/tree/master/conodictor/2.2.2).\n\n\n```bash\ndocker pull ebedthan/conodictor:latest\ndocker run ebedthan/conodictor:latest conodictor -h\n```\n\nExample of a run\n\n```bash\ndocker run --rm=True -v $PWD:/data -u $(id -u):$(id -g) ebedthan/conodictor:latest conodictor --out /data/outdir /data/input.fa.gz\n```\n\nSee https://staph-b.github.io/docker-builds/run_containers/ for more informations on how to properly run a docker container.\n\n\n#### Singularity\n\nThe singularity container does not need admin privileges making it\nsuitable for university clusters and HPC.\n\n```bash\nsingularity build conodictor.sif docker://ebedthan/conodictor:latest\nsingularity exec conodictor.sif conodictor -h\n```\n\n\n#### Install from source\n\n```bash\n# Download ConoDictor development version\ngit clone https://github.com/koualab/conodictor.git conodictor\n\n# Navigate to directory\ncd conodictor\n\n# Install with poetry: see https://python-poetry.org\npoetry install --no-dev\n\n# Enter the Python virtual environment with\npoetry shell\n\n# Test conodictor is correctly installed\nconodictor -h\n```\n\nIf you do not want to go into the virtual environment just do:\n\n```bash\npoetry run conodictor -h\n```\n\n## Test\n\n* Type `conodictor -h` and it should output something like:\n\n```\nusage: conodictor [options] <FILE>\n\noptional arguments:\n  -o DIR, --out DIR   output result to DIR [ConoDictor]\n  --mlen INT          minimum length of sequences to be considered [off]\n  --ndup INT          minimum occurence sequences to be considered [off]\n  --faa               dump a fasta file of matched sequences [false]\n  --filter            only keep sequences matching sig, pro and mat regions [false]\n  -a, --all           add unclassified sequences in result [false]\n  -j INT, --cpus INT  number of threads [1]\n  --force             re-use output directory [false]\n  -q, --quiet         decrease program verbosity\n  -v, --version       show program's version number and exit\n  -h, --help          show this help message and exit\n\nCitation: Koua et al., 2021, Bioinformatics Advances\n```\n\n\n## Invoking conodictor\n\n```bash\nconodictor file.fa.gz\nconodictor --out outfolder --cpus 4 --mlen 51 file.fa\n```\n  \n\n## Output files\n\nThe comma separeted-values file summary.csv can be easily viewed with any office suite,\nor text editor.\n\n```csv\nsequence,hmm_pred,pssm_pred definitive_pred\nSEQ_ID_1,A,A,A\nSEQ_ID_2,B,D,CONFLICT B and D\nSEQ_ID_3,O1,O1,O1\n...\n\n```\n\n## Citation\n\nWhen using ConoDictor2 in your work, you should cite:\n\nDominique Koua, Anicet Ebou, Sébastien Dutertre, Improved prediction of conopeptide superfamilies with ConoDictor 2.0, Bioinformatics Advances, Volume 1, Issue 1, 2021, vbab011, https://doi.org/10.1093/bioadv/vbab011.\n  \n## Bugs\n\nSubmit problems or requests to the [Issue Tracker](https://github.com/koualab/conodictor/issues).\n\n\n## Dependencies\n\n### Mandatory\n\n* [**HMMER 3**](https://hmmer.org)  \n  Used for HMM profile prediction.   \n  *Eddy SR, Accelerated Profile HMM Searches. PLOS Computational Biology 2011, 10.1371/journal.pcbi.1002195*\n\n* [**Pftools**](https://github.com/sib-swiss/pftools3)  \n  Used for PSSM prediction.    \n  *Schuepbach P et al. pfsearchV3: a code acceleration and heuristic to search PROSITE profiles. Bioinformatics 2013, 10.1093/bioinformatics/btt129*\n\n\n## Licence\n\n[GPL v3](https://github.com/koualab/conodictor/blob/main/LICENSE).\n\nFor commercial uses please contact Dominique Koua at dominique.koua@inphb.ci.\n\n## Authors\n\n* [Anicet Ebou](https://orcid.org/0000-0003-4005-177X)\n* [Dominique Koua](https://www.researchgate.net/profile/Dominique_Koua)",
    'author': 'Anicet Ebou',
    'author_email': 'anicet.ebou@gmail.com',
    'maintainer': 'Anicet Ebou',
    'maintainer_email': 'anicet.ebou@gmail.com',
    'url': 'https://github.com/koualab/conodictor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
