import numpy as np

def make_matrix_with_arrows(s1, s2, match=1, mismatch=-1, gap=-2):
    
    rows = len(s2) + 1
    cols = len(s1) + 1
    matrix = np.zeros((rows, cols), dtype=int)
    arrows = np.full((rows, cols), "", dtype=object)
    
    for i in range(1, rows):
        matrix[i][0] = matrix[i-1][0] + gap
        arrows[i][0] = '↑'  
    for j in range(1, cols):
        matrix[0][j] = matrix[0][j-1] + gap
        arrows[0][j] = '←'  
    
    for i in range(1, rows):
        for j in range(1, cols):
            if s1[j-1] == s2[i-1]:
                score = match
            else:
                score = mismatch
            diag = matrix[i-1][j-1] + score
            up = matrix[i-1][j] + gap
            left = matrix[i][j-1] + gap
            
            best = max(diag, up, left)
            matrix[i][j] = best
            
            arrow_str = ""
            if best == diag:
                arrow_str += '↖'  
            if best == up:
                arrow_str += '↑'  
            if best == left:
                arrow_str += '←'  
            arrows[i][j] = arrow_str
    
    string_mat = np.full((rows, cols), "", dtype=object)
    for i in range(rows):
        for j in range(cols):
            string_mat[i][j] = f"{matrix[i][j]} {arrows[i][j]}"
    return string_mat

s1 = input("Enter sequence 1: ")
s2 = input("Enter sequence 2: ")
match = int(input("Enter match score: "))
mismatch = int(input("Enter mismatch score: "))
gap = int(input("Enter gap penalty: "))

result_matrix = make_matrix_with_arrows(s1, s2, match, mismatch, gap)
print()
for row in result_matrix:
    print("\t".join(row))
