#Created by Pavel Honz 2024 for NPK a.s.
#Last update 5.3.2024

# Set logging
import logging
from logging import config
from datetime import datetime
import os
import glob
import argparse
from PIL import Image
import sys
import textwrap
import re

log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)

log_config = {
    "version":1,
    "root":{
        "handlers" : ["console", "file"],
        "level": "DEBUG"
    },
    "handlers":{
        "console":{
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        },
        "file":{
            "formatter":"standard",
            "class":"logging.FileHandler",
            "level":"INFO",
            "filename":f'logs/{datetime.now().strftime("%y%m")}' + ".log"
        }
    },
    "formatters":{
        "extended": {
            "format": "%(asctime)s - [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s",
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)-15s\t -  %(module)s\t| %(message)s",
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
}
config.dictConfig(log_config)

################ Logger #################
logger = logging.getLogger(__name__)
# module logs message, so importing it only after logging has been configured



def end_of_program(text = "", level=""):
    #Function to exit the program
    print(text)
    print("\nEnd of program.")
    if text !="" : 
        if level == "" : logger.info(text)
        if level == "error" : logger.error(text)
    logger.info("End of program.")
    pause()
    sys.exit()

def pause():
    #Function to pause the program on exit to read information on the console
    programPause = input("Press the <ENTER> key to continue...")
    
def path_to_dir(path):
    #Function to specify directory with jpg files to make animated gif
    if not path: 
        path = input("Input path to directory with jpg: ")
        if not os.path.isdir(path): 
            end_of_program(f'Directory "{path}" does not exist. Enter a valid file path. ', "error")       
    logger.info(f"Directory path is: {path}")
    return path

def frame_speed(ms):
    #Function to enter speed of animation gif if milliseconds per frame
    if not ms:
        ms = input("Input animation speed in milliseconds per frame (1-2000): ")
        ms = arg_speed(ms)
        print(ms, type(ms))
    logger.info(f"Animatione speed: {ms}")
    return ms

def arg_speed(ms):
    #Function define the type of the specified speed argument in cmd
    try: 
        x = int(ms)
    except:
        x = False

    if x and x > 0 and x <= 2000:
            return x
    else:
        raise argparse.ArgumentTypeError("Value must be int! Allowed values are in 1 - 2000") 

def sort_key(s):
    # Funkce pro získání klíče pro řazení
    # Rozdělí řetězec na části obsahující čísla a text
    # Vrátí tuple obsahující čísla jako celá čísla a zbytek řetězce
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', s)]

def make_gif(frame_folder, speed):
    #Function make gif file from jpg files in selected directory
    frames = [Image.open(image) for image in sorted(glob.glob(f"{frame_folder}*.JPG"), key=sort_key)]
    frame_one = frames[0]
    frame_one.save(f"{os.path.basename(frame_one.filename)[:-4]}.gif", format="GIF", append_images=frames,
               save_all=True, duration=speed, loop=0)
    logger.info(f"Gif {os.path.basename(frame_one.filename)[:-4]}.gif was maded from {len(frames)} images.")

if __name__ == "__main__":
    ### Start logging   
    logger.info("Start programu")
    #make_gif("/path/to/images")

    ### Command line arguments
    argParser = argparse.ArgumentParser(prog = "gif_from_jpg",
                                        epilog=textwrap.dedent('''\
                                            additional information:
                                                jpg files must be named in alphabetical order'''))
    argParser.add_argument("-d", "--dir", type=str, help="path to directory with jpg files")
    argParser.add_argument("-s", "--speed", type = arg_speed, help  = "animation speed milliseconds per frame")
    args = argParser.parse_args()

    ### Program running
    dir = path_to_dir(args.dir)
    speed = frame_speed(args.speed)
    make_gif(dir, speed)

    end_of_program