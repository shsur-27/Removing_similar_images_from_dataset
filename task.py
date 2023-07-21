import cv2
import imutils
#import shutil
import os
from imaging_interview import preprocess_image_change_detection
from imaging_interview import compare_frames_change_detection

def delete_similar(dataset_path, min_contour_area=100, score_threshold=10000):
    # Read all images in directory
    image_files = [files for files in os.listdir(dataset_path) if os.path.isfile(os.path.join(dataset_path, files))]
    images = [cv2.imread(os.path.join(dataset_path, files)) for files in image_files]

    images_preprocessed = [preprocess_image_change_detection(img) for img in images if img is not None]
    #images_preprocessed = cv2.resize(images_preprocessed, (640, 480))
    for i in range(len(images_preprocessed)):
        for j in range(i + 1, len(images_preprocessed)):
            try:
            # Calculation of score for previous frame and current frame using compare_frames_change_detection function
                score, _, _ = compare_frames_change_detection(images_preprocessed[i], images_preprocessed[j],
                                                              min_contour_area)

                if score < score_threshold:
                    #destination = r'/path where deleted files saved '
                    #destination_path = os.path.join(destination, image_files[j]) 
                    #shutil.move(os.path.join(dataset_path, image_files[j]), destination_path)
                    os.remove(os.path.join(dataset_path, image_files[j]))
                    print(f'Removed {image_files[j]}')
                 
                    images_preprocessed[j] = None
            except:
                
                continue

    print('Finished removing similar images.')


if __name__ == '__main__':
    # Call the function with the path to your directory
    delete_similar('dataset-candidates-ml\dataset')