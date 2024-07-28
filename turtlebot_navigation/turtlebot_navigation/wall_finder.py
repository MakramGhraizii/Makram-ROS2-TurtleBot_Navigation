import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from custom_interfaces.srv import FindWall
from std_msgs.msg import Bool

class WallFinderServer(Node):

    def __init__(self):
        super().__init__('wall_finder_server')
        self.srv = self.create_service(FindWall, 'find_wall', self.find_wall_callback)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, 10)
        self.wall_found_publisher = self.create_publisher(Bool, 'wall_found', 10)
        self.closest_distance = float('inf')
        self.closest_angle = 0
        self.is_searching = True

    def find_wall_callback(self, request, response):
        self.is_searching = True
        while self.is_searching:
            rclpy.spin_once(self)
        response.success = True
        return response

    def listener_callback(self, msg):
        if not self.is_searching:
            return
        ranges = msg.ranges
        self.closest_distance = min(ranges)
        self.closest_angle = ranges.index(self.closest_distance)
        
        twist = Twist()
        
        if self.closest_distance < 0.5:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.is_searching = False
            self.wall_found_publisher.publish(Bool(data=True))
            self.get_logger().info('wall found')

        else:
            twist.linear.x = 0.1
            if self.closest_angle < len(ranges) / 2:
                twist.angular.z = 0.1
            else:
                twist.angular.z = -0.1
        
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = WallFinderServer()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()