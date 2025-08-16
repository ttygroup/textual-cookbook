# Textual Cookbook Changelog

## [0.5.0] 2025-08-16

- Added new CLI launcher. It is now possible to enter recipes as an argument when launchin the cookbook, like so:

  ```bash
  uvx textual-cookbook spinner_widget
  ```

The above line will immediately select the spinner_widget recipe and display it in the code viewer. Furthermore you can also provide the -r or --run flag to immediately run the recipe:

  ```bash
  uvx textual-cookbook spinner_widget -r
  ```

The `just cook` command in the justfile was also modified to reflect this change, so you can now do:

  ```bash
  just cook spinner_widget -r
  ```

## [0.4.0] 2025-08-16

- Added 2 new recipes by NSPC911 (#15 by @NSPC911):
  - Modifying Widgets: decline_failed_input.py
  - Modifying Widgets: better_optionlist.py

- Added 1 new recipe by David Fokkema (#16 by @davidfokkema):
  - Architecture Patterns: use_default_screen.py

## [0.3.0] 2025-08-16

- Added 4 new recipes by NSPC911:
  - Animation Effects: shaking.py
  - Architecture patterns: screen_push_wait.py
  - Modifying Widgets: progress_colors.py
  - Textual API usage: workers_exclusive.py
- Changed unicode characters in the recipe runner to normal emojis for better compatibility

## [0.2.0] 2025-08-15

- Added context menu recipe in Animations section

## [0.1.0] 2025-08-09

- First release of Textual-Cookbook on PyPI
