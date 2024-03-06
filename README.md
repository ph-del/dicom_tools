# dicom_tools
My dicom tools that I created to work with dicom images.

### content:
"""
##### 1. [pixel_edit](#pixel_edit)
Edit wrong labels in dicom picture
##### 2. [gif_from_jpg](#gif_from_jpg)
Create gif from jpg
"""

## pixel_edit.py (overwrite mislabeled x-ray)<a name="pixel_edit"></a>
Occasionally I need to overwrite a radiographic mark on a mislabeled x-ray. Typically, when the image has already been deleted from the modality it was created on and I cannot correct the radiographic mark directly on the modality.

### requirements
python 3.9 \
library: pydicom (https://pydicom.github.io/)

### usage
start from file browser by doubleclick:\
console will ask you:
- path to input file ["C:\dir\dicomfile" (str) ]
- image area specified by coordinates (left top  x1,y1 right bottom x2, y2) that will be overwritten [x1,y1,x2,y2 (int,int,int,int)]
- new mark or text (if you want empty text insert one space) ["new mark" (str)]

or you can start from cmd with arguments:
```
usage: pixel_edit.py [-h] [-f FILE] [-c CORD] [-t TEXT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  path to dicom file
  -c CORD, --cord CORD  coordinates x1,y1,x2,y2 (x1,y1 top left - x2,y2 bottom right)
  -t TEXT, --text TEXT  text to insert into the dicom image
```
Program makes copy of original dicom file and overwrite specified area of pixels with new mark or text and save new dicom file to current working directory.\
Program logs its activity to a file pixel_edit.log that is created in the directory which the program was started from.\
The marker font size is automatically adjusted to the width of the selected area according to the coordinates.

### todo
this program suits my purposes but could be improved:
- customizable font size
- customizable colors
- custimizable SOPInstanceUID

## gif_from_jpg<a name="gif_from_jpg"></a>
Program to create gif file from jpg files. Sometime I need create gif file from jpg files for powerpoint presentation. I usually used tool https://gifmaker.me/, but this tool is limited to 300 jpg files. So I created program, which allow me create gif from unlimited jpg files (in program is condition to max.2000 jpg, but it can be overwitten)  

### requirements
python 3.9 \
library: PIL

### usage
start from file browser by doubleclick:\
console will ask you:
- path to directory with jpg files ["C:\dir\jpg_files" (str) ]
- animation speed milliseconds per frame [x (int)]

or you can start from cmd with arguments:
```
usage: gif_from_jpg.py [-h] [-d DIR] [-s SPEED]

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIRECTORY  path to directory with jpg files
  -s SPEED, --speed SPEED  animation speed milliseconds per frame
```
Program create gif file with name first jpg file in directory. Jpg files names must be ordered alphabetically, but program recognize no alphabetical number format 1,10,100,2,3, which is generated from our system MARIA Pacs.



