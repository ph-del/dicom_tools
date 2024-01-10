#This program was created to overwrite a radiographic mark in an X-ray image.
#The program allows you to insert your own text at the specified position into the dicom file.
#Program makes copy of original dicom file and overwrite specified area of pixels with new text mark and save new dicom file to current working directory. 
#pavel.honz@gmail.com
#10.1.2024

import argparse
import logging
import numpy as np
import os
import pydicom
from PIL import Image, ImageDraw, ImageFont
import sys

def arg_coords(s):
    #Function defines the type of the specified coordinate arguments in cmd.
    try:
        x1, y1, x2, y2 = map(int, s.split(','))
        return x1, y1, x2, y2
    except:
        raise argparse.ArgumentTypeError("Coordinates must be x1,y1,x2,y2")
    
def coordinates(cords):
    #Function to specify coordinates to be overwritten
    if not cords:
        print("Coordinates x1,y1 top left - x2,y2 bottom right")
        cords = input("Input coordinates x1,y1,x2,y2: ")
        try: 
            x1,y1,x2,y2 = map(int, cords.split(","))
            cords = x1,y1,x2,y2
        except: 
            end_of_program(f'Incorrectly inserted coordinates: "{cords}." Input correct coordinates x1,y1,x2,y2."', "error")
    log_info(f"Coordinates: {cords}")
    return cords

def draw2dcm(file, cord, text):
    #Function overwrites the coordinates of the specified area with new text and saves a new copy of the dicom file
    
    #load dicom file to ds
    ds = pydicom.dcmread(file)
    
    #get the pixel information into a numpy array
    dcmdata = ds.pixel_array

    #generate new SOPInstanceUID, if SOPInstanceUID not change, PACS do not accept edited dicom picture if original picture is still saved in pacs
    ds[0x08,0x18].value = pydicom.uid.generate_uid()

    #font setting
    width = cord[2] - cord[0]
    height = cord[3] - cord[1]
    textwidth = 1
    textheight = 1
    ImageFont.MAX_STRING_LENGTH = 64 # protect against potential DOS attacks
    
    #adapt font size to width of edited area
    while textwidth < width:
        font = ImageFont.truetype(font = "arial", size = textheight)
        textwidth = font.getlength(text)
        textheight +=1

    #create image with new text
    image =  Image.new("RGB", (width, height), color="black")
    draw = ImageDraw.Draw(image)
    
    #text to image
    draw.text((0, 0), text, font=font, fill="white")

    #image to numpy
    nptext = np.array(image)
    
    #insert image with new text to dicom image data
    for x in range(len(nptext[0])):
        for y in range(len(nptext)):
            if nptext[y][x][0] != 0 : 
                dcmdata[y+cord[1]][x+cord[0]] = nptext[y][x][0]*4000/255
            else: dcmdata[y+cord[1]][x+cord[0]] = 0000      

    #write pixel data to dicom
    ds.PixelData = dcmdata.tobytes()
    
    #path where copy of dicom will be saved
    newfile_path = os.getcwd() + f"//{ds[0x08,0x18].value}.dcm"
    
    #save new dicom file with overwritten pixels
    ds.save_as(newfile_path)
    log_info(f'New dicom file "{newfile_path}" was created')

def end_of_program(text = "", level=""):
    #Function to exit the program
    print(text)
    print("\nEnd of program.")
    if text !="" : 
        if level == "" : logging.info(text)
        if level == "error" : logging.error(text)
    logging.info("End of program.")
    pause()
    sys.exit()

def log_info(log):
    #Function to logging info to log file
    logging.info(log)

def log_error(log):
    #Function to logging error to log file
    logging.error(log)

def path_to_file(dicom_path):
    #Function to specify dicom file to edit
    if not dicom_path: 
        dicom_path = input("Input path to dicom file: ")
        if not os.path.isfile(dicom_path): 
            end_of_program(f'File "{dicom_path}" does not exist. Enter a valid file path. ', "error")
        
    log_info(f"Dicom file: {dicom_path}")
    return dicom_path


def pause():
    #Function to pause the program on exit to read information on the console
    programPause = input("Press the <ENTER> key to continue...")

def text_input(text):
    #Function to enter new text max. 64 chars
    if not text:
        text = input("Input text to insert into the dicom image: ")
    if text =="": end_of_program(f"No text inserted. Please enter corect text text.", "error")
    if len(text) > 64: end_of_program(f'text is too long. Max. allowed size is 64 chars. Inserted text "{text}" has "{len(text)}" chars.')
    log_info(f"New text is: {text}")
    return text

if __name__ == "__main__":
    ### Start logging
    logdir_path = os.getcwd()
    log_file = logdir_path + "\pixel_edit.log"
    logging.basicConfig(level=logging.INFO, filename=log_file, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("Start programu")

    ### Command line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--file", type=str, help="path to dicom file ")
    argParser.add_argument("-c", "--cord", type=arg_coords, help="coordinates x1,y1,x2,y2 (x1,y1 top left - x2,y2 bottom right)")
    argParser.add_argument("-t", "--text", type=str, help="text to insert into the dicom image")
    args = argParser.parse_args()
    
    ### Program running
    file = path_to_file(args.file)
    cord = coordinates(args.cord)
    text = text_input(args.text)
    draw2dcm(file, cord, text)
    
    end_of_program()
