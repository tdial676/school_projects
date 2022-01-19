"""
Thierno Diallo

Midterm_PartC

This is a coded implementation of the Jeopardy game.
"""
import csv
# Note: This constant is used to improve efficiency in some 
# areas, assuming there are TOTAL_SHOWS in jeopardy_data.csv 
# and showids are in consecutive order in the CSV file. This 
# constant will need to be changed if the dataset changes in 
# the future.
TOTAL_SHOWS = 3640


#C.1
def get_game_data(show_id):
  """
  This function takes an int showid number and finds the air date,
  number of rows, and the game data for that show from the jeopardy csv file
  as a tuple.

  Arguments: int (showid)
  Return Value: a tuple (air_date, row_count, game_data)
  """
  row_count = 0
  game_data = {}
  with open('jeopardy_data.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for line in reader:
      if int(line['showid']) == show_id:
        row_count +=1
        air_date = line['airdate']
        if line['category'] not in game_data:
          game_data[line['category']] = {}
        game_data[line['category']][line['value']] = (line['question']\
                                                    , line['answer'])
      elif int(line['showid']) > show_id:
        return (air_date, row_count, game_data)
  return (air_date, row_count, game_data)


#C.2
def print_column_header(clm_names):
  """
  This function takes a list of column names and prints them as a
  structured table.

  Arguments: list of column name
  Return Value: None
  """
  line_1 = ' | '.join(clm_names)
  line_2 = '-' * len(line_1)
  print(f'{line_1}\n{line_2}')


#C.3
def dict_to_table(dict, int_num):
  """
  This function takes a dictionary and an int and returns a nested list
  of n rows, with each row containing the score value for each category 
  column having that value as a key 

  Arguments:
    - a dictionary of categories mapping to value dictionaries (dict)
    - an int (int_num)
  Return Value: a nested list of n rows
  """
  final_lst = []
  for num in range(int_num):
    new_lst = []
    value = str((num + 1) * 100)
    for catagory in dict:
      if value not in dict[catagory]:
        new_lst.append('---')
      else:
        new_lst.append(value)
    final_lst.append(new_lst)
  return final_lst


#C.4
def print_game_table(game_data_dic):
  """
  This funtion takes a dictionary and prints the dictionary
  in a table format with columns and rows.

  Argument: a dictionary 
  Return Value: None
  """
  keys = list(game_data_dic.keys())
  print_column_header(keys)
  table = dict_to_table(game_data_dic, 5)
  final_lst = [] 
  for i,lst in enumerate(table):
    empty_lst = []
    for n in range(len(lst)):
      space = table[i][n] + ' ' * (len(keys[n]) - 3)
      empty_lst.append(space)
    final_lst.append(' | '.join(empty_lst))
  line = '\n'.join(final_lst)
  print(f'{line}')


# C.5
def play_round(game_data):
  """
 This function takes a dictionary and promts the user for input 
 regarding the catagory, question value, and aswer and prints whether their 
 answers are correct or incorrect. Also, it returns the points they
 gained from answering that question.

 Arguments: a dictionary of game data
 Return Value: an int number of points
  """
  print_game_table(game_data)
  category = input('Choose a category: ').upper()
  while not category in game_data or not game_data[category]:
    print('Incorrect category.')
    category = input('Choose a category: ').upper()
  
  value = input('Choose a value: ')
  while value not in game_data[category]:
    print('Incorrect value.')
    value = input('Choose a value: ')
  # while loop ends
  question = game_data[category][value][0]
  answer = game_data[category][value][1]
  print (f'(Q) {question}')
  guess = input('(A) What is: ').lower()
  del game_data[category][value]
  if guess != answer.lower():
    print(f'Incorrect.\n(Correct answer): What is: {answer}')
    return 0
  else:
    print('Correct!')
    return int(value)
  
    
# C.6.
def start_game():
  """
  This functions takes no arguments and prompts the user for input
  about which catagories and from which showid they want to play from.
  it returns false for the user is done playing and prints their score.

  Arguments: None
  Return Value: a bool false
  """
  showid = 0
  while True:
    showid = int(input('Select a Show ID between 1 and ' + \
                      f'{TOTAL_SHOWS} to play: '))
    if showid > 0 and showid <= TOTAL_SHOWS:
      break
    else:
      print('Incorrect showid given.')
  (air_date, row_count, game_data) = get_game_data(showid)
  print(f'Show Airdate: {air_date}')
  score = 0
  while True:
    score += play_round(game_data)
    replay = input('Continue? (y for yes) ')
    if replay.lower() != 'y':
      print(f'You won a total of {score}')
      return False


if __name__ == '__main__':
    start_game()
