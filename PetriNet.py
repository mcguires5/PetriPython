import numpy as np
from numpy.linalg import svd
from sympy import *

def main(input, output, state):
    global NumberOfIt
    global MarkingList
    global Dead
    global Cyclic
    global TabIndex
    global Trans
    global MaxMarking

    if np.shape(input) != np.shape(output):
        print("Error: Input size does not match output size")
        return
    if np.shape(input)[0] != np.shape(state)[0]:
        print("Error: Initial State Matrix is the wrong size must be length of- " + str(np.shape(input)[0]))
        return

    # Find Incidence Matrix
    A = output - input

    transitions = GetTransitions(input, state)
    NumberOfIt = NumberOfIt + 1
    if NumberOfIt > 20:
        transitions[0, Trans] = 0
    if NumberOfIt > 30:
        return
    if sum(transitions[0, :]) == 0:
        # DEADLOCKED
        Dead = True
        print("Dead")
    elif sum(transitions[0, :]) > 1:
        # Multiple Branches
        for count in range(0, np.shape(transitions)[1]):
            u = np.zeros([1, np.shape(transitions)[1]])
            if transitions[0, count] == 1:
                Trans = count
                u[0, count] = 1
                # print("Branched")
                NM = NextMarking(A, state, u.T)
                MaxMarking = CheckMaxMarking(NM, MaxMarking)
                found = False
                for elm in MarkingList:
                    if np.array_equal(elm, NM):
                        found = True
                        break
                if found:
                    Cyclic = True
                    for i in range(TabIndex):
                        print('    ', end=' ')
                    print("Cycle Found" + str(NM.T))
                else:
                    MarkingList.append(NM)
                    for i in range(TabIndex):
                        print('    ', end=' ')
                    print(NM.T)
                    TabIndex = TabIndex + 1
                    main(input, output, NM)
                    TabIndex = TabIndex - 1

    else:
        # Single Path
        NM = NextMarking(A, state, transitions.T)
        MaxMarking = CheckMaxMarking(NM, MaxMarking)
        found = False
        for elm in MarkingList:
            if np.array_equal(elm, NM):
                found = True
                break

        if found:
            Cyclic = True
            for i in range(TabIndex):
                print('    ', end=' ')
            print("Cycle Found" + str(NM.T))
        else:
            MarkingList.append(NM)
            for i in range(TabIndex):
                print('    ', end=' ')
            print(NM.T)
            main(input, output, NM)


def CheckMaxMarking(nextMarking, MaxMarking):
    if max(nextMarking) > MaxMarking:
        return int(max(nextMarking))
    return MaxMarking


def GetTransitions(input, state):
    # Determine which transitions can fire
    u = np.zeros([1, np.shape(input)[1]])
    for i in range(0, np.shape(input)[1]):
        if np.amin(state.T - input[:, i]) > -1:
            u[0, i] = 1
    return u


def InvarientSolver(input, output):
    A = Matrix(output - input)

    x = A.nullspace()
    tInvarient = len(x) > 0

    temp_A = Matrix(A.T)
    x = temp_A.nullspace()
    pInvarient = len(x) > 0

    return tInvarient, pInvarient

def nullspace(A, atol=1e-13, rtol=0):
    A = np.atleast_2d(A)
    u, s, vh = svd(A)
    tol = max(atol, rtol * s[0])
    nnz = (s >= tol).sum()
    ns = vh[nnz:].conj().T
    return ns


def NextMarking(A, M, u):
    MPrime = M + np.dot(A, u)
    # print(MPrime.T)
    return MPrime


# Slide 5 PN_3 PPT
input = np.asarray([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
output = np.asarray([[0, 1, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
initialState = np.asarray([[1], [0], [1], [1], [1]])
# Slide 12 PN_3 PPT
# input = np.asarray([[1, 0, 0], [1, 0, 0], [1, 0, 1], [0, 1, 0]])
# output = np.asarray([[1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1]])
# initialState = np.asarray([[1], [0], [1], [0]])
# T Invarient from Internet
# input = np.asarray([[0, 1, 0, 2], [1, 1, 0, 0], [0, 0, 1, 0]])
# output = np.asarray([[1, 0, 0, 2], [0, 0, 1, 0], [0, 2, 0, 0]])
# initialState = np.asarray([[1], [1], [0]])
# P Invarient from PN_3 Slide 37
# input = np.asarray([[2, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 1]])
# output = np.asarray([[0, 2, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [1, 0, 1, 0]])
# initialState = np.asarray([[3], [0], [1], [0]])
NumberOfIt = 0
Trans = 0
MaxMarking = 0
MarkingList = []
Cyclic = False
Dead = False
TabIndex = 0
main(input, output, initialState)
tInvarient, pInvarient = InvarientSolver(input, output)
print("T-Invarient = " + str(tInvarient))
print("P-Invarient = " + str(pInvarient))
print("Cycle Found = " + str(Cyclic))
print("Dead = " + str(Dead))
if MaxMarking > 6:
    print("Petri Net is unbounded")
else:
    print("Petri Net is " + str(MaxMarking) + " bounded")
