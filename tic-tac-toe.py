import sys
sys.path.append('../')
from board_utils.board import *

def unfill_postion(board, row_postion, column_postion, value):
  #unfill_postion 
  counter = 1
  for row in range(len(board)):
    for col in range(len(board[row])):
      if row == row_postion and col == column_postion:
          fill_postion(board, row, col, counter)
          return
      counter+= 1
   

def winner(board, character):
  # we got a verical winner
  for row in range(len(board)):
    if equals(board[row][0], board[row][1], board[row][2]):
      if character:
       return board[row][0]
      else:
        return True
  
  # we got a horizontal winner
  for col in range(len(board[row])):
    if equals(board[0][col], board[1][col],board[2][col]):
      if character:
        return board[0][col]
      else:
        return True

  # we got a winner going diagonal from top left
  if equals(board[0][0], board[1][1], board[2][2]):
    if character:
      return board[0][0]
    else:
      return True
  # we got a winner going diagonal from top right
  if equals(board[0][2], board[1][1], board[2][0]):
    if character:
      return board[0][2]
    else:
      return True
  # no winners
  if character:
    return "none"
  else:
    return False

# should take in a number arugement to go and the number should be between 1 - 9
def valid_move(number_position, board):
  """checks if a move is valid. returns either true or false"""
  for row in range(len(board)):
    for col in range(len(board[row])):
      if board[row][col] == number_position:
        # print("this is true: ", board[row][col], number_position)
        return True # move is valid return true 
  return False

# checking if the user input is valid, if not keep looping over until desired input is done, also handles valid_move()
def valid_input(input_string, board):
  """checks if the user input is valid, if not keep looping over until desired input is done"""
  not_valid = True # easier to read and understand the while loop
  while not_valid:
    is_number = input_string.isdigit() # checking if the input_string has a number in the string
    if is_number: # if is_number is true
      number = int(input_string) #convert input string to a int and store it to the number variable
      
      if number > 9 or number < 1: # if the number is not the desired options 
        print("invalid number") # informing the player, that the last input was a invalid number
        input_string = input("type a number postion to go there: ") # asking user for a new input
        continue # loops back with the new input that has been stored in the input_string

      elif valid_move(number, board) == False: # if the move is not valid 
        print("invalid space")
        input_string = input("type a number postion to go there: ") # asking user for a new input
        continue

      else: # if the number is valid then return the number and leaves the loop
        return number 

    else: # if the is_number is false / input is not a number
      print("invalid input") # informs the player, the previous input was not valid
      input_string = input("type a number postion to go there: ") # loops back with the new input that has been stored in the input_string


scores = {
  "X": -50, # if player 1 wins the game the computer gets a negative score 
  "O": 1000, # if player 2 wins give the computer a postive score
  "none": 0 # if none player wins give a score that is not negative or postive
}

def minimax(board, depth, maximizing_player):
  """returns a score value, depth determines how far forward to work from"""
  result = winner(board, True) # results on who is winning the game to determine the score 
  if depth == 0 or result != "none": # when the depth has hit 0 it will return a score or when the result not none
    score = scores[result] # checks the result winning character and puts into the scores dictonary and determines the score
    return score # returns score 
  
  if maximizing_player: # if its the maximizing turn 
    best_score = -math.inf  # setting the best score to be -infinity 
    number = 1
    for row in range(0, len(board)):
      for col in range(0, len(board[row])): # loops through the column
        if valid_move(number, board) == True: # if the spot is available
          fill_postion(board, row, col, player_2)# places the ai in the first spot 
          score = minimax(board, depth - 1, False) # checks the score by going further predicting game states
          unfill_postion(board, row, col, player_2) # removes the player from that spot 
          best_score = max(score, best_score) # compares the new score to the old best_score and chooses the higher score
        number+= 1
    return best_score # returns the best score that it has calculated

  else: # its not the maximizing player so going to make the best move for the player so lower score for the ai 
    best_score = math.inf # sets the score to the + infinity 
    number = 1
    for row in range(0, len(board)):
      for col in range(0, len(board[row])): # loops through the columns to choose from
        if valid_move(number, board) == True: # if the move is valid
          fill_postion(board, row, col, player_1) # places the player piece to 
          score = minimax(board, depth - 1, True) # checks the score by going further predicting game states
          unfill_postion(board, row, col, player_1) # removes the player piece from the board so it loops to the next column position 
          best_score = min(score, best_score) # compares the new score to the old best score and chooses the lower score 
        number += 1
    return best_score # returns the best score that it has calculated


def best_move(board):
  """returns a column to choose from. Uses the minimax algorithm to determine where to go"""
  best_score = -math.inf # best score is set to -infinity 
  coords = {} # creates the coords to return to the player
  score = -math.inf # score has to be defined and is set to -infinity 
  number = 1
  for row in range(0, len(board)):
    for column in range(0, len(board[row])): # loops through the columns
      print("working on it...") # tells the player that the ai is working on a move to make
      if valid_move(number, board) == True: # if the spot is available
        fill_postion(board, row, column, player_2)# places the ai in the first spot 
        score = minimax(board, 2, False) # checks the score by going deeper 
        unfill_postion(board, row, column, player_2) # removes the player from that spot 

      if score > best_score: # when the score is greater than the best score replace it
        # draw_board(board)
        # print("score: ", score)
        best_score = score # replacing the best score to score value
        coords["pos"] = number # storing the column value to the coords with a key of "col"
      number += 1
  print(coords)
  return coords["pos"] # returns the value of column postion 



# initizing the game
board = create_board(3,3)

counter = 1
for row in range(len(board)):
  for col in range(len(board[row])):
    if board[row][col] == "0":
        fill_postion(board, row, col, counter)
    counter+= 1


switch_player = 1
player_1 = "X"
player_2 = "O"
playing = True
computer = True

# game starts from here 
while playing:
  if switch_player == 1:
    current_player = player_1
  else:
    current_player = player_2
  print("\n" * 55)
  print("-" * 13)
  draw_board(board)
  print("-" * 13)

  if computer and current_player == player_2:
    number_postion = best_move(board)
  else:
    number_postion = valid_input(input("type a number postion to go there: "), board)


  for row in range(len(board)):
    for col in range(len(board[row])):
      if board[row][col] == number_postion:
          fill_postion(board, row, col, current_player)

  if winner(board, False):
    print(winner(board, False))
    playing = False
    print("\n" * 55)
    print(f"congrats {current_player} for winning the game")
    draw_board(board)
    break
  else:
    switch_player = -switch_player

  # check if its full  
  is_full = True
  for row in board:
    if is_full == False:
      break
    for numbers in range(1, 10):
      if numbers in row:
        is_full = False
        break
      else:
        is_full = True


  if is_full:
    playing = False
    print("it's a tie!")
  else:
    continue

 
  
