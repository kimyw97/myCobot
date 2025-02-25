# myCobot
코봇을 사용한 미니 프로젝트 및 실습 코드

# Troubletroubleshooting
1. Tread_Lock Attribute Error
python 3.11.7 버전과 pymycobot 3.8.0 버전 사용하면 `send_angles()`함수 호출 시 Attribute Error 발생
=> pthon 3.10.0 버전과 pymycobot 3.6.0 버전 사용
2. Permission Error
커널에서 다른 장치가 포트를 사용 중일 경우 Serial 연결할때 Permission Error가 발생함
=> 사용 중인 서비스 종료 후 재시도
3. 시리얼 연결은 되지만 명령들이 안먹힐 때
Transponder -> USB UART -> Atom:ok 이 창에서 해야만 가능(아마 통신 모드로 변경하는 기능 같음)

 # Video