#!/bin/bash

ROOT=$(pwd)
TABCPP_CURRENT=${ROOT}:${TABCPP_ROOT}

export PYTHONPATH=${TABCPP_ROOT}:${ROOT}/${2}

if [ -f "${ROOT}/construct_table.py" ] 
then 
    ${ROOT}/construct_table.py ${2} ${ROOT}/${1} 
else
    construct_table.py ${1} ${2} ${3} ${4}
fi

