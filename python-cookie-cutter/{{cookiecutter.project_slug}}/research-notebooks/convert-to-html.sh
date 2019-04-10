#!/bin/bash

jupyter nbconvert --to html --template ./clean_code.tpl "$1"
