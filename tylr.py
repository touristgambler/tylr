import sys
import json
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout, QSlider, QSpinBox
)
from PyQt5.QtCore import Qt
from screeninfo import get_monitors
import pygetwindow as gw
import keyboard


CONFIG_FILE = "tylr.json"


def load_config():
    """Load configuration from a file, or use defaults if the file doesn't exist."""
    default_config = {
        "aspect_ratio": 1.4,
        "regex": r" Table \d+",
        "height_adjustment": -50,
        "width_adjustment": 0,
        "keybinding": "F2",
    }
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default_config


def save_config(config):
    """Save configuration to a file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tylr")
        self.setGeometry(100, 100, 300, 200)

        # Load configuration
        self.config = load_config()
        self.aspect_ratio = self.config["aspect_ratio"]
        self.regex = self.config["regex"]
        self.height_adjustment = self.config["height_adjustment"]
        self.width_adjustment = self.config["width_adjustment"]
        self.keybinding = self.config["keybinding"]

        self.init_ui()

    def init_ui(self):
        """Initialize the GUI."""
        layout = QVBoxLayout()

        # Instructions
        instructions = QLabel("Press 'Apply Layout' or use the keybinding for automatic tiling.")
        layout.addWidget(instructions)

        # Aspect Ratio Input
        aspect_layout = QHBoxLayout()
        aspect_label = QLabel("Aspect Ratio:")
        aspect_slider = QSlider(Qt.Horizontal)
        aspect_slider.setMinimum(10)
        aspect_slider.setMaximum(30)
        aspect_slider.setValue(int(self.aspect_ratio * 10))
        aspect_value = QLineEdit(f"{self.aspect_ratio:.1f}")

        def update_aspect_ratio():
            self.aspect_ratio = aspect_slider.value() / 10
            aspect_value.setText(f"{self.aspect_ratio:.1f}")

        aspect_slider.valueChanged.connect(update_aspect_ratio)
        aspect_layout.addWidget(aspect_label)
        aspect_layout.addWidget(aspect_slider)
        aspect_layout.addWidget(aspect_value)
        layout.addLayout(aspect_layout)

        # Regex Input
        regex_layout = QHBoxLayout()
        regex_label = QLabel("Window Title Regex:")
        regex_input = QLineEdit(self.regex)
        regex_input.textChanged.connect(lambda: setattr(self, "regex", regex_input.text()))
        regex_layout.addWidget(regex_label)
        regex_layout.addWidget(regex_input)
        layout.addLayout(regex_layout)

        # Height Adjustment
        height_layout = QHBoxLayout()
        height_label = QLabel("Height Adjustment:")
        height_spinbox = QSpinBox()
        height_spinbox.setMinimum(-500)
        height_spinbox.setMaximum(500)
        height_spinbox.setValue(self.height_adjustment)
        height_spinbox.valueChanged.connect(lambda value: setattr(self, "height_adjustment", value))
        height_layout.addWidget(height_label)
        height_layout.addWidget(height_spinbox)
        layout.addLayout(height_layout)

        # Width Adjustment
        width_layout = QHBoxLayout()
        width_label = QLabel("Width Adjustment:")
        width_spinbox = QSpinBox()
        width_spinbox.setMinimum(-500)
        width_spinbox.setMaximum(500)
        width_spinbox.setValue(self.width_adjustment)
        width_spinbox.valueChanged.connect(lambda value: setattr(self, "width_adjustment", value))
        width_layout.addWidget(width_label)
        width_layout.addWidget(width_spinbox)
        layout.addLayout(width_layout)

        # Keybinding
        keybinding_layout = QHBoxLayout()
        keybinding_label = QLabel("Keybinding:")
        keybinding_input = QLineEdit(self.keybinding)
        keybinding_input.textChanged.connect(lambda: setattr(self, "keybinding", keybinding_input.text()))
        keybinding_layout.addWidget(keybinding_label)
        keybinding_layout.addWidget(keybinding_input)
        layout.addLayout(keybinding_layout)

        # Apply Button
        apply_button = QPushButton("Apply Layout")
        apply_button.clicked.connect(self.apply_layout)
        layout.addWidget(apply_button)

        # Save Button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Keybinding setup
        keyboard.add_hotkey(self.keybinding, self.apply_layout)

    def apply_layout(self):
        """Apply the dynamic layout."""
        screen_width, screen_height = get_main_screen_dimensions()
        tile_windows_dynamic(
            screen_width + self.width_adjustment,
            screen_height + self.height_adjustment,
            self.aspect_ratio,
            self.regex,
        )

    def save_settings(self):
        """Save the current settings to the configuration file."""
        self.config.update(
            {
                "aspect_ratio": self.aspect_ratio,
                "regex": self.regex,
                "height_adjustment": self.height_adjustment,
                "width_adjustment": self.width_adjustment,
                "keybinding": self.keybinding,
            }
        )
        save_config(self.config)
        keyboard.remove_all_hotkeys()
        keyboard.add_hotkey(self.keybinding, self.apply_layout)
        print("Settings saved!")


def get_main_screen_dimensions():
    """Fetch the width and height of the main screen."""
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor.width, monitor.height
    return get_monitors()[0].width, get_monitors()[0].height


def tile_windows_dynamic(screen_width, screen_height, aspect_ratio, regex):
    """Tiles windows dynamically based on the number of windows found."""
    found_windows = [
        win for win in gw.getWindowsWithTitle("") if win.visible and re.search(regex, win.title)
    ]
    window_count = len(found_windows)

    if window_count == 0:
        print("No matching windows found.")
        return

    layout, window_width, window_height, left_offset, top_offset = center_grid_layout(
        window_count, screen_width, screen_height, aspect_ratio
    )
    num_rows, num_columns = layout

    for i, window in enumerate(found_windows):
        if i >= num_rows * num_columns:
            print(f"Skipping extra window: {window.title}")
            break
        
        col = i % num_columns
        row = i // num_columns
        left = left_offset + col * window_width
        top = top_offset + row * window_height

        window.moveTo(left, top)
        window.resizeTo(window_width, window_height)


def center_grid_layout(window_count, screen_width, screen_height, aspect_ratio=1.4):
    """Determine grid layout and calculate centered positions based on the number of windows."""
    if window_count == 1:
        # Full height, centered horizontally
        layout = (1, 1)
    elif window_count == 2:
        # 1x2 grid centered on the screen
        layout = (1, 2)
    elif 3 <= window_count <= 4:
        # 2x2 grid centered on the screen
        layout = (2, 2)
    elif 5 <= window_count <= 6:
        # 2x3 grid centered on the screen
        layout = (2, 3)
    else:
        # 3x4 grid (handles 7 or more windows)
        layout = (3, 4)
    
    num_rows, num_columns = layout
    max_width = screen_width // num_columns
    max_height = screen_height // num_rows

    if max_width / aspect_ratio > max_height:
        window_height = max_height
        window_width = int(window_height * aspect_ratio)
    else:
        window_width = max_width
        window_height = int(window_width / aspect_ratio)

    total_grid_width = window_width * num_columns
    total_grid_height = window_height * num_rows
    left_offset = (screen_width - total_grid_width) // 2
    top_offset = (screen_height - total_grid_height) // 2

    return layout, window_width, window_height, left_offset, top_offset


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
