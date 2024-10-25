import pygame
import random
import pyautogui
from pygame.locals import *
import math

class Tiles:
    def __init__(self, screen, start_position_x, start_position_y, num, mat_pos_x, mat_pos_y):
        self.color = (179, 181, 179)
        self.screen = screen
        self.start_pos_x = start_position_x
        self.start_pos_y = start_position_y
        self.num = num
        self.width = tile_width
        self.depth = tile_depth
        self.selected = False
        self.position_x = mat_pos_x
        self.position_y = mat_pos_y
        self.target_position = (mat_pos_x, mat_pos_y)
        self.movable = False
        self.locked = False

    def draw_tile(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(
            self.start_pos_x, self.start_pos_y, self.width, self.depth))
        numb = font.render(str(self.num), True, (47, 49, 51))
        self.screen.blit(numb, (self.start_pos_x + 40, self.start_pos_y + 10))

    def lock_tile(self):
        self.locked = True
        self.color = (100, 100, 100)  # Change color to indicate it's locked
    def calculate_distance(self):
        ideal = [[1,2,3],[4,5,6],[7,8,'']]
        for i in range(len(ideal)):
            for j in range(len(ideal[i])):
                if ideal[i][j]==self.num:
                    ideal_x=i
                    ideal_y=j
        current_x, current_y = self.position_x, self.position_y
        return (abs(ideal_x - current_x)  + abs(ideal_y - current_y))

def create_tiles(flag= False):
    global tile_no, tiles
    tile_no = []
    tiles = []
    tile_no = [1, 2, 3, 4, 5, 6, 7, 8]
    if flag:
        random.shuffle(tile_no)
    
    tile_no.append(" ")
    
    k = 0
    for i in range(rows):
        for j in range(cols):
            if (i == rows - 1) and (j == cols - 1):
                pass
            else:
                t = Tiles(screen, tile_print_position[(i, j)][0], tile_print_position[(i, j)][1], tile_no[k], i, j)
                tiles.append(t)
            matrix[i][j] = tile_no[k]
            k += 1
    check_mobility()
def isSolveble():
    allcelldata = "".join(str(matrix[i][j]) for i in range(rows) for j in range(cols))
    inversion_count = 0
    for i in range(len(allcelldata)):
        for j in range(i+1,len(allcelldata)):
            if allcelldata[i]>allcelldata[j] and allcelldata[i]!=0 and allcelldata[j]!=0:
                inversion_count+=1
    return inversion_count %2==0
def check_mobility():
    for tile in tiles:
        #if tile.locked:  # Pular tiles bloqueados
        #    tile.movable = False
        #    continue
        
        # Verifique a posição e os adjacentes
        row_index = tile.position_x
        col_index = tile.position_y
        adjacent_cells = [
            [row_index - 1, col_index],  # cima
            [row_index + 1, col_index],  # baixo
            [row_index, col_index - 1],  # esquerda
            [row_index, col_index + 1]   # direita
        ]
        
        # Verifique se as células adjacentes são válidas
        tile.movable = any(
            0 <= adj[0] < rows and 0 <= adj[1] < cols and matrix[adj[0]][adj[1]] == " "
            for adj in adjacent_cells
        )

        # Debugging: mostre o estado do tile
        print(f'Tile {tile.num}: locked={tile.locked}, movable={tile.movable}')
def isGameOver():
    global game_over, game_over_banner
    allcelldata = "".join(str(matrix[i][j]) for i in range(rows) for j in range(cols))
    if allcelldata == "12345678 ":
        game_over = True
        game_over_banner = "Sucesso"
        for tile in tiles:
            tile.movable = False  # Desabilita o movimento para todos os blocos
def get_movable_tiles():
    return [tile for tile in tiles if tile.movable]    
def get_locked_tiles():
    return [tile for tile in tiles if tile.locked]

def get_weigth_status():
    peso_total = 0
    
    for tile in tiles:
        print(f'tile number: {tile.num}')
        distance = tile.calculate_distance()
        peso_total+=distance
        #print(f'Distância do Tile {tile.num} para a posição ideal: {distance}')
    print(f"Peso total : {peso_total}")
    base_penalty=math.exp((peso_total-0))
    penalty = base_penalty if tuple(map(tuple, matrix)) in visited_states else 0  # Penalidade alta se já foi visitado

    if peso_total<10:
        penalty/=2
    return peso_total+penalty
def generate_all_states(start_matrix, num_moves=5):
    global last_moved_tile
    movable_tiles = get_movable_tiles()
    print(20*"--/--")
    if last_moved_tile:
        print(f"Last tile moved : {last_moved_tile.num}")
    print("Movable tiles")
    for i in movable_tiles:
        print(f'numero : {i.num}')
    print("Movable tiles")
    if last_moved_tile in movable_tiles:
        movable_tiles.remove(last_moved_tile)
    for i in movable_tiles:
        print(f'numero : {i.num}')

    states = set()  # Para armazenar estados únicos
    pesos = []

    for tile in movable_tiles:
        original_matrix = [row[:] for row in start_matrix]  # Cópia profunda

        make_movent(tile, original_matrix)  # Mova o tile na cópia

        # Adicione o novo estado ao conjunto
        states.add(tuple(map(tuple, original_matrix)))
        pesos.append(get_weigth_status())  # Certifique-se de que essa função usa a matriz passada
        make_movent(tile, original_matrix)
    if pesos:
        peso_minimo = min(pesos)
        index_minimo = pesos.index(peso_minimo)
        chosen_tile = movable_tiles[index_minimo]

        print(f"Tile num: {chosen_tile.num}")
        make_movent(chosen_tile, start_matrix)  # Mova o tile na matriz original
        visited_states.add(tuple(map(tuple, matrix)))

    return states
def reset_game():
    global move_count, game_over,visited_states, game_over_banner, random_moving, solution_1_moving, last_moved_tile
    move_count = 0
    game_over = False
    game_over_banner = ""
    random_moving = False
    solution_1_moving = False
    last_moved_tile = None  # Redefine o último bloco movido
    visited_states = set()

    create_tiles()
def mix_numbers():
    create_tiles(True)
def make_movent(tile, original_matrix):
    empty_tile_pos = next((i, j) for i in range(rows) for j in range(cols) if original_matrix[i][j] == " ")
    empty_row, empty_col = empty_tile_pos

    # Move the tile
    original_matrix[tile.position_x][tile.position_y] = " "
    original_matrix[empty_row][empty_col] = tile.num

    # Update the position of the tile
    tile.position_x = empty_row
    tile.position_y = empty_col
    tile.start_pos_x = tile_print_position[(empty_row, empty_col)][0]
    tile.start_pos_y = tile_print_position[(empty_row, empty_col)][1]
    
    # Update the global last_moved_tile if necessary
    global last_moved_tile,move_count
    last_moved_tile = tile
    print(last_moved_tile.num)
    check_mobility()
    move_count += 1
    isGameOver()
def lock_tile_if_correct(tile):
    correct_positions = {
        1: (0, 0),
        2: (0,1),
        3: (0,2)
    }
    
    # Ordena os tiles com base no número
    for num in range(1, 4):
        if num in correct_positions:
            expected_pos = correct_positions[num]
            if tile.num == num and (tile.position_x, tile.position_y) == expected_pos:
                tile.lock_tile()
                return  # Sai após bloquear o tile correto
def move_random_tile():
    global last_moved_tile, game_over ,LoopFlag
    if game_over:
        return

    movable_tiles = get_movable_tiles()
    
    # Debug: Verifique quais tiles são movíveis
    print(f'Movable tiles before filtering: {[tile.num for tile in tiles if tile.movable]}')

    if last_moved_tile in movable_tiles:
        movable_tiles.remove(last_moved_tile)
    for i in movable_tiles:
        print("Num : {i.num}")
    if movable_tiles:
        tile_to_move = random.choice(movable_tiles)
        print(f'Tile to move: {tile_to_move.num}')
        
        make_movent(tile_to_move,matrix)
        
        #lock_tile_if_correct(tile_to_move)

        check_mobility()
        isGameOver()
    else:
        print("No movable tiles available after filtering.")
        LoopFlag+=1
        if LoopFlag >=2:
            print("Entrou aqui")
            last_moved_tile = None
            LoopFlag=0
def move_random_tile_2():
    pass
# Controlar o movimento aleatório
def random_solution():
    global random_moving
    random_moving = True
# Controlar o movimento da solucao 1
def solution_1():
    global solution_1_moving
    solution_1_moving = True

def print_states(states):
    for state in states:
        for row in state:
            print(" | ".join(str(x) if x != " " else " " for x in row))
        print("-" * 20)  # Linha separadora entre os estados


# Initialize window dimensions
page_width, page_depth = pyautogui.size()
page_width = int(page_width * .9)
page_depth = int(page_depth * .9)
move_stack = []

# Tile dimensions
tile_width = 200
tile_depth = 200
rows, cols = (3, 3)
tile_count = rows * cols - 1
matrix = [["" for _ in range(cols)] for _ in range(rows)]
tile_print_position = {
    (0, 0): (100, 50), (0, 1): (305, 50), (0, 2): (510, 50),
    (1, 0): (100, 255), (1, 1): (305, 255), (1, 2): (510, 255),
    (2, 0): (100, 460), (2, 1): (305, 460), (2, 2): (510, 460)
}

# Initialize game state
game_over = False
game_over_banner = ""
move_count = 0
random_moving = False
solution_1_moving = False
LoopFlag = 0

# Button properties
button_width = 200
button_height = 50  
button_start = pygame.Rect((1000, 60), (button_width, button_height))
button_mix_number = pygame.Rect((1000, 120), (button_width, button_height))
button_rect = pygame.Rect((1000, 180), (button_width, button_height))
button_solution_1 = pygame.Rect((1000, 240), (button_width, button_height))

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((page_width, page_depth))
pygame.display.set_caption("Slide Game")
font = pygame.font.Font('freesansbold.ttf', 200)
game_over_font = pygame.font.Font('freesansbold.ttf', 20)
move_count_font = pygame.font.Font('freesansbold.ttf', 20)
visited_states = set()

# Creation of tiles in the puzzle
create_tiles(False)

# Main loop
running = True
last_moved_tile = None
while running:
    screen.fill((47, 49, 51))
    pygame.draw.rect(screen, (247, 235, 235), pygame.Rect(95, 45, 620, 620))
    
    if game_over:
        game_over_print = game_over_font.render(game_over_banner, True, (20, 156, 27))
        screen.blit(game_over_print, (1010, 600))
        random_moving = False
    elif running:
        if move_count >= 100000000:
            game_over_print = game_over_font.render(game_over_banner, True, (20, 156, 27))
            screen.blit(game_over_print, (950, 600))
            random_moving = False
            solution_1_moving = False

    # Render move count
    move_count_render = move_count_font.render("Moves: " + str(move_count), True, (179, 181, 179))
    screen.blit(move_count_render, (1010, 400))

    # Draw buttons
    #Button Reset
    pygame.draw.rect(screen, (0, 128, 255), button_rect, border_radius=3)
    button_text = move_count_font.render("Reset", True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    #Button Mix Numbers
    pygame.draw.rect(screen, (67, 128, 59), button_mix_number, border_radius=3)
    button_mix_numbers_text = move_count_font.render("Mix Numbers", True, (255, 255, 255))
    text_mix_numbers = button_mix_numbers_text.get_rect(center=button_mix_number.center)
    screen.blit(button_mix_numbers_text, text_mix_numbers)
    #Button Random Search
    pygame.draw.rect(screen, (0, 128, 255), button_start, border_radius=3)
    button_start_text = move_count_font.render("Random Search", True, (255, 255, 255))
    text_start = button_start_text.get_rect(center=button_start.center)
    screen.blit(button_start_text, text_start)
    #Button Solution 1
    pygame.draw.rect(screen, (0, 128, 255), button_solution_1, border_radius=3)
    button_solution_1_text = move_count_font.render("Solution 1", True, (255, 255, 255))
    text_solution_1 = button_solution_1_text.get_rect(center=button_solution_1.center)
    screen.blit(button_solution_1_text, text_solution_1)
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_m_click, y_m_click = pygame.mouse.get_pos()
            if button_rect.collidepoint(x_m_click, y_m_click):
                reset_game()
            elif button_mix_number.collidepoint(x_m_click, y_m_click):
                mix_numbers()
            elif button_start.collidepoint(x_m_click, y_m_click) and not game_over:
                isGameOver()
                print(f'É solucionavel : {isSolveble()}')
                if isSolveble() and game_over!=True:
                    game_over = True
                    game_over_banner = 'Not Solvable'
                else:
                    random_solution()
            elif button_solution_1.collidepoint(x_m_click, y_m_click) and not game_over:
                #generate_all_states(matrix)
                #solution_1_moving 
                isGameOver()
                print(f'É solucionavel : {isSolveble()}')
                if isSolveble() and game_over!=True:
                    game_over = True
                    game_over_banner = 'Not Solvable'
                else:
                    solution_1()                
               
    if random_moving:
        move_random_tile()
        pygame.time.delay(1)  # Delay between moves
    if solution_1_moving:
        generate_all_states(matrix)
        pygame.time.delay(1)  # Delay between moves
    for tile in tiles:
        tile.draw_tile()  # Draw tiles

    pygame.display.flip()  # Update the display

pygame.quit()
