# Vision Node
This package implements a ROS2 node which runs YOLOv5 for object recognition. It outputs the following types of observation in the frame of the camera:

| Observation Type   | ROS2 Message    |
|--------------- | --------------- |
| Block   | `BlockPoseObservation`   |
| Bin   | `BinPoseObservation`   |
| BinOpening   | `BinOpeningPoseObservation`   |
| Platform   | `PlatformPoseObservation`   |

The node also implements smoothing and voting to mitigate false positives and noisy observations.

# Installation of Vision Node
## 1. Python Packages
To run the YOLO model, you need a number of packages installed. The best way to do this is by installing the relevant packages from the `ultralytics` repository - this will ensure the versions are compatible. NOTE: as with other ROS2 crap, this will install into the global system environment. You may also need to install `scikit-learn` for the classifiers.

```bash
sudo apt update
sudo apt install python3-pip
pip3 install --break-system-packages -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
pip3 install --break-system-packages scikit-learn
```

```
Another option is to installing the packages by hand. I *do not* recommend this if possible. A list of deps I had to sort is here:
## package installs 
- pandas
- ultralytics
- joblib
- torch
- torchvision
- tqdm
- seaborn
- numpy < 2.0.0
- opencv
- scikit-learn
```

## 2. ROS2 Packages
You also need to install the realsense ROS2 package to interface with the camera
```bash
sudo apt install 'ros-jazzy-realsense2-*'
```

## 3. Model Weights
The model weights are saved in [the team OneDrive](https://livemanchesterac.sharepoint.com/:u:/r/sites/UOM-FSE-SoE-DEEE-MScRobotics-2025-2026-Team10/Shared%20Documents/Team%2010/model_weights.zip?csf=1&web=1&e=yIRWIU). You need to download this zip file, and place it in `src/rsdp_perception` and extract it. The directory should look like this:
```bash
.
├── launch
│   └── vision.launch.py
├── model_weights
│   ├── bin_colors
│   │   └── clf_out
│   │       ├── best.pt
│   │       └── label_encoder.pkl
│   ├── block_attrs
│   │   └── clf_out
│   │       ├── best.pt
│   │       └── label_encoders.pkl
│   └── yolo.pt
├── package.xml
├── README.md
├── resource
│   └── rsdp_perception
├── rsdp_perception
│   ├── __init__.py
│   ├── perception_stable_attrs_node.py
│   ├── perception_stable_node.py
│   ├── perception_typed_node.py
│   ├── tracks_monitor_attrs_node.py
│   ├── tracks_monitor_node.py
│   ├── tracks_monitor_typed_node.py
│   ├── yolov5_realsense_node_nocvbridge.py
│   └── yolov5_realsense_node.py
├── setup.cfg
├── setup.py

13 directories, 27 files
```

# Running the Node
To launch the RealSense camera and `vision_node` together, run
```bash
ros2 launch rsdp_perception vision.launch.py
```

To run the node directly, run
```bash
ros2 run rsdp_perception vision_node
```

You can override a few useful `vision_node` parameters from launch without editing code. For example:
```bash
ros2 launch rsdp_perception vision.launch.py conf:=0.35 vote_window:=6 min_votes_to_output:=2
```

The launch file also exposes the subscribed topics and RealSense sync/aligned-depth settings:
```bash
ros2 launch rsdp_perception vision.launch.py \
  align_depth.enable:=true \
  enable_sync:=true \
  color_topic:=/camera/camera/color/image_raw \
  depth_topic:=/camera/camera/aligned_depth_to_color/image_raw \
  info_topic:=/camera/camera/color/camera_info
```
