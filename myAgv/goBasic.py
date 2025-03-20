from pymycobot import MyAgv
speed = 10;#1~127
agv = MyAgv('/dev/ttyAMA2')
agv.go_ahead(speed)
print('if you want to stop, press any keyboard btn')
input()
agv.stop()