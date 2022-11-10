# Projective Distortion Removal Tool



## Usage
#### 1. Open the perspective correction tool with:

``` bash
python3 perspectiveCorrection.py
```
###### Note: You must be using a container environmnet (such as conda or venv).

#### 2. A new window will open. Click `Choose Image`, and select the image that you want to undistort.

  <!--image-->

###### Tip: For best results, choose an image that has minimal projective distortion.

#### 3. After selecting your image, a new window will open asking you to select four points on the selected image. The selected points should correspond to the corners of the distorted rectangular plane that you want to correct.

  <!--image-->

###### Note: Select points in a counterclockwise order, beginning on the upper left corner of the rectangular plane.

###### Tip: For best results, choose points that are far apart.

#### 4. Return to the window where you clicked `Choose Image`. You should now see your selected image with the selected rectangular plane highlighted. 

  <!--image-->

#### 5. Select `Undistort (Full Image)` if you want to undistort the whole image. Otherwise, select `Undistort (Crop to Selection)`, if you only want to undistort the highlighted portion.

#### 6. After clicking any of the `Undistort` buttons, the undistorted image will be shown on the right of the original image.

  <!--image full-->
  <!--image cropped-->

###### Note: You might have to resize the window to see the undistorted image.

#### 7. To save the undistorted image, click `Save` or `Save As`.

###### Note: The `Save` button saves the undistorted image as `undistorted.jpg`; its location is the directory containing `perspectiveCorrection.py`.

###### Note: The default file extension for `Save As` is `.jpg`

## References

[1] [Perspective Transformation](https://theailearner.com/2020/11/06/perspective-transformation/)

[2] [Perspective correction in OpenCV using python](https://stackoverflow.com/questions/22656698/perspective-correction-in-opencv-using-python)

[3] [OpenCV Python: How to warpPerspective a large image based on transform inferred from small region](https://stackoverflow.com/questions/64825835/opencv-python-how-to-warpperspective-a-large-image-based-on-transform-inferred)

[4] [Computing Homography | Image Stitching](https://youtu.be/l_qjO4cM74o)

