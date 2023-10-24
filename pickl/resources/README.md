## Sample data
실제 데이터셋의 일부를 샘플로 제공합니다.
- `topic` : 첫 발화문에 대한 주제
- `primer` : 첫 발화문
- `conversations` : 대화 상대 모델(Bot)인 'A', 사용자 모델(User)인 'B'의 5 turn 대화

## Prompt
각각의 prompt에 대한 간단한 설명입니다.

### 대화의 첫 문장 생성
- `primer_gen_system.txt` : 첫 발화문을 생성하기 위한 system prompt
- `primer_gen.txt` : 첫 발화문을 생성하기 위한 user prompt

### 대화 생성
- `bot_model_system.txt` : 대화 생성을 위한 Bot(B)의 system prompt
- `bot_model.txt` : 대화 생성을 위한 Bot(B)의 user prompt

### GPT-4를 활용한 자동 평가

- `evaluation_system.txt` : 자동 평가를 위한 GPT-4의 system prompt

- `evaluation_base.txt` : 대화 품질에 기반하여 평가하는 prompt
  - G-Eval과 USR 논문을 참고하여 평가 Prompt를 구성했습니다.

- `evaluation_novel.txt` : 한국어 소설을 쓰고 있는 유저를 도와주기 위해, 소설 속 주인공들의 대화 초안 2개를 비교하여 한 번에 평가하는 prompt

- `evaluation_mbti.txt` : 사용자 모델(User)의 여러 가지 대화 묶음을 한 번에 보고, mbti를 구하는 prompt

### API example
- `api_example.txt` : api example에서 GPT-3.5가 일상 대화를 할 수 있게끔 작성한 prompt