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
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000]),
    bytearray([0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b01000000]),
    bytearray([0b11100000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b11100000, 0b00000000]),
    bytearray([0b11100000, 0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b00100000, 0b00100000, 0b00000000]),
    bytearray([0b10000000, 0b10000000, 0b11100000, 0b01000000, 0b01000000, 0b01000000, 0b00000000, 0b00000000]),
    bytearray([0b01000000, 0b01000000, 0b11100000, 0b01000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]),
    bytearray([0b10100000, 0b01000000, 0b10100000, 0b01000000, 0b10100000, 0b00000000, 0b11110000, 0b00000000]),
    bytearray([0b00010000, 0b00100000, 0b01000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b00000000]),
    bytearray([0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b10000000, 0b01000000, 0b00100000, 0b00010000]),
    bytearray([0b01100000, 0b10010000, 0b10010000, 0b01100000, 0b10010000, 0b10010000, 0b01100000, 0b00000000]),
    bytearray([0b11100000, 0b10100000, 0b10100000, 0b11100000, 0b10100000, 0b10100000, 0b11100000, 0b00000000]),
    bytearray([0b00000000, 0b11110000, 0b10010000, 0b10010000, 0b10010000, 0b11110000, 0b00000000, 0b00000000]),
    bytearray([0b00100000, 0b01100000, 0b10100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000]),
    bytearray([0b11100000, 0b00100000, 0b00100000, 0b11100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000]),
    bytearray([0b11110000, 0b10000000, 0b11110000, 0b00010000, 0b00010000, 0b00010000, 0b11110000, 0b00000000]),
    bytearray([0b01100000, 0b10010000, 0b00100000, 0b01000000, 0b10010000, 0b10010000, 0b01100000, 0b00000000]),
    bytearray([0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b11110000, 0b01100000, 0b00100000, 0b00000000]),
    bytearray([0b00100000, 0b01100000, 0b11110000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000]),
    bytearray([0b00000000, 0b00100000, 0b00100000, 0b11110000, 0b00100000, 0b00100000, 0b00000000, 0b00000000]),
    bytearray([0b00000000, 0b00000000, 0b00000000, 0b11110000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]),
    bytearray([0b00000000, 0b01100000, 0b01100000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]),
    bytearray([0b10100000, 0b01010000, 0b10100000, 0b01010000, 0b10100000, 0b01010000, 0b10100000, 0b01010000]),
    bytearray([0b10000000, 0b10000000, 0b01100000, 0b00100000, 0b00100000, 0b00000000, 0b00000000, 0b00000000]),
    bytearray([0b01100000, 0b10000000, 0b00100000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]),
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b01100000, 0b00000000]),
    bytearray([0b11100000, 0b10100000, 0b10100000, 0b10100000, 0b10100000, 0b10100000, 0b11100000, 0b00000000]),
    bytearray([0b10000000, 0b10000000, 0b11100000, 0b10000000, 0b10000000, 0b10000000, 0b11100000, 0b00000000]),
    bytearray([0b10000000, 0b10000000, 0b01100000, 0b10000000, 0b10000000, 0b00000000, 0b00000000, 0b00000000]),
    bytearray([0b10000000, 0b10000000, 0b11100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000, 0b00000000]),
    bytearray([0b01100000, 0b10010000, 0b00010000, 0b00100000, 0b00100000, 0b00000000, 0b00100000, 0b00000000]),
    bytearray([0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000, 0b00100000, 0b00000000]),
    bytearray([0b00000000, 0b01100000, 0b01100000, 0b00000000, 0b10010000, 0b01100000, 0b00000000, 0b00000000]),
]

# --- Small Glyphs (3x6) - Abstract & Katakana-inspired ---
# Most significant 3 bits used.
GLYPHS_SMALL = [
    bytearray([0b11100000, 0b10000000, 0b10000000, 0b10000000, 0b11100000, 0b00000000]), # Small Katakana Ko
    bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000]), # Small |-like
    bytearray([0b00100000, 0b01000000, 0b10000000, 0b01000000, 0b00100000, 0b00000000]), # Small Katakana No (variant)
    bytearray([0b01000000, 0b11100000, 0b01000000, 0b00000000, 0b00000000, 0b00000000]), # Small Katakana To
    bytearray([0b11100000, 0b00100000, 0b00100000, 0b01000000, 0b01000000, 0b00000000]), # Small 7-like
    bytearray([0b10100000, 0b01000000, 0b01000000, 0b10100000, 0b00000000, 0b00000000]), # Small X-like
    bytearray([0b01000000, 0b11100000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Small Triangle-like
    bytearray([0b11100000, 0b00100000, 0b01000000, 0b10000000, 0b11100000, 0b00000000]), # Small Z-like
]

# --- Large Glyphs (5x10) - Abstract & Katakana-inspired ---
# Most significant 5 bits used.
GLYPHS_LARGE = [
    bytearray([0b00100000, 0b01110000, 0b10001000, 0b10001000, 0b11111000, 0b10001000, 0b10001000, 0b00000000, 0b00000000, 0b00000000]), # Large Katakana A (modified)
    bytearray([0b01000000, 0b01000000, 0b11111000, 0b01000000, 0b01000000, 0b10010000, 0b10010000, 0b00000000, 0b00000000, 0b00000000]), # Large Katakana Ta
    bytearray([0b11100000, 0b11100000, 0b00100000, 0b00100000, 0b00010000, 0b00010000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Large Katakana Mi
    bytearray([0b11111000, 0b00100000, 0b00100000, 0b01110000, 0b10100000, 0b10100000, 0b10100000, 0b10100000, 0b10100000, 0b00000000]), # Large Abstract
    bytearray([0b11111000, 0b01010000, 0b01010000, 0b01010000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]), # Large Pi-like
    bytearray([0b11111000, 0b10000000, 0b10000000, 0b01110000, 0b00001000, 0b00001000, 0b11111000, 0b00000000, 0b00000000, 0b00000000]), # Large Sigma-like
    bytearray([0b00100000, 0b01110000, 0b11111000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00000000, 0b00000000]), # Large Arrow-like
    bytearray([0b01110000, 0b10001000, 0b10001000, 0b10001000, 0b10001000, 0b01010000, 0b01010000, 0b11011000, 0b00000000, 0b00000000]), # Large Omega-like
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

# --- Title Font Glyphs (5x7 pixels) ---
# Each character uses the 5 most significant bits of each byte.
TITLE_FONT_GLYPHS = {
    'A': bytearray([0b01110000, 0b10001000, 0b10001000, 0b11111000, 0b10001000, 0b10001000, 0b10001000]),
    'B': bytearray([0b11110000, 0b10001000, 0b10001000, 0b11110000, 0b10001000, 0b10001000, 0b11110000]),
    'C': bytearray([0b01110000, 0b10001000, 0b10000000, 0b10000000, 0b10000000, 0b10001000, 0b01110000]),
    'D': bytearray([0b11100000, 0b10010000, 0b10010000, 0b10010000, 0b10010000, 0b10010000, 0b11100000]),
    'E': bytearray([0b11111000, 0b10000000, 0b10000000, 0b11100000, 0b10000000, 0b10000000, 0b11111000]),
    'F': bytearray([0b11111000, 0b10000000, 0b10000000, 0b11100000, 0b10000000, 0b10000000, 0b10000000]),
    'G': bytearray([0b01110000, 0b10001000, 0b10000000, 0b10111000, 0b10001000, 0b10001000, 0b01110000]),
    'H': bytearray([0b10001000, 0b10001000, 0b10001000, 0b11111000, 0b10001000, 0b10001000, 0b10001000]),
    'I': bytearray([0b11111000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b11111000]),
    'J': bytearray([0b00111000, 0b00010000, 0b00010000, 0b00010000, 0b10010000, 0b10010000, 0b01100000]),
    'K': bytearray([0b10001000, 0b10010000, 0b10100000, 0b11000000, 0b10100000, 0b10010000, 0b10001000]),
    'L': bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b11111000]),
    'M': bytearray([0b10001000, 0b11011000, 0b10101000, 0b10001000, 0b10001000, 0b10001000, 0b10001000]),
    'N': bytearray([0b10001000, 0b11001000, 0b10101000, 0b10011000, 0b10001000, 0b10001000, 0b10001000]),
    'O': bytearray([0b01110000, 0b10001000, 0b10001000, 0b10001000, 0b10001000, 0b10001000, 0b01110000]),
    'P': bytearray([0b11110000, 0b10001000, 0b10001000, 0b11110000, 0b10000000, 0b10000000, 0b10000000]),
    'Q': bytearray([0b01110000, 0b10001000, 0b10001000, 0b10001000, 0b10101000, 0b10010000, 0b01101000]),
    'R': bytearray([0b11110000, 0b10001000, 0b10001000, 0b11110000, 0b10100000, 0b10010000, 0b10001000]),
    'S': bytearray([0b01111000, 0b10000000, 0b01110000, 0b00001000, 0b00001000, 0b10001000, 0b01110000]),
    'T': bytearray([0b11111000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000]),
    'U': bytearray([0b10001000, 0b10001000, 0b10001000, 0b10001000, 0b10001000, 0b10001000, 0b01110000]),
    'V': bytearray([0b10001000, 0b10001000, 0b10001000, 0b01010000, 0b01010000, 0b00100000, 0b00100000]),
    'W': bytearray([0b10001000, 0b10001000, 0b10001000, 0b10101000, 0b10101000, 0b01010000, 0b01010000]),
    'X': bytearray([0b10001000, 0b01010000, 0b00100000, 0b01010000, 0b10001000, 0b10001000, 0b10001000]),
    'Y': bytearray([0b10001000, 0b10001000, 0b01010000, 0b00100000, 0b00100000, 0b00100000, 0b00100000]),
    'Z': bytearray([0b11111000, 0b00001000, 0b00010000, 0b00100000, 0b01000000, 0b10000000, 0b11111000])
}
TITLE_CHAR_WIDTH = 5
TITLE_CHAR_HEIGHT = 7
TITLE_CHAR_SPACING = 1
APP_TITLE_STRING = "CODEFALL"

# --- Help Text Font Glyphs (3x5 pixels) ---
# Each character uses the 3 most significant bits of each byte.
HELP_TEXT_FONT_GLYPHS = {
    'A': bytearray([0b11100000, 0b10100000, 0b11100000, 0b10100000, 0b10100000]),
    'B': bytearray([0b11000000, 0b10100000, 0b11000000, 0b10100000, 0b11000000]),
    'D': bytearray([0b11000000, 0b10100000, 0b10100000, 0b10100000, 0b11000000]),
    'E': bytearray([0b11100000, 0b10000000, 0b11000000, 0b10000000, 0b11100000]),
    'F': bytearray([0b11100000, 0b10000000, 0b11000000, 0b10000000, 0b10000000]),
    'N': bytearray([0b10100000, 0b11100000, 0b11100000, 0b10100000, 0b10100000]), # Simplified N
    'P': bytearray([0b11100000, 0b10100000, 0b11100000, 0b10000000, 0b10000000]),
    'R': bytearray([0b11100000, 0b10100000, 0b11000000, 0b10100000, 0b10100000]),
    'S': bytearray([0b11100000, 0b10000000, 0b11100000, 0b00100000, 0b11100000]),
    'T': bytearray([0b11100000, 0b01000000, 0b01000000, 0b01000000, 0b01000000]),
    'Z': bytearray([0b11100000, 0b00100000, 0b01000000, 0b10000000, 0b11100000]),
    ':': bytearray([0b00000000, 0b01000000, 0b00000000, 0b01000000, 0b00000000]),
    '/': bytearray([0b00100000, 0b00100000, 0b01000000, 0b10000000, 0b10000000]), # Adjusted /
}
HELP_TEXT_FONT_GLYPHS.update({
    'C': bytearray([0b11100000, 0b10000000, 0b10000000, 0b10000000, 0b11100000]),
    'G': bytearray([0b11100000, 0b10000000, 0b10100000, 0b10100000, 0b11100000]),
    'H': bytearray([0b10100000, 0b10100000, 0b11100000, 0b10100000, 0b10100000]),
    'I': bytearray([0b11100000, 0b01000000, 0b01000000, 0b01000000, 0b11100000]),
    'J': bytearray([0b00100000, 0b00100000, 0b00100000, 0b10100000, 0b01100000]),
    'K': bytearray([0b10100000, 0b11000000, 0b10100000, 0b10100000, 0b10100000]),
    'L': bytearray([0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b11100000]),
    'M': bytearray([0b10100000, 0b11100000, 0b10100000, 0b10100000, 0b10100000]),
    'O': bytearray([0b11100000, 0b10100000, 0b10100000, 0b10100000, 0b11100000]),
    'Q': bytearray([0b11100000, 0b10100000, 0b10100000, 0b10110000, 0b11101000]), # Q with integrated tail
    'U': bytearray([0b10100000, 0b10100000, 0b10100000, 0b10100000, 0b11100000]),
    'V': bytearray([0b10100000, 0b10100000, 0b01000000, 0b01000000, 0b01000000]),
    'W': bytearray([0b10100000, 0b10100000, 0b11100000, 0b01000000, 0b01000000]), # W with middle point down
    'X': bytearray([0b10100000, 0b01000000, 0b10100000, 0b10100000, 0b10100000]),
    'Y': bytearray([0b10100000, 0b10100000, 0b11100000, 0b01000000, 0b01000000]),
})
HELP_CHAR_WIDTH = 3
HELP_CHAR_HEIGHT = 5
HELP_CHAR_SPACING = 1 # Horizontal space between help text characters
HELP_LINE_SPACING = 2 # Vertical space between lines of help text

# Help text strings (uppercase for font consistency)
HELP_LINE_1 = "A:FRZ B:RST"
HELP_LINE_2 = "D:SPD/DENS"
HELP_LINE_3 = "PRESS A/B"

TITLE_ANIM_TARGET_Y = 5  # Final Y position for the title letters
TITLE_ANIM_FALL_SPEED = 2 # Pixels per frame for title letter fall
TITLE_ANIM_START_Y = -TITLE_CHAR_HEIGHT - 2 # Start Y above screen
TITLE_ANIM_LETTER_START_DELAY_FRAMES = 3 # Frames delay before next letter starts falling

# Title screen animation state variables
title_anim_letter_ys = [] # Stores current Y for each letter
title_anim_next_letter_to_start_idx = 0 # Index of the next letter that should begin falling
title_anim_stagger_counter = 0 # Counter for staggering letter starts
title_anim_is_complete = False

# --- Morphing Constants ---
GLYPH_MORPH_PROBABILITY = 0.01  # Further Increased: Chance per glyph per frame to start morphing
GLYPH_MORPH_DURATION_FRAMES = 20 # How many frames the morph animation lasts


# --- Column and Display Configuration ---
COLUMN_SLOT_WIDTH = 5 # Width of each column "slot" to accommodate largest glyphs
# COLS = thumby.display.width // COLUMN_SLOT_WIDTH # Replaced by dynamic current_num_columns
MAX_PHYSICAL_COLS = thumby.display.width // COLUMN_SLOT_WIDTH
MIN_PHYSICAL_COLS = 1


# --- Depth Configuration ---
DEPTH_LEVELS = {
    'foreground': {'speed_min': 1, 'speed_max': 3, 'dim_pattern': 0, 'glyph_set_key': 'large'}, # 0 = solid
    'midground':  {'speed_min': 3, 'speed_max': 5, 'dim_pattern': 0, 'glyph_set_key': 'medium'},# 0 = solid
    'background': {'speed_min': 5, 'speed_max': 8, 'dim_pattern': 1, 'glyph_set_key': 'small'}, # 1 = checkerboard
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
# Assumes glyph_row_data has the glyph pixels in the N most significant bits for an N-wide glyph.
# Assumes color is 1 (ON), drawing on a black background cleared by fill(0).
def draw_glyph_pixels(glyph_data, draw_x, draw_y, glyph_w, glyph_h, dim_pattern=0):
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
                # Apply dimming pattern if active
                if dim_pattern == 1: # Checkerboard
                    if (r_offset + c_offset) % 2 != 0: # Skip this pixel for checkerboard
                        continue
                buffer_idx = screen_x + page_offset
                buffer[buffer_idx] |= bit_to_set

# --- Glyph Morphing Interpolation Function ---
def get_interpolated_glyph_frame(source_glyph_data, target_glyph_data, progress, glyph_w, glyph_h):
    interpolated_data = bytearray(glyph_h) # Initialize with zeros (all pixels off)
    
    # Ensure progress is clamped between 0.0 and 1.0
    clamped_progress = max(0.0, min(1.0, progress))

    for r in range(glyph_h):
        source_row_byte = source_glyph_data[r]
        target_row_byte = target_glyph_data[r]
        interpolated_row_byte = 0
        for c in range(glyph_w):
            # Determine if this pixel should come from source or target based on progress
            pixel_is_target = (random.random() < clamped_progress)
            
            source_pixel_on = (source_row_byte >> (7 - c)) & 0x01
            target_pixel_on = (target_row_byte >> (7 - c)) & 0x01
            chosen_pixel_on = target_pixel_on if pixel_is_target else source_pixel_on
            if chosen_pixel_on:
                interpolated_row_byte |= (1 << (7 - c))
        interpolated_data[r] = interpolated_row_byte
    return interpolated_data

# --- Initialize Thumby Display ---
thumby.display.fill(0)
thumby.display.update()

# --- Game State Variables ---
column_states = []

def _create_glyph_morph_state(num_glyphs_in_set):
    return {
        'id': random.randint(0, num_glyphs_in_set - 1),
        'target_id': -1,  # -1 means not currently morphing
        'progress': 0.0
    }

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
    col_data_obj['head_glyph_morph_state'] = _create_glyph_morph_state(col_data_obj['num_glyphs_in_set'])
    col_data_obj['trail_glyph_morph_states'] = [_create_glyph_morph_state(col_data_obj['num_glyphs_in_set']) for _ in range(col_data_obj['trail_len'])]
    col_data_obj['speed_counter'] = 0
    col_data_obj['base_speed_threshold'] = random.randint(depth_props['speed_min'], depth_props['speed_max'])

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

def initialize_title_screen_state():
    global title_anim_letter_ys, title_anim_current_letter_idx, title_anim_is_complete
    global title_anim_next_letter_to_start_idx, title_anim_stagger_counter

    title_anim_letter_ys = [TITLE_ANIM_START_Y] * len(APP_TITLE_STRING)
    title_anim_is_complete = False
    title_anim_next_letter_to_start_idx = 0
    title_anim_stagger_counter = 0

def draw_title_screen():
    global title_anim_letter_ys, title_anim_current_letter_idx, title_anim_is_complete
    global title_anim_next_letter_to_start_idx, title_anim_stagger_counter

    # --- Animate Title Letters ---
    all_letters_landed_check = True # Assume all are landed until proven otherwise
    if not title_anim_is_complete:
        # Stagger start of new letters
        if title_anim_next_letter_to_start_idx < len(APP_TITLE_STRING):
            title_anim_stagger_counter += 1
            if title_anim_stagger_counter >= TITLE_ANIM_LETTER_START_DELAY_FRAMES:
                title_anim_next_letter_to_start_idx += 1
                title_anim_stagger_counter = 0

        # Animate all letters that have started
        for i in range(title_anim_next_letter_to_start_idx):
            if title_anim_letter_ys[i] < TITLE_ANIM_TARGET_Y:
                title_anim_letter_ys[i] = min(TITLE_ANIM_TARGET_Y, title_anim_letter_ys[i] + TITLE_ANIM_FALL_SPEED)
                all_letters_landed_check = False # At least one letter is still moving
            # If title_anim_letter_ys[i] is already >= TITLE_ANIM_TARGET_Y, it's landed
        
        # Check if all letters that *should* have started have also landed
        if all_letters_landed_check and title_anim_next_letter_to_start_idx == len(APP_TITLE_STRING):
            title_anim_is_complete = True
            
    # --- Draw Title Letters ---
    title_total_pixel_width = (len(APP_TITLE_STRING) * TITLE_CHAR_WIDTH) + \
                              ((len(APP_TITLE_STRING) - 1) * TITLE_CHAR_SPACING)
    current_draw_x = (thumby.display.width - title_total_pixel_width) // 2

    for i, char_code in enumerate(APP_TITLE_STRING):
        if char_code in TITLE_FONT_GLYPHS:
            glyph_data = TITLE_FONT_GLYPHS[char_code]
            draw_glyph_pixels(glyph_data, current_draw_x, title_anim_letter_ys[i], TITLE_CHAR_WIDTH, TITLE_CHAR_HEIGHT)
        current_draw_x += TITLE_CHAR_WIDTH + TITLE_CHAR_SPACING

    # --- Draw Help Text using custom font if Title Animation is Complete ---
    if title_anim_is_complete:
        current_help_y = TITLE_ANIM_TARGET_Y + TITLE_CHAR_HEIGHT + 5 # Start Y for first help line

        help_lines = [HELP_LINE_1, HELP_LINE_2, HELP_LINE_3]

        for line_text in help_lines:
            line_pixel_width = (len(line_text) * HELP_CHAR_WIDTH) + \
                               ((len(line_text) - 1) * HELP_CHAR_SPACING if len(line_text) > 0 else 0)
            current_help_x = (thumby.display.width - line_pixel_width) // 2
            
            for char_code in line_text:
                if char_code == ' ': # Handle spaces by advancing X
                    current_help_x += HELP_CHAR_WIDTH + HELP_CHAR_SPACING 
                elif char_code in HELP_TEXT_FONT_GLYPHS:
                    glyph_data = HELP_TEXT_FONT_GLYPHS[char_code]
                    draw_glyph_pixels(glyph_data, current_help_x, current_help_y, HELP_CHAR_WIDTH, HELP_CHAR_HEIGHT)
                    current_help_x += HELP_CHAR_WIDTH + HELP_CHAR_SPACING
            
            current_help_y += HELP_CHAR_HEIGHT + HELP_LINE_SPACING

# Initialize column_states (will be properly initialized by full_reset_animation on first game start)
column_states = []
for _ in range(current_num_columns): # Initial population based on default current_num_columns
    new_col_data = {}
    reset_column_state(new_col_data) # Initialize with random properties
    column_states.append(new_col_data)
# --- Main Game Loop ---
while True:
    # --- Input Handling & Logic ---
    # Note: Title screen specific updates are handled within draw_title_screen or its callees for now
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
                
                # --- Update Morphing State for Glyphs in this Column (if not frozen) ---
                # This logic is per column, so it's inside the column loop
                if not is_frozen: # Though this outer 'if not is_frozen' already covers it
                    glyph_states_to_update = [col_data['head_glyph_morph_state']] + col_data['trail_glyph_morph_states']
                    num_glyphs_in_set = col_data['num_glyphs_in_set']

                    for glyph_state in glyph_states_to_update:
                        if glyph_state['target_id'] != -1: # Currently morphing
                            glyph_state['progress'] += 1.0 / GLYPH_MORPH_DURATION_FRAMES
                            if glyph_state['progress'] >= 1.0:
                                glyph_state['id'] = glyph_state['target_id']
                                glyph_state['target_id'] = -1
                                glyph_state['progress'] = 0.0
                        else: # Not morphing, check if should start
                            if random.random() < GLYPH_MORPH_PROBABILITY:
                                new_target_id = random.randint(0, num_glyphs_in_set - 1)
                                # Ensure new target is different from current
                                while new_target_id == glyph_state['id'] and num_glyphs_in_set > 1:
                                    new_target_id = random.randint(0, num_glyphs_in_set - 1)
                                if new_target_id != glyph_state['id'] or num_glyphs_in_set == 1: # Allow morph to self if only 1 glyph
                                    glyph_state['target_id'] = new_target_id
                                    glyph_state['progress'] = 0.0

    # --- Drawing ---
    thumby.display.fill(0) # Clear the entire display to black each frame

    if current_game_state == STATE_TITLE and not title_anim_letter_ys: # Check if title anim needs init
        initialize_title_screen_state()


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
            
            slot_start_x = col_idx * COLUMN_SLOT_WIDTH
            padding_x = (COLUMN_SLOT_WIDTH - current_glyph_w) // 2
            draw_x = slot_start_x + padding_x
            current_dim_pattern = depth_props['dim_pattern']

            # Draw Head Glyph
            head_y_pixel = col_data['head_y']
            head_morph_state = col_data['head_glyph_morph_state']
            if head_morph_state['target_id'] != -1: # Morphing
                source_glyph = current_glyphs[head_morph_state['id']]
                target_glyph = current_glyphs[head_morph_state['target_id']]
                glyph_to_draw_data = get_interpolated_glyph_frame(
                    source_glyph, target_glyph, head_morph_state['progress'],
                    current_glyph_w, current_glyph_h
                )
            else: # Not morphing
                glyph_to_draw_data = current_glyphs[head_morph_state['id']]
            draw_glyph_pixels(glyph_to_draw_data, draw_x, head_y_pixel, current_glyph_w, current_glyph_h, current_dim_pattern)

            # Draw Trail Glyphs
            for i in range(col_data['trail_len']):
                trail_y_pixel = head_y_pixel - ((i + 1) * current_glyph_h)
                trail_morph_state = col_data['trail_glyph_morph_states'][i]
                if trail_morph_state['target_id'] != -1: # Morphing
                    source_glyph = current_glyphs[trail_morph_state['id']]
                    target_glyph = current_glyphs[trail_morph_state['target_id']]
                    glyph_to_draw_data = get_interpolated_glyph_frame(
                        source_glyph, target_glyph, trail_morph_state['progress'],
                        current_glyph_w, current_glyph_h
                    )
                else: # Not morphing
                    glyph_to_draw_data = current_glyphs[trail_morph_state['id']]
                draw_glyph_pixels(glyph_to_draw_data, draw_x, trail_y_pixel, current_glyph_w, current_glyph_h, current_dim_pattern)

    thumby.display.update() # Update the physical display

    time.sleep(0.01) # Maintain a consistent frame rate
