# Self_Driving_GTAV
Perform lanes segmentation from the first person perspective of the vehicle and make a decision to turn left or right.

Objective:
-Based upon the first person view obtained by the vehicle, segment the lanes and road boundaries.
-The first person view in the video game is almost the same as the real-life view, with various lighting, reflections, occlusions. The agent has to overcome these obstacles.   
-From the segmentation lines, control the vehicle to turn left or right.

Procedure: <br />
1)Convert to birdview perspective:<br />
-Choose 4 points in the first person view and 4 corresponding points in the birdview<br />
-Compute homography matrix<br />
-Warp the input image<br />
<br />
2)Lines segmentation:<br />
-Apply Gaussian filter to blur out noises<br />
-Apply Sober operation for edges detection. Then apply a threshold to filter out unimportant edges, most notably are road cracks and rough surfaces<br />
-Perform Hough transform to detect lines. The lines are probabilistic meaning that they do not run across the screen but are segments with starting points and ending points. A line must have a minimum length to be considered<br />
-The most challenging part was determining the threshold since the lighting constantly changes<br />
=>Adaptive threshold: increase or decrease the threshold such that the number of detected lines are not to dense but also not too sparse.<br /> 
<br />
3)Make decision:<br />
-Average the lines’ angles with respect to the screen vertical axis.<br />
-Angles are weighted by their lengths so that longer lines are larger deciding factors comparing to short lines.<br />
-Positive average angle: turn right, negative average angle: turn left<br />
<br />

Shortcomings:<br />
-Adaptive threshold does not always solve the problem, there can still be a lot of noises with the determined threshold<br />
-Any other vehicles passed by would also be seen as lines and would deviate the decision<br />
<br />

Execution:<br />

To run:<br />
-Run GTAV, change resolution to 640x800 windowed, and move it to topleft corner of the screen (use Alt+Tab to free the arrow)<br />
-In the terminal type command: python run.py (make sure you have all the following libraries: numpy,PIL,cv2,time,pyautogui,scipy,math)<br />
<br />
To exit:<br />
-On the terminal, press Ctrl+C
<br />
Acknowledgement:<br />
Inspired by sentdex: https://www.youtube.com/watch?v=rvnHikUJ9T0&t=273s
