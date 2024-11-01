#!/usr/bin/env python3

import itertools
import math
import random
import subprocess
import time
from datetime import timedelta

# https://www.ef.com/wwen/english-resources/english-vocabulary/top-3000-words/
wordlist = '3000-most-common-words-in-English'

start_time_total = time.time()

with open(wordlist, 'r') as f:
    words = f.read().splitlines()
    total_size = f.tell()

print(f'[*] Characters in the wordlist file: {total_size:,}')

# add 'password' to the wordlist
print("[*] Add 'password' to wordlist")
words.append('password')
total_size += 8

number_of_words = len(words)
print(f'[*] Number of words: {number_of_words:,}')

# shuffle the list, start with randomly choosen seed
print('[*] Shuffle wordlist')
random.seed(785)
random.shuffle(words)

words_per_permutation = 3
print(f'[*] Words per permutation: {words_per_permutation}')
number_of_permutations = math.perm(number_of_words, words_per_permutation)
print(f'[*] Number of permutations: {number_of_permutations:,}')

average_length_per_string = total_size / number_of_words
estimated_total_size = int(number_of_permutations * (words_per_permutation * average_length_per_string))
print(f'[*] Estimated size of permutation wordlist: ~ {estimated_total_size:,} bytes')

part = 0
permutations = itertools.permutations(words, words_per_permutation)

reached_end = False
while not reached_end:
    print(f'[*] Start writing permutation wordlist part #{part}')
    start_time_chunk = time.time()
    with open(f'combined-password.lst', 'w') as f:
        reached_end = True
        for _ in permutations:
            reached_end = False
            f.write(''.join(_))
            f.write('\n')
            # write the permutation wordlist in chunks of 1GB
            if f.tell() > 1_000_000_000:
                break
        end_time_chunk = time.time()
        duration_chunk = timedelta(seconds=end_time_chunk - start_time_chunk)
        print(f'[+] Finished writing permutations to file'
              f' - Duration: {duration_chunk}')
    if reached_end:
        print('[-] Password was not found')
        break
    else:
        print(f'[*] Start cracking part #{part}')
        part += 1
        proc = subprocess.Popen(['./run-jtr.sh'], encoding='utf-8', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        proc.wait()
        if proc.returncode == 0:
            print('[+] Password found - check the flag.pot file')
            break

end_time_total = time.time()

print(f'[*] Duration: {timedelta(seconds=end_time_total - start_time_total)}')
