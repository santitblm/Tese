import numpy as np
import cv2

#def apply_homography(image, src_points, dst_points):
#    # Convert points to numpy arrays
#    src_pts = np.array(src_points, dtype=np.float32)
#    dst_pts = np.array(dst_points, dtype=np.float32)
#
#    # Calculate homography matrix
#    H, _ = cv2.findHomography(src_pts, dst_pts)
#
#    # Apply the homography to the image
#    height, width = image.shape[:2]
#    warped_image = cv2.warpPerspective(image, H, (width, height))
#
#    return warped_image

def apply_homography(image, src_points, dst_points, ref_image_size):
    # Convert points to numpy arrays
    src_pts = np.array(src_points, dtype=np.float32)
    dst_pts = np.array(dst_points, dtype=np.float32)

    # Calculate homography matrix
    H, _ = cv2.findHomography(src_pts, dst_pts)

    # Apply the homography to the image
    warped_image = cv2.warpPerspective(image, H, (ref_image_size[1], ref_image_size[0]))

    return warped_image

ref_points = []
second_image_points = []

def mouse_callback(event, x, y, flags, param):
    global ref_points, second_image_points

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(ref_points) < 4:
            ref_points.append((x, y))
            cv2.circle(ref_image, (x, y), 2, (0, 0, 255), -1)
            cv2.imshow('Reference Image', ref_image)

        elif len(second_image_points) < 4:
            second_image_points.append((x, y))
            cv2.circle(second_image, (x, y), 2, (0, 0, 255), -1)
            cv2.imshow('Second Image', second_image)

        if len(ref_points) == 4 and len(second_image_points) == 4:
            # Apply homography
            print(ref_image.shape[:2])
            warped_image = apply_homography(second_image, second_image_points, ref_points, ref_image.shape[:2])
            cv2.imshow('Warped Image', warped_image)
            
        elif len(ref_points) == 4 and len(second_image_points) == 0:
            cv2.destroyWindow('Reference Image')
            cv2.imshow('Second Image', second_image)


# Load the reference image
ref_image = cv2.imread('C:/Users/Santi LM/Downloads/For homography/PL30MR.png')

# Create a copy of the reference image for visualization
ref_image_vis = ref_image.copy()

# Load the second image
second_image = cv2.imread('C:/Users/Santi LM/Downloads/For homography/Z.jfif')

# Create a copy of the second image for visualization
second_image_vis = second_image.copy()

# Create windows to display the images
cv2.namedWindow('Reference Image')
cv2.namedWindow('Second Image')
#cv2.namedWindow('Warped Image')

# Set the mouse callback function
cv2.setMouseCallback('Reference Image', mouse_callback)
cv2.setMouseCallback('Second Image', mouse_callback)

# Display the reference image and wait for points selection
cv2.imshow('Reference Image', ref_image_vis)
cv2.waitKey(0)

# Display the second image and wait for points selection
cv2.imshow('Second Image', second_image_vis)
cv2.waitKey(0)

cv2.destroyAllWindows()
