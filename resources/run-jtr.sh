#!/bin/bash

set -o errexit
set -o nounset

john --wordlist="combined-password.lst" \
    --format=PKZIP \
    --pot="flag.pot" \
    "flag.hash"

if [ -s "flag.pot" ]
then
  echo "[*] Password found!"
  exit 0
else
  echo "[-] Password not found."
  exit 1
fi
