def is_empty(board):
    for i in range(len(board)):
        for j in board[i]:
            if j != " ":
                return False
    return True

def is_full(board):
    for i in range(len(board)):
        for j in board[i]:
            if j == " ":
                return False
    return True

def is_sq_in_board(board, y, x):
    if 0 <= y < len(board) and 0 <= x < len(board[0]):
        return True
    return False

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    open_bool_1 = is_sq_in_board(board, y_end + d_y, x_end + d_x) and board[y_end + d_y][x_end + d_x] == " "
    open_bool_2 = is_sq_in_board(board, y_end - d_y * length, x_end - d_x * length) and board[y_end - d_y * length][x_end - d_x * length] == " "
    if open_bool_1 and open_bool_2:
        return "OPEN"
    elif (open_bool_1 and not open_bool_2) or (open_bool_2 and not open_bool_1):
        return "SEMIOPEN"
    else:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0; y, x, = y_start, x_start; sequence = length
    while is_sq_in_board(board, y, x):
        if board[y][x] == col:
            sequence -= 1
        else:
            if sequence == 0:
                if is_bounded(board, y - d_y, x - d_x, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1
                if is_bounded(board, y - d_y, x - d_x, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
            sequence = length
        y += d_y; x += d_x
    if sequence == 0:
        if is_bounded(board, y - d_y, x - d_x, length, d_y, d_x) == "SEMIOPEN":
            semi_open_seq_count += 1
        if is_bounded(board, y - d_y, x - d_x, length, d_y, d_x) == "OPEN":
            open_seq_count += 1
    return open_seq_count, semi_open_seq_count

def detect_closed(board, col, y_start, x_start, length, d_y, d_x):
    y, x, = y_start, x_start; sequence = length; closed_count = 0
    while is_sq_in_board(board, y, x):
        if board[y][x] == col:
            sequence -= 1
        else:
            if sequence == 0:
                if is_bounded(board, y - d_y, x - d_x, length, d_y, d_x) == "CLOSED":
                    closed_count += 1
            sequence = length
        y += d_y;
        x += d_x
    if sequence == 0:
        if is_bounded(board, y - d_y, x - d_x, length, d_y, d_x) == "CLOSED":
            closed_count += 1
    return closed_count

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    for y in range(len(board)):
        open_seq_count += detect_row(board, col, y, 0, length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col, y, 0, length, 0, 1)[1]    # everything horizontal
        if y < len(board):
            open_seq_count += detect_row(board, col, y, 0, length, 1, 1)[0]
            semi_open_seq_count += detect_row(board, col, y, 0, length, 1, 1)[1]     # half of across down
        if 0 < y < len(board):
            open_seq_count += detect_row(board, col, y, len(board[0]) - 1, length, 1, -1)[0]
            semi_open_seq_count += detect_row(board, col, y, len(board[0]) - 1, length, 1, -1)[1]   # half of across up
    for x in range(len(board[0])):
        open_seq_count += detect_row(board, col, 0, x, length, 1, 0)[0]
        semi_open_seq_count += detect_row(board, col, 0, x, length, 1, 0)[1]     # everything vertical
        if 0 < x < len(board[0]):
            open_seq_count += detect_row(board, col, 0, x, length, 1, 1)[0]
            semi_open_seq_count += detect_row(board, col, 0, x, length, 1, 1)[1]   # half of across down
            open_seq_count += detect_row(board, col, 0, x, length, 1, -1)[0]
            semi_open_seq_count += detect_row(board, col, 0, x, length, 1, -1)[1]  # half of across up
    return open_seq_count, semi_open_seq_count

def detect_closeds(board, col, length):
    closed_count = 0
    for y in range(len(board)):
        closed_count += detect_closed(board, col, y, 0, length, 0, 1)   # everything horizontal
        if y < len(board):
            closed_count += detect_closed(board, col, y, 0, length, 1, 1)     # half of across down
        if 0 < y < len(board):
            closed_count += detect_closed(board, col, y, len(board[0]) - 1, length, 1, -1)   # half of across up
    for x in range(len(board[0])):
        closed_count += detect_closed(board, col, 0, x, length, 1, 0)    # everything vertical
        if 0 < x < len(board[0]):
            closed_count += detect_closed(board, col, 0, x, length, 1, 1)   # half of across down
            closed_count += detect_closed(board, col, 0, x, length, 1, -1)  # half of across up
    return closed_count

def search_max(board):
    high = 0
    res = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                board[i][j] = "b"
                if res is None or score(board) > high:
                    high = score(board)
                    res = i, j
                board[i][j] = " "
    return res

def is_win(board):
    seq_5_open, seq_5_semi, seq_5_closed = detect_rows(board, "w", 5)[0], detect_rows(board, "w", 5)[1], detect_closeds(board, "w", 5)
    if seq_5_open > 0 or seq_5_semi > 0 or seq_5_closed > 0:
        return "White won"
    else:
        seq_5_open, seq_5_semi, seq_5_closed = detect_rows(board, "b", 5)[0], detect_rows(board, "b", 5)[1], detect_closeds(board, "b", 5)
        if seq_5_open > 0 or seq_5_semi > 0 or seq_5_closed > 0:
            return "Black won"
    if not is_full(board):
        return "Continue playing"
    return "Draw"


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def print_board(board):
    s = "*"
    for i in range(len(board[0]) - 1):
        s += str(i % 10) + "|"
    s += str((len(board[0]) - 1) % 10)
    s += "*\n"
    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0]) - 1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0]) - 1])

        s += "*\n"
    s += (len(board[0]) * 2 + 1) * "*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "] * sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x
