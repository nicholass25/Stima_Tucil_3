import numpy as np
import library as lb
import time
from pathlib import Path
import os

# Baca input (via file/input langsung)
print("Baca dari file? (Y/N)")
choice = input()
if(choice == 'Y'):
    print("Masukkan nama file:")
    path_input = str(input())
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('STIMA_TUCIL_3\\test\\' + path_input, cur_path)
    with open(Path(new_path), 'r') as f:
        input_matrix = np.array(
            [[int(num) for num in line.split(' ')] for line in f])
else:
    input_matrix = np.zeros((4, 4))
    for y in range(4):
        for x in range(4):
            print("Masukkan Matrix[" + str(x + 1) + "][" + str(y + 1) + "] :")
            input_matrix[y][x] = int(input())

# Main program
solved_matrix = np.array(
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
start = time.time()
print()
lb.MatrixPuzzle.print_kurangi_tabel(input_matrix)
solvable = lb.MatrixPuzzle.solvable(np.array(input_matrix))
print(f'Hasil kurang(i) + X: {solvable}', end="\n\n")

# Mengecek apakah bisa di solve atau tidak
if((solvable) % 2 == 0):
    print("Matrix awal: ")
    lb.MatrixPuzzle.print_matrix(input_matrix)
    print("\nLangkah solusi: ")

    # Manggil fungsi untuk menyelesaikan,
    list_of_matrix, solved_list_matrix, p = lb.MatrixPuzzle.solve(
        input_matrix, solved_matrix)
    for i in range(len(solved_list_matrix)):
        lb.MatrixPuzzle.print_matrix((lb.MatrixPuzzle.turn_to_list(
            0, solved_list_matrix))[i])
        print()
    lb.MatrixPuzzle.print_matrix(solved_matrix)
    print(f"\nTotal simpul hidup: {len(list_of_matrix)}", end="\n\n")
    print(f'Waktu jalan: {time.time() - start} s')
else:
    print("Unsolvable!")
