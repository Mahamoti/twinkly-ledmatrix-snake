import xled
import io
import struct
import time
import random
import keyboard
import requests

# LED Matrix initialization
discovered_device = xled.discover.discover()
if not discovered_device:
    print("No Twinkly LED-board found.")
    exit()

# Adjust the dimensions of the matrix
matrix_rows = 16
matrix_cols = 24

num_food = 5
snake_pos = [(4, 4)]

# Variables to keep track of food and golden food status
food_positions = []

# Variable for old direction
last_direction = None

# Variable to keep track of old score
last_score = -1

# Variable to store start time
start_time = time.time()

score = 0

'''
Mapping Led matrix tiles

See pictures for layout and cable setup to create the same.

# 1 tile
led_matrix = [
    [63, 62, 61, 60, 59, 58, 57, 56],
    [48, 49, 50, 51, 52, 53, 54, 55],
    [47, 46, 45, 44, 43, 42, 41, 40],
    [32, 33, 34, 35, 36, 37, 38, 39],
    [31, 30, 29, 28, 27, 26, 25, 24],
    [16, 17, 18, 19, 20, 21, 22, 23],
    [15, 14, 13, 12, 11, 10, 9, 8],
    [0, 1, 2, 3, 4, 5, 6, 7]
]

# 2 tiles
led_matrix = [
    [127, 126, 125, 124, 123, 122, 121, 120, 63, 62, 61, 60, 59, 58, 57, 56],
    [112, 113, 114, 115, 116, 117, 118, 119, 48, 49, 50, 51, 52, 53, 54, 55],
    [111, 110, 109, 108, 107, 106, 105, 104, 47, 46, 45, 44, 43, 42, 41, 40],
    [96, 97, 98, 99, 100, 101, 102, 103, 32, 33, 34, 35, 36, 37, 38, 39],
    [95, 94, 93, 92, 91, 90, 89, 88, 31, 30, 29, 28, 27, 26, 25, 24],
    [80, 81, 82, 83, 84, 85, 86, 87, 16, 17, 18, 19, 20, 21, 22, 23],
    [79, 78, 77, 76, 75, 74, 73, 72, 15, 14, 13, 12, 11, 10, 9, 8],
    [64, 65, 66, 67, 68, 69, 70, 71, 0, 1, 2, 3, 4, 5, 6, 7]
]

# 3 tiles
led_matrix = [
        [191, 190, 189, 188, 187, 186, 185, 184, 127, 126, 125, 124, 123, 122, 121, 120, 63, 62, 61, 60, 59, 58, 57, 56],
        [176, 177, 178, 179, 180, 181, 182, 183, 112, 113, 114, 115, 116, 117, 118, 119, 48, 49, 50, 51, 52, 53, 54, 55],
        [175, 174, 173, 172, 171, 170, 169, 168, 111, 110, 109, 108, 107, 106, 105, 104, 47, 46, 45, 44, 43, 42, 41, 40],
        [160, 161, 162, 163, 164, 165, 166, 167, 96, 97, 98, 99, 100, 101, 102, 103, 32, 33, 34, 35, 36, 37, 38, 39],
        [159, 158, 157, 156, 155, 154, 153, 152, 95, 94, 93, 92, 91, 90, 89, 88, 31, 30, 29, 28, 27, 26, 25, 24],
        [144, 145, 146, 147, 148, 149, 150, 151, 80, 81, 82, 83, 84, 85, 86, 87, 16, 17, 18, 19, 20, 21, 22, 23],
        [143, 142, 141, 140, 139, 138, 137, 136, 79, 78, 77, 76, 75, 74, 73, 72, 15, 14, 13, 12, 11, 10, 9, 8],
        [128, 129, 130, 131, 132, 133, 134, 135, 64, 65, 66, 67, 68, 69, 70, 71, 0, 1, 2, 3, 4, 5, 6, 7]
]
'''


# 6 tiles
led_matrix = [
        [383, 382, 381, 380, 379, 378, 377, 376, 319, 318, 317, 316, 315, 314, 313, 312, 255, 254, 253, 252, 251, 250, 249, 248],
        [368, 369, 370, 371, 372, 373, 374, 375, 304, 305, 306, 307, 308, 309, 310, 311, 240, 241, 242, 243, 244, 245, 246, 247],
        [367, 366, 365, 364, 363, 362, 361, 360, 303, 302, 301, 300, 299, 298, 297, 296, 239, 238, 237, 236, 235, 234, 233, 232],
        [352, 353, 354, 355, 356, 357, 358, 359, 288, 289, 290, 291, 292, 293, 294, 295, 224, 225, 226, 227, 228, 229, 230, 231],
        [351, 350, 349, 348, 347, 346, 345, 344, 287, 286, 285, 284, 283, 282, 281, 280, 223, 222, 221, 220, 219, 218, 217, 216],
        [336, 337, 338, 339, 340, 341, 342, 343, 272, 273, 274, 275, 276, 277, 278, 279, 208, 209, 210, 211, 212, 213, 214, 215],
        [335, 334, 333, 332, 331, 330, 329, 328, 271, 270, 269, 268, 267, 266, 265, 264, 207, 206, 205, 204, 203, 202, 201, 200],
        [320, 321, 322, 323, 324, 325, 326, 327, 256, 257, 258, 259, 260, 261, 262, 263, 192, 193, 194, 195, 196, 197, 198, 199],

        [191, 190, 189, 188, 187, 186, 185, 184, 127, 126, 125, 124, 123, 122, 121, 120, 63, 62, 61, 60, 59, 58, 57, 56],
        [176, 177, 178, 179, 180, 181, 182, 183, 112, 113, 114, 115, 116, 117, 118, 119, 48, 49, 50, 51, 52, 53, 54, 55],
        [175, 174, 173, 172, 171, 170, 169, 168, 111, 110, 109, 108, 107, 106, 105, 104, 47, 46, 45, 44, 43, 42, 41, 40],
        [160, 161, 162, 163, 164, 165, 166, 167, 96, 97, 98, 99, 100, 101, 102, 103, 32, 33, 34, 35, 36, 37, 38, 39],
        [159, 158, 157, 156, 155, 154, 153, 152, 95, 94, 93, 92, 91, 90, 89, 88, 31, 30, 29, 28, 27, 26, 25, 24],
        [144, 145, 146, 147, 148, 149, 150, 151, 80, 81, 82, 83, 84, 85, 86, 87, 16, 17, 18, 19, 20, 21, 22, 23],
        [143, 142, 141, 140, 139, 138, 137, 136, 79, 78, 77, 76, 75, 74, 73, 72, 15, 14, 13, 12, 11, 10, 9, 8],
        [128, 129, 130, 131, 132, 133, 134, 135, 64, 65, 66, 67, 68, 69, 70, 71, 0, 1, 2, 3, 4, 5, 6, 7]
]


control = xled.ControlInterface(discovered_device.ip_address, discovered_device.hw_address)
control.set_mode('rt')

numleds = control.get_device_info()['number_of_led']
print("Total leds:", numleds)
base_grid = [struct.pack(">BBB", 0, 0, 0)] * numleds


def set_led_color(control, grid, led_number, color):
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    grid[led_number] = struct.pack(">BBB", r, g, b)
    movie = io.BytesIO()
    movie.write(b"".join(grid))
    movie.seek(0)
    control.set_rt_frame_socket(movie, 2)

def reset_leds(control, grid):
    for i in range(len(grid)):
        grid[i] = struct.pack(">BBB", 0, 0, 0)
    movie = io.BytesIO()
    movie.write(b"".join(grid))
    movie.seek(0)
    control.set_rt_frame_socket(movie, 2)

def generate_food(snake_pos):
    global num_food, food_positions, matrix_cols, matrix_rows
    for _ in range(num_food):
        while True:
            x = random.randint(0, matrix_cols - 1)
            y = random.randint(0, matrix_rows - 1)
            if (x, y) not in snake_pos and (x, y) not in food_positions:
                food_positions.append((x, y))
                break
    #print("Food positions: ", food_positions)

def generate_food_if_needed(snake_pos):
    global food_positions, num_food
    if len(food_positions) < num_food:
        while True:
            x = random.randint(0, matrix_cols - 1)
            y = random.randint(0, matrix_rows - 1)
            if (x, y) not in snake_pos and (x, y) not in food_positions:
                food_positions.append((x, y))
                break

def update_food(control, grid, snake_pos):
    global food_positions, score
    new_food = []
    for x, y in food_positions:
        led_num = led_matrix[y][x]
        print(led_num)
        set_led_color(control, base_grid, led_num, '110000')
        if (x, y) in snake_pos:
            if random.random() < 0.9:  # 90% chance it's red food
                set_led_color(control, grid, led_num, "FF0000")
                score += 1
                snake_pos.append(snake_pos[-1])
            else:  # 10% chance it's yellow food
                set_led_color(control, grid, led_num, "FFFF00")
                score += 3
                snake_pos += [snake_pos[-1]] * 3
        else:
            new_food.append((x, y))
    food_positions = new_food
    #print("Updated food positions: ", food_positions)

def move_snake(snake_pos, direction):
    head_x, head_y = snake_pos[0]
    if direction == "up":
        new_head = (head_x, head_y - 1)
    elif direction == "down":
        new_head = (head_x, head_y + 1)
    elif direction == "left":
        new_head = (head_x - 1, head_y)
    else:
        new_head = (head_x + 1, head_y)
    new_head = (new_head[0] % matrix_cols, new_head[1] % matrix_rows)  # aanpassen naar nieuwe dimensies
    return [new_head] + snake_pos[:-1]

def check_collision(snake_pos):
    head_x, head_y = snake_pos[0]
    if head_x < 0 or head_x >= matrix_cols or head_y < 0 or head_y >= matrix_rows:  # aanpassen naar nieuwe dimensies
        return True
    return False

def play_game():
    global snake_pos
    direction = "right"
    food_pos = generate_food(snake_pos)
    score = 0

def turn_screen_color(control, base_grid, color):
    half_length = len(led_matrix) // 2
    for i in range(half_length):
        for j in range(len(led_matrix[i])):
            # Vanaf het begin
            set_led_color(control, base_grid, led_matrix[i][j], color)
            # Vanaf het einde
            set_led_color(control, base_grid, led_matrix[-(i+1)][j], color)
            time.sleep(0.005)  # Wacht 50 milliseconden tussen elk LED

        # Verstuur frame na het bijwerken van elke rij
        movie = io.BytesIO()
        movie.write(b"".join(base_grid))
        movie.seek(0)
        control.set_rt_frame_socket(movie, 2)

def play_game():
    global snake_pos, score
    direction = "right"  # Initieer direction
    generate_food(snake_pos)


    last_score = score  # Initieer last_score
    start_time = time.time()  # Markeer starttijd

    last_direction = direction  # Plaats dit binnen de functie

    def set_direction(e):
        nonlocal direction
        nonlocal last_direction  # Nu binnen dezelfde functie, dus werkt nu wel
        if (e.name == 'up' or e.name == 'w') and last_direction != "down":
            direction = "up"
        elif (e.name == 'down' or e.name == 's') and last_direction != "up":
            direction = "down"
        elif (e.name == 'left' or e.name == 'a') and last_direction != "right":
            direction = "left"
        elif (e.name == 'right' or e.name == 'd') and last_direction != "left":
            direction = "right"
        last_direction = direction  # Update last_direction

    keyboard.on_press(set_direction)

    while True:
        # Reset de LEDs waar de slang was
        for x, y in snake_pos[-1:]:
            led_number = led_matrix[y][x]
            set_led_color(control, base_grid, led_number, '000000')

        # Move the snake
        snake_pos = move_snake(snake_pos, direction)

        # Draw the snake
        for i, (x, y) in enumerate(snake_pos):
            led_number = led_matrix[y][x]
            if i == 0:  # Head
                set_led_color(control, base_grid, led_number, '008800')
            else:  # Tail
                set_led_color(control, base_grid, led_number, '001100')

        # Detect if the snake hits himself
        if snake_pos[0] in snake_pos[1:]:
            print("Game Over! The snake hits itself")
            turn_screen_color(control, base_grid, '110000')
            break

        # Check for collision
        if check_collision(snake_pos):
            print("Game Over!")
            turn_screen_color(control, base_grid, '110000')
            break

        generate_food_if_needed(snake_pos)  # Generate new food if needed

        update_food(control, base_grid, snake_pos)

        if last_score != score:
            print("Score:", score)
            last_score = score  # Update last_score

        time.sleep(0.2)



    end_time = time.time()
    total_time = end_time - start_time  # Calculate time

    print(f"Total play time: {total_time:.2f} seconds")
    # If you have a sonos system with text to speech, let it say your score
    url = f"http://192.168.2.10:5005/huiskamer/say/Your snake score is {score}"
    requests.get(url)


# First, turn all LEDs red
turn_screen_color(control, base_grid, '001100')

# Reset the LEDs to black before the game starts
reset_leds(control, base_grid)

generate_food(snake_pos)

# Start the game
play_game()