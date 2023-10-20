## API example


### 설명

- `speaker`는 대화 상대 모델(Bot)이 'A', 사용자 모델(User)이 'B'로 고정되어 있습니다.
- `message`는 해당 모델이 생성한 대화문입니다.
- `messages`는 `speaker`, `message` 쌍으로 이루어진 전체 대화 기록입니다.


&nbsp; 

### 주의사항
- 대화 기록에는 연속된 발화가 있을 수 있습니다.(JSON payload 참고) 사용자 모델에서 연속된 발화를 처리하는 로직에 맞추어 사용해야합니다 (e.g concat, separator token 등).

- 모델이 연속된 발화를 할 경우, 별도의 separator 토큰을 사용하지 않고 리스트에 추가해야 합니다 (response format 참고).

&nbsp; 

---

### JSON payload
```
{
    "messages": [
        {
            "speaker" : "A",
            "message" : "오랜만에 레트로 게임 어때? '슈퍼 마리오' 같은 게임 오랜만에 해보자고?ㅋㅋㅋ"
        },
        {
            "speaker" : "B",
            "message" : "슈퍼마리오? 옛날 게임이야?"
        },
        {
            "speaker" : "A",
            "message" : "ㅇㅇ, 그런데 그게 완전 흥미로워! 재밌을 거야"
        },
        {
            "speaker" : "A",
            "message" : "연습해봐!ㅋㅋ"
        }
    ]
}
```

&nbsp; 

### Response Format
```
{
    "response": [
        {
            "speaker" : "B",
            "message" : "오오, 좋아! ㅋㅋㅋㅋ"
        },
        {
            "speaker" : "B",
            "message" : "일단 너가 우리 집에 와서 해줘!"
        }
    ]
}
```

