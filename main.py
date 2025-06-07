# main.py
# The main application file for Thumby Codefall
# Rewritten to use thumby.display.setPixel for drawing, as blit is unreliable.

import thumby
import random
import time

# --- Thumby Display Configuration ---
# THUMBY_WIDTH = 72
# THUMBY_HEIGHT = 40

# --- Glyph Definitions ---
# Each glyph is a list of 8 bytes, representing 8 rows of 4 pixels each.
# The most significant 4 bits of each byte are used for the 4-pixel width.

GLYPHS = [
    # Glyph 0: A simple vertical line
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000]),

    # Glyph 1: Diagonal
    bytearray([0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b10000000, 0b01000000, 0b00100000, 0b00010000]),

    # Glyph 2: Blocky 'E'
    bytearray([0b11100000, 0b10000000, 0b11000000, 0b10000000, 0b11100000, 0b00000000, 0b00000000, 0b00000000]),

    # Glyph 3: Some random pattern
    bytearray([0b10100000, 0b01010000, 0b10100000, 0b01010000, 0b10100000, 0b01010000, 0b10100000, 0b01010000]),

    # Glyph 4: Stacked blocks
    bytearray([0b11000000, 0b11000000, 0b00000000, 0b11000000, 0b11000000, 0b00000000, 0b11000000, 0b11000000]),

    # Glyph 5: Another diagonal with a twist
    bytearray([0b00010000, 0b00100000, 0b01000000, 0b10000000, 0b00010000, 0b00100000, 0b01000000, 0b10000000]),

    # Glyph 6: A simple 'X'
    bytearray([0b10010000, 0b01100000, 0b01100000, 0b10010000, 0b10010000, 0b01100000, 0b01100000, 0b10010000]),
    
    # Glyph 7: A sort of 'H'
    bytearray([0b10010000, 0b10010000, 0b11110000, 0b10010000, 0b10010000, 0b00000000, 0b00000000, 0b00000000]),

    # Glyph 8: Random dots
    bytearray([0b10000000, 0b00100000, 0b01000000, 0b00010000, 0b10000000, 0b00100000, 0b01000000, 0b00010000]),

    # Glyph 9: Solid block (very visible)
    bytearray([0b11110000, 0b11110000, 0b11110000, 0b11110000, 0b11110000, 0b11110000, 0b11110000, 0b11110000]),
]

NUM_GLYPHS = len(GLYPHS)
GLYPH_WIDTH = 4
GLYPH_HEIGHT = 8

COLS = thumby.display.width // GLYPH_WIDTH  # 72 / 4 = 18 columns
ROWS = thumby.display.height // GLYPH_HEIGHT # 40 / 8 = 5 rows

# --- Custom draw_glyph_pixels function (re-used from diagnostic) ---
# Draws a glyph using setPixel for each pixel
def draw_glyph_pixels(glyph_data, draw_x, draw_y, width, height, color):
    for row_idx in range(height):
        byte_data = glyph_data[row_idx]
        for col_idx in range(width):
            # Check if the pixel at this position in the bitmap is 'on' (1)
            # We are interested in the most significant 4 bits for our 4-pixel width
            if (byte_data >> (7 - col_idx)) & 0x01:
                # Only set pixel if within screen bounds (crucial for performance and avoiding errors)
                pixel_x = draw_x + col_idx
                pixel_y = draw_y + row_idx
                if 0 <= pixel_x < thumby.display.width and 0 <= pixel_y < thumby.display.height:
                    thumby.display.setPixel(pixel_x, pixel_y, color)

# --- Initialize Thumby Display ---
thumby.display.fill(0)
thumby.display.update()

# --- Game State Variables ---
column_states = []
for _ in range(COLS):
    column_states.append({
        'head_y': random.randint(-GLYPH_HEIGHT * (ROWS + 2), -GLYPH_HEIGHT), # Start significantly off-screen top
        'trail_len': random.randint(3, ROWS),
        'glyph_idx': random.randint(0, NUM_GLYPHS - 1),
        'speed_counter': 0,
        'speed_threshold': random.randint(1, 3) # Slower speeds to try and see animation
    })

# --- Main Game Loop ---
while True:
    thumby.display.fill(0) # Clear the entire display to black each frame

    # For each column, draw the glyphs using our setPixel helper
    for col_idx, col_data in enumerate(column_states):
        x = col_idx * GLYPH_WIDTH

        # Draw the head glyph (brightest)
        head_y_pixel = col_data['head_y']
        head_glyph = GLYPHS[col_data['glyph_idx']]
        # Use our custom draw function
        draw_glyph_pixels(head_glyph, x, head_y_pixel, GLYPH_WIDTH, GLYPH_HEIGHT, 1) # White

        # Draw the trail glyphs
        for i in range(1, col_data['trail_len'] + 1):
            trail_y_pixel = head_y_pixel - (i * GLYPH_HEIGHT)
            # Random glyph for each part of the trail for more chaos
            trail_glyph = GLYPHS[random.randint(0, NUM_GLYPHS - 1)]
            # Use our custom draw function
            draw_glyph_pixels(trail_glyph, x, trail_y_pixel, GLYPH_WIDTH, GLYPH_HEIGHT, 1) # White

    # Update column states for scrolling
    for col_data in column_states:
        col_data['speed_counter'] += 1
        if col_data['speed_counter'] >= col_data['speed_threshold']:
            col_data['head_y'] += 1 # Move down by 1 pixel
            col_data['speed_counter'] = 0 # Reset counter

            # If the entire column (head + trail) has scrolled off the bottom
            if col_data['head_y'] > thumby.display.height + (col_data['trail_len'] * GLYPH_HEIGHT):
                # Reset to start off-screen top, with new random properties
                col_data['head_y'] = random.randint(-GLYPH_HEIGHT * (ROWS + 2), -GLYPH_HEIGHT)
                col_data['trail_len'] = random.randint(3, ROWS)
                col_data['glyph_idx'] = random.randint(0, NUM_GLYPHS - 1)
                col_data['speed_threshold'] = random.randint(1, 3)

    thumby.display.update() # Update the physical display

    # Control animation speed. This might need fine-tuning.
    # Start with a slower value and decrease if it's too choppy/slow.
    time.sleep(0.02) # Try 0.01 for faster, 0.05 for slower, 0.005 if possible.