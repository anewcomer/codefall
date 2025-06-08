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
        *   `draw_probability`: Controls the chance of a glyph being rendered each frame (e.g., `1.0` for always render, `0.33` for a 33% chance). This replaces the previous `render_skip` mechanism.
*   **Column Depth Integration:**
    *   Each column in `column_states` is now assigned a `depth_type`.
    *   `speed_threshold` is now randomly chosen based on the `speed_min` and `speed_max` of the column's assigned depth.
*   **Conditional Rendering Logic:**
    *   Glyphs for a column are drawn if `random.random() < depth_props['draw_probability']`.
    *   This creates a more organic, less "strobe-like" effect for background columns, making them appear dimmer or less consistently present.
*   **Dynamic Reset with Depth:**
    *   When a column resets, it's assigned a new random `depth_type`, and its `speed_threshold` is updated accordingly.
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
### Interactive Controls & Title Screen

*   **Title Screen Implementation:**
    *   **Stylish Design:** Features an animated "CODEFALL" title where letters "rain" into place sequentially.
    *   **Custom Pixel Font:** The "CODEFALL" title uses a custom-designed 5x7 pixel font for a unique look.
    *   The title screen focuses solely on the animated title and help text for clarity.
*   **Help Text:** Provides a clear legend for button controls using a compact custom pixel font (e.g., 3x5), appearing after the title animation completes. This ensures a consistent visual style across all title screen text.
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
### Visual Enhancements - Glyph Morphing

*   **Random Morphing:** Individual glyphs in the falling columns can now randomly decide to morph into another glyph from their current set.
    *   Controlled by `GLYPH_MORPH_PROBABILITY`.
*   **Transition Effect:** The morph is not instantaneous. It occurs over `GLYPH_MORPH_DURATION_FRAMES`.
    *   During the transition, the glyph flickers between its original and target forms, with the target form becoming more prevalent as the morph progresses.
    *   This is achieved by rendering interpolated glyph frames using `get_interpolated_glyph_frame`. Pixels randomly switch from the source glyph to the target glyph based on the morph progress, creating a "digital dissolve" effect.
*   **State Management:** Each glyph (head and trail) now maintains its own morphing state (`id`, `target_id`, `progress`) within the `column_states`.

---
*Last Updated: Implemented glyph morphing feature and updated title screen animation.*