from modules.parse import parse_config, Conf
from mutagen import File as MutagenFile
from modules.file import File
from PIL import Image

import imageio.v3 as iio
import os
import logging
import pymsgbox

CONFIG: Conf = parse_config()

# Setup logging
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.abspath(os.path.join(log_dir, 'match.log'))
logging.basicConfig(
    filename=log_path,
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MatchChecker:
    def __init__(self, call: callable, accept: tuple):
        self.accept = accept
        self.call = call
    def check(self, file):
        if file.ext in self.accept:
            return self.call(file)
match_checkers = []

def match_checker(*accept):
    def decorator(func):
        match_checkers.append(MatchChecker(call=func, accept=accept))
        return func
    return decorator

@match_checker("mp3", "m4a", "wav", "ogg")
def audio_length(media):
    try:
        audio = MutagenFile(media.path, easy=True)
        if audio is None:
            logger.error(f"{media.name} is not a valid audio file.")
            pymsgbox.alert(f"{media.name} is not a valid audio file.", "Sorter Error")
            return None
        duration = getattr(audio.info, 'length', 0)
        tags = {k.lower(): str(v).lower() for k, v in (audio.tags or {}).items()}
        filename = getattr(media, 'name', getattr(media, 'path', '')).lower()
        sfx_keywords = ["sfx", "effect", "sound"]
        has_sfx_in_name = any(keyword in filename for keyword in sfx_keywords)
        has_sfx_in_tags = any(keyword in v for keyword in sfx_keywords for v in tags.values())
        music_fields = ["title", "artist", "album"]
        has_music_metadata = any(tags.get(field) not in (None, '', 'none') for field in music_fields)
        has_music_in_tags = any('music' in v for v in tags.values())
        if has_sfx_in_name or has_sfx_in_tags:
            flag = "issfx"
        elif duration < 60:
            flag = "issfx"
        elif has_music_metadata:
            flag = "ismusic"
        elif duration > 60 or has_music_in_tags:
            flag = "ismusic"
        else:
            flag = "issfx"
        set_path = CONFIG.overrides.get(flag).split(":")[1]
        path = os.path.abspath(os.path.join(CONFIG.ROOTDIR, set_path, filename))
        return path
    except Exception as e:
        logger.error(f"Error in audio_length for {media.name}: {e}")
        pymsgbox.alert(f"Error in audio_length for {media.name}: {e}", "Sorter Error")
        return None

@match_checker("avif", "webp")
def convert_img(media: File):
    filename: str = media.name
    namewithoutext = os.path.splitext(filename)[0]
    filepath: str = media.path
    filedir: str = os.path.dirname(filepath)
    if filename.startswith("$cv$"):
        try:
            if filename.lower().endswith(".avif"):
                img = iio.imread(os.path.abspath(filepath))
                new_filepath = os.path.abspath(os.path.join(filedir, namewithoutext.replace("$cv$", "")+".png"))
                iio.imwrite(new_filepath, img, plugin="pillow")
            else:
                image = Image.open(os.path.abspath(filepath))
                new_filepath = os.path.abspath(os.path.join(filedir, namewithoutext.replace("$cv$", "")+".png"))
                image.save(new_filepath, "png")
            os.remove(filepath)
        except Exception as e:
            logger.error(f"Invalid or unsupported image file: {e}. Skipping {filename}")
            pymsgbox.alert(f"Invalid or unsupported image file: {e}. Skipping {filename}", "Sorter Error")