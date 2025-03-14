import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import math

class GoalPublisher(Node):
    def __init__(self):
        super().__init__('goal_publisher')
        self.publisher_ = self.create_publisher(PoseStamped, '/goal_pose', 10)

    def publish_goal(self, x, y, yaw):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = 0.0

        # yaw 값을 이용해 회전(쿼터니언)을 계산
        # 회전이 없는 상태: yaw=0 -> quaternion: (x=0, y=0, z=0, w=1)
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = qz
        msg.pose.orientation.w = qw

        self.publisher_.publish(msg)
        self.get_logger().info(f"Published goal: x={x:.2f}, y={y:.2f}, yaw={yaw:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = GoalPublisher()

    try:
        while rclpy.ok():
            # 터미널에서 입력받은 좌표로 목표 설정
            user_input = input("Enter goal coordinates in format (x y yaw): ")
            try:
                values = user_input.strip().split()
                if len(values) != 3:
                    print("Please enter exactly 3 numbers: x y yaw")
                    continue
                x, y, yaw = map(float, values)
                node.publish_goal(x, y, yaw)
            except ValueError:
                print("Invalid input. Please enter numeric values.")
    except KeyboardInterrupt:
        print("\nExiting goal publisher.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
