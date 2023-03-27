# SeniorDesign

# Combined Pages

### Motivations

I have an interest in artificial intelligence and machine learning and have taken a few classes on the topic and thought this would be a great way to apply my skills to a real-world project. I also believe this project has the potential to make an impact in the future and be used in disaster surveillance and management, terrain mapping, ect.

### Ideas

Our sponsor, Dr. Shaurya Agarwal, has left the project quite open-ended in regards to what technologies we will use, so we as a team have spent this time searching for what techniques and algorithms we can use. Our front-end/visualization will most likely be in Unity and back-end in Python and/or C++. Part of the visualization includes the detection of objects such as fallen trees, downed power lines, and debris, which will be achieved using object detection and instance segmentation. Gathering training data for our machine learning models is one of the main issues we have had to tackle, since we are focusing on use during disaster scenarios. Well-documented lidar data is few and far between and not exactly easy to replicate, so it is difficult to have enough data for effective training. In my opinion, the best ways to get around this problem would be to either use anomaly detection or simulated environments since neither options require the real-life disaster data that is so scarce. 

# Video Object Detection

### What is object detection?

Object detection is a technique in computer vision that detects objects (shocker) in an image or video, typically shown by a colored box around the detected object accompanied with a label of what the object is. It has many uses, a few examples being facial recognition, surveillance footage, and sports footage.

### How does it work?

Typically there are two parts to an object detection method, an encoder and a decoder. The encoder takes an image or video frame and processes it to extract and locate objects, which are then labeled. The decoder then finds the bounding boxes and proper labels for those objects using predictions.

### Methods

Due to the need for real-time footage, performance is a priority when searching for a method to employ. Post-Processing methods use frame-by-frame detection, which provides a significantly accuracy but worse performance. 3D Convolution is a multi-frame method that is better used for processing 3D images, such as MRI scans, and due to many multi-dimensional matrix computations performance is slow and cannot process in real time. Recurrent Neural Networks, another type of multi-frame method, are a special type of network that deals with sequential data. This architecture effectively creates long-term memory that helps to guide smaller neural networks which allows for must better performance, up to 70 frames per second (fps) in some cases on a mobile device. Optical Flow is a method where movement is estimated by comparing two frames. Sparse Feature Propagation falls under the Optical Flow umbrella and uses sparse key frames that is used in comparison for the next $n-1$ frames. The $n^{th}$ frame will be the next key frame. While this method is slightly less accurate, it is faster and more efficient then most.

(Source: The Ultimate Guide to Video Object Detection)

### What should we use?

Based solely on performance, Recurrent Neural Networks and Sparse Feature Propagation are the best contenders. Even though Recurrent Neural Networks are faster with slightly better accuracy, it has a complicated architecture and would be difficult to maintain and debug. Sparse Feature Propagation is slightly worse in comparison, but it still works well in the circumstances given and the simplicity of the code is better in the long run.

Recurrent Neural Networks (RNN)

- Up to 70 fps on a mobile device
- Good accuracy
- Very complex architecture
    
    ![Example of Recurrent Neural Networks](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/54354898-327e-4bbb-9490-06ec53814838/Untitled.png)
    
    Example of Recurrent Neural Networks
    

Sparse Feature Propagation (SFP)

- Runs real-time
- Slight drop in accuracy (~4.5%)
- Simple architecture
    
    ![Example of Sparse Feature Propagation](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/88c948ad-1d16-4c97-88df-14b273bad272/Untitled.webp)
    
    Example of Sparse Feature Propagation
    

### Sources

- The Ultimate Guide to Video Object Detection - [https://towardsdatascience.com/ug-vod-the-ultimate-guide-to-video-object-detection-816a76073aef#3ddf](https://towardsdatascience.com/ug-vod-the-ultimate-guide-to-video-object-detection-816a76073aef#3ddf)

# Camera-Lidar Fusion

Cameras are good for perceiving an environment in 3D and lidar is good for determining distance from the vehicle, so using a combination of the two is best for object detection in autonomous vehicles. Fusion is the process of combining data from the camera and lidar systems. A few challenges of fusion include proper calibration between the camera and lidar (relative distance from each other), finding unique features in both sets of data to find a relationship, and either turning 3D lidar data into 2D or mapping 2D camera data onto 3D.

![An example of camera and lidar position calibration](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0866f43a-aac8-4c6b-b62a-4c9841568302/Untitled.webp)

An example of camera and lidar position calibration

![The result from fusion](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1a9f2ae5-3381-4292-b2b4-fd481caa8d92/Untitled.webp)

The result from fusion

### Unique Features

One such challenge is finding unique features and using them to line up the lidar points to the camera data. Features that can be used to combine the data can be either intrinsic (a) or extrinsic (b).

Marker detection with the point cloud looks like *$p_v=C_i*p_i$*, where $C_i$ is the camera’s intrinsic parameters (i.e. position), $p_i$ is the original point cloud data, and $p_v$ is the resulting point cloud from the camera’s POV. 

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ed5431e1-1137-49e9-aae4-f367c1475739/Untitled.webp)

Camera marker detection can be done using Sobel edge detection and Hough transformation. Then the data needs to be translated to account for the distance between the camera and lidar using the translation matrix

$$
M_{projective}=\begin{bmatrix}f & 0 & u_0 & 0 \\0 & f & v_0 & 0 \\0 & 0 & 0 & 1 \end{bmatrix} \times \begin{bmatrix}
1 & 0 & 0 & t_x \\
0 & 1 & 0 & t_y \\
0 & 0 & 1 & t_z \\
0 & 0 & 0 & 1 
\end{bmatrix}
$$

where $(t_x, t_y, t_z)$ is the translation vector, $f$ is the focal length from the camera to the object, and $(v_0, u_0)$ is the center of the image.

After translation, rotation is done to increase the calibration accuracy using the boundary features sets $b_i^l$ (lidar) and $b_i^c$ (camera) in the equation 

$$
(R,t)=arg~min \sum_{i-1}^n w_i ||(Rb^l_i+t) - b_i^c||^2
$$

. The weighted centered vectors are calculated using 

$$
b^{-l}= \frac{\sum_{i=1}^n w_i b_i^l}{\sum_{i=1}^n w_i}
$$

and

$$
b^{-c}= \frac{\sum_{i=1}^n w_i b_i^c}{\sum_{i=1}^n w_i}
$$

where the weights for each point is $w_i>0$ and $i=1$ to $n$ which is then used for the centered vectors $x_i=b_i^l-b^{-l}$ and $y_i=b_i^c-b^{-c}$. Next is the covariance matrix $S=XWY^T$ where $X$and $Y$are $d \times n$ matrices that have $x_i$ and $y_i$ as columns and $W=diag(w_1, w_2, ..., w_n)$. The rotation matrix is finally calculated by taking the singular value decomposition of $S=U \sum V^T$ and rotation $r$, resulting in 

$$
c_i \begin{bmatrix} U \\ V \\ 1 
\end{bmatrix} = \begin{bmatrix}
r_{11} & r_{12} & r_{13} & t_x \\
r_{21} & r_{22} & r_{23} & t_y \\
r_{31} & r_{32} & r_{33} & t_z \\
0 & 0 & 0 & 1 \end{bmatrix} P_i \begin{bmatrix} X \\ Y \\ Z \\ 1
\end{bmatrix}
$$

. After all the preprocessing, the camera and lidar data are ready to be fused into either 2D or 3D. For demonstration purposes, I will use the 2D equation 

$$
P_{2D} \begin{bmatrix} u_i \\ v_i \\ 1 
\end{bmatrix} = \begin{bmatrix}
r_{11} & r_{12} & r_{13} & t_x \\
r_{21} & r_{22} & r_{23} & t_y \\
r_{31} & r_{32} & r_{33} & t_z \\
0 & 0 & 0 & 1 \end{bmatrix} P_i \begin{bmatrix} x_i \\ y_i \\ z_i \\ 1
\end{bmatrix}
$$

### Sources

- Lidar and Camera Fusion Approach for Object Distance Estimation in Self-Driving Vehicles - [https://www.mdpi.com/2073-8994/12/2/324](https://www.mdpi.com/2073-8994/12/2/324)
- Camera-Lidar Projection: Navigating Between 2D and 3D - [https://medium.com/swlh/camera-lidar-projection-navigating-between-2d-and-3d-911c78167a94](https://medium.com/swlh/camera-lidar-projection-navigating-between-2d-and-3d-911c78167a94)

# Simulation

### Training Data

Using simulated data allows for full control over different aspects of the data, the creation of different scenarios with relative ease, and the collection of pre-labeled data. The environment can be built using assets from the Unity asset store, creating models on Blender, or just using basic shapes provided by Unity in its editor. There exists a handful of packages created to simulate lidar and camera sensors, one such being Unity SensorSDK which is created and maintained by Unity for use in such cases. The package provides eleven different lidars, seven cameras, and many options for visualization and customization so we can test and tailor what data we need and what sensors we might use on the real vehicle.

The Generic 3D Segmentation Lidar is one of the options that uses the Perception package to perform instance and semantic segmentation, which can be customized using the labels of objects to assign colors. There also exists the Velodyne Puck Lidar that is a recreation of a real lidar available on the market, and may be helpful to experiment and get an understanding of how the real lidar would work.

![Example of lidar data layered on top of a scene](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ff2e464c-9c3a-460d-8b9a-5617dc8b4dd2/Untitled.jpeg)

Example of lidar data layered on top of a scene

One of the camera options available is the Segmentation Camera, which creates a label for each object in view and assigns a unique color to. It also provides ground truth data, or data that is known to be correct, that is ideal for training.

![Real lidar data from a Velodyne Puck lidar](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/fb1e4c5d-f06f-4012-b6c8-1fbf300e7aa2/Untitled.jpeg)

Real lidar data from a Velodyne Puck lidar

![Simulated lidar data from the Velodyne Puck lidar provided by Unity SensorSDK](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9c81c753-95a3-41d9-a2fd-02a0b327af8f/Untitled.jpeg)

Simulated lidar data from the Velodyne Puck lidar provided by Unity SensorSDK

### Sources

- Unity SensorSDK Documentation - [https://docs.unity3d.com/Packages/com.unity.sensorsdk@2.0/manual/index.html](https://docs.unity3d.com/Packages/com.unity.sensorsdk@2.0/manual/index.html)
