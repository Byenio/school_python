file = open("szachy.txt")

board = []
white = []
black = []

for line in file:
    board.append(line[:8])
    for box in line[:8]:
        if box.isupper():
            white.append(box)
        elif box.islower():
            black.append(box.upper())


# print(board)
# print("white", len(white), white, sep=" ")
# print("black", len(black), black, sep=" ")
#
# if sorted(white) == sorted(black):
#     print("rownowaga")


def find_kings():  # finds white and black king's coordinates, later 'cords'
    white_king = []
    black_king = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'k':
                black_king = [i, j]
            if board[i][j] == 'K':
                white_king = [i, j]
    return white_king, black_king


kings = find_kings()  # saves cords to a variable


def enemy(piece, char):  # checks for enemy pieces color and returns either lowercase or uppercase letter
    if piece.isupper():
        return char.lower()
    else:
        return char.upper()


def find_rook_captures(cords_x, cords_y):  # finds possible rooks captures based on white or black king's cords
    rooks = ['By rooks']
    compare_to = enemy(board[cords_x][cords_y], 'w')

    # finds possible rooks captures in all directions, checks for collision
    for i in range(cords_x):
        square = board[i][cords_y]
        free_of_collision = True
        if square == compare_to:
            for j in range(i + 1, cords_x):
                if board[j][cords_y] != '.':
                    free_of_collision = False
            if free_of_collision:
                rooks.append([cords_y, i])

    for i in range(cords_x + 1, 8):
        square = board[i][cords_y]
        free_of_collision = True
        if square == compare_to:
            for j in range(cords_x + 1, i):
                if board[j][cords_y] != '.':
                    free_of_collision = False
            if free_of_collision:
                rooks.append([cords_y, i])

    for i in range(cords_y):
        square = board[cords_x][i]
        free_of_collision = True
        if square == compare_to:
            for j in range(i + 1, cords_y):
                if board[cords_x][j] != '.':
                    free_of_collision = False
            if free_of_collision:
                rooks.append([i, cords_x])

    for i in range(cords_y + 1, 8):
        square = board[cords_x][i]
        free_of_collision = True
        if square == compare_to:
            for j in range(cords_y + 1, i):
                if board[cords_x][j] != '.':
                    free_of_collision = False
            if free_of_collision:
                rooks.append([i, cords_x])

    return rooks  # returns array with possible rooks captures


def find_bishop_captures(cords_x, cords_y):  # finds possible bishop captures based on white or black king's cords
    bishops = ['By bishops']
    compare_to = enemy(board[cords_x][cords_y], 'b')

    def collision(collides, arr):
        if collides & (len(arr) > 0):
            bishops.append(arr[0])

    # finds possible bishop captures in all directions, checks for collision
    i = cords_x - 1
    j = cords_y - 1
    free_of_collision = True
    cords = []
    while (i >= 0) & (j >= 0):
        square = board[i][j]
        if square == compare_to:
            cords.append([i, j])
            x = cords_x - 1
            y = cords_y - 1
            diagonal = []
            while (x >= i) | (y >= j):
                diagonal.append(board[x][y])
                x -= 1
                y -= 1
            for i in range(diagonal.count('.')):
                diagonal.remove('.')
            if (diagonal[0] != '.') & (diagonal[0] != compare_to):
                free_of_collision = False
        i -= 1
        j -= 1

    collision(free_of_collision, cords)

    i = cords_x + 1
    j = cords_y + 1
    free_of_collision = True
    cords = []
    while (i <= 7) & (j <= 7):
        square = board[i][j]
        if square == compare_to:
            cords.append([i, j])
            x = cords_x + 1
            y = cords_y + 1
            diagonal = []
            while (x <= i) | (y <= j):
                diagonal.append(board[x][y])
                x += 1
                y += 1
            for i in range(diagonal.count('.')):
                diagonal.remove('.')
            if (diagonal[0] != '.') & (diagonal[0] != compare_to):
                free_of_collision = False
        i += 1
        j += 1

    collision(free_of_collision, cords)

    i = cords_x - 1
    j = cords_y + 1
    free_of_collision = True
    cords = []
    while (i >= 0) & (j <= 7):
        square = board[i][j]
        if square == compare_to:
            cords.append([i, j])
            x = cords_x - 1
            y = cords_y + 1
            diagonal = []
            while (x >= i) | (y <= j):
                diagonal.append(board[x][y])
                x -= 1
                y += 1
            for i in range(diagonal.count('.')):
                diagonal.remove('.')
            if diagonal[0] != compare_to:
                free_of_collision = False
        i -= 1
        j += 1

    collision(free_of_collision, cords)

    i = cords_x + 1
    j = cords_y - 1
    free_of_collision = True
    cords = []
    while (i <= 7) & (j >= 0):
        square = board[i][j]
        if square == compare_to:
            cords.append([i, j])
            x = cords_x + 1
            y = cords_y - 1
            diagonal = []
            while (x <= i) | (y >= j):
                diagonal.append(board[x][y])
                x += 1
                y -= 1
            for i in range(diagonal.count('.')):
                diagonal.remove('.')
            if diagonal[0] != compare_to:
                free_of_collision = False
        i += 1
        j -= 1

    collision(free_of_collision, cords)

    return bishops  # returns array with possible bishop captures


def find_all_captures(white_king_cords, black_king_cords):
    # rooks -> wieze
    captures_by_black_rooks = find_rook_captures(white_king_cords[0], white_king_cords[1])
    captures_by_white_rooks = find_rook_captures(black_king_cords[0], black_king_cords[1])

    # bishops -> gonce
    captures_by_black_bishops = find_bishop_captures(white_king_cords[0], white_king_cords[1])
    captures_by_white_bishops = find_bishop_captures(black_king_cords[0], black_king_cords[1])

    return [captures_by_black_rooks, captures_by_black_bishops], [captures_by_white_rooks, captures_by_white_bishops]


captures = find_all_captures(kings[0], kings[1])
print('Black captures: ', captures[0][0], captures[0][1])
print('White captures: ', captures[1][0], captures[1][1])
