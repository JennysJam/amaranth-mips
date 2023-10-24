#!/usr/bin/python3
"""
entry point for running code
"""

from argparse import ArgumentParser
from mips.cli.sim import simulate
from mips.cli.flash import flash
from mips.cli.synth import synth

ap = ArgumentParser(
    prog="Amaranth Mips",
    description="CLI for Mips FPGA/Synth"
)

parsers = ap.add_subparsers(
    prog="command",
    description="command to evoke",
    dest="command",
)

sim_parser = parsers.add_parser(
    "sim",
    help="Perform a simulation of the chip"
)

sim_parser.add_argument(
    "--out",
    help="output file to store simulation",
    default="simulation.vcd"
)

synth_parser = parsers.add_parser(
    "synth",
    help="Synthesize code and save to file"
)

flash_parser = parsers.add_parser(
    "flash",
    help="Synthesize and flash code to device"
)

args = ap.parse_args()

if args.command == "sim":
    simulate(args.out)
elif args.command == "synth":
    synth()
elif args.command == "flash":
    flash()
else:
    ap.print_help()