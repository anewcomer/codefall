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
    # Katakana-like / Abstract digital symbols (4x8 pixels)
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000]),
    bytearray([0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000]), # | (Thin I, offset)
    bytearray([0b11110000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b11110000]), # [ ] (Bracket-like)
    bytearray([0b11100000, 0b10000000, 0b11100000, 0b10000000, 0b10000000, 0b10000000, 0b11100000, 0b00000000]), # E-like
    bytearray([0b11110000, 0b10000000, 0b11100000, 0b10000000, 0b11110000, 0b00000000, 0b00000000, 0b00000000]), # B-like
    bytearray([0b01000000, 0b11100000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b00000000]), # T-like
    bytearray([0b10010000, 0b10010000, 0b11110000, 0b10010000, 0b10010000, 0b10010000, 0b10010000, 0b00000000]), # H-like
    bytearray([0b11110000, 0b00100000, 0b01000000, 0b10000000, 0b00100000, 0b01000000, 0b11110000, 0b00000000]), # Z-like / N-like
    bytearray([0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b00010000, 0b00100000, 0b01000000, 0b10000000]), # X-like (thin)
    bytearray([0b01100000, 0b10010000, 0b10010000, 0b01100000, 0b10010000, 0b10010000, 0b01100000, 0b00000000]), # 8-like / S-like
    bytearray([0b11100000, 0b10100000, 0b10100000, 0b11100000, 0b10100000, 0b10100000, 0b11100000, 0b00000000]), # Grid-like
    bytearray([0b00000000, 0b11110000, 0b10010000, 0b10010000, 0b10010000, 0b11110000, 0b00000000, 0b00000000]), # 0-like / O-like
    bytearray([0b00100000, 0b01100000, 0b10100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000]), # 1-like / J-like
    bytearray([0b11000000, 0b01000000, 0b01000000, 0b11000000, 0b10000000, 0b10000000, 0b11110000, 0b00000000]), # P-like / R-like
    bytearray([0b11110000, 0b10000000, 0b11110000, 0b00010000, 0b00010000, 0b00010000, 0b11110000, 0b00000000]), # F-like / 5-like
    bytearray([0b01100000, 0b10010000, 0b00100000, 0b01000000, 0b10010000, 0b10010000, 0b01100000, 0b00000000]), # G-like / 6-like
]
# --- Additional Glyphs to reach 32 total ---
GLYPHS.extend([
    bytearray([0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b11110000, 0b01100000, 0b00100000, 0b00000000]), # Arrow Down-like
    bytearray([0b00100000, 0b01100000, 0b11110000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000]), # Arrow Up-like
    bytearray([0b00000000, 0b00100000, 0b00100000, 0b11110000, 0b00100000, 0b00100000, 0b00000000, 0b00000000]), # Plus-like
    bytearray([0b00000000, 0b00000000, 0b00000000, 0b11110000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Minus-like
    bytearray([0b00000000, 0b01100000, 0b01100000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Small Square
    bytearray([0b10100000, 0b01010000, 0b10100000, 0b01010000, 0b10100000, 0b01010000, 0b10100000, 0b01010000]), # Checkerboard
    bytearray([0b10010000, 0b01100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000]), # Y-like
    bytearray([0b10010000, 0b10100000, 0b11000000, 0b10100000, 0b10010000, 0b10010000, 0b10010000, 0b00000000]), # K-like
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b11110000, 0b00000000]), # L-like
    bytearray([0b01110000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b01110000, 0b00000000]), # C-like
    bytearray([0b10010000, 0b10010000, 0b10010000, 0b10010000, 0b10010000, 0b10010000, 0b01100000, 0b00000000]), # U-like
    bytearray([0b10010000, 0b10010000, 0b10010000, 0b01100000, 0b01100000, 0b00100000, 0b00100000, 0b00000000]), # V-like
    bytearray([0b10010000, 0b10010000, 0b10010000, 0b10100000, 0b11110000, 0b10100000, 0b10100000, 0b00000000]), # W-like
    bytearray([0b01100000, 0b10010000, 0b00010000, 0b00100000, 0b00100000, 0b00000000, 0b00100000, 0b00000000]), # Question Mark-like
    bytearray([0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000, 0b00100000, 0b00000000]), # Exclamation Mark-like
    bytearray([0b00000000, 0b01100000, 0b01100000, 0b00000000, 0b10010000, 0b01100000, 0b00000000, 0b00000000]), # Abstract Smiley-like
])

NUM_GLYPHS = len(GLYPHS)
GLYPH_WIDTH = 4
GLYPH_HEIGHT = 8

COLS = thumby.display.width // GLYPH_WIDTH  # 72 / 4 = 18 columns
ROWS = thumby.display.height // GLYPH_HEIGHT # 40 / 8 = 5 rows

# --- Optimized draw_glyph_pixels function using direct buffer access ---
# Draws a glyph by directly manipulating thumby.display.display.buffer
# Assumes thumby.display.fill(0) has been called prior to any calls in a frame.
# Assumes color is 1 (ON), drawing on a black background cleared by fill(0).
def draw_glyph_pixels(glyph_data, draw_x, draw_y, glyph_w, glyph_h):
    # Cache display dimensions
    disp_width = thumby.display.width
    disp_height = thumby.display.height

    # Early exit if entire glyph is off-screen
    if draw_x >= disp_width or (draw_x + glyph_w) <= 0 or \
       draw_y >= disp_height or (draw_y + glyph_h) <= 0:
        return

    buffer = thumby.display.display.buffer

    for r_offset in range(glyph_h):  # Iterate through each row of the glyph (0 to GLYPH_HEIGHT-1)
        screen_y = draw_y + r_offset

        # Skip row if it's entirely off-screen vertically
        if not (0 <= screen_y < disp_height):
            continue

        glyph_row_data = glyph_data[r_offset] # Get the byte for the current glyph row
        
        # Calculate the byte index in the screen buffer for this screen_y's page
        # and the bit mask for the pixel within that byte.
        page_offset = (screen_y // 8) * disp_width
        bit_to_set = 1 << (screen_y % 8)

        for c_offset in range(glyph_w):  # Iterate through each column of the glyph (0 to GLYPH_WIDTH-1)
            screen_x = draw_x + c_offset

            # Skip pixel if it's off-screen horizontally
            if not (0 <= screen_x < disp_width):
                continue

            # Check if the pixel in the glyph definition (most significant 4 bits) is set
            if (glyph_row_data >> (7 - c_offset)) & 0x01:
                buffer_idx = screen_x + page_offset
                buffer[buffer_idx] |= bit_to_set

# --- Initialize Thumby Display ---
thumby.display.fill(0)
thumby.display.update()

# --- Game State Variables ---
column_states = []
for _ in range(COLS):
    trail_len = random.randint(1, 3) # Max 3 trail glyphs (total 4 with head)
    trail_glyph_indices = [random.randint(0, NUM_GLYPHS - 1) for _ in range(trail_len)]
    column_states.append({
        'head_y': random.randint(-GLYPH_HEIGHT * (ROWS + 2), -GLYPH_HEIGHT), # Start significantly off-screen top
        'trail_len': trail_len,
        'glyph_idx': random.randint(0, NUM_GLYPHS - 1),
        'trail_glyph_indices': trail_glyph_indices,
        'speed_counter': 0,
        'speed_threshold': random.randint(1, 7) # Greater variation in speeds
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
        draw_glyph_pixels(head_glyph, x, head_y_pixel, GLYPH_WIDTH, GLYPH_HEIGHT)

        # Draw the trail glyphs (which are fixed for this column's fall)
        for i in range(col_data['trail_len']): # i from 0 to trail_len-1
            trail_y_pixel = head_y_pixel - ((i + 1) * GLYPH_HEIGHT) # Glyph i is (i+1) positions above head
            trail_glyph_idx = col_data['trail_glyph_indices'][i]
            trail_glyph = GLYPHS[trail_glyph_idx]
            draw_glyph_pixels(trail_glyph, x, trail_y_pixel, GLYPH_WIDTH, GLYPH_HEIGHT)

    # Update column states for scrolling
    for col_data in column_states:
        col_data['speed_counter'] += 1
        if col_data['speed_counter'] >= col_data['speed_threshold']:
            col_data['head_y'] += 1 # Move down by 1 pixel
            col_data['speed_counter'] = 0 # Reset counter

            # If the *entire column* (head + all trail glyphs) has scrolled off the bottom.
            # This means the top edge of the topmost trail glyph is at or below the screen's bottom edge.
            top_of_topmost_glyph_y = col_data['head_y'] - (col_data['trail_len'] * GLYPH_HEIGHT)
            
            if top_of_topmost_glyph_y >= thumby.display.height:
                # Reset to start off-screen top, with new random properties
                col_data['head_y'] = random.randint(-GLYPH_HEIGHT * (ROWS + 1), -GLYPH_HEIGHT) # Adjusted starting range slightly
                col_data['trail_len'] = random.randint(1, 3) # Max 3 trail glyphs
                col_data['glyph_idx'] = random.randint(0, NUM_GLYPHS - 1)
                col_data['trail_glyph_indices'] = [random.randint(0, NUM_GLYPHS - 1) for _ in range(col_data['trail_len'])]
                col_data['speed_threshold'] = random.randint(1, 4) # Greater variation in speeds

    thumby.display.update() # Update the physical display

    # Control animation speed. This might need fine-tuning.
    # Start with a slower value and decrease if it's too choppy/slow.
    time.sleep(0.01) # Adjusted for potentially smoother, more consistent animation