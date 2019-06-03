from styx_msgs.msg import TrafficLight

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        PATH_TO_MODEL = './fine_tuned_model/frozen_inference_graph.pb'
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            # Works up to here.
            with tf.gfile.GFile(PATH_TO_MODEL, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            self.d_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            self.d_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.d_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_d = self.detection_graph.get_tensor_by_name('num_detections:0')
        self.sess = tf.Session(graph=self.detection_graph)

    def get_classification(self, image):
         # Bounding Box Detection.
        with self.detection_graph.as_default():
            # Expand dimension since the model expects image to have shape [1, None, None, 3].
            img_expanded = np.expand_dims(img, axis=0)  
            (boxes, scores, classes, num) = self.sess.run(
                [self.d_boxes, self.d_scores, self.d_classes, self.num_d],
                feed_dict={self.image_tensor: img_expanded})
        red_light = 0
        green_light = 0
        yellow_light = 0
        red_score = 0
        green_score = 0
        yellow_score =0
        for i in range(0,int(num)):
        	class_id = int(classes[0,i])
        	score = scores[0,i]
        	if score > 0.3: 
        		if (class_id == 1):
        			green_light += 1
        			green_score += score
        		elif (class_id == 2):
        			yellow_light += 1
        			yellow_score += score
        		elif (class_id == 3):
        			red_light += 1
        			red_score += score

        max_score  = max(green_score,yellow_score,red_score)

        if max_score < 0.5:
        	return  TrafficLight.UNKNOWN
        else:
	        if (max_score == green_score):
	        	return TrafficLight.GREEN
	        elif (max_score == yellow_score):
	        	return TrafficLight.YELLOW
	        elif (max_score == red_score):
	        	return TrafficLight.RED


