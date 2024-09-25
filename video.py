#installations for pip libraries in terminal for code
#python3 -m pip install opencv-python
#python3 -m pip install numpy
#python3 -m pip install opencv-contrib-python

import cv2
import time
import numpy as np

# URL for the video stream over the Cat 5 cable (e.g., IP camera or video server)
video_url = 'http://<camera_ip>:<port>/video'  # Replace with your actual video stream URL

# Initialize video capture
cap = cv2.VideoCapture(video_url)

# Check if the video capture opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Define a list to store the captured images
captured_images = []

# Set the number of images to capture
total_images = 50
capture_interval = 5  # Capture every 5 seconds

# Capture images
for i in range(total_images):
    ret, frame = cap.read()  # Read a frame from the video stream
    if not ret:
        print(f"Error: Failed to read frame {i}.")
        break

    # Store the frame
    captured_images.append(frame)
    print(f"Captured image {i + 1}/{total_images}")

    # Wait for 5 seconds before capturing the next image
    time.sleep(capture_interval)

# Release the video capture object
cap.release()

# Stitch the captured images in order
print("Stitching images together...")

# Convert images to grayscale for stitching (you can also use color)
gray_images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in captured_images]

# Create an instance of the stitcher
stitcher = cv2.Stitcher_create()

# Try to stitch the images
status, stitched_image = stitcher.stitch(gray_images)

# Check if the stitching was successful
if status == cv2.Stitcher_OK:
    print("Image stitching successful.")
    
    # Display the stitched image
    cv2.imshow('Stitched Image', stitched_image)
    cv2.waitKey(0)  # Press any key to close the window
    
    # Save the stitched image to a file
    cv2.imwrite('stitched_image.jpg', stitched_image)
    print("Stitched image saved as 'stitched_image.jpg'.")
else:
    print("Error: Image stitching failed.")

# Close any OpenCV windows
cv2.destroyAllWindows()
