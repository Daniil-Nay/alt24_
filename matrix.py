import sympy as sp
import numpy as np
import copy
from accessify import private
from dataclasses import dataclass
from typing import List, Union


@dataclass
class Matrix:

    def __init__(self, rows):
        """
        Инициализирует объект класса Matrix.

        :param rows: Список списков, представляющих строки матрицы.
        :return: None
        """

        self.expanded_matrix = None
        self.rows = rows
        self.num_rows = len(rows)
        self.num_cols = len(rows[0])

    def __getitem__(self, index) -> 'Matrix':
        """
        возвращает строку матрицы по индексу
        :param index: индекс строки
        :return: Объект класса Matrix
        """
        return self.rows[index]

    def __tr__(self) -> None:
        """
        Транспонирует матрицу.
        :return: None
        """
        self.rows = [[self.rows[j][i] for j in range(self.num_rows)] for i in range(self.num_cols)]
        self.num_rows, self.num_cols = self.num_cols, self.num_rows

    def __determinant(self) -> Union[int, float, ValueError]:
        """
        Вычисляет определитель матрицы.
        :return: Определитель матрицы или ValueError, если матрица не квадратная.
        """
        if self.num_rows != self.num_cols:
            raise ValueError("Матрица должна быть квадратной для вычисления определителя")

        if self.num_rows == 2:
            return self.rows[0][0] * self.rows[1][1] - self.rows[0][1] * self.rows[1][0]

        det = 0
        for j in range(self.num_cols):
            det += (-1) ** j * self.rows[0][j] * self.__minor(0, j).__determinant()
        return det

    def __minor(self, row, col) -> 'Matrix':
        """
        Возвращает минор матрицы по заданным строке и столбцу.
        :param row: Индекс строки.
        :param col: Индекс столбца.
        :return: Минор матрицы.
        """
        minors = [row[:col] + row[col + 1:] for row in (self.rows[:row] + self.rows[row + 1:])]
        return Matrix(minors)

    def __copy(self) -> 'Matrix':
        """
        Создает копию матрицы.
        :return: Копия матрицы.
        """
        return Matrix([row[:] for row in self.rows])

    def __submatrices_2x2(self) -> list:
        """
        Создает список всех 2x2 подматриц данной матрицы.
        :return: Список 2x2 подматриц.
        """
        sub_matrices = []
        for i in range(self.num_rows - 1):
            for j in range(self.num_cols - 1):
                sub_matrix = [[self.rows[i][j], self.rows[i][j + 1]], [self.rows[i + 1][j], self.rows[i + 1][j + 1]]]
                sub_matrices.append(Matrix(sub_matrix))
        return sub_matrices

    @private
    def __same_sign(self, num) -> bool:
        """
        Проверяет, имеют ли все элементы матрицы один и тот же знак.
        :param num: Число для проверки знака.
        :return: True, если все элементы имеют одинаковый знак, иначе False.
        """
        # Проверяем, является ли num числовым значением или символьным выражением
        if isinstance(num, (int, float)):
            return all(num * elem > 0 for row in self.rows for elem in row)
        else:
            v = 1
            # Подставляем 'v' в символьные выражения и проверяем знаки
            nums = [elem.subs('v', v) for row in self.rows for elem in row]
            return all(num * elem > 0 for elem in nums)

    def __solve_cramer(self, vector) -> List[Union[ValueError, list]]:
        """
        Решает систему уравнений методом Крамера.
        :param vector: Вектор правых частей уравнений.
        :return: Список решений или ValueError, если определитель равен нулю.
        """
        print("1. Метод Крамера\n")
        det_A = self.__determinant()
        if det_A == 0:
            raise ValueError("Определитель матрицы коэффициентов равен нулю, система уравнений вырождена")

        solutions = []
        num_vars = len(vector)
        for i in range(num_vars):
            matrix_A_copy = self.__copy()
            for j in range(num_vars):
                matrix_A_copy.rows[j][i] = vector[j]
            det_A_i = matrix_A_copy.__determinant()
            print(f"1.{i + 1} Вычисление дополнительного определителя для матрицы:", *matrix_A_copy.rows,
                  f"Доп.определитель:{det_A_i}", sep="\n")
            solutions.append(det_A_i)

        # Вычисляем определители подсистемы A для транспонированной матрицы
        transposed_A = Matrix([[self.rows[j][i] for j in range(num_vars)] for i in range(num_vars)])

        print("\nДля транспонированной матрицы:", *transposed_A.rows, sep="\n")
        for i in range(num_vars):
            matrix_A_transposed_copy = transposed_A.__copy()
            for j in range(num_vars):
                matrix_A_transposed_copy.rows[j][i] = vector[j]
            det_A_i_transposed = matrix_A_transposed_copy.__determinant()
            print(f"1.{i + 1} Вычисление дополнительного определителя для транспонированной матрицы:",
                  *matrix_A_transposed_copy.rows,
                  f"Доп.определитель:{det_A_i_transposed}", sep="\n")
            solutions.append(det_A_i_transposed)

        return solutions

    def __set_expanded_matrix(self) -> 'Matrix':
        """
        Создает расширенную матрицу, добавляя пустую строку и столбец.
        :return: Расширенная матрица.
        """
        # Создаем новую матрицу с пустой строкой и столбцом в начале
        self.expanded_matrix = [[0] * (self.num_cols + 1) for _ in range(self.num_rows + 1)]

        # Заполняем новую матрицу значениями из исходной
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.expanded_matrix[i + 1][j + 1] = self[i][j]
        return Matrix(self.expanded_matrix)

    def _some_calcs_algorithm_step_1(self, vector) -> None:
        """
        Выполняет первый шаг алгоритма расчета оптимальных стратегий.
        :param vector: Вектор правых частей уравнений.
        :return: None
        """
        solutions = self.__solve_cramer(vector)
        total_determinant = self.__determinant()
        solutions = {
            "игрока 1": [Matrix([solutions[:3]])],
            "игрока 2": [Matrix([solutions[3:]])]
        }

        print(f"\n2. Сравнение знака дополнительных определителей с определением матрицы.",
              f"Общий определитель матрицы: {total_determinant}\n", sep="\n")
        for idx, (name, solution) in enumerate(solutions.items(), start=1):
            if solution[0].__same_sign(total_determinant):
                print(f"2.{idx} Условие положительности для {name} выполняется.",
                      f"Вектор из доп. определителей:{solution[0].rows[0]}", sep="\n")
            else:
                print(f"2.{idx} Условие положительности для {name} не выполняется. "
                      f"Игра не является вполне смешанной",
                      f"Вектор из доп. определителей:{solution[0].rows[0]}", sep="\n")
                if name == "игрока 2":
                    self.__tr__()
                self.__some_calcs_algorith_step_2()

    def __some_calcs_algorith_step_2(self) -> None:
        """
        Выполняет второй шаг алгоритма расчета оптимальных стратегий.
        :return: None
        """

        print("\n3. Поиск оптимальных стратегий игроков 1 и 2 перебором подматриц исходной матрицы:", *self.rows,
              sep="\n")
        self.__set_expanded_matrix()
        submatrices = self.__submatrices_2x2()
        for idz, submatrix in enumerate(submatrices, start=1):
            print('-' * 20,
                  f"3.{idz} Рассматриваемая подматрица:",
                  *submatrix.rows,
                  sep="\n")
            coeffs = submatrix.rows
            x_1, x_2, y_1, y_2, v = sp.symbols('x_1 x_2 y_1 y_2 v')

            eq_x_1 = sp.Eq(coeffs[0][0] * x_1 + coeffs[1][0] * x_2, v)
            eq_x_2 = sp.Eq(coeffs[0][1] * x_1 + coeffs[1][1] * x_2, v)
            eq_x_3 = sp.Eq(x_1 + x_2, 1)
            solution1 = sp.solve((eq_x_1, eq_x_2, eq_x_3), (x_1, x_2, v))

            eq_y_1 = sp.Eq(coeffs[0][0] * y_1 + coeffs[0][1] * y_2, v)
            eq_y_2 = sp.Eq(coeffs[1][0] * y_1 + coeffs[1][1] * y_2, v)
            eq_y_3 = sp.Eq(y_1 + y_2, 1)
            solution2 = sp.solve((eq_y_1, eq_y_2, eq_y_3), (y_1, y_2, v))

            print(f"Компоненты подматрицы 2х2 находятся аналитическим способом:",

                  f"Система 1 игрока:",
                  f"{coeffs[0][0]}x₁ + {coeffs[1][0]}x₂ = v\n{coeffs[0][1]}x₁ + {coeffs[1][1]}x₂ = v",
                  f"x₁+x₂=1",

                  f"Решение к системе 1 игрока:",
                  f"x₁={solution1[x_1]}",
                  f"x₂={solution1[x_2]}",

                  f"Система 2 игрока:",
                  f"{coeffs[0][0]}y₁+{coeffs[0][1]}y₂=v\n{coeffs[1][0]}y₂+{coeffs[1][1]}y₂=v",
                  f"y₁+y₂=1",

                  f"Решение к системе 2 игрока:",
                  f"y₁={solution2[y_1]}",
                  f"y₂={solution2[y_2]}",
                  sep="\n"
                  )

            F_x_y = solution2[y_1] * solution1[x_1] * coeffs[0][0] + \
                    solution2[y_1] * solution1[x_2] * coeffs[1][0] + \
                    solution2[y_2] * solution1[x_1] * coeffs[0][1] + \
                    solution2[y_2] * solution1[x_2] * coeffs[1][1]

            print('-' * 20,
                  f"4. Находим F:",
                  f"F={F_x_y}",
                  '-' * 20,
                  f"5. Проверяем устойчивость ситуации F относительно чистых стратегий игроков.", sep="\n")
            counter = 0
            new_indexes = []

            for i in range(self.num_rows):
                for j in range(self.num_rows):
                    for k in range(2):
                        for l in range(2):
                            if self.expanded_matrix[i + k][j + l] == coeffs[k][l] and counter < 2:
                                new_indexes.append(j + l)
                                counter += 1
                            if counter == 2:
                                break

            local_exp_matrix = Matrix(copy.deepcopy(self.expanded_matrix))
            local_exp_matrix[0][new_indexes[0]] = solution2[y_1]
            local_exp_matrix[0][new_indexes[1]] = solution2[y_2]
            local_exp_matrix[new_indexes[0]][0] = solution1[x_1]
            local_exp_matrix[new_indexes[0] + 1][0] = solution1[x_2]
            np.set_printoptions(formatter={'all': lambda x: f'{x:0.2f}'})
            print(f"5.{idz} Рассматриваемая матрица:",
                  *local_exp_matrix.rows,
                  '-' * 20,
                  sep="\n")

            for i in range(1, local_exp_matrix.num_rows):
                res1 = sum(a * b for a, b in zip(local_exp_matrix[0][1:], local_exp_matrix[i][1:]))
                if res1 <= F_x_y:
                    print(f"Стратегия А{i}: {res1} <= {F_x_y}")
                else:
                    print(f"Стратегия А{i}: {res1} > {F_x_y}. Игрок получает больший выигрыш, чем должно быть")

            res1 = sum(
                list(local_exp_matrix[i][0:][0] * local_exp_matrix[i][1:][0] for i in
                     range(1, len(local_exp_matrix[0]))))
            res2 = sum(
                list(local_exp_matrix[i][0:][0] * local_exp_matrix[i][2:][0] for i in
                     range(1, len(local_exp_matrix[0]))))
            res3 = sum(
                list(local_exp_matrix[i][0:][0] * local_exp_matrix[i][3:][0] for i in
                     range(1, len(local_exp_matrix[0]))))
            reses = [res1, res2, res3]
            flag = False
            for i in range(len(reses)):
                if reses[i] >= F_x_y:
                    print(f"Стратегия B{i + 1}: {reses[i]} >= {F_x_y}")
                else:
                    print(
                        f"Стратегия B{i + 1}: {reses[i]} <  {F_x_y}. Игрок 2 получает меньший проигрыш, чем должно быть")
                    flag = True
            print('-' * 20, f"\nВыходные данные:")
            if flag:
                print(f"Ситуация неустойчива, потому выбор подматрицы {idz} оказался неудачным.",
                      f"Ситуация F={F_x_y} не является седловой точкой",
                      sep="\n")
            else:
                print(
                    f"Ситуация устойчива относительно чистых отклонений игроков.",
                    f"Ситуация F={F_x_y} является седловой точкой в матричной игре:",
                    *local_exp_matrix,
                    f"А также в игре с первоначальной платежной матрицей",
                    *self.rows,
                    f"А стратегии игрока 1 {[row[0] for row in local_exp_matrix]} и игрока 2 {local_exp_matrix[0][1:]}",
                    "являются оптимальными",
                    sep="\n")

    def matrix_info(self, vector):
        """
        Выводит информацию о матрице и решает задачу оптимальных стратегий.
        :param vector: Вектор правых частей уравнений.
        :return: None
        """
        n = 20
        print('-' * n, "Входные данные:", *self.rows, '-' * n, "Алгоритм:", sep="\n", )
        self._some_calcs_algorithm_step_1(vector)
