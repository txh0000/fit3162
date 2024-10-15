import cv2
import os

# Function to extract frames
def FrameCapture(path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Path to video file
    vidObj = cv2.VideoCapture(path)

    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = True

    while success:
        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()

        if success:
            # Saves the frames with frame-count in the output folder
            cv2.imwrite(os.path.join(output_folder, f"frame{count:04d}.jpg"), image)
            count += 1

    print(f"Extracted {count} frames to {output_folder}")

# Driver Code
if __name__ == '__main__':
    # Specify the input video path and output folder
    video_path = "/content/video-retalking/examples/face/1.mp4"
    output_folder = "extracted_frames"

    # Calling the function
    FrameCapture(video_path, output_folder)
