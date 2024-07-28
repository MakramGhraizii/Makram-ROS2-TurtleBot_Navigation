import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from custom_interfaces.action import MeasureLapTime
from std_msgs.msg import Bool


class LapTimeActionClient(Node):

    def __init__(self):
        super().__init__('lap_time_action_client')
        self._action_client = ActionClient(self, MeasureLapTime, 'measure_lap_time')
        self.subscription = self.create_subscription(Bool, 'wall_found', self.wall_found_callback, 10)

    def wall_found_callback(self, msg):
        if msg.data:
            self.send_goal()
            self.get_logger().info('wall found!')


    def send_goal(self):
        goal_msg = MeasureLapTime.Goal()

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected ')
            return

        self.get_logger().info('Goal accepted ')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        elapsed_time = feedback_msg.feedback.elapsed_time
      #  self.get_logger().info(f'Received feedback: {elapsed_time} seconds elapsed')

    def get_result_callback(self, future):
        result = future.result().result
        total_time = result.total_time
        self.get_logger().info(f'Result: Lap completed in {total_time} seconds')

def main(args=None):
    rclpy.init(args=args)
    action_client = LapTimeActionClient()
    try:
        rclpy.spin(action_client)
    except KeyboardInterrupt:
        pass
    action_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()