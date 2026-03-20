### 前言

目前发现SLAM toolbox不能使用单激光进行建图，故采用catorgrapher进行建模
SLAM Toolbox不能自动推算里程计，原因未知

### 查看tf树

```
ros2 run tf2_tools view_frames
```

### 查看变换坐标

如果要在代码中使用请订阅/tf

```
ros2 topic echo /tf
ros2 topic echo /tf --once
```
