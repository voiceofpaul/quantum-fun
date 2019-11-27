import math
import random

from qiskit import Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute
from qiskit.tools.visualization import plot_histogram, circuit_drawer


def main():
    N = 15
    x, r, p, q = shor_quantum(N)
    print("semiprime N = ", N, ", coprime x = ", x, ", period r = ", r, ", prime factors = ", p, " and ", q, sep="")


# qc = quantum circuit, qr = quantum register, cr = classical register, a = 2, 7, 8, 11 or 13
def circuit_amod15(qc, qr, cr, a):
    if a == 2:
        qc.cswap(qr[4], qr[3], qr[2])
        qc.cswap(qr[4], qr[2], qr[1])
        qc.cswap(qr[4], qr[1], qr[0])
    elif a == 7:
        qc.cswap(qr[4], qr[1], qr[0])
        qc.cswap(qr[4], qr[2], qr[1])
        qc.cswap(qr[4], qr[3], qr[2])
        qc.cx(qr[4], qr[3])
        qc.cx(qr[4], qr[2])
        qc.cx(qr[4], qr[1])
        qc.cx(qr[4], qr[0])
    elif a == 8:
        qc.cswap(qr[4], qr[1], qr[0])
        qc.cswap(qr[4], qr[2], qr[1])
        qc.cswap(qr[4], qr[3], qr[2])
    elif a == 11:  # this is included for completeness
        qc.cswap(qr[4], qr[2], qr[0])
        qc.cswap(qr[4], qr[3], qr[1])
        qc.cx(qr[4], qr[3])
        qc.cx(qr[4], qr[2])
        qc.cx(qr[4], qr[1])
        qc.cx(qr[4], qr[0])
    elif a == 13:
        qc.cswap(qr[4], qr[3], qr[2])
        qc.cswap(qr[4], qr[2], qr[1])
        qc.cswap(qr[4], qr[1], qr[0])
        qc.cx(qr[4], qr[3])
        qc.cx(qr[4], qr[2])
        qc.cx(qr[4], qr[1])
        qc.cx(qr[4], qr[0])


# qc = quantum circuit, qr = quantum register, cr = classical register, a = 2, 7, 8, 11 or 13
def circuit_aperiod15(qc, qr, cr, a):
    if a == 11:
        circuit_11period15(qc, qr, cr)
        return

    # Initialize q[0] to |1>
    qc.x(qr[0])

    # Apply a**4 mod 15
    qc.h(qr[4])
    #   controlled identity on the remaining 4 qubits, which is equivalent to doing nothing
    qc.h(qr[4])
    #   measure
    qc.measure(qr[4], cr[0])
    #   reinitialise q[4] to |0>
    qc.reset(qr[4])

    # Apply a**2 mod 15
    qc.h(qr[4])
    #   controlled unitary
    qc.cx(qr[4], qr[2])
    qc.cx(qr[4], qr[0])
    #   feed forward
    if cr[0] == 1:
        qc.u1(math.pi / 2., qr[4])
    qc.h(qr[4])
    #   measure
    qc.measure(qr[4], cr[1])
    #   reinitialise q[4] to |0>
    qc.reset(qr[4])

    # Apply a mod 15
    qc.h(qr[4])
    #   controlled unitary.
    circuit_amod15(qc, qr, cr, a)
    #   feed forward
    if cr[1] == 1:
        qc.u1(math.pi / 2., qr[4])
    if cr[0] == 1:
        qc.u1(math.pi / 4., qr[4])
    qc.h(qr[4])
    #   measure
    qc.measure(qr[4], cr[2])


def circuit_11period15(qc, qr, cr):
    # Initialize q[0] to |1>
    qc.x(qr[0])

    # Apply a**4 mod 15
    qc.h(qr[4])
    #   controlled identity on the remaining 4 qubits, which is equivalent to doing nothing
    qc.h(qr[4])
    #   measure
    qc.measure(qr[4], cr[0])
    #   reinitialise q[4] to |0>
    qc.reset(qr[4])

    # Apply a**2 mod 15
    qc.h(qr[4])
    #   controlled identity on the remaining 4 qubits, which is equivalent to doing nothing
    #   feed forward
    if cr[0] == 1:
        qc.u1(math.pi / 2., qr[4])
    qc.h(qr[4])
    #   measure
    qc.measure(qr[4], cr[1])
    #   reinitialise q[4] to |0>
    qc.reset(qr[4])

    # Apply 11 mod 15
    qc.h(qr[4])
    #   controlled unitary.
    qc.cx(qr[4], qr[3])
    qc.cx(qr[4], qr[1])
    #   feed forward
    if cr[1] == 1:
        qc.u1(math.pi / 2., qr[4])
    if cr[0] == 1:
        qc.u1(math.pi / 4., qr[4])
    qc.h(qr[4])
    #   measure
    qc.measure(qr[4], cr[2])


def shor_quantum(n):
    q = QuantumRegister(5, 'q')
    c = ClassicalRegister(5, 'c')

    shor = QuantumCircuit(q, c)
    best = 1
    x = 0

    while best % 2 != 0:
        x = random.randint(2, n - 1)
        if math.gcd(x, n) != 1:
            return x, 0, math.gcd(x, n), int(n / math.gcd(x, n))
        circuit_aperiod15(shor, q, c, 7)

        backend = Aer.get_backend('qasm_simulator')
        sim_job = execute([shor], backend)
        sim_result = sim_job.result()
        sim_data = sim_result.get_counts(shor)
        print(x)
        print(sim_data)
        best = best_result_number(sim_data)
        if x ** (best / 2) == 1 or x ** (best / 2) == -1:
            best = 1
    p = math.gcd(x ** (int(best / 2)) + 1, 15)
    q = math.gcd(x ** (int(best / 2)) - 1, 15)
    return x, best, p, q


def best_result_number(data):
    highest_hits = 0
    best_value = 0
    for key in data:
        if data[key] > highest_hits:
            highest_hits = data[key]
            best_value = key
    return int(best_value, base=2)


if __name__ == "__main__":
    main()
