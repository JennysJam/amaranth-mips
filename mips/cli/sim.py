from mips.cpu.alu import simulate as alu_simulate


def simulate(filename: str):
    print("performing alu simulation")
    alu_simulate(filename)