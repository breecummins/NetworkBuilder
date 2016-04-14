#!/bin/bash

# Argument is results file

. ./makedatabases.sh
. ./loopthroughdb.sh > $1
. ./movedatabases.sh