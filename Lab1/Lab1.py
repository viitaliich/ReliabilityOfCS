# Default values and constants
DEFAULT_ARRAY = [1325, 977, 243, 3, 145, 997, 27, 67, 30, 934,
                 1039, 240, 371, 86, 164, 96, 156, 145, 280,
                 444, 887, 726, 41, 503, 174, 1809, 349, 532,
                 1541, 148, 489, 198, 4, 761, 389, 37, 317,
                 1128, 514, 426, 23, 184, 365, 153, 624, 31,
                 49, 1216, 61, 189, 286, 1269, 365, 1085,
                 279, 228, 95, 391, 683, 39, 7, 486, 715, 204,
                 1553, 736, 1622, 1892, 448, 23, 135, 555,
                 252, 569, 8, 491, 724, 331, 1243, 567, 788,
                 729, 62, 636, 227, 227, 245, 153, 151, 217,
                 1009, 143, 301, 342, 48, 493, 117, 78, 113,
                 67]
GAMMA = 0.74
PROB_TIME = 1586
INTENSITY_TIME = 1798
INT_NUM = 10

# INPUT
input_mode = input("Press '0' to enter elements one by one\n"
                   "Press '1' to enter an array of elements separated by spaces\n"
                   "Press '2' to use default values\n")

array = list()  # array of elements

if input_mode == '0':
    print("Enter 'S' to stop input")
    val = input()
    while val != 'S' and not val.isalpha():
        array.append(int(val))
        val = input()
    else:
        GAMMA = int(input("GAMMA (percentage) -> \n"))
        PROB_TIME = int(input("TIME of trouble-free work -> \n"))
        INTENSITY_TIME = int(input("TIME for intensity -> \n"))
        print("LIST of time:", array)

elif input_mode == '1':
    array = input("'enter' to stop input\n").split()
    for i in range(len(array)):
        if array[i].isalpha():
            print("ERROR: NUMBERS ONLY ALLOWED")
            exit(1)
            # array.remove(array[i])
        else:
            array[i] = int(array[i])
    GAMMA = int(input("GAMMA (percentage) -> \n"))
    PROB_TIME = int(input("TIME of trouble-free work -> \n"))
    INTENSITY_TIME = int(input("TIME for intensity -> \n"))
    print("LIST of time:", array)
elif input_mode == '2':
    array = DEFAULT_ARRAY
    print("GAMMA (percentage):", GAMMA)
    print("TIME of trouble-free work:", PROB_TIME)
    print("TIME for intensity:", INTENSITY_TIME)
    print("LIST of time:", array)
else:
    print("ERROR: ILLEGAL INPUT")
    exit(1)

# TASK 1: Average time to failure
Tcp = sum(array) / len(array)
print("Tcp =", Tcp)

# Intervals
array.sort()
h = max(array) / INT_NUM
int_matrix = list()

int_end = h
j = 0
for i in range(0, INT_NUM):
    row = list()
    while j < len(array) and array[j] <= int_end:
        row.append(array[j])
        j = j + 1
    int_matrix.append(row)
    int_end = int_end + h

int_bounds = list()  # TO DO

# statistical density of the probability distribution
f_list = list()
for i in range(INT_NUM):
    f_list.append(round(len(int_matrix[i]) / len(array) / h, 6))

# probability of trouble-free device operation
P_list = list()
S = 0
for i in range(len(f_list)):
    S = min(S + f_list[i] * h, 1)  # max(P) = 1
    P_list.append(round(1 - S, 6))

print("P list =", P_list)

# TASK 2: Gamma-percentage
for i in range(1, len(P_list)):
    if P_list[i - 1] <= GAMMA <= P_list[i]:
        t_left = h * (i - 1)
        t_left_index = i - 1
        t_right = h * i
        t_right_index = i
        T_gamma = t_left + h * ((P_list[t_left_index] - GAMMA) / (P_list[t_left_index] - P_list[t_right_index]))
        break
    else:
        T_gamma = 0 + h * ((1 - GAMMA) / (1 - P_list[0]))
print("T_gamma =", T_gamma)

# TASK 3: Probability of troble-free device operation at specific time
i = 0
accum = 0
while int_matrix[i][len(int_matrix[i]) - 1] < PROB_TIME:
    accum = accum + (f_list[i] * h)
    i = i + 1
else:
    accum = accum + f_list[i] * (PROB_TIME - int_matrix[i - 1][len(int_matrix[i - 1]) - 1])
P = 1 - accum
print("P =", round(P, 6))

# TASK 4
I = f_list[i] / P
print("I =", round(I, 6))
