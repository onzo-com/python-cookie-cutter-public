#!/bin/bash
cd "$(dirname "$0")"

scriptversion="0.0.0.0"

#if no cmd line params
if [ -z "$1" ]
  then
    rake default
    exit $?
fi

rake $1
exit $?
