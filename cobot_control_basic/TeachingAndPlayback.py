from pymycobot import MyCobot320
import time
'''
1. 시간동안 모두 기록
너무 많은 기록으로 인해 아주 조금씩 움직임
2. 움직이는 동안은 기록 x
중간에 생략 되는 기록이 있음
3. 1초 딜레이
시간이 너무 길어 기록 안되는 타이밍이 있음
3. 0.2초 딜레이
적당함
'''
mc = MyCobot320('COM4')
mc.send_angles([0,0,0,0,0,0],20)
timer = 10
print('Record during 10 Seconds')
print('Start in 10 Seconds')
while timer > 0:
    time.sleep(1.0)
    print(timer)
    timer -= 1
for i in range(1,7):
    mc.release_servo(i)
    
record = []
start = time.time()
current = time.time()
while current < start + 10:
    time.sleep(0.2)
    record.append(mc.get_angles())
    current = time.time()
    
print('Record End') 
for i in range(1,7):
    mc.focus_servo(i)

print('Play recording')
for angle in record:
    mc.send_angles(angle,20)
    
print('init')
mc.send_angles([0,0,0,0,0,0],20)