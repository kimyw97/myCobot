from pymycobot import MyCobot320
import time
import random

bot = MyCobot320('/dev/tty.usbserial-575E0789631')
time.sleep(3.0)

base_angles = [32.25, -20.3, 74.44, 7.91, -71.98, -44.73]

try:
    while True:
        user_input = input("계속하려면 Enter, 종료하려면 q 입력: ")
        if user_input.lower() == 'q':
            print("루프 종료")
            break

        angle_5 = base_angles[4] + random.uniform(-5, 5)
        angle_6 = base_angles[5] + random.uniform(-5, 5)

        new_angles = base_angles[:4] + [angle_5, angle_6]
        print(f"보내는 각도: {new_angles}")
        bot.send_angles(new_angles, 20)

        time.sleep(1.0)
except KeyboardInterrupt:
    print("강제 종료됨")

bot.send_angles([0, 0, 0, 0, 0, 0], 20)
