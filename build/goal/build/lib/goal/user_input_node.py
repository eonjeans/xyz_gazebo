import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseArray, Pose

class UserInputNode(Node):
    def __init__(self):
        super().__init__('user_input_node')
        
        # 두 가지 토픽 퍼블리셔 생성
        self.goal_publisher = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.waypoints_publisher = self.create_publisher(PoseArray, '/waypoints', 10)

        self.get_logger().info("User Input Node Started.")
        self.show_menu()

    def show_menu(self):
        while rclpy.ok():
            print("\n========== MENU ==========")
            print("1: Send Single Goal")
            print("2: Send Multiple Waypoints")
            print("q: Quit")
            print("==========================")

            choice = input("Select an option: ").strip()

            if choice == '1':
                self.send_single_goal()
            elif choice == '2':
                self.send_waypoints()
            elif choice.lower() == 'q':
                self.get_logger().info("Exiting User Input Node...")
                break
            else:
                print("Invalid option. Try again!")

    def send_single_goal(self):
        try:
            user_input = input("Enter target coordinates (x y): ").strip().split()
            x, y = map(float, user_input)

            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.header.stamp = self.get_clock().now().to_msg()
            goal_pose.pose.position.x = x
            goal_pose.pose.position.y = y
            goal_pose.pose.orientation.w = 1.0

            self.goal_publisher.publish(goal_pose)
            self.get_logger().info(f"Published Single Goal: x={x}, y={y}")

        except ValueError:
            print("Invalid input. Please enter two numbers (x y).")

    def send_waypoints(self):
        waypoints = PoseArray()
        waypoints.header.frame_id = 'map'

        print("Enter waypoints as 'x y'. Type 'w' to finish input.")
        
        while rclpy.ok():
            try:
                user_input = input("Waypoint (x y) or 'w' to finish: ").strip()

                if user_input.lower() == 'w':
                    if not waypoints.poses:
                        print("No waypoints entered. Cancelling...")
                        return
                    waypoints.header.stamp = self.get_clock().now().to_msg()
                    self.waypoints_publisher.publish(waypoints)
                    self.get_logger().info(f"Published {len(waypoints.poses)} waypoints.")
                    break

                x, y = map(float, user_input.split())

                pose = Pose()
                pose.position.x = x
                pose.position.y = y
                pose.orientation.w = 1.0

                waypoints.poses.append(pose)
                self.get_logger().info(f"Added waypoint: x={x}, y={y}")

            except ValueError:
                print("Invalid input. Please enter two numbers (x y) or 'w' to finish.")

def main(args=None):
    rclpy.init(args=args)
    node = UserInputNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
