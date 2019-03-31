import numpy as np
def main(input, output, State):
    global NumberOfIt
    global MarkingList
    global Dead
    global Depth
    global Cyclic
    NumberOfIt = NumberOfIt + 1
    if NumberOfIt > 100:
        return
    if np.shape(input) != np.shape(output):
        print("Error: Input size does not match output size")
        return
    if np.shape(input)[0] != np.shape(State)[0]:
        print("Error: Initial State Matrix is the wrong size must be length of- " + str(np.shape(input)[0]))
        return
    # Find Incidence Matrix
    A = output-input

    Transitions = GetTransitions(input, output, A, State)
    if sum(Transitions[0,:]) == 0:
        # DEADLOCKED
        Dead = True;
        print("Dead")
    elif sum(Transitions[0,:]) > 1:
        # Multiple Branches
        for count in range(0,np.shape(Transitions)[1]):
            u = np.zeros([1,np.shape(Transitions)[1]])
            if Transitions[0,count] == 1:
                u[0,count] = 1
                print("Branched")
                NM = NextMarking(A, State, u.T)
                MarkingList.append(NM)
                Depth = Depth + 1
                main(input, output, NM)
                print(Depth)
            Depth = 0;
    else:
        # Single Path
        NM = NextMarking(A, State, Transitions.T)
        found = False
        for elm in MarkingList:
            if np.array_equal(elm, NM):
                found = True
                break

        if found:
            Cyclic = True;
        else:
            MarkingList.append(NM)
            main(input, output, NM)

def GetTransitions(input, output, A, State):
    # Determine which transitions can fire
    u = np.zeros([1,np.shape(input)[1]])
    for i in range(0, np.shape(input)[1]):
        if np.amin(State.T - input[:,i]) > -1:
            u[0,i] = 1
    return u

def NextMarking(A, M, u):
    MPrime = M + np.dot(A, u)
    print(MPrime.T)
    return MPrime
# Slide 5 PN_3 PPT
input = [[1, 0, 0, 0],[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
output = [[0, 1, 0, 0],[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
initialState = []
# Slide 12 PN_3 PPT
input = [[1, 0, 0],[1, 0, 0], [1, 0, 1], [0, 1, 0]]
output = [[1, 0, 0],[0, 1, 0], [0, 1, 0], [0, 0, 1]]
initialState = [[1], [0], [1], [0]]
NumberOfIt = 0
Depth = 0;
MarkingList = []
Cyclic = False;
Dead = False;
main(np.asarray(input), np.asarray(output), np.asarray(initialState))
print("Cyclic = " + str(Cyclic))
print("Dead = " + str(Dead))