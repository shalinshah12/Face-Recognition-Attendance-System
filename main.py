import face_recognition
import cv2
import numpy as np
import os
import datetime
from multiprocessing import Process
import pickle
import mysql.connector
# Load present date and time
now= datetime.datetime.now()
today=now.day
timestr = now.timestamp()
month=now.month
"""
configuring the database connection
"""
cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="concurrent"
)
"""
creating the table for inserting the entries.
"""
cursor = cnx.cursor()
cursor.execute("use concurrent")
cursor.execute("CREATE TABLE Attendance (Name VARCHAR(255), TimeStamp TIMESTAMP, Location VARCHAR(255))")


"""
    load the face encodings and labels created using create_encoding.py
"""
known_face_encodings = []
known_face_names = []
with open('path to the encoding-names folder/stored_face_encodings','rb') as fp:
  known_face_encodings = pickle.load(fp)
  
with open('path to the encoding-names folder/stored_face_names','rb') as fp:
  known_face_names = pickle.load(fp)

# Initialize some variables 
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

class FaceDetection:
    
    """
        constructor calls the multiple() function which handles the 
        face recognition task.
    """
    def __init__(self, ip):
        self.multiple(ip)
        
    """
        multiple() function takes ip address/link to the video footage as the 
        input parameter.
    """
    def multiple(ip):            
        
        video_capture=cv2.VideoCapture(ip)
        process_this_frame = True
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            type(ret)
            type(frame)
        
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
        
            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    
                    """
                        face_distance function of face_recognition library calculates the distance
                        (euclidean distance) between the detected face encodings and the encodings 
                        that we have stored (near to 0 for most similar, and near to 1 for least 
                        similar). Here we have used the threshold distance of 0.5, but you can play 
                        around with it and find what suits best for your application.                        
                    """                    
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    
                    temp=[]
                    for i in face_distances:
                        if i<0.5:
                            # if distance is less then 0.5 then append the distance value
                            temp.append(i)
                        else:
                            # else append 1. This will maintain the correspondance with the names and encodings
                            temp.append(1)
                                           
                    
                    best_match_index = np.argmin(temp)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        name1 = best_match_index + 1
                        now1=datetime.datetime.now()
                        if int(name1) in range(1,61):                    
                            cursor.execute("insert into Attendance(Name, TimeStamp, Location) values(%s,%s,%s)",(name,now1,ip[1]))
                            cnx.commit() 
                        else:
                            pass
        
                    face_names.append(name)
        
            process_this_frame = not process_this_frame
        
        
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
        
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
        
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
            # Display the resulting image
            cv2.imshow('Video', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
    
if __name__== "__main__":
    
    """
        give a list of ip's that we want to monitor.
        The links can be changed with respect to the installed cctv system.
    """    
    ip = { 'rtsp://admin:examplepass123!@192.168.1.100:554/Streaming/Channels/101/' : 'Main Office',
       'rtsp://admin:examplepass123!@192.168.1.100:554/Streaming/Channels/102/'  : 'Work Area',
       'rtsp://admin:examplepass123!@192.168.1.100:554/Streaming/Channels/103/'  : 'Classroom Back',
       'rtsp://admin:examplepass123!@192.168.1.100:554/Streaming/Channels/104/'  :  'Reception',
       'rtsp://admin:examplepass123!@192.168.1.100:554/Streaming/Channels/105/' : 'IN',
       'rtsp://admin:examplepass123!@192.168.1.100:554/Streaming/Channels/106/' : 'Conference Room',
       'rtsp://admin:examplepass123!@192.168.1.100:554/Streaming/Channels/107/' : 'OUT'}
    #ip=["http://192.168.43.139:8080/video","http://192.168.43.155:8080/video"]
        
    """
        creating separate processes for each ip for parallel monitoring
    """
    processes = []
    for i in ip:
        processes.append(Process(target = FaceDetection,args=(i,)))
            
    print(processes)
    for process in processes:
        print(type(process))
        process.start()
        print("started " + str(os.getpid()))
        
    
    for process in processes:
        process.join()
print(os.cpu_count())
        
