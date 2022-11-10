# 한국어 Instruction Tuning 데이터 빌더
Working In Progress...



순서 
1. templates/ 폴더 안에 YAML 포맷으로 템플릿을 만든다.
2. 템플릿에서 지정된 데이터셋을 불러온다.
3. 데이터셋의 각 instance에 대해, task 중 하나를 무작위로 골라 아래 형식의 데이터를 생성한다.
```
# 예시
{
    "task": "nsmc-binary-classification",
    "input": "리뷰를 읽고 사용자가 긍정적으로 평가했는지 대답하세요\n리뷰: {text}\n대답: ",
    "output": "예"
}
```
4. 결과는 tasks/{task} 에 저장된다.

## 데이터셋
공개 데이터가 아닐 경우에는 data/ 폴더에 데이터를 저장한다.


## 템플릿 작성 가이드
