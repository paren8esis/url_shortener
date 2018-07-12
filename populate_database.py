#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for populating the URL shortener database with the words included in
a specified .txt file.

Must be run once after the installation of the app.
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'url_shortener_project.settings')

import django
django.setup()

from tqdm import tqdm
import argparse

from url_shortener.models import Letter, Word


def populate(file_path):
    '''
    Reads the specified file and populates a SQLite database with its contents.

    Parameters
    ----------
    file_path: str
        The path of the file with which we will populate the database.
    '''

    # Check whether the given file_path is valid.
    if not os.path.isfile(file_path):
        print('The specified file does not exist')
        exit(1)

    # Create a dictionary mapping letter -> word list.
    letters = {}
    with open(file_path, 'r') as f:
        for line in f:
            letter = line[0]
            if letter not in letters.keys():
                letters[letter] = [line]
            else:
                letters[letter].append(line)

    # Save the dictionary elements to the database
    for letter, words in tqdm(letters.items()):
        let = add_letter(letter, len(words))
        for word_id in range(len(words)):
            add_word(words[word_id], word_id, let)


def add_letter(letter, num_words=0):
    '''
    Saves a Letter object in the database.
    '''
    let = Letter.objects.get_or_create(letter=letter, current_index=0,
                                       num_words=num_words)[0]
    let.save()
    return let


def add_word(word, word_id, letter):
    '''
    Saves a Word object in the database.
    '''
    w = Word.objects.get_or_create(word=word,
                                   word_id=word_id,
                                   letter=letter)[0]
    w.save()
    return w


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="A path of the file to be used in order to populate the database. File must be in a .txt format.")
    args = parser.parse_args()

    print("Starting the database population script.\nThis might take several minutes.")
    populate(args.file_path)
