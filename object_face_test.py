import object_face
import cv2
cap = cv2.VideoCapture(0)

# This is needed since the notebook is stored in the object_detection folder.
#sys.path.append("..")

while True:
    ret, image_np = cap.read()
    object_face.face(image_np)
    print("------------------------------------------")
    cv2.imshow('object detection', cv2.resize(image_np, (800,600)))
  
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
