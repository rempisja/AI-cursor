import cv2
import mediapipe as mp
import pygame
import random

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tetris with Hand Gestures")
clock = pygame.time.Clock()

# Tetris Game Variables
WIDTH = 10
HEIGHT = 20
BLOCK_SIZE = 30
grid = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Tetrimino shapes and colors
SHAPES = [
    [[1, 1, 1, 1]],  # Line
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # Square
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

COLORS = [(0, 255, 255), (255, 165, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)]


class Piece:
    def __init__(self, shape, color, x, y):
        self.shape = shape
        self.color = color
        self.x = x
        self.y = y
        self.rotation = 0


# Functions to count fingers and determine gesture
def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    fingers = 0

    # Check thumb (right hand logic — adjust if needed)
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        fingers += 1

    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers += 1

    return fingers


def get_gesture(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    gesture = "none"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = count_fingers(hand_landmarks)

            if fingers == 0:
                gesture = "drop"
            elif fingers == 1:
                gesture = "rotate"
            elif fingers == 2:
                gesture = "right"
            elif fingers == 3:
                gesture = "left"
            else:
                gesture = "none"

            cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return gesture, frame


def handle_gesture(gesture):
    if gesture == "drop":
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}))
    elif gesture == "rotate":
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
    elif gesture == "right":
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}))
    elif gesture == "left":
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT}))


# Tetris Game Logic Functions

def create_piece():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return Piece(shape, color, 3, 0)


def draw_grid():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pygame.draw.rect(screen, grid[y][x],
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, (255, 255, 255),
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def valid_space(piece):
    shape = piece.shape[piece.rotation % len(piece.shape)]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + piece.x < 0 or x + piece.x >= WIDTH or y + piece.y >= HEIGHT:
                    return False
                if grid[y + piece.y][x + piece.x] != (0, 0, 0):
                    return False
    return True


def rotate_piece(piece):
    piece.rotation = (piece.rotation + 1) % len(piece.shape)
    if not valid_space(piece):
        piece.rotation = (piece.rotation - 1) % len(piece.shape)


def move_piece(piece, dx, dy):
    piece.x += dx
    piece.y += dy
    if not valid_space(piece):
        piece.x -= dx
        piece.y -= dy


def merge_piece(piece):
    shape = piece.shape[piece.rotation % len(piece.shape)]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + piece.y][x + piece.x] = piece.color


def clear_lines():
    global grid
    grid = [row for row in grid if any(cell == (0, 0, 0) for cell in row)]
    while len(grid) < HEIGHT:
        grid.insert(0, [(0, 0, 0)] * WIDTH)


# Main Loop
def main():
    piece = create_piece()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        gesture, processed_frame = get_gesture(frame)
        handle_gesture(gesture)

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_piece(piece, -1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_piece(piece, 1, 0)
                elif event.key == pygame.K_UP:
                    rotate_piece(piece)
                elif event.key == pygame.K_SPACE:
                    move_piece(piece, 0, 1)

        # Move piece down
        move_piece(piece, 0, 1)
        if not valid_space(piece):
            move_piece(piece, 0, -1)
            merge_piece(piece)
            piece = create_piece()
            clear_lines()

        # Fill the screen with background color
        screen.fill((0, 0, 0))

        # Draw the grid
        draw_grid()

        # Draw the falling piece
        shape = piece.shape[piece.rotation % len(piece.shape)]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, piece.color,
                                     ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
