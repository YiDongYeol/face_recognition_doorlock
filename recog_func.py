import face_recognition
import cv2
import file_func as ff
import numpy as np

def known_face_encode(gpio):
    video_capture = cv2.VideoCapture(0)
    chance = 3
    cnt = 0
    face_locations = []
    face_locations_list = []
    face_frame_list = []
    face_encoding_list = None
    process_this_frame = True
    gpio.idle_off()

    while True:
        if chance<1:
            break
        gpio.cap_on()
        ret, frame = video_capture.read()

        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if len(face_locations)!=0:
                if face_encoding_list is None:
                    cnt+=1
                    face_frame_list.append(rgb_small_frame)
                    face_locations_list.append(face_locations)
                else :
                    gpio.cap_off()
                    gpio.enc_on()
                    face_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]
                    matches = face_recognition.compare_faces(face_encoding_list, face_encoding, 0.35)
                    gpio.enc_off()
                    tcnt = matches.count(True)
                    if tcnt == 30:
                        ff.save_encode_file(face_encoding_list)
                        break
                    else :
                        video_capture.release()
                        gpio.fail()
                        chance-=1
                        video_capture=cv2.VideoCapture(0)
            if cnt >= 30:
                for i in range(0,30):
                    video_capture.release()
                    gpio.cap_off()
                    gpio.enc_on()
                    face_encoding = face_recognition.face_encodings(face_frame_list[i], face_locations_list[i])[0]
                    if face_encoding_list is None:
                        face_encoding_list = np.array([face_encoding])
                    else:
                        face_encoding_list = np.append(face_encoding_list, np.array([face_encoding]), axis = 0)
                    cnt = 0
                    gpio.enc_off()
                    video_capture=cv2.VideoCapture(0)
        process_this_frame = not process_this_frame

    video_capture.release()
    gpio.idle_on()

def face_recog(gpio):
    video_capture = cv2.VideoCapture(0)
    known_encoding_list = ff.load_encode_file();
    face_locations = []
    process_this_frame = True
    is_match = False
    chance = 3

    gpio.idle_off()

    while True:
        if chance<1:
            break

        gpio.cap_on()
        ret, frame = video_capture.read()
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if len(face_locations)!=0:
                gpio.cap_off()
                gpio.enc_on()
                face_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]

                for known_encodings in known_encoding_list:
                    matches = face_recognition.compare_faces(known_encodings, face_encoding, 0.35)
                    tcnt = matches.count(True)
                    if tcnt >= 27 :
                        is_match = True
                        break

                gpio.enc_off()

                if is_match:
                    gpio.serv_unlock()
                    break
                else :
                    video_capture.release()
                    gpio.fail()
                    chance-=1
                    video_capture=cv2.VideoCapture(0)
        process_this_frame = not process_this_frame

    video_capture.release()
    gpio.idle_on()
