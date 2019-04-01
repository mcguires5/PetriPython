import PetriNet
def test_nextMarking(self):
    A = [[0, 0, 0], [-1, 1, 0], [0, -1, 1]]
    M = [[1],[0],[1],[0]]
    u = [[0], [0],[1]]
    assert PetriNet.NextMarking(A, M, u) == [[1],[0],[0],[1]]
