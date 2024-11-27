import pygetwindow as gw

# Get all windows
windows = gw.getAllTitles()

# Filter and print window names containing " Table "
for window_name in windows:
    if " Table " in window_name:
        print(window_name)
