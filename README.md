# 외한 챗봇 시스템 구현

## 1. 개발 동기
* 달러를 이용한 수익 창출
* 시스템 구축으로 인간 감정 대응
* 환율, 달러지수, 관련 뉴스 등 정보 제공

## 2. 기술개발 동향
* 국민은행, 삼성카드, 기업은행 등 24시간 금융 관련 상담 기능, 간편이체, 적금가입, 환전신청 등 시행
* 업무 생산성 향상 및 영업 비용 감소

## 3. 개발 내용
* 사용자 입력(현재 환율 알려줘, 달러 살까? 등)
* 챗봇 코어: 데이터 요청 및 해당 데이터 결과 출력
* 크롤링 코어: 웹페이지 탐색 및 챗봇코어에 전달
     
![image](https://github.com/Developerinsight/Forex_Chatbot/assets/123748877/05648376-9b36-45a2-a3cb-67d224e51e08)

### 3-1. 챗봇 알고리즘
* 사용자에게 입력 받아 user_input이라는 변수에 저장   
     
* user_input이라는 변수에서 우선 기간에 관한 정보 뽑아옴   

* user_input에 day, week, month, year 문자열 존재하면 이에 대한 기간을 현재 날짜에서 빼주어 해당하는 날짜 계산하고, 존재하지 않으면 현재 날짜 기준으로 계산
 
* user_input에 word_list(purchase, hi, dollar, excahnge rate 등)에 존재하는 단어가 있으면 그에 관한 정보 출력   
<img width="404" alt="image" src="https://github.com/Developerinsight/Forex_Chatbot/assets/123748877/908e43d4-813e-4568-948f-e6b50a34ac74">

  
* word_list에 존재하지 않으면 fallback으로 이해하지 못했다는 답변 함
  
* 위에서 기간과 domain에 관한 정보를 얻었다면, 웹 크롤링하여 이에 대한 정보 얻음
  
* 예를 들어, 기간이 2022년 3월 10일이고 domain이 dollar exchange라면 3월 10일의 정보부터 어제의 날짜까지 평균 dollar exchange에 관한 정보 크롤링 해옴
  
* 최종적으로 답변의 리스트인 response에서 domain에 맞는 사전 정의된 답변 뽑아오게 되고, 이를 크롤링했던 정보와 합쳐 최종 답변을 사용자에게 알려줌   
  
![image](https://github.com/Developerinsight/Forex_Chatbot/assets/123748877/90174a77-c2c5-4140-980a-fa8399c7d029)

## 4. 개발환경
* 우분투 20.04 python version 3.8
* 파이썬 라이브러리 설치: pip install bs4, pip install selenium
* 크롬 버전 확인: -google-chrome --version
* 크로 설치
```
sudo apt update
sudo apt upgrade -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common wget -y
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable -y
```

## 5. 챗봇 수행 결과 화면
* 3일 전 달러 환율 요청
![image](https://github.com/Developerinsight/Forex_Chatbot/assets/123748877/dbb73a86-bacf-4f84-95d1-51228f4956ec)   

* 1년 전 유로화 환율 정보 요청
![image](https://github.com/Developerinsight/Forex_Chatbot/assets/123748877/6c3a8290-3268-4b51-911a-0ba9150a26a7)

* 매수 가능 확인 요청
![image](https://github.com/Developerinsight/Forex_Chatbot/assets/123748877/8b211919-16cf-4724-b838-beff438e5060)

* 매도 가능 확인 요청
![image](https://github.com/Developerinsight/Forex_Chatbot/assets/123748877/f50a4596-bf91-427e-b91c-75954aaef709)

* 최신 주요 뉴스 요청   
![image](https://github.com/Developerinsight/Forex_Chatbot/assets/123748877/370c5cde-ef40-4be1-9c8b-aa70eaa6ef1c)


## 6. 매매 결정 조건문
```
 if ex_1 < ex_1y and index_1 < index_1y and (index_1/ex_1*100) > (index_1y/ex_1y*100) and ex_1 < (index_1 /(index_1y/ex_1y*100))*100:
        return "Buy it now!"
        
    else:
        return "Wait!"
```
* ex_1 < ex_1y: 현재 환율(ex_1)이 지난 1년 평균 환율(ex_1y)보다 낮은지를 확인. 이는 현재 환율이 상대적으로 유리하다고 판단할 수 있는 조건   
* index_1 < index_1y: 현재 지수(index_1)가 지난 1년 평균 지수(index_1y)보다 낮은지 확인. 이는 현재 시장 가치가 과거 평균보다 낮게 평가되었음을 나타냄   
* (index_1/ex_1*100) > (index_1y/ex_1y*100): 현재 지수 대 환율의 비율이 지난 1년 평균 지수 대 환율의 비율보다 높은지 확인. 이 비율이 높다는 것은 투자 가치가 환율 변동을 고려했을 때 상대적으로 더 높음을 의미.   
* ex_1 < (index_1 /(index_1y/ex_1y*100))*100: 현재 환율이 지난 1년 동안의 지수 대 환율 비율을 현재 지수에 적용했을 때의 계산값보다 낮은지 확인. 이는 현재 환율이 지난 1년 동안의 평균 시장 성과 대비 환율에 비해 유리한 조건인지를 평가하는 방식
