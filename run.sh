#!/bin/bash

if [[ "$0" = "$BASH_SOURCE" ]]; then
    echo "Needs to be run using source: bash run.sh"

else
    if pip install --no-input --quiet virtualenv; then
        echo "Virtual environment ready to load"
    else
        echo "Python or pip is not setup properly"
        exit
    fi

    VENVPATH="env/bin/activate"

    if source "$VENVPATH"; then
        echo "Virtual environment activated"
    fi
fi


if [ -d "$PWD/Sample" -a -d "$PWD/7 files with range data"  ]; then
    echo "Dataset directories verified"
else
    echo "Dataset directories does not exists."
fi

if pip install --quiet -r requirements.txt; then
    echo "All dependencies been set up"
fi

python solve.py

deactivate

echo "exiting.."