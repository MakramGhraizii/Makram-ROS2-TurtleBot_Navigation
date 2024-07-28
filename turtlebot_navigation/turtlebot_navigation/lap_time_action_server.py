import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from custom_interfaces.action import MeasureLapTime
import time

class LapTimeActionServer(Node):

    def __init__(self):
        super().__init__('lap_time_action_server')
        self._action_server = ActionServer(
            self,
            MeasureLapTime,
            'measure_lap_time',
            self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)

        self.subscription = self.create_subscription(Odometry,'/odom',self.odom_callback,10)
        self.start_pose = None
        self.current_pose = None

    def goal_callback(self, goal_request):
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        if self.start_pose is None:
            self.start_pose = self.current_pose

        start_time = time.time()

        while rclpy.ok():
            if self.check_lap_complete() and ((time.time() - start_time) > 10):
                total_time = time.time() - start_time
                goal_handle.succeed()
                result = MeasureLapTime.Result()
                result.total_time = total_time
                self.get_logger().info(f'Lap completed, Time = {total_time} seconds')
                return result

            elapsed_time = time.time() - start_time
            feedback = MeasureLapTime.Feedback()
            feedback.elapsed_time = elapsed_time
            goal_handle.publish_feedback(feedback)

            rclpy.spin_once(self)

    def check_lap_complete(self):
        if self.start_pose is None or self.current_pose is None:
            return False

        distance = self.calculate_distance(self.start_pose, self.current_pose)
        return distance < 0.4  

    def calculate_distance(self, pose1, pose2):
        dx = pose1.position.x - pose2.position.x
        dy = pose1.position.y - pose2.position.y
        return (dx**2 + dy**2)**0.5

def main(args=None):
    rclpy.init(args=args)
    node = LapTimeActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()