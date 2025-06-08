# Project Milestones

This document outlines the planned features and development stages for Thumby Codefall.

## Milestone 1: Simulated Depth Effect
**Original Goal:** Add simulated "depth" to the rain effect.
**Status: Implemented & Enhanced!**

**Key Features Achieved (as per `Codefall.py`):**
*   **Depth Property:** Each column now has a `depth_type` (e.g., `layer1_farthest` to `layer5_nearest`) stored in `column_states`.
    *   Expanded from 3 to **5 distinct depth layers** for a more nuanced effect.
*   **Varied Properties by Depth:**
    *   **Speed:** Columns at different depths have distinct and wider ranges for `speed_min` and `speed_max` in `DEPTH_LEVELS`, increasing variability.
    *   **Dimming Pattern (Simulated Brightness/Fading):** Farthest layers use a `dim_pattern` (checkerboard) to appear less distinct.
    *   **Glyph Set:** Different depth layers now use different glyph sets (`small`, `medium`, `large`) via `glyph_set_key` in `DEPTH_LEVELS`, significantly enhancing the visual depth.
*   **`column_states` Modification:** Each column state includes `depth_type`, `base_speed_threshold`, `speed_counter`, `current_glyph_set_key`, `glyph_w`, `glyph_h`, `num_glyphs_in_set`, and `draw_x`.
*   **Main Loop Update:**
    *   Columns are assigned a random depth on initialization/reset.
    *   Speed updates and rendering logic now factor in the column's depth properties.
*   **Overlapping Columns:** Column placements are now fully randomized horizontally (`draw_x`), allowing them to overlap and further enhancing the depth illusion.

**Initial Discussion (Archived from previous state):**
> Coding partner
> That's an excellent idea to add more visual interest and realism to the Codefall effect! Simulating depth can really enhance the overall aesthetic.
>
> Here's an overview of how we can approach adding "depth" to the rain effect:
>
> Introduce a depth property for each column: This property will determine how a column is rendered.
> Vary glyph properties based on depth:
> Size: Background columns could use smaller glyphs, while foreground columns use the current 4x8 glyphs.
> Speed: Background columns could move slower, and foreground columns faster.
> Color/Brightness (Simulated): On a monochrome display like Thumby, we can't truly change color. However, we can simulate "fading" for background elements by:
> Rendering them less frequently (e.g., skipping frames).
> Using a "thinner" or more sparse version of the glyph. For simplicity and keeping glyph definitions clean, we'll focus on the frequency for now.
> Adjust the draw_glyph_pixels function (or create a new one): This function will need to be flexible enough to handle different glyph sizes or rendering methods.
> Development Steps
> Here's how we'll implement this feature:
>
> Define different depth levels: We'll start with two or three distinct depth levels (e.g., "foreground," "midground," "background").
> Create new smaller glyph sets (optional but good for true depth): If we want to truly simulate smaller glyphs, we'd need to define 2x4 pixel glyphs, for example. For a first pass, we can use the existing glyphs and primarily adjust speed and rendering frequency. Let's aim to simplify this for now and just adjust speed and rendering frequency.
> Modify column_states: Each column will get a depth attribute, and its speed_threshold and rendering logic will depend on this depth.
> Update the main loop:
> When a column is initialized or reset, assign it a random depth.
> Modify the speed update logic to factor in depth.
> Implement conditional rendering or modify draw_glyph_pixels to account for depth (e.g., skip drawing based on depth for a flickering effect).
> Assumptions and Restrictions
> Monochrome Display: We'll be simulating depth using speed, size (if new glyphs are made), and rendering frequency, not actual color gradients.
> Performance: Introducing more complexity can impact performance. We'll try to keep the drawing logic efficient.
> Glyph Sizes: For simplicity, we'll initially stick with the 4x8 glyphs and simulate depth through speed and rendering frequency. If that's not visually convincing, we can explore adding smaller glyph sets.
> Let's start by modifying the column_states initialization to include a depth level and adjust speed_threshold based on it. We'll aim for three depth levels:
>
> Foreground: Fastest, always drawn.
> Midground: Medium speed, always drawn.
> Background: Slowest, drawn less frequently (to simulate fading/flickering).

## Future Milestones (Potential Next Steps)
## Milestone 2: Enhanced Visuals & Customization
**Status: Partially Implemented**

*   **Glyph Variation:**
    *   **Implemented:** Multiple glyph sets (`GLYPHS_SMALL`, `GLYPHS` (medium), `GLYPHS_LARGE`) are defined and used by different depth layers.
    *   **Implemented:** Glyphs now morph into other glyphs within their set, adding dynamic visual variation.
    *   *To Do (Option 2):* Allow the "head" glyph of a column to be *always* visually distinct (e.g., brighter, or a specific "leader" glyph beyond current morphing).
*   **Trail Effects:**
    *   **Implemented:** Dynamic trail length (`trail_len`) is randomized for each column upon reset.
    *   *To Do:* Fading trail: Glyphs in a trail could become progressively "dimmer".

## Milestone 3: User Interaction & Controls
**Status: Partially Implemented**

*   **Button Controls:**
    *   **Implemented:** Pause/resume the animation (Button A: `is_frozen`).
    *   **Implemented:** Control overall speed (D-Pad Up/Down: `GLOBAL_SPEED_ADJUSTMENT`).
    *   **Implemented:** Control glyph density/number of streaks (D-Pad Left/Right: `current_num_columns`).
    *   **Implemented:** Reset animation to initial state (Button B: `full_reset_animation`).
    *   *To Do:* Cycle through different visual themes or glyph sets (if implemented).

## Milestone 4: Performance & Refinement
**Status: In Progress / Partially Implemented**

*   **Code Cleanup:**
    *   **Implemented:** General refactoring for clarity and maintainability (e.g., `_get_drawing_glyph_data` helper, modularized title screen drawing, consistent reset behavior).
*   **Optimization:**
    *   **Implemented:** Optimized glyph drawing using direct buffer manipulation (`draw_glyph_pixels`).
    *   **Implemented:** Title screen initialization logic improved.
    *   *To Do:* Profile and identify any further performance bottlenecks, especially with increased streak counts and morphing.

These milestones are suggestions and can be prioritized or modified as the project evolves.
