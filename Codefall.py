# main.py
# The main application file for Thumby Codefall
# Rewritten to use thumby.display.setPixel for drawing, as blit is unreliable.

import thumby
import random
import time

# --- Thumby Display Configuration ---
# THUMBY_WIDTH = 72
# THUMBY_HEIGHT = 40

# --- Glyph Definitions (Medium Size - 4x8) ---
# Each glyph is a list of bytes, representing rows of pixels.
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

# --- Small Glyphs (3x6) ---
# Most significant 3 bits used.
GLYPHS_SMALL = [
    bytearray([0b11100000, 0b10000000, 0b11100000, 0b10000000, 0b11100000, 0b00000000]), # Small E-like
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000]), # Small |-like
    bytearray([0b11000000, 0b10000000, 0b11000000, 0b01000000, 0b01000000, 0b11000000]), # Small S-like
    bytearray([0b01000000, 0b11100000, 0b01000000, 0b01000000, 0b01000000, 0b00000000]), # Small T-like
]

# --- Large Glyphs (5x10) ---
# Most significant 5 bits used.
GLYPHS_LARGE = [
    bytearray([0b11111000, 0b10000000, 0b10000000, 0b11110000, 0b10000000, 0b10000000, 0b10000000, 0b11111000, 0b00000000, 0b00000000]), # Large E-like
    bytearray([0b10001000, 0b10001000, 0b10001000, 0b11111000, 0b10001000, 0b10001000, 0b10001000, 0b10001000, 0b10001000, 0b00000000]), # Large H-like
    bytearray([0b01110000, 0b10001000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10001000, 0b01110000, 0b00000000]), # Large C-like
    bytearray([0b11111000, 0b00100000, 0b00100000, 0b01110000, 0b10100000, 0b10100000, 0b10100000, 0b10100000, 0b10100000, 0b00000000]), # Large Abstract
]

# --- Glyph Set Configuration ---
GLYPH_SETS = {
    'small': {
        'glyphs': GLYPHS_SMALL, 'width': 3, 'height': 6, 'num_glyphs': len(GLYPHS_SMALL)
    },
    'medium': {
        'glyphs': GLYPHS, 'width': 4, 'height': 8, 'num_glyphs': len(GLYPHS)
    },
    'large': {
        'glyphs': GLYPHS_LARGE, 'width': 5, 'height': 10, 'num_glyphs': len(GLYPHS_LARGE)
    }
}

# --- Column and Display Configuration ---
COLUMN_SLOT_WIDTH = 5 # Width of each column "slot" to accommodate largest glyphs
COLS = thumby.display.width // COLUMN_SLOT_WIDTH

# --- Depth Configuration ---
DEPTH_LEVELS = {
    'foreground': {'speed_min': 1, 'speed_max': 3, 'render_skip': 0, 'glyph_set_key': 'large'},
    'midground':  {'speed_min': 3, 'speed_max': 5, 'render_skip': 0, 'glyph_set_key': 'medium'},
    'background': {'speed_min': 5, 'speed_max': 8, 'render_skip': 1, 'glyph_set_key': 'small'},
}
DEPTH_TYPES = list(DEPTH_LEVELS.keys())

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

def reset_column_state(col_data_obj):
    depth_type = random.choice(DEPTH_TYPES)
    depth_props = DEPTH_LEVELS[depth_type]
    glyph_set_key = depth_props['glyph_set_key']
    glyph_set_info = GLYPH_SETS[glyph_set_key]

    col_data_obj['depth_type'] = depth_type
    col_data_obj['current_glyph_set_key'] = glyph_set_key
    col_data_obj['glyph_w'] = glyph_set_info['width']
    col_data_obj['glyph_h'] = glyph_set_info['height']
    col_data_obj['num_glyphs_in_set'] = glyph_set_info['num_glyphs']

    col_data_obj['head_y'] = random.randint(-col_data_obj['glyph_h'] * 5, -col_data_obj['glyph_h']) # Start off-screen
    col_data_obj['trail_len'] = random.randint(1, 3)
    col_data_obj['glyph_idx'] = random.randint(0, col_data_obj['num_glyphs_in_set'] - 1)
    col_data_obj['trail_glyph_indices'] = [random.randint(0, col_data_obj['num_glyphs_in_set'] - 1) for _ in range(col_data_obj['trail_len'])]
    col_data_obj['speed_counter'] = 0
    col_data_obj['speed_threshold'] = random.randint(depth_props['speed_min'], depth_props['speed_max'])
    col_data_obj['render_counter'] = 0

for _ in range(COLS):
    new_col_data = {}
    reset_column_state(new_col_data) # Initialize with random properties
    column_states.append(new_col_data)

# --- Main Game Loop ---
while True:
    thumby.display.fill(0) # Clear the entire display to black each frame

    # For each column, draw the glyphs
    for col_idx, col_data in enumerate(column_states):
        # Handle rendering based on depth
        depth_props = DEPTH_LEVELS[col_data['depth_type']]
        glyph_set_info = GLYPH_SETS[col_data['current_glyph_set_key']]
        current_glyph_w = col_data['glyph_w']
        current_glyph_h = col_data['glyph_h']
        current_glyphs = glyph_set_info['glyphs']

        col_data['render_counter'] += 1
        
        # Only render if render_skip is 0 (always render)
        # or if render_counter is a multiple of (render_skip + 1)
        # e.g., if render_skip=1, draw every 2nd frame
        if depth_props['render_skip'] == 0 or col_data['render_counter'] % (depth_props['render_skip'] + 1) == 0:
            # Calculate x position to center glyph in its slot
            slot_start_x = col_idx * COLUMN_SLOT_WIDTH
            padding_x = (COLUMN_SLOT_WIDTH - current_glyph_w) // 2
            draw_x = slot_start_x + padding_x

            # Draw the head glyph
            head_y_pixel = col_data['head_y']
            head_glyph = current_glyphs[col_data['glyph_idx']]
            draw_glyph_pixels(head_glyph, draw_x, head_y_pixel, current_glyph_w, current_glyph_h)

            # Draw the trail glyphs
            for i in range(col_data['trail_len']): # i from 0 to trail_len-1
                trail_y_pixel = head_y_pixel - ((i + 1) * current_glyph_h) # Glyph i is (i+1) positions above head
                trail_glyph_idx = col_data['trail_glyph_indices'][i]
                trail_glyph = current_glyphs[trail_glyph_idx]
                draw_glyph_pixels(trail_glyph, draw_x, trail_y_pixel, current_glyph_w, current_glyph_h)
        
        # Reset render_counter if it exceeds render_skip to loop its cycle
        if col_data['render_counter'] > depth_props['render_skip']:
            col_data['render_counter'] = 0


    # Update column states for scrolling
    for col_data in column_states:
        col_data['speed_counter'] += 1
        if col_data['speed_counter'] >= col_data['speed_threshold']:
            col_data['head_y'] += 1 # Move down by 1 pixel
            col_data['speed_counter'] = 0 # Reset counter

            # If the *entire column* (head + all trail glyphs) has scrolled off the bottom.
            # This means the top edge of the topmost trail glyph is at or below the screen's bottom edge.
            top_of_topmost_glyph_y = col_data['head_y'] - (col_data['trail_len'] * col_data['glyph_h'])
            
            if top_of_topmost_glyph_y >= thumby.display.height:
                reset_column_state(col_data) # Reset with new random properties, including depth and size
                

    thumby.display.update() # Update the physical display

    time.sleep(0.01) # Adjusted for potentially smoother, more consistent animation
