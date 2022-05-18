# 라즈베리파이와 영상처리를 이용한 자동 출석 프로그램
## 교수와 학생을 위한 자동으로 출결을 관리해주는 플랫폼 
## 기술스택 : Nginx, SQLite, Django

### 시스템 구조
![image](https://user-images.githubusercontent.com/64186072/169101640-1942c4c2-8be7-40bf-823a-11a7466c7ccf.png)


1. 로그인 시 교수와 학생에게 보여주는 페이지가 다름
2. 교수는 수업을 개설 가능
3. 학생은 교수들이 만든 수업에 수강신청을 할 수가 있음![image](https://user-images.githubusercontent.com/64186072/169102980-57ffda9f-72fa-4489-bba8-a0f001e8c857.png)
4. 학생은 자신의 출석용 사진을 업로드(인식율을 위해 복수개 가능)할 수 있고, 강의마다 주차별로 자신의 출결 상태를 확인 가능![image](https://user-images.githubusercontent.com/64186072/169102956-acf14a8e-8595-4f49-91b4-cd3717970aea.png)
5. 교수는 자신이 만든 수업에 수강신청 한 학생들의 목록을 볼 수 있음
6. 교수가 자동 출결을 버튼을 누르면 라즈베리파이 카메라에 인식된 학생들 모두가 자동으로 출석에 반영됨
![image](https://user-images.githubusercontent.com/64186072/169103733-52eb4f32-e00c-4df9-8a83-38961bb744d9.png)
![image](https://user-images.githubusercontent.com/64186072/169103814-383ea933-74ee-4327-baf9-a37c3ec4a8f8.png)
