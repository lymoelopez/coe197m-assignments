# Projective Distortion Removal Tool

A simple python program used to remove the projective distortion on images. This repository serves as my submission for our first activity in **Foundations of Machine Learning** (CoE 197M).


## Usage
#### 1. Open the perspective correction tool with:

``` bash
python3 perspectiveCorrection.py
```
> Note: You must be using a container environmnet (such as conda or venv).

#### 2. A new window will open. Click `Choose Image`, and select the image that you want to undistort.

  <img src="https://user-images.githubusercontent.com/99809831/200984297-0ce58f2d-0610-47b7-b5f9-00ceeb9620ad.png" width="70%"/>

> Tip: For best results, choose an image that has minimal projective distortion.

#### 3. After selecting your image, a new window will open asking you to select four points on the selected image. The selected points should correspond to the corners of the distorted rectangular plane that you want to correct.

  <img src="https://user-images.githubusercontent.com/99809831/200985200-13af38df-179d-404a-84e1-5d2c530f90de.png" width="70%"/>

> Note: Select points in a counterclockwise order, beginning on the upper left corner of the rectangular plane.

> Tip: For best results, choose points that are far apart.

#### 4. Return to the window where you clicked `Choose Image`. You should now see your selected image with the selected rectangular plane highlighted. 

  <img src="https://user-images.githubusercontent.com/99809831/200985629-08153e9b-078f-499c-8197-ae820e3e2164.png" width="70%"/>

#### 5. Select `Undistort (Full Image)` if you want to undistort the whole image. Otherwise, select `Undistort (Crop to Selection)`, if you only want to undistort the highlighted portion.

#### 6. After clicking any of the `Undistort` buttons, the undistorted image will be shown on the right of the original image.

  <img src="https://user-images.githubusercontent.com/99809831/200985863-f7068784-8d42-4a2d-9eea-d0f9858f13f1.png" width="70%"/>
  <img src="https://user-images.githubusercontent.com/99809831/200985895-66eb102f-52f3-40dc-823a-97362e186f27.png" width="70%"/>

> Note: You might have to resize the window to see the undistorted image.

#### 7. To save the undistorted image, click `Save` or `Save As`.

> Note: The `Save` button saves the undistorted image as ***undistorted.jpg***; its location is the directory containing ***perspectiveCorrection.py***.

> Note: The default file extension for `Save As` is ***.jpg***.

#### 8. To undistort another image, select the `Try Again` Button.

## Sample Outputs

<table>

<tr>
<td> <img src="https://user-images.githubusercontent.com/99809831/201005846-79dade3f-4c09-47fb-a158-9e87ace3fe07.jpg" width=100%/> </td>
<td> <img src="https://user-images.githubusercontent.com/99809831/201005540-b606a10f-1d61-468f-a698-41aee4f1f6d3.jpg" width=100%/> </td>
</tr>

<tr>
<td> <img src="https://user-images.githubusercontent.com/99809831/201005848-3c6baf32-50be-4a7f-b6b4-0543279f8213.jpg" width=100%/> </td>
<td> <p align="center">
<img src="https://user-images.githubusercontent.com/99809831/201005544-24f0f4b6-81d7-4491-8948-456d2e509bb9.jpg" width=25%/> 
</p> </td>
</tr>

<tr>
<td> <img src="https://user-images.githubusercontent.com/99809831/201005843-af45efc9-faa4-4e8e-b52a-295320869c95.png" width=100%/> </td>
<td> <img src="https://user-images.githubusercontent.com/99809831/201005537-ea37cbe0-7ee2-4180-9c4e-482fe68ddbcd.jpg" width=100%/> </td>
</tr>

<tr>
<td> <img src="https://user-images.githubusercontent.com/99809831/201007711-3688acce-5da1-4a8f-84bf-ea0d12f72c2d.jpg" width=900/> </td>
<td> <p align="center">
<img src="https://user-images.githubusercontent.com/99809831/201007778-b27b6f2f-7c3c-4485-9252-90fa8d37af30.jpg" width=35%/> 
</p> </td>
</tr>

</table>

## References

[1] [Perspective Transformation](https://theailearner.com/2020/11/06/perspective-transformation/)

[2] [Perspective correction in OpenCV using python](https://stackoverflow.com/questions/22656698/perspective-correction-in-opencv-using-python)

[3] [OpenCV Python: How to warpPerspective a large image based on transform inferred from small region](https://stackoverflow.com/questions/64825835/opencv-python-how-to-warpperspective-a-large-image-based-on-transform-inferred)

[4] [Computing Homography | Image Stitching](https://youtu.be/l_qjO4cM74o)

