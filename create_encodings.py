import face_recognition
import os
import subprocess
import pickle

"""
    -images
        -name1
            -frame1.jpg
            -frame2.jpg
            .
            .
        -name2
            -frame1.jpg
            -frame2.jpg
            .
            .
    -videos
        -name1.mp4
        -name2.mp4
    -encoding-names
        -stored_face_encodings
        -stored_face_names
        
    createEncoding class contains a get_encoded_faces function which browses
    through the "images" directory and its subdirectories, and creates the
    encodings for each face image present. As shown in the hierarchy it creates
    the encodings of the jpg file (for example: frame1,frame2,etc) and also takes its corresponding 
    directory name as the label (for example: name1).
"""
class createEncoding:
    def get_encoded_faces(en, na):
        """
            looks through the images folder and encodes all
            the faces of all the people
        """
        for subdir, dirs, files in os.walk("images//demo"):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".JPG"):
                    face = face_recognition.load_image_file(subdir + "/"+ file)
                    print(subdir + file)
                    
                    temp_encoding = face_recognition.face_encodings(face)
                    """
                        if for an image encodings are not found, then that image
                        will be removed from the directory
                    """
                    if not len(temp_encoding):
                        subprocess.call(["rm",subdir+"/"+file])
                    else:
                        encoding = temp_encoding[0]                          
                        en.append(encoding)
                        na.append(subdir.split("/")[-1])
                        print(subdir + file)
        return 0

if __name__ == "__main__":
    c = createEncoding()    
    face_encodings = [] # list to append the face encodings
    face_names = [] # list to append the face labels
    c.get_encoded_faces(face_encodings,face_names)

    """
        storing the created encodings and labels in a pickle file
    """
    with open('path to the encoding-names folder/stored_face_encodings','wb') as fp:
        pickle.dump(face_encodings, fp)
  
    with open('path to the encoding-names folder/stored_face_names','wb') as fp:
        pickle.dump(face_names, fp)