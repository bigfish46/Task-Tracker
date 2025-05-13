# AFISH Task Tracker

A modern, Windows 11-styled task tracking application built with Python and Tkinter.

## Features

- Clean, modern Windows 11-inspired interface
- Dark theme with high contrast
- Add tasks with due dates
- Mark tasks as complete
- Remove tasks
- Automatic sorting by due date
- Data persistence using JSON storage
- Desktop installer available

## Installation

### From Source
1. Clone the repository:
```bash
git clone https://github.com/bigfish46/Task_Tracker.git
cd Task_Tracker
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python task_tracker_gui.py
```

### Using Installer
1. Download the latest installer from the [releases page](https://github.com/bigfish46/Task_Tracker/releases)
2. Run the installer
3. Launch from Start Menu or Desktop shortcut

## Development

### Project Structure
- `task_tracker_gui.py`: Main GUI application
- `task_tracker_oop.py`: Core task management logic
- `requirements.txt`: Python dependencies
- `installer.iss`: Inno Setup installer script

### Building
To build the executable:
```bash
pyinstaller afish_task_tracker.spec
```

To create the installer:
1. Install Inno Setup
2. Run:
```bash
iscc installer.iss
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details. 