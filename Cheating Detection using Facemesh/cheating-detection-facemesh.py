import numpy as np
import cv2
import mediapipe as mp
import time
import warnings
warnings.filterwarnings('ignore')


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=5,  # atur seberapa wajah yang ingin dideteksi
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    start = time.time()

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_mesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, img_c = image.shape

    if results.multi_face_landmarks:
        for face_id, face_landmarks in enumerate(results.multi_face_landmarks):
            face_2d = []
            face_3d = []
            x_min, y_min = img_w, img_h
            x_max, y_max = 0, 0

            for idx, lm in enumerate(face_landmarks.landmark):
                x, y = int(lm.x * img_w), int(lm.y * img_h)

                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)

                if idx in [33, 263, 1, 61, 291, 199]:
                    if idx == 1:
                        nose_2d = (x, y)
                        nose_3d = (x, y, lm.z * 3000)

                    face_2d.append([x, y])
                    face_3d.append([x, y, lm.z])

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            focal_length = 1 * img_w
            cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                   [0, focal_length, img_w / 2],
                                   [0, 0, 1]])
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
            rmat, _ = cv2.Rodrigues(rot_vec)
            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

            x_rot = angles[0] * 360
            y_rot = angles[1] * 360
            z_rot = angles[2] * 360

            if y_rot < -10:
                direction = "Looking Left"
                cheating = True
            elif y_rot > 10:
                direction = "Looking Right"
                cheating = True
            else:
                direction = "Forward"
                cheating = False

            # Proyeksi arah kepala
            nose_end, _ = cv2.projectPoints(np.array([nose_3d]), rot_vec, trans_vec, cam_matrix, dist_matrix)
            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(p1[0] + y_rot * 10), int(p1[1] - x_rot * 10))
            cv2.line(image, p1, p2, (255, 0, 0), 3)

            # Bounding box
            cv2.rectangle(image, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), (255, 255, 0), 2)

            # Label wajah
            label = f"Face {face_id + 1}: {direction}"
            status = "Cheating Detected!" if cheating else "Not Cheating"

            label_color = (0, 0, 255) if cheating else (0, 255, 0)
            cv2.putText(image, label, (x_min, y_min - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, status, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, label_color, 2)

            # Gambar landmark
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )

    end = time.time()
    elapsed = end - start
    fps = 1 / elapsed if elapsed > 0 else 0
    cv2.putText(image, f'FPS: {int(fps)}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow('Exam Monitoring - Cheating Detection', image)
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        print("Program ditutup oleh pengguna.")
        break

cap.release()
cv2.destroyAllWindows()
