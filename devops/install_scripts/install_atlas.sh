#!/bin/bash

wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh -O ~/miniconda.sh
bash $HOME/miniconda.sh -b -p $HOME/miniconda
eval "$($(pwd)/miniconda/bin/conda shell.bash hook)"
conda init
source ~/.bashrc

# create conda env for atlas installation if not already exists
if [[ $(conda env list | grep atlas_ce_env | awk '{print $1}') != 'atlas_ce_env' ]]; then
   conda update -n base -c defaults conda --yes
   conda create -n atlas_ce_env python=3.6 --yes
fi

if [[ `which python` != '$HOME/miniconda/bin/python' ]]; then
  # activate the environment
  eval "$(conda shell.bash hook)"
  conda activate atlas_ce_env
fi

echo "using python from `which python`"

if [ ! -f atlas_ce_installer.py ]; then
   wget https://s3.amazonaws.com/foundations-public/atlas_ce_installer.py
fi

MAIN_PATH=`which python | grep -o '^.*atlas_ce_env'`/lib/python3.6/site-packages/atlas-server/

if [ ! -d ${MAIN_PATH} ]; then
   yes | python atlas_ce_installer.py

 # ip fix
 echo -e "import urllib.request\nexternal_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')" > ${MAIN_PATH}/new_main.py
 cat ${MAIN_PATH}/__main__.py >> ${MAIN_PATH}/new_main.py
 sed -i 's/"localhost"/f"\{external_ip\}"/g' ${MAIN_PATH}/new_main.py
 sed -i 's@localhost:@\{external_ip\}:@g' ${MAIN_PATH}/new_main.py
 mv ${MAIN_PATH}/new_main.py ${MAIN_PATH}/__main__.py
fi

if [[ `sudo lsof -i:5555` == '' ]]; then
   atlas-server start > /dev/null 2>&1 &
fi

cd
mkdir atlas-tutorials && cd atlas-tutorials
git clone https://github.com/DeepLearnI/auction-price-regression-tutorial.git
