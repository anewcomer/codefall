# main.py
# The main application file for Thumby Codefall
# Rewritten to use thumby.display.setPixel for drawing, as blit is unreliable.

import thumby
import random
import time

# --- Thumby Display Configuration ---
# THUMBY_WIDTH = 72
# THUMBY_HEIGHT = 40

# --- Glyph Definitions (Medium Size - 4x8) - Abstract & Katakana-inspired ---
# Each glyph is a list of bytes, representing rows of pixels.
# The most significant 4 bits of each byte are used for the 4-pixel width.
GLYPHS = [
    # Original 16 Glyphs (some modified)
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000]), # Katakana No/So stroke
    bytearray([0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000]), # Vertical Bar (offset)
    bytearray([0b11100000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b11100000, 0b00000000]), # Katakana Ko
    bytearray([0b11100000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b00100000, 0b00100000, 0b00000000]), # Katakana Te
    bytearray([0b10000000, 0b10000000, 0b11100000, 0b01000000, 0b01000000, 0b01000000, 0b00000000, 0b00000000]), # Katakana Ka
    bytearray([0b01000000, 0b01000000, 0b11100000, 0b01000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Katakana To
    bytearray([0b10100000, 0b01000000, 0b10100000, 0b01000000, 0b10100000, 0b00000000, 0b11110000, 0b00000000]), # Abstract Bars & Line
    bytearray([0b00010000, 0b00100000, 0b01000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b00000000]), # Katakana So
    bytearray([0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b10000000, 0b01000000, 0b00100000, 0b00010000]), # Katakana Me (stylized)
    bytearray([0b01100000, 0b10010000, 0b10010000, 0b01100000, 0b10010000, 0b10010000, 0b01100000, 0b00000000]), # Number 8-like
    bytearray([0b11100000, 0b10100000, 0b10100000, 0b11100000, 0b10100000, 0b10100000, 0b11100000, 0b00000000]), # Grid-like
    bytearray([0b00000000, 0b11110000, 0b10010000, 0b10010000, 0b10010000, 0b11110000, 0b00000000, 0b00000000]), # Number 0-like
    bytearray([0b00100000, 0b01100000, 0b10100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000]), # Number 1-like
    bytearray([0b11100000, 0b00100000, 0b00100000, 0b11100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000]), # Katakana Ra
    bytearray([0b11110000, 0b10000000, 0b11110000, 0b00010000, 0b00010000, 0b00010000, 0b11110000, 0b00000000]), # Number 5-like
    bytearray([0b01100000, 0b10010000, 0b00100000, 0b01000000, 0b10010000, 0b10010000, 0b01100000, 0b00000000]), # Number 6-like
]
# --- Additional Glyphs to reach 32 total ---
GLYPHS.extend([
    # Kept abstract glyphs
    bytearray([0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b11110000, 0b01100000, 0b00100000, 0b00000000]), # Arrow Down-like
    bytearray([0b00100000, 0b01100000, 0b11110000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000]), # Arrow Up-like
    bytearray([0b00000000, 0b00100000, 0b00100000, 0b11110000, 0b00100000, 0b00100000, 0b00000000, 0b00000000]), # Plus-like
    bytearray([0b00000000, 0b00000000, 0b00000000, 0b11110000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Minus-like
    bytearray([0b00000000, 0b01100000, 0b01100000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Small Square
    bytearray([0b10100000, 0b01010000, 0b10100000, 0b01010000, 0b10100000, 0b01010000, 0b10100000, 0b01010000]), # Checkerboard
    # New Katakana-inspired / abstract glyphs
    bytearray([0b10000000, 0b10000000, 0b01100000, 0b00100000, 0b00100000, 0b00000000, 0b00000000, 0b00000000]), # Katakana Ya
    bytearray([0b01100000, 0b10000000, 0b00100000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Katakana Fu
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b01100000, 0b00000000]), # Katakana Re
    bytearray([0b11100000, 0b10100000, 0b10100000, 0b10100000, 0b10100000, 0b10100000, 0b11100000, 0b00000000]), # Katakana Ro
    bytearray([0b10000000, 0b10000000, 0b11100000, 0b10000000, 0b10000000, 0b10000000, 0b11100000, 0b00000000]), # Katakana Yu
    bytearray([0b10000000, 0b10000000, 0b01100000, 0b10000000, 0b10000000, 0b00000000, 0b00000000, 0b00000000]), # Katakana Ha
    bytearray([0b10000000, 0b10000000, 0b11100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000, 0b00000000]), # Katakana Wa
    # Kept abstract glyphs
    bytearray([0b01100000, 0b10010000, 0b00010000, 0b00100000, 0b00100000, 0b00000000, 0b00100000, 0b00000000]), # Question Mark-like
    bytearray([0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000, 0b00100000, 0b00000000]), # Exclamation Mark-like
    bytearray([0b00000000, 0b01100000, 0b01100000, 0b00000000, 0b10010000, 0b01100000, 0b00000000, 0b00000000]), # Abstract Smiley-like
])

# --- Small Glyphs (3x6) - Abstract & Katakana-inspired ---
# Most significant 3 bits used.
GLYPHS_SMALL = [
    bytearray([0b11100000, 0b10000000, 0b10000000, 0b10000000, 0b11100000, 0b00000000]), # Small Katakana Ko
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000]), # Small |-like
    bytearray([0b00100000, 0b01000000, 0b10000000, 0b00000000, 0b00000000, 0b00000000]), # Small Katakana No
    bytearray([0b01000000, 0b11100000, 0b01000000, 0b00000000, 0b00000000, 0b00000000]), # Small Katakana To
]

# --- Large Glyphs (5x10) - Abstract & Katakana-inspired ---
# Most significant 5 bits used.
GLYPHS_LARGE = [
    bytearray([0b00100000, 0b01110000, 0b00100000, 0b10001000, 0b10001000, 0b10001000, 0b10001000, 0b00000000, 0b00000000, 0b00000000]), # Large Katakana A
    bytearray([0b01000000, 0b01000000, 0b11111000, 0b01000000, 0b01000000, 0b10010000, 0b10010000, 0b00000000, 0b00000000, 0b00000000]), # Large Katakana Ta
    bytearray([0b11100000, 0b11100000, 0b00100000, 0b00100000, 0b00010000, 0b00010000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Large Katakana Mi
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
# COLS = thumby.display.width // COLUMN_SLOT_WIDTH # Replaced by dynamic current_num_columns
MAX_PHYSICAL_COLS = thumby.display.width // COLUMN_SLOT_WIDTH
MIN_PHYSICAL_COLS = 1


# --- Depth Configuration ---
DEPTH_LEVELS = {
    'foreground': {'speed_min': 1, 'speed_max': 3, 'render_skip': 0, 'glyph_set_key': 'large'},
    'midground':  {'speed_min': 3, 'speed_max': 5, 'render_skip': 0, 'glyph_set_key': 'medium'},
    'background': {'speed_min': 5, 'speed_max': 8, 'render_skip': 1, 'glyph_set_key': 'small'},
}
DEPTH_TYPES = list(DEPTH_LEVELS.keys())

# --- Game State Constants ---
STATE_TITLE = 0
STATE_CODEFALL = 1

# --- Interactive Control Variables & Constants ---
is_frozen = False
GLOBAL_SPEED_ADJUSTMENT = 0
# Max adjustment allows any column's speed threshold to become 1 (fastest)
MAX_SPEED_ADJUST = max(max(level['speed_min'], level['speed_max']) for level in DEPTH_LEVELS.values()) - 1
MIN_SPEED_ADJUST = -10 # Allow slowing down significantly (higher threshold values)

current_num_columns = MAX_PHYSICAL_COLS # Start with max columns

current_game_state = STATE_TITLE

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

    # Start slightly more off-screen to accommodate varying trail lengths better on initial drop
    col_data_obj['head_y'] = random.randint(-col_data_obj['glyph_h'] * 8, -col_data_obj['glyph_h'] * 2)
    col_data_obj['trail_len'] = random.randint(1, 3)
    col_data_obj['glyph_idx'] = random.randint(0, col_data_obj['num_glyphs_in_set'] - 1)
    col_data_obj['trail_glyph_indices'] = [random.randint(0, col_data_obj['num_glyphs_in_set'] - 1) for _ in range(col_data_obj['trail_len'])]
    col_data_obj['speed_counter'] = 0
    col_data_obj['base_speed_threshold'] = random.randint(depth_props['speed_min'], depth_props['speed_max'])
    col_data_obj['render_counter'] = 0

def full_reset_animation():
    global is_frozen, GLOBAL_SPEED_ADJUSTMENT, column_states, current_num_columns
    
    is_frozen = False
    GLOBAL_SPEED_ADJUSTMENT = 0
    # current_num_columns = MAX_PHYSICAL_COLS # Optionally reset density; current behavior keeps existing density.

    column_states = []
    for _ in range(current_num_columns): # Use the current_num_columns
        new_col_data = {}
        reset_column_state(new_col_data)
        column_states.append(new_col_data)

def draw_title_screen():
    # Approximate center calculations for text
    # Text chars are roughly 5px wide, 7px tall
    title_text = "Codefall"
    title_x = (thumby.display.width - (len(title_text) * 5)) // 2
    thumby.display.drawText(title_text, title_x, 2, 1)

    line2_text = "A:Frz B:Rst"
    line2_x = (thumby.display.width - (len(line2_text) * 5)) // 2
    thumby.display.drawText(line2_text, line2_x, 11, 1)

    line3_text = "D:Spd/Dens"
    line3_x = (thumby.display.width - (len(line3_text) * 5)) // 2
    thumby.display.drawText(line3_text, line3_x, 20, 1)

    line4_text = "Press A/B"
    line4_x = (thumby.display.width - (len(line4_text) * 5)) // 2
    thumby.display.drawText(line4_text, line4_x, 30, 1)

# Initialize column_states (will be properly initialized by full_reset_animation on first game start)
column_states = []
for _ in range(current_num_columns): # Initial population based on default current_num_columns
    new_col_data = {}
    reset_column_state(new_col_data) # Initialize with random properties
    column_states.append(new_col_data)
# --- Main Game Loop ---
while True:
    # --- Input Handling & Logic ---
    if current_game_state == STATE_TITLE:
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            current_game_state = STATE_CODEFALL
            full_reset_animation() # Ensure a clean start for the animation

    elif current_game_state == STATE_CODEFALL:
        # --- Handle Inputs for Codefall Animation ---
        if thumby.buttonA.justPressed():
            is_frozen = not is_frozen
        
        if thumby.buttonB.justPressed():
            full_reset_animation()

        # Speed and Density controls can be used even if frozen, affecting next active state or new columns
        if thumby.buttonU.justPressed():
            GLOBAL_SPEED_ADJUSTMENT = min(MAX_SPEED_ADJUST, GLOBAL_SPEED_ADJUSTMENT + 1)
        if thumby.buttonD.justPressed():
            GLOBAL_SPEED_ADJUSTMENT = max(MIN_SPEED_ADJUST, GLOBAL_SPEED_ADJUSTMENT - 1)
        
        if thumby.buttonR.justPressed():
            current_num_columns = min(MAX_PHYSICAL_COLS, current_num_columns + 1)
        if thumby.buttonL.justPressed():
            current_num_columns = max(MIN_PHYSICAL_COLS, current_num_columns - 1)

        # --- Adjust column_states list based on current_num_columns ---
        while len(column_states) < current_num_columns:
            new_col = {}
            reset_column_state(new_col)
            column_states.append(new_col)
        while len(column_states) > current_num_columns:
            column_states.pop()
            
        # --- Update column states for scrolling (if not frozen) ---
        if not is_frozen:
            for col_data in column_states:
                col_data['speed_counter'] += 1
                effective_speed_threshold = max(1, col_data['base_speed_threshold'] - GLOBAL_SPEED_ADJUSTMENT)
                
                if col_data['speed_counter'] >= effective_speed_threshold:
                    col_data['head_y'] += 1 # Move down by 1 pixel
                    col_data['speed_counter'] = 0 # Reset counter

                    # If the *entire column* (head + all trail glyphs) has scrolled off the bottom.
                    top_of_topmost_glyph_y = col_data['head_y'] - (col_data['trail_len'] * col_data['glyph_h'])
                    
                    if top_of_topmost_glyph_y >= thumby.display.height:
                        reset_column_state(col_data) # Reset with new random properties

    # --- Drawing ---
    thumby.display.fill(0) # Clear the entire display to black each frame

    if current_game_state == STATE_TITLE:
        draw_title_screen()
    elif current_game_state == STATE_CODEFALL:
        # For each column, draw the glyphs
        for col_idx, col_data in enumerate(column_states):
            depth_props = DEPTH_LEVELS[col_data['depth_type']]
            glyph_set_info = GLYPH_SETS[col_data['current_glyph_set_key']]
            current_glyph_w = col_data['glyph_w']
            current_glyph_h = col_data['glyph_h']
            current_glyphs = glyph_set_info['glyphs']

            col_data['render_counter'] += 1
            
            if depth_props['render_skip'] == 0 or col_data['render_counter'] % (depth_props['render_skip'] + 1) == 0:
                slot_start_x = col_idx * COLUMN_SLOT_WIDTH
                padding_x = (COLUMN_SLOT_WIDTH - current_glyph_w) // 2
                draw_x = slot_start_x + padding_x

                head_y_pixel = col_data['head_y']
                head_glyph = current_glyphs[col_data['glyph_idx']]
                draw_glyph_pixels(head_glyph, draw_x, head_y_pixel, current_glyph_w, current_glyph_h)

                for i in range(col_data['trail_len']):
                    trail_y_pixel = head_y_pixel - ((i + 1) * current_glyph_h)
                    trail_glyph_idx = col_data['trail_glyph_indices'][i]
                    trail_glyph = current_glyphs[trail_glyph_idx]
                    draw_glyph_pixels(trail_glyph, draw_x, trail_y_pixel, current_glyph_w, current_glyph_h)
            
            if col_data['render_counter'] > depth_props['render_skip']:
                col_data['render_counter'] = 0

    thumby.display.update() # Update the physical display

    time.sleep(0.01) # Maintain a consistent frame rate
