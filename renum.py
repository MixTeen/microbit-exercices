#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Renumérote le fiches

import re
from os import listdir, remove, rename
from os.path import isdir, join

basepath = '.'
dir_regex = re.compile('^([0-9]+[0-9a-z.]*)_(.*)$')

dirs = sorted([d for d in listdir(basepath) if isdir(join(basepath, d)) and dir_regex.match(d)])

class Fiche:
    """ Fiche d'exercice"""
    def __init__(self, source_dir, target_num):
        self.source_dir = source_dir
        self.target_num = target_num
        dir_match = dir_regex.match(source_dir)
        self.source_num = dir_match.group(1)
        self.name = dir_match.group(2)

    def get_target_num(self):
        """Construit le numéro de fiche cible"""
        return str(self.target_num).zfill(2)

    def get_target_dir(self):
        """Construit le nom du dossier cible"""
        return "{0}_{1}".format(self.get_target_num(), self.name)

    def is_changed(self):
        """Indique si le dossier doit être renommé"""
        return self.get_target_num() != self.source_num

fiches = [Fiche(d, i + 1) for i, d in enumerate(dirs)]

def search_replace(source_file, source_str, target_file, target_str):
    """ Remplace source_str dans le fichier source_file par target_str
        en utilisant le fichier target_file """
    print "{0}, {1} -> {2}, {3}".format(source_file, source_str, target_file, target_str)
    changed = False
    with open(source_file, 'r') as in_file:
        with open(target_file, 'w') as out_file:
            for source_line in in_file:
                target_line = source_line.replace(source_str, target_str)
                if source_line != target_line:
                    changed = True
                out_file.write(target_line)
    if changed:
        remove(source_file)
        rename(target_file, source_file)
    else:
        remove(target_file)


for fiche in fiches:
    if not fiche.is_changed():
        continue
    target_dir = fiche.get_target_dir()
    print "{0} -> {1}".format(fiche.source_dir, target_dir)
    search_replace(join(basepath, 'README.adoc'), fiche.source_dir, join(basepath, 'README.adoc.renum'), target_dir)
    search_replace(join(basepath, 'SUMMARY.md'), fiche.source_dir, join(basepath, 'SUMMARY.md.renum'), target_dir)
    try:
        i_source_num = int(fiche.source_num)
        search_replace(join(basepath, fiche.source_dir, 'index.adoc'), 'Fiche ' + str(i_source_num), join(basepath, fiche.source_dir, 'index.adoc.renum'), 'Fiche ' + str(fiche.target_num))
    except ValueError:
        pass
    rename(join(basepath, fiche.source_dir), join(basepath, target_dir))
