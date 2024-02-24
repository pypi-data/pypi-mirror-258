# SPDX-FileCopyrightText: 2023 Civic Hacker, LLC
#
# SPDX-License-Identifier: GPL-3.0-or-later

import csv
import pathlib


PREFIX_TYPES = [
    "mathematical",
    "empty"
]

SUFFIX_TYPES = [
    'numerical',
    'mathematical',
    'empty'
]

NAME_SOURCES = [
    "male_klingon",
    "exoplanets",
    "female_klingon"
]

MATHEMATICAL = [
    'Alpha',
    'Prime',
    'Beta',
    'Rho',
    'Delta',
    'Omega',
    'Epsilon',
    'Theta'
]

DATAFILE = 'NameExoWorlds.csv'

EXOPLANETS = list()
STARNAMES = list()


def get_data_path():
    return (pathlib.Path(__file__).parent).joinpath('data').joinpath(DATAFILE)


with open(get_data_path(), 'r') as f:
    reader = csv.DictReader(f)
    for line in reader:
        EXOPLANETS.append(line.get("Name Exoplanet"))
        STARNAMES.append(line.get("Name Star"))
