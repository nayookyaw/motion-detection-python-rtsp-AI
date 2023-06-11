"""
    Author
    Nay Oo Kyaw
    nayookyaw.nok@gmail.com
"""

import cv2
import threading

rtsp_url = "rtsp://192.168.xx.xx/stream1"  # Replace with your RTSP URL

def detectMotion():
    # Replace 'your_rtsp_url' with the actual RTSP stream URL
    cap = cv2.VideoCapture(rtsp_url)

    # Parameters for motion detection
    threshold_value = 80 # adjust based on your requirement
    min_area = 500 # adjust based on your requirement

    # Initialize previous frame
    ret, prev_frame = cap.read()
    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_frame = cv2.GaussianBlur(prev_frame, (21, 21), 0)

    while True:
        # Read current frame
        ret, frame = cap.read()

        # Convert to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        # Calculate frame difference
        frame_diff = cv2.absdiff(prev_frame, gray_frame)
        _, thresh_frame = cv2.threshold(frame_diff, threshold_value, 255, cv2.THRESH_BINARY)
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) > min_area:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion_detected = True
                print ((x, y, w, h))

                # x = threading.Thread(target=takePicture, args=())
                # x.start()

        if motion_detected:
            # do action whatever you want babe
            # (e.g take recording video, take capture images, etc...)

            cv2.putText(frame, "Motion Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display frame
        cv2.imshow("Motion Detection", frame)

        # Update previous frame
        prev_frame = gray_frame.copy()

        # Exit on key press (optional)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close windows
    cap.release()
    cv2.destroyAllWindows()

detectMotion()