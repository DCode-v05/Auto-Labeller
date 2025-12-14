import cv2
import os

def video_to_frames(video_path, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save each frame as image
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:05d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    print(f"✅ Extracted {frame_count} frames to '{output_folder}'")

if __name__ == "__main__":
    video_path = "C:\\Users\\NBC123\\Videos\\Dataset.mp4"      # path to your .mp4 video
    output_folder = "C:\\Users\\NBC123\\Videos\\Dataset"     # folder to save images
    video_to_frames(video_path, output_folder)
