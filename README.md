# dicom_tools
My dicom tools that I created to work with dicom images.

## pixel_edit.py (overwrite mislabeled x-ray)
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
Program makes copy of original dicom file and overwrite specified area of pixels with new mark or text and save new dicom file to current working directory. Program logs its activity to a file pixel_edit.log that is created in the directory from which the program was started. The marker font size is automatically adjusted to the width of the selected area according to the coordinates.

### todo
this program suits my purposes but could be improved:
- customizable font size
- customizable colors
- custimizable SOPInstanceUID

    


