from collections import deque

# def weigh_surrounding

def BFS_weigh (init_row, init_col, map_row, map_col, source_map, man_board):
  weight_map = []
  weight_map = [0]*map_row
  for r in range(map_row):
    weight_map[r] = [0]*map_col

  arr_4d = [(0,1), (0,-1),(1,0), (-1,0)]
  record = deque()
  item=(init_row, init_col)
  record.append(item)
  bridges = bridge_list(man_board)

  weight_map[init_row][init_col] = 1

  weigh_numb = 2
  while (len(record)!= 0):
    temp = len(record)
    for _ in range(temp):
      row, col = record.popleft()
       
      for direction in arr_4d:
        r,c = direction
        new_row = row+r
        new_col = col+c

        if (new_row < 0 or new_row >= map_row or new_col < 0 or new_col >= map_col):
          continue


        if (weight_map[new_row][new_col] == False and \
            (source_map[new_row][new_col] != 0 or (new_row, new_col) in bridges)):
          weight_map[new_row][new_col] = weigh_numb
          record.append((new_row, new_col))
    
    weigh_numb +=1

  # map_bridge_to_switch(man_board, weight_map, map_row, map_col, source_map)
  # print(weight_map)
  return weight_map

def bridge_list(man_board):
  bri = []
  for r in range(len(man_board)):
    bri.append(man_board[r][3:])
  
  flatten_list = [item for sublist in bri for item in sublist]
  it = iter(flatten_list)
  tuple_row_col = list(zip(it,it))
  # print(tuple_row_col)

  return tuple_row_col

def map_bridge_to_switch(man_board, weight_map, map_row, map_col, source_map):
  bridges = bridge_list(man_board)
  for item in man_board:
    col = item[0]
    row = item[1]
    # print(item)
    weigh = weight_map[item[3]][item[4]]
    weight_map[row][col] = weigh

    arr_4d = [(0,1), (0,-1),(1,0), (-1,0)]
    for direction in arr_4d:
      r,c = direction
      new_row = row+r
      new_col = col+c

      if (new_row < 0 or new_row >= map_row or new_col < 0 or new_col >= map_col):
        continue

      if (source_map[new_row][new_col] != 0 or (new_row, new_col) not in bridges):
        weight_map[new_row][new_col] = weigh+1


# boarding = [[2, 2, 2, 4, 4, 4, 5],[8, 1, 2, 4, 10, 4, 11]]
# print(map_bridge_to_switch(2,2,boarding))



# def main ():
#   new_map = [0]*MAP_ROW
#   for r in range(MAP_ROW):
#     new_map[r] = [0]*MAP_COL

#   BFS_weigh(7, 6, new_map)
#   print_arr(new_map)

# def print_arr (arr_2d):
#   for row in arr_2d:
#     print(f'\n {row}')
  
  


#########
# MAP_ROW, MAP_COL, xStart, yStart, source_map, man_board = read_map(
#     'map/map04.txt')

# main()