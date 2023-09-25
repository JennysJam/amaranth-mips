"""
entry point for running code
"""

from argparse import ArgumentParser
import mips.cli.sim as sim

ap = ArgumentParser()
parsers = ap.add_subparsers(
    dest="command"
)

sim_parser = parsers.add_parser(
    "sim",
    help="Perform a simulation of the chip"
)

sim_parser.add_argument(
    "--out",
    help="output file to store simulation",
    default="simulation.gtkw"
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
    sim.simulate(args.out)
else:
    raise NotImplementedError(f"{args.command} not yet implemented")