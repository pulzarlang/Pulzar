import numpy as np

class Quantum:
    def __init__(self):
        self.stdout = ""

    def H(self, x): #  Hadamard transform gate
        """
        This method handles Hadamard transform gate
        :param x:
            0
        :return:
            1/√2n(|0⟩y +- |1⟩y)
            or
            1/ √2n([[1, 1], [1, -1]])
        """
    def SWAP(self, quibits):
        """
        This method swaps two qubits and return it in representation of matrix.
        :param quibits:
            |00⟩, |01⟩, |10⟩, |11⟩
        :return: Matrix
            [[1, 0, 0, 0]
             [0, 0, 1, 0]
             [0, 1, 0, 0]
             [0, 0, 0, 1]]
        """