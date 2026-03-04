# TODOs for the controller and simulator

1. Fill in the rest of the controller logic
    1. Rotate on startup (how coordinate with nav stub? Could send cmd_vel direct)
    2. Explore action 
    3. Handle action-in-flight checks - will get quite flabby...
    4. Manipulator 
    5. Return to bin - should be easy
    6. Continue
2. Manipulator stub
    1. Just "acquire" block if in range
    2. Can just handle in controller at first - but move to proper action server to mock the action integration
3. Integrate LIDAR mocking for the navigation stub
    1. Mike sorting
4. Integrate Depth camera mocking for the CV node proper 
5. Integration with actual ROS packages as they come in. They must work in sim.
6. Proper frames and tf transforms
7. Remaining action definitions (navigation and manipulator)
8. Visualisation setup
    1. Current map and robot location in map 
    2. Current estimates of block positions (and status)
    3. Current estimates of bin positions 
    4. Current phase of controller 
