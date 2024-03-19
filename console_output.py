from matrix import Matrix

def solve_cramer(matrix_A, vector_B):
    det_A = matrix_A.determinant()

    if det_A == 0:
        raise ValueError("Определитель матрицы коэффициентов равен нулю, система уравнений вырождена")

    solutions = []
    num_vars = len(vector_B)

    # Вычисляем определители подсистемы B для исходной матрицы
    for i in range(num_vars):
        matrix_A_copy = matrix_A.copy()
        for j in range(num_vars):
            matrix_A_copy.rows[j][i] = vector_B[j]
        det_A_i = matrix_A_copy.determinant()
        solutions.append(det_A_i)

    # Вычисляем определители подсистемы A для транспонированной матрицы
    transposed_A = Matrix([[matrix_A.rows[j][i] for j in range(num_vars)] for i in range(num_vars)])
    for i in range(num_vars):
        matrix_A_transposed_copy = transposed_A.copy()
        for j in range(num_vars):
            matrix_A_transposed_copy.rows[j][i] = vector_B[j]
        det_A_i_transposed = matrix_A_transposed_copy.determinant()
        solutions.append(det_A_i_transposed)

    return solutions

# Пример использования:
matrix_A = Matrix([[8, 2, 4],
                   [4, 5, 6],
                   [1, 7, 3]])

def same_sign(num, nums):
    if isinstance(num, (int, float)):  # Check if num is a numeric value
        return all(num * elem > 0 for elem in nums)
    else:  # num is a symbolic expression
        v = 1
        nums = [elem.subs('v', v) for elem in nums]  # Substitute 'v' with a numeric value
        return all(num * elem > 0 for elem in nums)

vector_B = [1, 1, 1]  # Теперь используем числовые значения

solutions = solve_cramer(matrix_A, vector_B)
solutions_A, solutions_B = solutions[:3], solutions[3:]
print(solutions_B)
print(solutions_A)

def calculate_total_determinant(matrix_A):
    return matrix_A.determinant()

total_determinant = calculate_total_determinant(matrix_A)
print("Общий определитель матрицы:", total_determinant)

if same_sign(total_determinant, solutions_A):
    print("Условие выполнено")
else:
    print(f"{solutions_A} Условие не выполнено")

if same_sign(total_determinant, solutions_B):
    print("Условие выполнено")
else:
    print(f"{solutions_B} Условие не выполнено")

import sympy as sp
import copy
def some_calcs(matrix_coefs,exp_matrix):
    print(matrix_coefs)
    x, y, v = sp.symbols('x y v')
    print(f"Система 1:\n{matrix_coefs[0][0]}x+{matrix_coefs[0][1]}y=v\n{matrix_coefs[1][0]}x+{matrix_coefs[1][1]}y=v")
    print(f"x+y=1")
    eq2 = sp.Eq(matrix_coefs[1][0] * x + matrix_coefs[1][1] * y, v)
    eq3 = sp.Eq(x + y, 1)
    # Решение системы уравнений
    eq1 = sp.Eq(matrix_coefs[0][0] * x + matrix_coefs[0][1] * y, v)
    eq2 = sp.Eq(matrix_coefs[1][0] * x + matrix_coefs[1][1] * y, v)
    eq3 = sp.Eq(x + y, 1)
    solution1 = sp.solve((eq1, eq2, eq3), (x, y, v))
    print("решение к системе 1", solution1)

    print(f"Система 2:\n{matrix_coefs[0][0]}x+{matrix_coefs[1][0]}y=v\n{matrix_coefs[0][1]}x+{matrix_coefs[1][1]}y=v")
    print(f"x+y=1")
    print(matrix_coefs[0][0])
    print(matrix_coefs[1][0])
    # Задание уравнений
    eq1 = sp.Eq(matrix_coefs[0][0] * x + matrix_coefs[1][0] * y, v)
    eq2 = sp.Eq(matrix_coefs[0][1] * x + matrix_coefs[1][1] * y, v)
    eq3 = sp.Eq(x + y, 1)
    solution2 = sp.solve((eq1, eq2, eq3), (x, y, v))
    print("решение к системе 2", solution2)
    print(solution1, "sol2", solution2)
    print(matrix_coefs)
    F_x_y = solution1[x]*solution2[x]*matrix_coefs[0][0]+\
            solution1[x]*solution2[y]*matrix_coefs[1][0]+\
            solution1[y]*solution2[x]*matrix_coefs[0][1]+\
            solution1[y]*solution2[y]*matrix_coefs[1][1]
    print(F_x_y)
    counter = 0
    new_indexes = []

    print(matrix_coefs)
    for i in range(len(exp_matrix) - 1):
        for j in range(len(exp_matrix[i]) - 1):
            found = False
            for k in range(2):
                for l in range(2):
                    if exp_matrix[i + k][j + l] == matrix_coefs[k][l] and counter<2:
                        new_indexes.append(j+l)
                        counter +=1
                        print(counter)
                        print(f"found elememnt {exp_matrix[i+k][j+l]}")
                        print(f"indexes exp_matrix {i+k, j+l} matrix 2x2 {k,l}")
                        # exp_matrix[0][j] = solution1[x]
                        # exp_matrix[0][j+l] = solution1[y]
                    if counter==2:
                        break

    local_exp_matrix = copy.deepcopy(exp_matrix)

    local_exp_matrix[0][new_indexes[0]] = solution1[x]
    local_exp_matrix[0][new_indexes[1]] = solution1[y]
    local_exp_matrix[new_indexes[0]][0] = solution2[x]
    local_exp_matrix[new_indexes[0]+1][0] = solution2[y]
    # for j in local_exp_matrix:
    #     print(j[1:4])
    for i in range(1,len(local_exp_matrix)):
        res1 = sum(a * b for a, b in zip(local_exp_matrix[0][1:], local_exp_matrix[i][1:]))
        print("reeeees",res1)
        if res1<=F_x_y:
            print("устойчивость ситуации  относительно чистыхm отклонений игрока 1 имеет место.")
        else:
            print("Ситуация неустойчивая")
        # print(res2)
    for i in local_exp_matrix:
        print(i)
    print('poop')
    # print(local_exp_matrix[1:][1][0])
    print(local_exp_matrix[1:][0][1])
    #local_exp_matrix[1:][0][i] * local_exp_matrix[1:][i][0]
    #local_exp_matrix[i][1:][0]
    res1 = sum(list(local_exp_matrix[i][0:][0]*local_exp_matrix[i][1:][0] for i in range(1,len(local_exp_matrix[0]))))
    res2 = sum(list(local_exp_matrix[i][0:][0]*local_exp_matrix[i][2:][0] for i in range(1,len(local_exp_matrix[0]))))
    res3 = sum(list(local_exp_matrix[i][0:][0]*local_exp_matrix[i][3:][0] for i in range(1,len(local_exp_matrix[0]))))
    reses = [res1,res2,res3]

    for i in reses:
        if i>=F_x_y:
            print("устойчивость ситуации  относительно чистыхm отклонений игрока 1 имеет место.")
        else:
            print("Ситуация неустойчивая")

    # res1 = sum(a * b for a, b in zip(local_exp_matrix[0][1:], local_exp_matrix[1][1:]))
    # res2 = sum(a * b for a, b in zip(local_exp_matrix[0][1:], local_exp_matrix[2][1:]))
    # res3 = sum(a * b for a, b in zip(local_exp_matrix[0][1:], local_exp_matrix[3][1:]))
    # print(res1)
    # print("res",res2)
    # print("res",res3)
# Выводим подматрицы
original_matrix = [
    [8, 2, 4],
    [4, 5, 6],
    [1, 7, 3]
]

# Создаем новую матрицу с пустой строкой и столбцом в начале
expanded_matrix = [[0] * (len(original_matrix[0]) + 1) for _ in range(len(original_matrix) + 1)]

# Заполняем новую матрицу значениями из исходной
for i in range(len(original_matrix)):
    for j in range(len(original_matrix[0])):
        expanded_matrix[i + 1][j + 1] = original_matrix[i][j]

# Выводим новую матрицу

submatrices = matrix_A.submatrices_2x2()
i = 1
for submatrix in submatrices:
    print((submatrix.rows))
print('oof')
array = []

for submatrix in submatrices:
    # print(f"{i})",*submatrix.rows,sep='\n')
    array.append(some_calcs(submatrix.rows,expanded_matrix))
    i +=1

for i in expanded_matrix:
    print(i)
