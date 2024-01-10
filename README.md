# dicom_tools
My dicom tools that I created to work with dicom images.

## pixel_edit.py
Occasionally I need to overwrite a radiographic mark on a mislabeled x-ray. Typically, when the image has already been deleted from the modality it was created on and I cannot correct the radiographic mark directly on the modality.

### requirements

python 3.9\n
library: pydicom (https://pydicom.github.io/)

### usage

start from file browser by doubleclick:
  console will ask you:
- path to input file [C:\dir\dicomfile]
- image area specified by coordinates (left top corner x1,y1 right bottom corner x2, y2) that will be overwritten [x1,y1,x2,y2]
- new mark or text (if you want empty text insert one space) ["new mark"]

    


