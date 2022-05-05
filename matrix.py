class Matrix:

    def __init__(self, lines: list) -> list:

        def rewrite(ln):
            """Rewrites given lines from list"""
            n = []
            for line in ln:
                n.append([])
                for elem in line:
                    n[-1].append(elem)
            return n

        self.lines = rewrite(lines)

    def size(self):
        """Matrix size: rows * columns"""
        return len(self.lines), len(self.lines[0])

    def transpose(self):
        """Transpose: changes lines of current matrix"""
        new = [[0 for line in self.lines] for i in self.lines[0]]
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i])):
                new[j][i] = self.lines[i][j]
        self.lines = new
        return self

    def transposed(self):
        """Transpose: returns transposed matrix as different object"""
        new = [[0 for line in self.lines] for i in self.lines[0]]
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i])):
                new[j][i] = self.lines[i][j]
        return Matrix(new)

    def solve(self, coef: list) -> list:
        """Solve matrix linear system with coefficient vector"""
        if self.size()[0] < self.size()[1]:
            raise ImportError
        else:
            m = Matrix(self.lines)
            for i in range(len(m.lines[0])):
                line_num = i
                for j in range(i, len(m.lines)):
                    if m.lines[j][i] != 0:
                        break
                    line_num += 1
                if line_num == len(m.lines):
                    raise ImportError
                m.lines[line_num], m.lines[i] = m.lines[i], m.lines[line_num]
                coef[line_num], coef[i] = coef[i], coef[line_num]
                for j in range(len(m.lines)):
                    if i != j:
                        c = m.lines[j][i] / m.lines[i][i]
                        m.lines[j] = [m.lines[j][k] - c * m.lines[i][k] for k in range(len(m.lines[i]))]
                        coef[j] = coef[j] - c * coef[i]
            res = []
            for i in range(len(m.lines[0])):
                res.append(coef[i] / m.lines[i][i])
            if m.size()[0] > m.size()[1]:
                for i in range(m.size()[0] - 1, len(m.lines)):
                    ss = 0
                    for g in range(m.size()[1]):
                        ss += m.lines[i][g] * res[g]
                    if ss != coef[i]:
                        raise ImportError
            return res

    def __str__(self):
        stringed = '\n'.join(['\t'.join([str(k) for k in line]) for line in self.lines])
        return stringed

    def __add__(self, m2):
        if self.size() != m2.size():
            raise MatrixError(self, m2)
        else:
            sum = []
            for i in range(len(self.lines)):
                sum.append([])
                for j in range(len(self.lines[i])):
                    sum[-1].append(self.lines[i][j] + m2.lines[i][j])
            return Matrix(sum)

    def __mul__(self, n):
        if type(n) == Matrix or type(n) == SquareMatrix:
            if self.size()[1] != n.size()[0]:
                raise MatrixError(self, n)
            else:
                mult = [[0 for j in n.lines[0]] for i in self.lines]
                for i in range(len(self.lines)):
                    for j in range(len(n.lines[0])):
                        for k in range(len(self.lines[0])):
                            mult[i][j] += self.lines[i][k] * n.lines[k][j]
                return Matrix(mult)
        else:
            mult = []
            for line in self.lines:
                mult.append([])
                for j in line:
                    mult[-1].append(j * n)
            return Matrix(mult)

    __rmul__ = __mul__


class MatrixError(BaseException):

    def __init__(self, m1, m2):
        self.matrix1 = m1
        self.matrix2 = m2


class SquareMatrix(Matrix):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __pow__(self, p):
        rr = SquareMatrix([[0 for i in range(self.size()[0])] for j in range(self.size()[0])])
        for i in range(self.size()[0]):
            rr.lines[i][i] = 1
        n = SquareMatrix(self.lines)
        while p > 0:
            if p % 2 == 1:
                rr = rr * n
                p -= 1
            n = n * n
            p = p // 2
        print('n =', n)
        print('rr =', rr)
        return rr
