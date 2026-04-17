## Zenon Text Editor

## Overview

This project is a feature-rich desktop text editor built using PyQt5. It provides a modern interface for editing and formatting text, along with support for plugins, themes, and detailed file information.

The editor is designed to be extensible and customizable, making it suitable for both basic text editing and more advanced use cases.

---

## Features

### Core Editing

* Create, open, save, and save files as HTML or custom `.myhtml` format
* Undo and redo functionality
* Cut, copy, and paste support
* Automatic modification tracking with unsaved changes indicator

### Text Formatting

* Bold, italic, and underline styles
* Text alignment:

  * Left
  * Center
  * Right
  * Justified
* Font selection and font size customization
* Font color adjustment

### File Management

* File information viewer (size, content stats, metadata, etc.)
* Save confirmation dialog for unsaved changes

### Plugins

* Plugin system with dynamic loading from a `plugins` folder
* Plugin manager UI for enabling and managing plugins

### Themes

* Theme manager for applying different UI styles
* Theme browser dialog for selecting themes

### UI Features

* Toolbar with quick access to actions
* Non-movable and fixed toolbar layout
* Clean and structured PyQt5 interface

---

## Project Structure

```
.
├── main.py
├── UI/
│   └── Text_editor_ui.ui
├── plugins/
├── colordialog.py
├── FontDialog.py
├── FontSizeDialog.py
├── SaveDialog.py
├── PluginDialog.py
├── plugin_manager.py
├── ThemeManager.py
├── ThemeBrowser.py
├── fileinfo.py
```

---

## Requirements

* Python 3.x
* PyQt5

Install dependencies using:

```
pip install PyQt5
```

---

## How to Run

```
python main.py
```

---

## Usage

1. Launch the application.
2. Use the toolbar or menu options to:

   * Create or open a file
   * Edit and format text
   * Save your work
3. Access additional features:

   * Plugins via the Plugins menu
   * Themes via the Themes menu
   * File information via File Info

---

## File Formats

* `.html` – Standard HTML format
* `.myhtml` – Custom format used by the editor

---

## Extending the Editor

### Plugins

* Place plugin files inside the `plugins` directory
* They will be automatically loaded at startup

### Themes

* Themes are managed through the `ThemeManager`
* Use the Theme Browser to apply available themes

---

## Known Limitations

* Only HTML-based file formats are supported
* Help section is not yet implemented
* Some dialogs depend on external modules included in the project

---

## Future Improvements

* Add support for more file formats (e.g., plain text, markdown)
* Implement help/documentation inside the app
* Improve plugin API for better extensibility
* Add autosave functionality


## Be Aware

Please be aware that this project is still is in it's alpha stage and you might experience some bugs. Some features like find and replace and find are still in under development and will be back in future updates.

---

## License

This project is open-source. You may modify and distribute it as needed.

---

## Author

Developed by PixelPal. Developed as a PyQt5-based customizable text editor project.
