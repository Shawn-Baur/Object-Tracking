import cv2, math
from object_detection import ObjectDetection

def main(video, mspf):
    cap = cv2.VideoCapture(video)
    od = ObjectDetection()
    
    count = 0
    center_prev_frame = []
    tracking_objects = {}
    track_id = 0
    
    while(1):
        ok, frame = cap.read()
    
    # Set up logistical things
        # Creates break if there is video error
        if not ok:
            break
        # Resizing
        frame = cv2.resize(frame, (0,0), fx=.5, fy=.5)
        # Copy frame
        copy = frame
        # Starts counter and initialize center array
        count += 1
        center_cur_frame = []
        # End if video isn't valid
        if not ok:
            break
        
    # Detect object in frame
        (class_ids, score, boxes) = od.detect(frame)
        for box in boxes:
            (x, y, w, h) = box
            cx = int((x + x + w)/2)
            cy = int((y + y + h)/2)
            center_cur_frame.append((cx, cy))
            # print('FRAME N°', count, ' ', x, y, w, h)
            
            # cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        
        if count <= 2:
            for pt in center_cur_frame:
                for pt2 in center_prev_frame:
                    distance = math.hypot(pt2[0]-pt[0], pt2[1]-pt[1])

                    if distance < 50:
                        tracking_objects[track_id] = pt
                        track_id += 1
        else:
            tracking_objects_cpy = tracking_objects.copy()
            center_cur_frame_cpy = center_cur_frame.copy()
            
            for object_id, pt2 in tracking_objects_cpy.items():
                object_exit = False
                
                for pt in center_cur_frame_cpy:
                    distance = math.hypot(pt2[0]-pt[0], pt2[1]-pt[1])

                    if distance < 50:
                        tracking_objects[object_id] = pt
                        object_exit = True
                        if pt in center_cur_frame:
                            center_cur_frame.remove(pt)
                        continue
                
                if not object_exit:
                    tracking_objects.pop(object_id)
        
            for pt in center_cur_frame:
                tracking_objects[track_id] = pt
                track_id += 1
            
        for object_id, pt in tracking_objects.items():
            cv2.circle(frame, pt, 5, (0,0,255), -1)
            cv2.putText(frame, str(object_id), (pt[0], pt[1]-7), 0, 1, (0,0,255), 2)
        
        # Display the video
        cv2.imshow('Video', frame)
        
        center_prev_frame = center_cur_frame.copy()
        
    # Exit code
        key = cv2.waitKey(mspf)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# main(0,1)
main('video.mp4', 1)