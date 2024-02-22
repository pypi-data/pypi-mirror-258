"""
Each edge is a int,
0 - no edge (omitted from graph)
1 - directed edge
2 - bidirected edge
3 - both directed and bidirected edge
"""

# loop graph
LG = {
1: {2:1},
2: {3:1},
3: {4:1},
4: {5:1},
5: {1:1}
}

# 2 cycles
C = {
    1: {2:1,4:1},
    2: {3:1},
    3: {4:1},
    4: {1:1}
}

# a cycle of two
N = {
1: {2:1},
2: {1:1,4:1},
3: {4:1},
4: {3:1},
}

N1 = {
1: {4:1},
2: {3:1},
3: {2:1},
4: {2:1,1:1},
}

# a cycle of three
A = {
1: {2:1,5:1},
2: {3:1},
3: {1:1},
4: {1:1},
5: {4:1},
}

# no cycles
U = {
1: {4:1,2:1},
2: {3:1},
3: {},
4: {3:1},
}

# DAG
D = {
1: {2:1,3:1},
2: {3:1},
3: {}
}

D2 = {
1: {},
2: {},
3: {4:1,8:1,1:1,2:1},
4: {},
5: {4:1,6:1},
6: {7:1,8:1},
7: {3:1},
8: {},
}

# 3 SCC DAG
D3 = {
1: {2:1,3:1},
2: {5:1,9:1,4:1},
3: {4:1},
4: {1:1},
5: {6:1},
6: {7:1},
7: {5:1,8:1},
8: {9:1},
9: {8:1},
}

P = {
1: {2:1},
2: {3:1},
3: {4:1},
4: {1:1,2:1},
}

L = {
1: {2:1},
2: {3:1},
3: {4:1},
4: {5:1},
5: {6:1,1:1},
6: {1:1},
7: {8:1},
8: {9:1},
9: {7:1},
}

UL = {
1: {3:1,9:1},
3: {4:1},
4: {5:1},
5: {1:1,6:1},
6: {5:1,7:1},
7: {8:1},
8: {6:1},
9: {10:1},
10: {11:1},
11: {12:1},
13: {1:1},
}

UL11 = {
1: {2:1,3:1},
2: {4:1},
3: {4:1,3:1},
4: {},
}

# tree
T2 = {
1: {2:1,15:1},
2: {6:1,3:1},
3: {4:1,5:1},
4: {},
5: {},
6: {7:1,8:1},
7: {},
8: {},
9: {},
10: {},
11: {9:1,10:1},
12: {},
13: {},
14: {13:1,12:1},
15: {14:1,11:1},
}

# one loop
L1 = {
1: {2:1},
2: {3:1},
3: {4:1},
4: {5:1},
5: {1:1},
}

L25 = {
1: {2:1,1:1},
2: {3:1},
3: {5:1,6:1},
#4: {5:1},
5: {6:1},
6: {7:1,2:1},
7: {1:1},
}
#8: {9:1},
#9: {1:1},b
#1: {1:1},
# 2: {3:1,6:1},
# 3: {1:1},
# }

L01 = {
1: {2:1},
2: {3:1,7:1},
3: {4:1,7:1},
4: {5:1,6:1},
5: {6:1},
6: {3:1},
7: {1:1},
}
L02 = {
1: {2:1,1:1},
2: {3:1},
3: {4:1,6:1},
4: {5:1},
5: {6:1,4:1},
6: {7:1},
7: {1:1,7:1},
}

L03 = {
1: {2:1,1:1},
2: {3:1},
3: {4:1},
4: {5:1},
5: {6:1},
6: {7:1},
7: {1:1},
}


TT = {
1: {2:1},
2: {3:1},
3: {4:1,1:1},
4: {5:1},
5: {6:1},
6: {7:1},
7: {8:1},
8: {9:1},
9: {1:1,10:1},
10: {10:1},
}

T10 = {
1: {2:1},
2: {3:1},
3: {4:1},
4: {5:1},
5: {6:1},
6: {7:1},
7: {8:1},
8: {9:1},
9: {1:1,10:1},
10: {10:1},
}

T22 = {
1: {2:1,10:1},
2: {1:1},
3: {4:1,10:1},
4: {3:1},
5: {6:1,10:1},
6: {5:1},
7: {8:1},
8: {9:1},
9: {7:1,10:1},
10: {10:1},
}

T63 = {
1: {2:1},
2: {3:1},
3: {4:1},
4: {5:1},
5: {6:1},
6: {1:1,10:1},
7: {8:1},
8: {9:1},
9: {7:1,10:1},
10: {10:1},
}

T631 = {
1: {2:1},
2: {3:1},
3: {4:1},
4: {5:1},
5: {6:1},
6: {1:1,10:1},
7: {8:1},
8: {9:1},
9: {7:1,10:1,9:1},
10: {10:1},
}

T33 = {
1: {2:1,10:1},
2: {3:1},
3: {1:1},
4: {5:1},
5: {6:1},
6: {4:1,10:1},
7: {8:1},
8: {9:1},
9: {7:1,10:1},
10: {10:1},
}


OO = {
1: {2:1,11:1},
2: {3:1},
3: {4:1},
4: {5:1},
5: {6:1},
6: {7:1},
7: {8:1},
8: {9:1},
9: {10:1},
10: {1:1},
11: {11:1},
12: {5:1,6:1,12:1},
}

OO5 = {
1: {3:1,11:1},
2: {4:1},
3: {5:1},
4: {6:1},
5: {7:1},
6: {8:1},
7: {9:1},
8: {10:1},
9: {1:1},
10: {2:1,11:1},
11: {11:1},
12: {5:1,6:1,12:1},
}

MV = {
1: {4:1},
2: {},
3: {},
4: {6:1},
5: {4:1,2:1},
6: {3:1, 5:1},
}


MV_ = {
1: {2:1,3:1},
2: {3:2},
3: {2:2},
}

G96 = {
1: {2:1},
2: {3:1},
3: {4:1},
4: {1:1,5:1},
5: {6:1},
6: {7:1,8:1},
7: {4:1},
8: {9:1,24:1},
9: {10:1},
10: {11:1},
11: {12:1},
12: {13:1},
13: {14:1},
14: {6:1},

# 15: {16:1,15:1},
# 16: {17:1},
# 17: {18:1},
# 18: {19:1},
# 19: {20:1},
# 20: {21:1},
# 21: {21:1},
22: {1:1,22:1},



24: {24:1},
#25: {26:1},
#26: {26:1},
}

G960 = {
1: {2:1},
2: {3:1},
3: {4:1},
4: {5:1},
5: {6:1},
6: {7:1,1:1},
7: {8:1},
8: {9:1},
9: {1:1},
}

DDD1 = {
    1: {2:1,1:1},
    2: {3:1},
    3: {4:1, 6:1},
    4: {5:1},
    5: {6:1},
    6: {1:1}
}

DDD2 = {
    1: {2:1,1:1},
    2: {3:1},
    3: {6:1},
    4: {3:1},
    5: {4:1},
    6: {1:1, 5:1}
}
