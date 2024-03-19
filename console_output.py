from matrix import Matrix


def output():
    matrix_A = Matrix([[8, 4, 1],
                       [2, 5, 7],
                       [4, 6, 3]])

    vector_B = [1, 1, 1]
    matrix_A.matrix_info(vector_B)


if __name__ == '__main__':
    output()
