import PetriNet
import numpy as np
def test_nextMarking():
    A = [[0, 0, 0], [-1, 1, 0], [-1, 1, -1], [0, -1, 1]]
    M = [[1],[0],[1],[0]]
    u = [[0], [0],[1]]
    assert np.array_equal(PetriNet.NextMarking(A, M, u), [[1],[0],[0],[1]])
