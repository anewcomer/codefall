# Project Progress Log

This document tracks the major features and improvements implemented in the Thumby Codefall project.

## Completed Features & Key Developments

### Core Animation & Rendering (Initial Version)

*   **Basic Animation Engine:**
    *   Implemented falling columns of glyphs.
    *   Columns reset at the top after falling off-screen.
*   **Custom Glyph Set:**
    *   Defined an initial set of 16 unique 4x8 pixel glyphs.
    *   Expanded glyph set to 32 unique glyphs (`GLYPHS` array).
*   **Optimized Glyph Drawing:**
    *   Developed `draw_glyph_pixels` function to directly manipulate `thumby.display.display.buffer`. This method was chosen over `blit` for reliability and fine-grained control.
*   **Column State Management:**
    *   Each column in `column_states` tracks its `head_y` position, `trail_len`, `glyph_idx`, `trail_glyph_indices`, and `speed_counter`/`speed_threshold`.
    *   Randomized properties for each column upon reset.

### Depth Simulation Feature - Phase 1 (Speed & Render Skipping)

*   **Depth Level Configuration (`DEPTH_LEVELS`):**
    *   Introduced three depth levels: `foreground`, `midground`, and `background`.
    *   Each depth level has distinct properties:
        *   `speed_min`, `speed_max`: Defines the range for falling speed.
        *   `render_skip`: Controls rendering frequency (e.g., `0` for always render, `1` for skip every other frame).
*   **Column Depth Integration:**
    *   Each column in `column_states` is now assigned a `depth_type`.
    *   `speed_threshold` is now randomly chosen based on the `speed_min` and `speed_max` of the column's assigned depth.
*   **Conditional Rendering Logic:**
    *   Implemented a `render_counter` for each column.
    *   Glyphs are drawn only if `depth_props['render_skip'] == 0` or if `col_data['render_counter'] % (depth_props['render_skip'] + 1) == 0`.
    *   This creates the effect of background columns appearing dimmer or less distinct.
*   **Dynamic Reset with Depth:**
    *   When a column resets, it's assigned a new random `depth_type`, and its `speed_threshold` and `render_counter` are updated accordingly.
*   **Timing:**
    *   Main loop includes `time.sleep(0.01)` for animation pacing.

---

### Depth Simulation Feature - Phase 2 (Variable Glyph Sizes)

*   **Multiple Glyph Sets (`GLYPH_SETS`):**
    *   Introduced `GLYPHS_SMALL` (e.g., 3x6), `GLYPHS` (original 4x8, now 'medium'), and `GLYPHS_LARGE` (e.g., 5x10).
    *   `GLYPH_SETS` dictionary manages these sets, storing glyph data, dimensions (`width`, `height`), and counts.
*   **Depth-Linked Glyph Sizes:**
    *   `DEPTH_LEVELS` configuration now includes a `glyph_set_key` for each level, associating `foreground`, `midground`, and `background` with large, medium, and small glyphs respectively.
*   **Column Slot System (`COLUMN_SLOT_WIDTH`):**
    *   Implemented `COLUMN_SLOT_WIDTH` to define fixed horizontal spacing for columns.
    *   Glyphs of varying widths are centered within their assigned slot.
*   **Dynamic Column Properties:**
    *   Each column in `column_states` now stores its current `glyph_w`, `glyph_h`, and the key for its active glyph set.
*   **Enhanced Drawing and Reset Logic:**
    *   Drawing functions now use the specific dimensions of each column's glyphs.
    *   Reset logic correctly calculates off-screen positions based on variable glyph heights.
*       This significantly enhances the 3D depth illusion by visually scaling glyphs based on their perceived distance.

---

### Interactive Controls & Title Screen (Planned)

*   **Title Screen Implementation:**
    *   A simple screen displayed at startup.
    *   Shows the application name (e.g., "Codefall").
    *   Provides a brief legend for button controls.
    *   Requires a new game state to differentiate between title and main animation.
*   **B Button (Reset):**
    *   Functionality: Resets the entire Codefall display.
    *   Action: Re-initializes all column states, effectively restarting the animation with new random parameters (depth, speed, glyphs, trail lengths) for each column.
*   **A Button (Freeze/Unfreeze):**
    *   Functionality: Pauses or resumes the animation.
    *   Action: Toggles a "frozen" state. When frozen, column positions and glyphs do not update.
*   **D-Pad Up (Increase Speed):**
    *   Functionality: Increases the overall falling speed of glyphs.
    *   Action: Adjusts a global speed modifier or modifies the base speed thresholds for all depth levels.
*   **D-Pad Down (Decrease Speed):**
    *   Functionality: Decreases the overall falling speed of glyphs.
    *   Action: Adjusts a global speed modifier or modifies the base speed thresholds, ensuring speeds don't become excessively slow or negative.
*   **D-Pad Left (Decrease Density):**
    *   Functionality: Reduces the number of active columns (glyphs appear less dense).
    *   Action: Decreases the `COLS` variable and adjusts the `column_states` list accordingly, down to a minimum number of columns.
*   **D-Pad Right (Increase Density):**
    *   Functionality: Increases the number of active columns (glyphs appear denser).
    *   Action: Increases the `COLS` variable and adjusts the `column_states` list, up to a maximum determined by screen width and `COLUMN_SLOT_WIDTH`.
---
*Last Updated: Planning for interactive controls and title screen.*