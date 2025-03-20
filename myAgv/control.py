import time
import math
from pymycobot.myagv import MyAgv

class MyAGVController:
    def __init__(self):
        self.agv = MyAgv('/dev/ttyAMA2')
        self.speed = 10
        self.current_x = 0
        self.current_y = 0
        self.current_angle = 0

    def go_head(self):
        print("Moving forward")
        self.agv.go_ahead(self.speed)
        time.sleep(2)
        self.stop()

    def retreat(self):
        print("Moving backward")
        self.agv.retreat(self.speed)
        time.sleep(2)
        self.stop()

    def stop(self):
        print("Stopping")
        self.agv.stop()

    def patrol(self):
        print("Starting patrol mode")
        while True:
            self.go_head()
            time.sleep(1)
            self.retreat()
            time.sleep(1)

    def move_by_distance(self, distance):
        speed = (self.speed / 127) * 0.9 # Speed in m/s
        move_time = distance / speed

        print(f"Moving {distance}m...")
        self.agv.go_ahead(self.speed)
        time.sleep(move_time)
        self.stop()

    def move_by_coordinate(self, x, y, speed=50):
        # Calculate the difference in position
        dx = x - self.current_x
        dy = y - self.current_y

        # Calculate the distance to the target point
        distance = math.sqrt(dx**2 + dy**2)

        # Calculate the target angle relative to the current position
        target_angle = math.degrees(math.atan2(dy, dx))

        # Calculate the angle to rotate (difference between target angle and current angle)
        angle_to_rotate = target_angle - self.current_angle

        # Normalize the angle to the range [-180, 180]
        angle_to_rotate = (angle_to_rotate + 180) % 360 - 180

        # Rotate the AGV to face the target point
        if angle_to_rotate > 0:
            self.agv.counterclockwise_rotation(speed)
            time.sleep(abs(angle_to_rotate)/speed)
            self.agv.stop()
        else:
            self.agv.clockwise_rotation(speed)
            time.sleep(abs(angle_to_rotate)/speed)
            self.agv.stop()

        # Update the current angle
        self.current_angle = target_angle

        # Move forward to the target point
        self.agv.go_ahead(speed)
        time.sleep(distance / (speed / 127))

        # Update the current position
        self.current_x = x
        self.current_y = y

        # Stop the AGV
        self.agv.stop()

        print(f"Moved to ({x}, {y})")

def main():
    controller = MyAGVController()

    while True:
        controller.stop()
        print("\nSelect a command:")
        print("1: Move to one point")
        print("2: Patrol two points")
        print("3: Move by distance")
        print("4: Move by coordinates")
        print("0: Exit")

        command = input("Enter command: ")

        if command == "1":
            controller.go_head()
        elif command == "2":
            controller.patrol()
        elif command == "3":
            distance = float(input("Enter distance (m): "))
            controller.move_by_distance(distance)
        elif command == "4":
            x = float(input("Enter X coordinate: "))
            y = float(input("Enter Y coordinate: "))
            controller.move_by_coordinate(x, y)
        elif command == "0":
            print("Exiting...")
            break
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
