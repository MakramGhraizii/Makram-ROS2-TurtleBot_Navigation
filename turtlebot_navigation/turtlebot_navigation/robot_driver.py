import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from custom_interfaces.srv import FindWall
from std_msgs.msg import Bool


class RobotDriver(Node):

    def __init__(self):
        super().__init__('robot_driver')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, 10)

        
        self.wall_found_publisher = self.create_publisher(Bool, 'wall_found', 10)

        self.client = self.create_client(FindWall, 'find_wall')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')

        self.distance_to_wall = 0.3
        self.wall_distance_tolerance = 0.05 
        self.distance_threshold = 0.3 
        self.finding_wall = True

    def listener_callback(self, msg):
        twist = Twist()

        if self.finding_wall:
            self.find_wall_logic(msg, twist)
        else:            
            self.follow_wall_logic(msg, twist)
        self.publisher_.publish(twist)

    def find_wall_logic(self, msg, twist):
        ranges = msg.ranges
        front_region = min(min(ranges[0:20] + ranges[-20:]), 10)

        if front_region < self.distance_threshold:
            twist.linear.x = 0.0
            twist.angular.z = 0.5  
            self.finding_wall = False
            self.wall_found_publisher.publish(Bool(data=True))
            self.get_logger().info('Wall Found!')
        else:
            twist.linear.x = 0.2
            twist.angular.z = 0.0  

    def follow_wall_logic(self, msg, twist):
        # Logic to follow the wall
        ranges = msg.ranges
        front_region = min(min(ranges[0:20] + ranges[-20:]), 10)
        right_region = min(min(ranges[-90:-60]), 10)  

        if front_region < self.distance_threshold:
            twist.linear.x = 0.0
            twist.angular.z = 0.4 
        else:
            if right_region < self.distance_to_wall - self.wall_distance_tolerance:
                twist.linear.x = 0.4
                twist.angular.z = 0.2  # turn left
            elif right_region > self.distance_to_wall + self.wall_distance_tolerance:
                twist.linear.x = 0.4
                twist.angular.z = -0.2 # turn right
            else:
                twist.linear.x = 0.4
                twist.angular.z = 0.0  

def main(args=None):
    rclpy.init(args=args)
    node = RobotDriver()
    node.req = FindWall.Request()
    node.future = node.client.call_async(node.req)
    rclpy.spin_until_future_complete(node, node.future)
    node.get_logger().info('Found the wall')
    node.finding_wall = False 
    rclpy.spin(node)    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
