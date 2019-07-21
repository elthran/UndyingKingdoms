#!/usr/bin/env bash

source bin/config.sh

ssh -t $HOST '
cd UndyingKingdoms
bash -l
'
