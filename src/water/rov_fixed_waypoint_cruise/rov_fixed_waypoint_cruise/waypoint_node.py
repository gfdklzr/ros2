import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import math

class WaypointCruiseNode(Node):
    def __init__(self):
        super().__init__("waypoint_cruise_node")
        self.waypoints = [(3.0, 0.0), (3.0, 3.0), (0.0, 3.0), (0.0, 0.0)]
        self.wp_index = 0
        self.curr_x = 0.0
        self.curr_y = 0.0
        self.threshold = 0.3

        self.target_pub = self.create_publisher(PoseStamped, "/rov/target_pose", 10)
        self.odom_sub = self.create_subscription(Odometry, "/odom", self.odom_cb, 10)
        self.timer = self.create_timer(0.2, self.timer_cb)
        self.get_logger().info("waypoint cruise node start")

    def odom_cb(self, msg):
        self.curr_x = msg.pose.pose.position.x
        self.curr_y = msg.pose.pose.position.y

    def timer_cb(self):
        if self.wp_index >= len(self.waypoints):
            self.get_logger().info("all waypoints finished")
            return
        tx, ty = self.waypoints[self.wp_index]
        target = PoseStamped()
        target.header.frame_id = "world"
        target.header.stamp = self.get_clock().now().to_msg()
        target.pose.position.x = tx
        target.pose.position.y = ty
        self.target_pub.publish(target)

        dist = math.hypot(tx - self.curr_x, ty - self.curr_y)
        if dist < self.threshold:
            self.wp_index += 1
            self.get_logger().info(f"reach waypoint, next index:{self.wp_index}")

def main(args=None):
    rclpy.init(args=args)
    node = WaypointCruiseNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
