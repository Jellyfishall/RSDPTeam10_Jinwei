uint32 id
geometry_msgs/Pose pose
float32 confidence
uint32 age
uint32 missed
int32 center_u
int32 center_v

# Block/bin shared colour enum.
uint8 color
uint8 BLUE = 0
uint8 RED = 1
uint8 YELLOW = 2
uint8 PURPLE = 3
uint8 PINK = 4
uint8 GREEN = 5
uint8 UNKNOWN = 255

float32 color_confidence
uint32 color_votes

string shape_label
float32 shape_confidence
uint32 shape_votes
