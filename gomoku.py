# Alexander Wang and Pierre Ishak
# November 19, 2021

def is_empty(board):
    '''Checks if board empty'''
    for i in range(len(board)):
      for j in range(len(board[0])):
        if board[i][j] != " ":
          return False
    return True
  
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''Returns OPEN, CLOSED, SEMIOPEN sequence'''
    start = False
    end = False
    #Checks start
    if len(board) not in (y_end - length * d_y, x_end - length * d_x) and -1 not in (y_end - length * d_y, x_end - length * d_x):
      if board[y_end - length * d_y][x_end - length * d_x] == " ":
        start = True
    #Checks end 
    if len(board) not in (y_end + d_y, x_end + d_x) and -1 not in (y_end + d_y, x_end + d_x):
      if board[y_end + d_y][x_end + d_x] == " ":
        end = True
  
    if start and end:
      return "OPEN"
    elif not start and not end:
      return "CLOSED"
    else:
      return "SEMIOPEN"
    
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0
    count = 0

    for i in range(len(board)):
      if board[y_start][x_start] == col:
        count += 1
        
        if count == length:
          #Checks if the end is an edge
          if (len(board) in (y_start + d_y, x_start + d_x)) or (-1 in (y_start + d_y, x_start + d_x)):
            if is_bounded(board, y_start, x_start, count, d_y, d_x) == "OPEN":
              open_seq_count += 1
            elif is_bounded(board, y_start, x_start, count, d_y, d_x) == "SEMIOPEN":
              semi_open_seq_count += 1
      else:
        if count == length:
          #Normal case
          if is_bounded(board, y_start - d_y, x_start - d_x, count, d_y, d_x) == "OPEN":
            open_seq_count += 1
          elif is_bounded(board, y_start - d_y, x_start - d_x, count, d_y, d_x) == "SEMIOPEN":
            semi_open_seq_count += 1
            
        count = 0
        
      y_start += d_y
      x_start += d_x
    
      if len(board) in (y_start, x_start) or -1 in (y_start, x_start):
        break

    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    
    for i in range (len(board)):
      # Horizontal:
      open_seq_count += detect_row(board, col, i, 0 , length, 0 , 1)[0]
      semi_open_seq_count += detect_row(board, col, i, 0 , length, 0 , 1)[1]

      # Vertical:
      open_seq_count += detect_row(board, col, 0, i, length, 1 , 0)[0]
      semi_open_seq_count += detect_row(board, col, 0, i, length, 1 , 0)[1]
      
      # TL to BR:
        # Left edge
      open_seq_count += detect_row(board, col, i, 0, length, 1, 1)[0]
      semi_open_seq_count += detect_row(board, col, i, 0, length, 1, 1)[1]
        # Top edge
      open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[0]
      semi_open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[1]
        
      #TR to BL:  
        # Right edge
      open_seq_count += detect_row(board, col, i, len(board) - 1, length, 1, -1)[0]
      semi_open_seq_count += detect_row(board, col, i, len(board) - 1, length, 1, -1)[1]
        # Top edge
      open_seq_count += detect_row(board, col, 0, i, length, 1, -1)[0]
      semi_open_seq_count += detect_row(board, col, 0, i, length, 1, -1)[1]
        
    # Deletes repeated iteration
    open_seq_count -= detect_row(board, col, 0, 0, length, 1, 1)[0]
    semi_open_seq_count -= detect_row(board, col, 0, 0, length, 1, 1)[1]
    # Deletes repeated iteration
    open_seq_count -= detect_row(board, col, 0, len(board) - 1, length, 1, -1)[0]
    semi_open_seq_count -= detect_row(board, col, 0, len(board) - 1, length, 1, -1)[1]
    
    return open_seq_count, semi_open_seq_count
    
def search_max(board):
  move_y = 0
  move_x = 0
  maxPoints = -100001
  
  for i in range(len(board)):
    for j in range(len(board)):
      if board[i][j] == " ":
        board[i][j] = "b"
        currentPoints = score(board)
        if currentPoints > maxPoints:
          maxPoints = currentPoints
          move_y = i
          move_x = j         
        board[i][j] = " "
  return move_y, move_x
    
def score(board):
    '''Computes and returns the score for the position of the board. It assumes that black has just moved'''
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
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def is_win_closed(board):
  b_win = False
  w_win = False

  if detect_closed_rows(board, "b") > 0:
    b_win = True
  if detect_closed_rows(board, "w") > 0:
    w_win = True

  return b_win, w_win

def detect_closed_rows(board, col):
  closed_seq_count = 0
  for i in range(len(board)):
    # Horizontal:
    closed_seq_count += detect_closed_row(board, col, i, 0 , 5, 0 , 1)
    # Vertical:
    closed_seq_count += detect_closed_row(board, col, 0, i, 5, 1 , 0)
    # TL to BR:
      # Left edge
    closed_seq_count += detect_closed_row(board, col, i, 0, 5, 1, 1)
      # Top edge
    closed_seq_count += detect_closed_row(board, col, 0, i, 5, 1, 1)
    #TR to BL:  
      # Right edge
    closed_seq_count += detect_closed_row(board, col, i, len(board) - 1, 5, 1, -1)
      # Top edge
    closed_seq_count += detect_closed_row(board, col, 0, i, 5, 1, -1)
  # Deletes repeated iteration
  closed_seq_count -= detect_closed_row(board, col, 0, 0, 5, 1, 1)
  # Deletes repeated iteration
  closed_seq_count -= detect_closed_row(board, col, 0, len(board) - 1, 5, 1, -1)

  return closed_seq_count

def detect_closed_row(board, col, y_start, x_start, length, d_y, d_x):
    closed_seq_count = 0
    count = 0

    for i in range(len(board)):
      if board[y_start][x_start] == col:
        count += 1
        
        if count == length:
          #Checks if the end is an edge
          if (len(board) in (y_start + d_y, x_start + d_x)) or (-1 in (y_start + d_y, x_start + d_x)):
            if is_bounded(board, y_start, x_start, count, d_y, d_x) == "CLOSED":
              closed_seq_count += 1
      else:
        if count == length:
          #Checks if closed but the end is another player
          if is_bounded(board, y_start - d_y, x_start - d_x, count, d_y, d_x) == "CLOSED":
            closed_seq_count += 1            
        count = 0
        
      y_start += d_y
      x_start += d_x
    
      if len(board) in (y_start, x_start) or -1 in (y_start, x_start):
        break

    return closed_seq_count

def is_win(board):
    if score(board) == 100000 or is_win_closed(board)[0]:
      return "Black won"
    elif score(board) == -100000 or is_win_closed(board)[1]:
      return "White won"
    elif not any(" " in i for i in board):
      return "Draw"
    else:
      return "Continue playing"

def print_board(board):
    '''Prints out the Gomoku Board'''
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    '''Analyses the position of the board by computing the number of open and semi-open sequences of both colours.'''
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open)) 
    
def play_gomoku(board_size):
    '''Allows the user to play against a computer on a board of size 'board_size'x'board_size'. Interacts with the AI engine by calling the function searchMax().'''
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
        #analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        #analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    '''Adds the sequence of stones of colour col of length 'length' to 'board', starting at location (y, x) and moving in the direction (d_y, d_x). Facilitates the testing the AI engine.'''
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

if __name__ == '__main__':
  play_gomoku(8)