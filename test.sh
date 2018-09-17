#!/bin/bash
#

gitshow=$(git show)
echo "$gitshow"
IFS=$'\n'
gitlines=($gitshow)
echo ${gitlines[1]}
