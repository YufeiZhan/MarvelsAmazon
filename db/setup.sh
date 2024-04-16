#!/bin/bash

# Make sure to be in the directory where the script file is
mypath=`realpath "$0"`
mybase=`dirname "$mypath"`
cd $mybase

# See whether the 'generated' argument is passed in 
datadir="${1:-data/}" # use either generate/ or data/ by default
if [ ! -d $datadir ] ; then
    echo "$datadir does not exist under $mybase"
    exit 1
fi

source ../.flaskenv
dbname=$DB_NAME

# Create new database and drop the current one
if [[ -n `psql -lqt | cut -d \| -f 1 | grep -w "$dbname"` ]]; then
    dropdb $dbname
fi
createdb $dbname

# Initialze the database and load the data
psql -af create.sql $dbname
cd $datadir
psql -af $mybase/load.sql $dbname
