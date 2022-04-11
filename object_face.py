import numpy as np
import tensorflow as tf
import sys
from PIL import Image
import cv2
cap = cv2.VideoCapture(0)

from utils import label_map_util
from utils import visualization_utils as vis_util


# ------------------ Face Model Initialization ------------------------------ #
face_label_map = label_map_util.load_labelmap('training_face/labelmap.pbtxt')
face_categories = label_map_util.convert_label_map_to_categories(
    face_label_map, max_num_classes=2, use_display_name=True)
face_category_index = label_map_util.create_category_index(face_categories)

face_detection_graph = tf.Graph()

with face_detection_graph.as_default():
    face_od_graph_def = tf.GraphDef()
    with tf.gfile.GFile('inference_graph_face_ssd_2/frozen_inference_graph.pb', 'rb') as fid:
        face_serialized_graph = fid.read()
        face_od_graph_def.ParseFromString(face_serialized_graph)
        tf.import_graph_def(face_od_graph_def, name='')

    face_session = tf.Session(graph=face_detection_graph)

face_image_tensor = face_detection_graph.get_tensor_by_name('image_tensor:0')
face_detection_boxes = face_detection_graph.get_tensor_by_name('detection_boxes:0')
face_detection_scores = face_detection_graph.get_tensor_by_name('detection_scores:0')
face_detection_classes = face_detection_graph.get_tensor_by_name('detection_classes:0')
face_num_detections = face_detection_graph.get_tensor_by_name('num_detections:0')
# ---------------------------------------------------------------------------- #



def face(image_np):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    (boxes, scores, classes, num) = face_session.run(
    [face_detection_boxes, face_detection_scores,
        face_detection_classes, face_num_detections],
        feed_dict={face_image_tensor: image_np_expanded})
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        face_category_index,
        use_normalized_coordinates=True,
        line_thickness= 8,
        min_score_thresh=0.70)
    # Get coordinates of detected boxes ; ymin, ymax, xmin, xmax
    coordinates_face = vis_util.return_coordinates(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        face_category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.70)

    print("face: ", *coordinates_face)



if __name__ == '__main__':
    print(' in main')
