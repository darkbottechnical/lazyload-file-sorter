# Lazyload File Sorter
## Contents
[Description](#Description)
## Description
Your downloads can be put in one place now! (Hopefully)

## Features
- Automatically sorts images, audio, video, and more
- Customizable rules and overrides (e.g., music vs. SFX)
- Image format conversion (AVIF, WebP to PNG)
- Audio classification by metadata and duration
- Logging to file and error popups for issues
- Extendable

## Installation

```bash
git clone https://github.com/darkbottechnical/lazyload-file-sorter
cd lazyload-file-sorter
pip install -r requirements.txt
```

## Updating

```bash
cd lazyload-file-sorter
git pull
pip install -r requirements.txt
```

## Configuration

1. Edit `config.json` to set your root, sort, and destination folders.
   - **root**: The absolute path to the folder where all destination folders (like images, audio, etc.) will be created or found.
   - **sort**: The absolute path to the folder where you will dump files to be sorted. UniSort will move files from here.
2. Customize `root_locations` to define the subfolders for each file type. These are relative to `root`.
   - Example: If `root` is `C:/Users/yourname/` and `images` is `Pictures`, images will be moved to `C:/Users/yourname/Pictures`.
   - Supported keys: `images`, `audio`, `video`, `else` (for uncategorized files).
3. Customize `filetype_matching` to control which file extensions go into which categories. This is now fully configurable in your `config.json`.
   - Example: Add or remove extensions from any category as needed.
   - You can add new categories and reference them in `root_locations`.
4. Customize `overrides` to add special rules for certain file types or custom logic.
   - Example: `ismusic` and `issfx` can be used to further sort audio files into subfolders like `Audio/Music` and `Audio/SFX`.
   - You can add more overrides for custom behaviors (see code for details).

Example `config.json`:
```json
{
    "root": "C:/Users/yourname/",
    "sort": "C:/Users/yourname/ToSort",
    "root_locations": {
        "images": "Pictures",
        "audio": "Audio",
        "video": "Videos",
        "else": "Misc"
    },
    "filetype_matching": {
        "images": ["png", "jpg", "jpeg", "webp", "avif", "gif", "bmp", "tiff", "svg", "heic"],
        "audio": ["mp3", "m4a", "wav", "ogg", "flac", "aac", "wma", "aiff"],
        "video": ["mov", "mp4", "webm", "mkv", "avi", "flv", "wmv"],
        "documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "odt", "csv", "rtf"],
        "archives": ["zip", "rar", "7z", "tar", "gz", "xz", "bz2", "iso"],
        "executables": ["exe", "msi", "bat", "sh", "py", "jar", "apk", "app", "deb", "rpm"],
        "code": ["html", "css", "js", "ts", "py", "java", "cpp", "c", "cs", "php", "go", "rs", "swift", "kt", "lua"],
        "ebooks": ["epub", "mobi", "azw", "azw3", "cbz", "cbr"],
        "fonts": ["ttf", "otf", "woff", "woff2"],
        "design": ["psd", "ai", "xd", "sketch", "fig"],
        "system": ["dll", "sys", "ini", "log"],
        "installer_packages": ["dmg", "pkg", "appx", "xapk"]
    },
    "overrides": {
        "ismusic": "path:Audio/Music",
        "issfx": "path:Audio/SFX",
        "isdisposable": "path:images/disposable"
    }
}
```

**Notes:**
- All paths must use forward slashes `/` or double backslashes `\\` on Windows.
- You can add more keys to `overrides` for custom sorting logic if you extend the code.
- If a file type is not matched, it will go to the `else` folder.
- The program will create destination folders if they do not exist.

## Usage

```bash
python main.py
```

- The program will run in the background and sort files from your sort folder.
- Logs are saved in the `logs/` directory.
- Errors will also show a popup alert.

## Running on Startup (Windows)
- [Optional] Compile to an executable with PyInstaller for easier startup.
- Add a shortcut to the executable or `main.py` in the Windows Startup folder (`Win + R`, then `shell:startup`).

## License
[MIT](LICENSE)
