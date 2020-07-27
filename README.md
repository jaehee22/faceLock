# Raspberry Pi를 이용한 얼굴인식 스마트 도어락 설계 및 구현
## 1. 개요
소켓 통신을 기반으로 한 얼굴인식 도어락을 구현합니다.

도어락의 기능은 기존 내장된 키패트 잠금제어 기능에 얼굴인식 잠금제어, 어플리케이션 잠금제어 기능을 추가합니다.
어플리케이션과 연동하여 어플리케이션 내에서 사용자의 얼굴을 등록할 수 있고, 등록된 사용자의 얼굴과 방문자의 얼굴을 확인할 수 있게 구현합니다.

## 2. 구현 환경
1) OS : Android
2) H/W : Raspberry Pi
3) Application : Android studio
3) Database : Firebase
4) Language 
	- H/W : python
	- Application : JAVA

## 3. 개발 기간
- 프로젝트 기간 : 19.09.02 ~ 19.11.19
- 프로젝트 인원 : 2명

## 4. 구성 요소
![image](https://user-images.githubusercontent.com/58822916/73519862-797eb280-4445-11ea-8f3f-4168fa262199.png)

## 5. 설계 구조

![image](https://user-images.githubusercontent.com/58822916/73525787-36c3d700-4453-11ea-8e4a-5578f9c970fc.png)

서버는 라즈베리파이의 AppSocket.py

클라이언트는 라즈베리파이의 ultrasonic.py, 안드로이드 어플로 서로 통신을 하며 데이터를 주고받는다.


## 6. 구현
### 6-1. Application 메인화면
![image](https://user-images.githubusercontent.com/58822916/73519971-d24e4b00-4445-11ea-8f81-9fc095be48c8.png)

1. 사용자 등록 버튼을 누르고 도어락 앞에 있는 카메라에 가서 사진을 찍으면 사용자를 등록할 수 있다.
2. 1번을 완료한 후, 사용자 목록에 사진이 추가된다.
3. 2가 수행된 후에는 해당 사용자가 도어락 앞으로 가면 사용자라고 인식하여 도어락을 제어할 수 있다.
(인식률은 43%로 설정했습니다)
4. 등록되지 않은 사용자가 도어락 앞으로가면 33번의 인식 실패 후 방문기록 조회에 사진이 추가된다.
5. 사용자는 방문기록조회의 얼굴을 보고 어플리케이션을 통해 도어락을 제어할 수 있다.

### 6-2. 도어락 앞, 내부 모습
![image](https://user-images.githubusercontent.com/58822916/73525247-252dff80-4452-11ea-96d0-c1938e35eaf5.png)
