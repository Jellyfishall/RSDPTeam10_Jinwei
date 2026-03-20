import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yht/SLAM_2D_Learn/SLAM_2D_Learn/install/lslidar_catorgrapher'
