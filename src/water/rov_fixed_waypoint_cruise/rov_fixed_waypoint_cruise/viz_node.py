import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker

class WaypointVizNode(Node):
    def __init__(self):
        super().__init__("waypoint_viz_node")
        self.waypoints = [(3.0, 0.0), (3.0, 3.0), (0.0, 3.0), (0.0, 0.0)]
        self.marker_pub = self.create_publisher(Marker, "/waypoint_marker", 10)
        self.timer = self.create_timer(0.5, self.publish_marker)

    def publish_marker(self):
        marker = Marker()
        marker.header.frame_id = "world"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.type = Marker.SPHERE_LIST
        marker.action = Marker.ADD
        marker.scale.x = 0.3
        marker.scale.y = 0.3
        marker.scale.z = 0.3
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 0.8
        for x,y in self.waypoints:
            from geometry_msgs.msg import Point
            p = Point()
            p.x = x
            p.y = y
            p.z = 0.0
            marker.points.append(p)
        self.marker_pub.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = WaypointVizNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
