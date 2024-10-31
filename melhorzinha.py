import pygame
import random
import time

# Inicializando o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quebra-Cabeça 3x3")

# Cores
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (30, 144, 255)

# Fontes e tamanhos
FONT = pygame.font.SysFont("Arial", 50)
FONT_SMALL = pygame.font.SysFont("Arial", 20)

# Tamanho do quebra-cabeça
TAM = 3
TILE_SIZE = 100
OFFSET_X = 50
OFFSET_Y = 50
ANIMATION_SPEED = 10  # Velocidade de animação dos movimentos

# Funções auxiliares
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Classe do Quebra-Cabeça
class Puzzle:
    def __init__(self):
        self.tiles = [[TAM * i + j + 1 for j in range(TAM)] for i in range(TAM)]
        self.tiles[-1][-1] = 0  # A última peça é o espaço vazio
        self.blank_pos = (TAM - 1, TAM - 1)
        self.moves = 0

    def shuffle(self):
        for _ in range(100):
            self.move_blank(random.choice(["up", "down", "left", "right"]))
        self.moves = 0  # Resetar o contador de movimentos

    def move_blank(self, direction, animate=True):
        x, y = self.blank_pos
        if direction == "up" and y > 0:
            self.animate_move((x, y), (x, y - 1), animate)
        elif direction == "down" and y < TAM - 1:
            self.animate_move((x, y), (x, y + 1), animate)
        elif direction == "left" and x > 0:
            self.animate_move((x, y), (x - 1, y), animate)
        elif direction == "right" and x < TAM - 1:
            self.animate_move((x, y), (x + 1, y), animate)

    def animate_move(self, pos1, pos2, animate=True):
        if not animate:
            self.swap_tiles(pos1, pos2)
            return
        
        # Animação da peça
        x1, y1 = pos1
        x2, y2 = pos2
        dx = (x2 - x1) * TILE_SIZE
        dy = (y2 - y1) * TILE_SIZE
        tile_value = self.tiles[y1][x1]

        for i in range(0, TILE_SIZE, ANIMATION_SPEED):
            SCREEN.fill(DARK_GRAY)
            self.draw(exclude=(x1, y1))
            draw_text(
                SCREEN, str(tile_value), FONT, BLACK,
                OFFSET_X + x1 * TILE_SIZE + dx * (i / TILE_SIZE),
                OFFSET_Y + y1 * TILE_SIZE + dy * (i / TILE_SIZE)
            )
            pygame.display.flip()
            pygame.time.delay(10)

        self.swap_tiles(pos1, pos2)

    def swap_tiles(self, pos1, pos2):
        self.tiles[pos1[1]][pos1[0]], self.tiles[pos2[1]][pos2[0]] = self.tiles[pos2[1]][pos2[0]], self.tiles[pos1[1]][pos1[0]]
        self.blank_pos = pos2
        self.moves += 1

    def reset(self):
        self.__init__()  # Reconfigura o tabuleiro para o estado inicial

    def manhattan_distance(self):
        distance = 0
        for y in range(TAM):
            for x in range(TAM):
                value = self.tiles[y][x]
                if value != 0:
                    target_x = (value - 1) % TAM
                    target_y = (value - 1) // TAM
                    distance += abs(x - target_x) + abs(y - target_y)
        return distance

    def misplaced_tiles(self):
        misplaced = 0
        for y in range(TAM):
            for x in range(TAM):
                if self.tiles[y][x] != 0 and self.tiles[y][x] != TAM * y + x + 1:
                    misplaced += 1
        return misplaced

    def random_search(self):
        for _ in range(20):
            self.move_blank(random.choice(["up", "down", "left", "right"]))

    def heuristic_one_level(self):
        # Implementação simples: escolher o movimento que mais reduz a Manhattan Distance
        best_move = None
        best_distance = float('inf')
        for direction in ["up", "down", "left", "right"]:
            original_blank_pos = self.blank_pos
            self.move_blank(direction, animate=False)
            distance = self.manhattan_distance()
            if distance < best_distance:
                best_distance = distance
                best_move = direction
            self.blank_pos = original_blank_pos
        if best_move:
            self.move_blank(best_move)

    def heuristic_two_levels(self):
        # Avalia dois movimentos à frente, somando a Manhattan Distance de ambos
        best_move = None
        best_distance = float('inf')
        for first_move in ["up", "down", "left", "right"]:
            original_blank_pos = self.blank_pos
            self.move_blank(first_move, animate=False)
            first_distance = self.manhattan_distance()
            for second_move in ["up", "down", "left", "right"]:
                self.move_blank(second_move, animate=False)
                second_distance = self.manhattan_distance()
                total_distance = first_distance + second_distance
                if total_distance < best_distance:
                    best_distance = total_distance
                    best_move = first_move
                self.blank_pos = original_blank_pos  # Reverte o movimento
            self.blank_pos = original_blank_pos  # Reverte o primeiro movimento
        if best_move:
            self.move_blank(best_move)

    def personal_heuristic(self):
        # Heurística personalizada combinando peças fora do lugar e Manhattan Distance
        if self.manhattan_distance() < self.misplaced_tiles():
            self.heuristic_one_level()
        else:
            self.random_search()

    def draw(self, exclude=None):
        for y in range(TAM):
            for x in range(TAM):
                if exclude and (x, y) == exclude:
                    continue
                tile_value = self.tiles[y][x]
                if tile_value != 0:  # Não desenhar o espaço vazio
                    rect = pygame.Rect(OFFSET_X + x * TILE_SIZE, OFFSET_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(SCREEN, GRAY, rect)
                    pygame.draw.rect(SCREEN, WHITE, rect, 3)
                    draw_text(SCREEN, str(tile_value), FONT, BLACK, rect.centerx, rect.centery)

# Função para desenhar os botões e verificar cliques
def draw_buttons():
    button_texts = ["Random Search", "Mix Numbers", "Reset", "Heuristic 1", "Heuristic 2", "Personal Heuristic"]
    buttons = []
    y = 70
    for i, text in enumerate(button_texts):
        color = GREEN if text == "Mix Numbers" else BLUE
        rect = pygame.Rect(450, y, 120, 40)
        pygame.draw.rect(SCREEN, color, rect)
        draw_text(SCREEN, text, FONT_SMALL, WHITE, rect.centerx, rect.centery)
        buttons.append((rect, text))  # Armazena o retângulo e o nome do botão
        y += 60
    return buttons

# Função principal
def main():
    clock = pygame.time.Clock()
    puzzle = Puzzle()
    running = True

    while running:
        SCREEN.fill(DARK_GRAY)
        buttons = draw_buttons()  # Desenha os botões e armazena suas posições

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, action in buttons:
                    if rect.collidepoint(mouse_pos):
                        if action == "Mix Numbers":
                            puzzle.shuffle()
                        elif action == "Reset":
                            puzzle.reset()
                        elif action == "Random Search":
                            puzzle.random_search()
                        elif action == "Heuristic 1":
                            puzzle.heuristic_one_level()
                        elif action == "Heuristic 2":
                            puzzle.heuristic_two_levels()
                        elif action == "Personal Heuristic":
                            puzzle.personal_heuristic()

        # Desenha o quebra-cabeça e exibe o número de movimentos
        puzzle.draw()
        draw_text(SCREEN, f"Moves: {puzzle.moves}", FONT_SMALL, WHITE, 100, HEIGHT - 80)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
