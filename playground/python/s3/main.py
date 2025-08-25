import boto3
import requests
from io import BytesIO
from botocore.exceptions import NoCredentialsError, ClientError

def send_s3_file_to_api(
        s3_file_key,
        bucket_name,
        aws_access_key_id,
        aws_secret_access_key,
        amount,
        date,
        seller,
        item,
        api_url="",
        region_name="ap-northeast-2"  # 기본값으로 서울 리전 설정
):
    """
    S3에서 파일을 다운로드하고 지정된 API 엔드포인트로 전송하는 함수

    Args:
        s3_file_key (str): S3 객체의 키 (파일 경로)
        bucket_name (str): S3 버킷 이름
        aws_access_key_id (str): AWS Access Key ID
        aws_secret_access_key (str): AWS Secret Access Key
        amount (str): 금액 정보
        date (str): 날짜 정보 (YYYYMMDD 형식)
        seller (str): 판매자 정보
        item (str): 상품 정보
        api_url (str): API 엔드포인트 URL (기본값: 제공된 URL)
        region_name (str): AWS 리전 (기본값: ap-northeast-2)

    Returns:
        dict: API 응답 결과
    """

    try:
        # S3 클라이언트 생성
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        # S3에서 파일 다운로드
        print(f"S3에서 파일 다운로드 중: {bucket_name}/{s3_file_key}")
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_file_key)
        file_content = response['Body'].read()

        # 파일 이름 추출 (경로에서 파일명만)
        filename = s3_file_key.split('/')[-1]

        # API로 전송할 데이터 준비
        files = {
            'file': (filename, BytesIO(file_content), 'application/octet-stream')
        }

        data = {
            'amount': amount,
            'date': date,
            'seller': seller,
            'item': item
        }

        headers = {
            'Accept': 'application/json'
        }

        # API 요청 전송
        print(f"API로 데이터 전송 중: {api_url}")
        api_response = requests.post(
            api_url,
            headers=headers,
            files=files,
            data=data
        )

        # 응답 확인
        api_response.raise_for_status()  # HTTP 에러 발생 시 예외 처리

        print("API 요청 성공!")
        return {
            'status_code': api_response.status_code,
            'response': api_response.json() if api_response.headers.get('content-type', '').startswith('application/json') else api_response.text
        }

    except NoCredentialsError:
        error_msg = "AWS 자격 증명을 찾을 수 없습니다."
        print(f"에러: {error_msg}")
        return {'error': error_msg}

    except ClientError as e:
        error_msg = f"S3 클라이언트 에러: {e}"
        print(f"에러: {error_msg}")
        return {'error': error_msg}

    except requests.exceptions.RequestException as e:
        error_msg = f"API 요청 에러: {e}"
        print(f"에러: {error_msg}")
        return {'error': error_msg}

    except Exception as e:
        error_msg = f"예상치 못한 에러: {e}"
        print(f"에러: {error_msg}")
        return {'error': error_msg}


# 사용 예시
if __name__ == "__main__":
    # 함수 호출 예시
    result = send_s3_file_to_api(
        s3_file_key="",  # S3 파일 경로
        bucket_name="",              # S3 버킷 이름
        aws_access_key_id="",  # AWS Access Key
        aws_secret_access_key="",  # AWS Secret Key
        amount="12200",
        date="20250807",
        seller="커피빈코리아",
        item="커피빈카노노"
    )

    print("결과:", result)