import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt


class VisualizeNode(Node):
    def __init__(self):
        super().__init__('visualize_node')
        self.get_logger().info("Initializing VisualizeNode")
        
        self.odom_subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        self.scan_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
        
        self.positions = []
        self.distances = []
        
        self.fig, self.ax = plt.subplots(2, 1)
        self.ax[0].set_title('Robot Path')
        self.ax[1].set_title('Distance to Wall')
        plt.ion()
        plt.show()
        
        self.timer = self.create_timer(0.1, self.plot_data)
        self.get_logger().info("VisualizeNode initialized and timer set")

    def odom_callback(self, msg):
        position = msg.pose.pose.position
        self.positions.append((position.x, position.y))
        self.get_logger().info(f"Received odom: ({position.x}, {position.y})")
        
    def scan_callback(self, msg):
        front_distance = min(msg.ranges)
        self.distances.append(front_distance)
        self.get_logger().info(f"Received scan: {front_distance}")
        
    def plot_data(self):
        self.ax[0].clear()
        self.ax[1].clear()
        
        if self.positions:
            x, y = zip(*self.positions)
            self.ax[0].plot(x, y, label='Path')
            self.ax[0].legend()
        
        if self.distances:
            self.ax[1].plot(self.distances, label='Distance to Wall')
            self.ax[1].legend()
        
        plt.pause(0.01)

def main(args=None):
    rclpy.init(args=args)
    node = VisualizeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    print("Starting visualize_node")
    main()
    print("visualize_node finished")
