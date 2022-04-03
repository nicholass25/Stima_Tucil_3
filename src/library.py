import numpy as np


class MatrixPuzzle:

    # Bikin datatype baru
    def __init__(Matrix, pos, P, C, W):
        Matrix.pos = pos
        Matrix.P = P
        Matrix.C = C
        Matrix.W = W

    # mengubah list of datatype Matrix ke yg diinginkan
    def turn_to_list(type, listIn):
        listOut = []
        if(type == 0):
            for i in range(len(listIn)):
                listOut.append(listIn[i].pos)
        elif(type == 1):
            for i in range(len(listIn)):
                listOut.append(listIn[i].P)
        elif(type == 2):
            for i in range(len(listIn)):
                listOut.append(listIn[i].C)
        elif(type == 3):
            for i in range(len(listIn)):
                listOut.append(listIn[i].W)
        return listOut

    # Print matriks dengan susunan rapi
    def print_matrix(matrix):
        for i in range(4):
            for j in range(4):
                if(matrix[i][j] > 9):
                    print(f"| {matrix[i][j]} ", end="")
                else:
                    print(f"| {matrix[i][j]}  ", end="")
                if(j == 3):
                    print("|")

    # Melakukan branch dari satu matrix ke beberapa matrix yang memungkinkan
    def GDown(matrix, last_move, p):
        LOut = []
        for i in range(4):
            if(MatrixPuzzle.movable(matrix, i) and i != last_move):
                temp = MatrixPuzzle.move(matrix, i)
                LOut.append(MatrixPuzzle(
                    temp, p + 1, MatrixPuzzle.findC(temp, p), i))
        return LOut

    # Print tabel dari i dan kurang(i)
    def print_kurangi_tabel(matrix):
        l = matrix.reshape(-1)
        tabel_kurangi = []
        for a in range(16):
            if(l[a] == 0):
                l[a] = 16
        for i in range(16):
            total = 0
            for j in range(i, 16):
                if(l[i] > l[j]):
                    total += 1
            tabel_kurangi.append([l[i], total])
        tabel_kurangi.sort()
        for b in range(16):
            if(l[b] == 16):
                l[b] = 0
        tabel_kurangi = [["i", "kurang(i)"]] + tabel_kurangi
        for k in range(17):
            for l in range(2):
                if(k > 9):
                    print(tabel_kurangi[k][l], end="   ")
                else:
                    print(tabel_kurangi[k][l], end="    ")
            print("")
        print("")

    # Mengecek apakah satu matrix ada di list matrix
    def matrix_in(M, MPlist):
        for i in range(len(MPlist)):
            if np.array_equal(M, np.array(MPlist[i].pos)):
                return True
        return False

    # Mencari lokasi dari 0 di matrix
    def find0(Matrix):
        for y in range(4):
            for x in range(4):
                if(Matrix[y][x] == 0):
                    return [x, y]

    # Mengeluarkan hasil dari kurang(i) + x
    def solvable(Matrix):
        total = 0
        if((MatrixPuzzle.find0(Matrix)[0] + (MatrixPuzzle.find0(Matrix)[1]*4)) % 2 == 0):
            x = 1
        else:
            x = 0
        l = Matrix.reshape(-1)
        for a in range(16):
            if(l[a] == 0):
                l[a] = 16
        for i in range(16):
            for j in range(i, 16):
                if(l[i] > l[j]):
                    total += 1
        return total + x

    # Mengecek apakah gerakan tertentu itu valid atau tidak
    def movable(Matrix, dir):
        x = MatrixPuzzle.find0(Matrix)[0]
        y = MatrixPuzzle.find0(Matrix)[1]
        if (dir == 0):
            if(y - 1 > -1):
                return True
        elif(dir == 1):
            if(x + 1 < 4):
                return True
        elif (dir == 2):
            if(y + 1 < 4):
                return True
        elif(dir == 3):
            if(x - 1 > -1):
                return True
        return False

    # Melakukan pertukaran lokasi 0
    def move(Matrix, dir):
        Mout = np.copy(Matrix)
        x = MatrixPuzzle.find0(Matrix)[0]
        y = MatrixPuzzle.find0(Matrix)[1]
        if (dir == 0):
            Mout[y][x] = Matrix[y - 1][x]
            Mout[y - 1][x] = 0
        elif(dir == 1):
            Mout[y][x] = Matrix[y][x + 1]
            Mout[y][x + 1] = 0
        elif (dir == 2):
            Mout[y][x] = Matrix[y + 1][x]
            Mout[y + 1][x] = 0
        elif(dir == 3):
            Mout[y][x] = Matrix[y][x - 1]
            Mout[y][x - 1] = 0
        return Mout

    # Mencari g(i)
    def findG(Matrix):
        k = 1
        total = 0
        for i in range(4):
            for j in range(4):
                if(k > 15 and total == 0):
                    total = 0
                elif(Matrix[i][j] == k):
                    k += 1
                else:
                    total += 1
                    k += 1
        return total

    # Mencari c(i) dengan f(i) + g(i)
    def findC(Matrix, p):
        g = MatrixPuzzle.findG(Matrix)
        return g + p

    # Melakukan penyelesaiian, menghasilkan semua simpul hidup, list dari matrix yang menjadi langkah, serta berapa langkah yang dilakukan
    def solve(matrix, solved_matrix):
        # inisialisasi
        list_of_matrix = []
        list_step_matrix = []
        p = 0
        last_move = -1

        # Melakukan penurunan dengan langkah-langkah yang ada
        list_of_matrix += MatrixPuzzle.GDown(matrix, last_move, p)
        p = 1
        last_move = MatrixPuzzle.turn_to_list(2, list_of_matrix).index(
            min(MatrixPuzzle.turn_to_list(2, list_of_matrix)))

        # Diulang sampai ada solusi matrix yang ada di list_of_matrix
        while(not MatrixPuzzle.matrix_in(solved_matrix, list_of_matrix)):
            temp_matrix = list_of_matrix[MatrixPuzzle.turn_to_list(2, list_of_matrix).index(
                min(MatrixPuzzle.turn_to_list(2, list_of_matrix)))].pos
            to_be_pop = MatrixPuzzle.turn_to_list(2, list_of_matrix).index(
                min(MatrixPuzzle.turn_to_list(2, list_of_matrix)))

            list_step_matrix.append(list_of_matrix[to_be_pop])
            list_of_matrix += MatrixPuzzle.GDown(temp_matrix, last_move, p)
            list_of_matrix.pop(to_be_pop)

            p += 1
            last_move = MatrixPuzzle.turn_to_list(2, list_of_matrix).index(
                min(MatrixPuzzle.turn_to_list(2, list_of_matrix)))
        return list_of_matrix, list_step_matrix, p
