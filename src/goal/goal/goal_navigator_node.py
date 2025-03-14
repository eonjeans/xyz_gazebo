import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped, PoseArray
from nav2_msgs.action import NavigateToPose, FollowWaypoints
from rclpy.duration import Duration

class GoalNavigator(Node):
    def __init__(self):
        super().__init__('goal_navigator_node')

        # NavigateToPose 액션 클라이언트
        self.navigate_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # FollowWaypoints 액션 클라이언트
        self.follow_waypoints_client = ActionClient(self, FollowWaypoints, 'follow_waypoints')

        # Topic subscriber 생성
        self.goal_pose_sub = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )

        self.waypoints_sub = self.create_subscription(
            PoseArray,
            '/waypoints',
            self.waypoints_callback,
            10
        )

        self.get_logger().info("Goal Navigator Node Started with Action Clients!")

    def goal_callback(self, msg: PoseStamped):
        self.get_logger().info(f"Received single goal: x={msg.pose.position.x}, y={msg.pose.position.y}")

        # Goal 생성
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = msg
        goal_msg.behavior_tree = ''

        # 서버 연결 기다리기
        self.navigate_to_pose_client.wait_for_server()
        self.get_logger().info("Sending NavigateToPose goal...")

        # Goal 전송
        self._send_goal_future = self.navigate_to_pose_client.send_goal_async(goal_msg, feedback_callback=self.goal_feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f"Current progress: {feedback.current_pose.pose.position.x}, {feedback.current_pose.pose.position.y}")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("Goal rejected!")
            return

        self.get_logger().info("Goal accepted, waiting for result...")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.goal_result_callback)

    def goal_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == 4:  # SUCCEEDED
            self.get_logger().info("Goal succeeded!")
        elif status == 2:  # CANCELED
            self.get_logger().warn("Goal was canceled!")
        else:
            self.get_logger().error(f"Goal failed with status: {status}")

    def waypoints_callback(self, msg: PoseArray):
        self.get_logger().info(f"Received {len(msg.poses)} waypoints.")

        # PoseStamped 리스트 생성
        waypoints = []
        for idx, pose in enumerate(msg.poses):
            pose_stamped = PoseStamped()
            pose_stamped.header.frame_id = 'map'
            pose_stamped.header.stamp = self.get_clock().now().to_msg()
            pose_stamped.pose = pose
            waypoints.append(pose_stamped)

            self.get_logger().info(f"Waypoint {idx + 1}: x={pose.position.x}, y={pose.position.y}")

        # Goal 생성
        goal_msg = FollowWaypoints.Goal()
        goal_msg.poses = waypoints

        # 서버 연결 기다리기
        self.follow_waypoints_client.wait_for_server()
        self.get_logger().info("Sending FollowWaypoints goal...")

        # Goal 전송
        self._send_waypoints_goal_future = self.follow_waypoints_client.send_goal_async(goal_msg, feedback_callback=self.waypoints_feedback_callback)
        self._send_waypoints_goal_future.add_done_callback(self.waypoints_response_callback)

    def waypoints_feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f"Currently at waypoint index: {feedback.current_waypoint}")

    def waypoints_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("Waypoints goal rejected!")
            return

        self.get_logger().info("Waypoints goal accepted, waiting for result...")
        self._get_waypoints_result_future = goal_handle.get_result_async()
        self._get_waypoints_result_future.add_done_callback(self.waypoints_result_callback)

    def waypoints_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == 4:  # SUCCEEDED
            self.get_logger().info("Waypoints navigation succeeded!")
        elif status == 2:  # CANCELED
            self.get_logger().warn("Waypoints navigation was canceled!")
        else:
            self.get_logger().error(f"Waypoints navigation failed with status: {status}")


def main(args=None):
    rclpy.init(args=args)
    node = GoalNavigator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
