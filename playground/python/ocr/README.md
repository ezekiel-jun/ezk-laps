# 초기 설정
- 파이썬 3.11 기준 작성 (안정성 목표)

# 실행
1. 가상환경 설정: `python -m venv ocr_env`
2. 가상환경 실행 (윈도우 기준): `./ocr_env/Scripts/activate`
3. 패키지 설치: `pip install -r requirements-dev.txt` 또는 `pip install -r requirments.txt`

# 테스트 방법
1. 테스트: `python test.py`, test.py 내에 main.py 수정 실행

# 의존성 freezing
1. 목적: product용 freezing 목적일 때는 requirements.txt로 freezing
- `pip freeze > requirements.txt`