# Project Milestones

This document outlines the planned features and development stages for Thumby Codefall.

## Completed: Milestone 1 - Simulated Depth Effect

**Original Goal:** Add simulated "depth" to the rain effect, where some columns are closer in the foreground, and others appear more in the background.

**Status: Implemented!**

**Key Features Achieved (as per `Codefall.py`):**
*   **Depth Property:** Each column now has a `depth_type` (`foreground`, `midground`, `background`) stored in `column_states`.
*   **Varied Properties by Depth:**
    *   **Speed:** Background columns move slower, foreground columns faster. This is controlled by `speed_min` and `speed_max` in the `DEPTH_LEVELS` dictionary.
    *   **Rendering Frequency (Simulated Brightness/Fading):** Background elements are rendered less frequently (e.g., skipping frames for `background` which has `render_skip: 1`) using the `render_skip` property in `DEPTH_LEVELS`.
*   **`column_states` Modification:** Each column state now includes `depth_type`, `speed_threshold` (derived from depth), and `render_counter`.
*   **Main Loop Update:**
    *   Columns are assigned a random depth on initialization/reset.
    *   Speed updates and rendering logic now factor in the column's depth.
*   **Glyph Size:** For this iteration, the project stuck with the existing 4x8 glyphs and simulated depth primarily through speed and rendering frequency.

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

*   **Milestone 2: Enhanced Visuals & Customization**
    *   **Glyph Variation:**
        *   Option 1: Introduce a second, smaller glyph set (e.g., 2x4 or 3x6) for background elements to create a more pronounced depth effect. This would require updating `draw_glyph_pixels` or adding a new drawing function.
        *   Option 2: Allow the "head" glyph of a column to be visually distinct (e.g., brighter, or a specific "leader" glyph).
    *   **"Color" Themes (Simulated):**
        *   Explore an "inverse" mode (white background, black glyphs).
    *   **Trail Effects:**
        *   Fading trail: Glyphs in a trail could become progressively "dimmer" (rendered even less frequently).
        *   Dynamic trail length based on depth or other factors.

*   **Milestone 3: User Interaction & Controls**
    *   **Button Controls:**
        *   Allow users to pause/resume the animation.
        *   Control overall speed.
        *   Cycle through different visual themes or glyph sets (if implemented).

*   **Milestone 4: Performance & Refinement**
    *   **Code Cleanup:** General refactoring for clarity and maintainability.
    *   **Further Optimization:** Profile and identify any remaining performance bottlenecks.

These milestones are suggestions and can be prioritized or modified as the project evolves.