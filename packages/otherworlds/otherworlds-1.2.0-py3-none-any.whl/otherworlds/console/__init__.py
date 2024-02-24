# SPDX-FileCopyrightText: 2023 Civic Hacker, LLC
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
from ast import literal_eval
from otherworlds.main import generate_name
from otherworlds.utils import slugify
from pathlib import Path
from random import Random

parser = argparse.ArgumentParser()
resume_group = parser.add_mutually_exclusive_group()

parser.add_argument("-k", "--klingon", help="include Klingon names",
                    action="store_true")
parser.add_argument("-n", "--num",
                    type=int,
                    help="how many names to generate at once (defaults to 1)",
                    default=1,
                    action="store")
parser.add_argument("--save", help="save generator state to a file",
                    default=False,
                    action="store_true")
resume_group.add_argument("--seed", type=int, help="user-supplied seed",
                          action="store")
parser.add_argument("--slug", help="print the name as a slug",
                    action="store_true")
parser.add_argument("--state",
                    help="filename of state file (defaults to .state.rnd)",
                    default=".state.rnd",
                    action="store")

resume_group.add_argument("--resume", help="retrieve a previously saved state",
                          default=False,
                          action="store_true")


def run():
    args = parser.parse_args()
    output = None
    previous_state = ''

    random_instance = Random(args.seed) if args.seed else Random()
    if args.resume:
        if Path(args.state).exists():
            with open(args.state, 'r') as rs:
                previous_state = rs.read()
            random_instance.setstate(literal_eval(previous_state))

    creator = generate_name(
        include_klingon=args.klingon,
        generator=random_instance)
    output = [next(creator) for i in range(args.num)]
    if args.save:
        with open(args.state, 'w') as rs:
            rs.write(repr(random_instance.getstate()))
    if args.slug:
        output = [slugify(o) for o in output]
    print("\n".join(output))
