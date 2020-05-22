import cv2
vidcap = cv2.VideoCapture('path to video with name.mp4')
"""
videos/XYZ.mp4
Here XYZ is the name of the person
"""
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("path to images folder with name/frame%d.jpg" % count, image)     # save frame as JPEG file      
  """
  images/XYZ/frame%d
  """
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1