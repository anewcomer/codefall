# Thumby Codefall

## Project Overview

Thumby Codefall is a visual demonstration project for the Thumby handheld console. It aims to recreate the iconic "digital rain" or "Matrix code" effect, showcasing dynamic animation and optimized rendering techniques on the Thumby's monochrome display.

## Core Features

*   **Digital Rain Animation:** Columns of pseudo-random glyphs continuously fall down the screen.
*   **Custom Glyphs:** Utilizes a custom-defined set of 32 unique 4x8 pixel glyphs, designed to evoke a "digital" or "Katakana-like" aesthetic.
*   **Simulated Depth Effect:**
    *   **Multiple Layers:** Columns are assigned to foreground, midground, or background depth levels.
    *   **Variable Speed:** Glyphs in different depth layers fall at varying speeds (foreground fastest, background slowest).
    *   **Variable Rendering Frequency:** Background glyphs are rendered less frequently to simulate fading or being further away.
*   **Optimized Rendering:** Employs direct manipulation of the Thumby display buffer (`thumby.display.display.buffer`) for efficient pixel drawing, bypassing potentially less reliable `blit` operations.
*   **Dynamic Column Resets:** Columns reset with new random properties (glyphs, trail length, speed, depth) once they scroll off-screen.

## Target Platform

*   **Thumby Handheld Console:** Specifically designed for its screen dimensions (72x40 pixels) and performance characteristics.

## Current Status

*   The core animation and depth simulation features are implemented. The project is focused on refining visuals and exploring potential new features.