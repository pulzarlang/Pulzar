class Quantum:
    def __init__(self):
        self.stdout = ""

    def H(self, x): #  Hadamard transform
        """
        This method handles Hadamard transform
        :param x:
            0
        :return:
            1/√2n(|0⟩y + |1⟩y)
        """
    def SWAP(self, quibits):
        """
        This method swaps to quibits and return it in representation of matrix.
        :param quibits:
            |00⟩, |01⟩, |10⟩, |11⟩
        :return: Matrix
            [[1, 0, 0, 0]
             [0, 0, 1, 0]
             [0, 1, 0, 0]
             [0, 0, 0, 1]]
        """