class Matrix:
    def __init__(self, rows):
        self.rows = rows
        self.num_rows = len(rows)
        self.num_cols = len(rows[0])

    def determinant(self):
        if self.num_rows != self.num_cols:
            raise ValueError("Матрица должна быть квадратной для вычисления определителя")

        # Base case for 2x2 matrix
        if self.num_rows == 2:
            return self.rows[0][0] * self.rows[1][1] - self.rows[0][1] * self.rows[1][0]

        det = 0
        for j in range(self.num_cols):
            det += (-1) ** j * self.rows[0][j] * self.minor(0, j).determinant()
        return det

    def minor(self, row, col):
        minors = [row[:col] + row[col + 1:] for row in (self.rows[:row] + self.rows[row + 1:])]
        return Matrix(minors)

    def copy(self):
        return Matrix([row[:] for row in self.rows])

    def submatrices_2x2(self):
        sub_matrices = []
        for i in range(self.num_rows - 1):
            for j in range(self.num_cols - 1):
                sub_matrix = [[self.rows[i][j], self.rows[i][j + 1]], [self.rows[i + 1][j], self.rows[i + 1][j + 1]]]
                sub_matrices.append(Matrix(sub_matrix))
        return sub_matrices

