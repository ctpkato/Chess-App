import pygame
import chess
import chess.engine

# Initialize Pygame
pygame.init()

# Set up display
size = 1000
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("Chess")

# Load images
pieces = {}
piece_files = {
    'P': 'white_pawn.png', 'R': 'white_rook.png', 'N': 'white_knight.png', 'B': 'white_bishop.png', 'Q': 'white_queen.png', 'K': 'white_king.png',
    'p': 'black_pawn.png', 'r': 'black_rook.png', 'n': 'black_knight.png', 'b': 'black_bishop.png', 'q': 'black_queen.png', 'k': 'black_king.png'
}

# Replace this path with your chess piece images directory 

images_directory = "path/to/your/generic/chess/pieces/directory/"

for piece, filename in piece_files.items():
    try:
        pieces[piece] = pygame.image.load(images_directory + filename)
        print(f"Loaded image for {piece}")
    except pygame.error as e:
        print(f"Error loading image for {piece}: {e}")

# Initialize the chess board and engine
board = chess.Board()
engine_path = "path/to/your/stockfish/executable/stockfish.exe"  # Replace with your Stockfish executable path
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

def draw_board(screen, board):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for i in range(8):
        for j in range(8):
            color = colors[(i + j) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(j * size // 8, i * size // 8, size // 8, size // 8))
            piece = board.piece_at(chess.square(j, 7 - i))
            if piece:
                screen.blit(pieces[piece.symbol()], pygame.Rect(j * size // 8, i * size // 8, size // 8, size // 8))

# Convert pixel position to chessboard square
def pixel_to_square(pos):
    x, y = pos
    row = 7 - (y // (size // 8))
    col = x // (size // 8)
    return chess.square(col, row)

# Main loop
running = True
selected_square = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            square = pixel_to_square(pos)
            
            if selected_square is None:
                # Select a piece
                if board.piece_at(square) and board.piece_at(square).color == board.turn:
                    selected_square = square
            else:
                # Move the selected piece
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                    selected_square = None
                else:
                    selected_square = None

    draw_board(screen, board)
    pygame.display.flip()

    # Stockfish's move
    if not board.is_game_over() and board.turn == chess.BLACK:
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)

print("Game over")
print("Result: ", board.result())
engine.quit()
pygame.quit()
