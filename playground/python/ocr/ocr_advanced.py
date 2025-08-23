#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaddleOCR 고급 모드 - 고정확도 인식 + 이미지 전처리
Python 3.11+ 필수
"""

from typing import Tuple, Optional
import os
import sys
from paddleocr import PaddleOCR

def preprocess_image_for_ocr(image_path: str, output_path: str = None) -> str:
    """
    OCR 인식률 향상을 위한 이미지 전처리

    Args:
        image_path (str): 원본 이미지 경로
        output_path (str): 전처리된 이미지 저장 경로 (None이면 임시 파일)

    Returns:
        str: 전처리된 이미지 경로
    """
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("⚠️  이미지 전처리를 위해 opencv-python을 설치하세요: pip install opencv-python")
        return image_path

    # 이미지 읽기
    img = cv2.imread(image_path)
    if img is None:
        return image_path

    print("🔧 이미지 전처리 중...")

    # 1. 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 노이즈 제거 (가우시안 블러)
    blurred = cv2.GaussianBlur(gray, (1, 1), 0)

    # 3. 대비 향상 (CLAHE - Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)

    # 4. 이진화 (Otsu's method)
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 5. 모폴로지 연산으로 글자 선명화
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # 전처리된 이미지 저장
    if output_path is None:
        import tempfile
        output_path = tempfile.mktemp(suffix='_processed.png')

    cv2.imwrite(output_path, processed)
    print(f"✅ 전처리 완료: {output_path}")

    return output_path

def analyze_image_advanced(image_path: str, use_preprocess: bool = True,
                           high_accuracy: bool = True) -> Tuple[Optional[list], str, dict]:
    """
    고급 모드로 이미지에서 텍스트 분석

    Args:
        image_path (str): 분석할 이미지 파일 경로
        use_preprocess (bool): 이미지 전처리 사용 여부
        high_accuracy (bool): 고정확도 모델 사용 여부

    Returns:
        Tuple[Optional[list], str, dict]: (raw_result, parsed_text, stats)
    """

    # 파일 존재 여부 확인
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {image_path}")

    # 이미지 전처리 (옵션)
    processed_image_path = image_path
    if use_preprocess:
        processed_image_path = preprocess_image_for_ocr(image_path)

    # PaddleOCR 3.x 초기화 (매우 간소화됨)
    if high_accuracy:
        # 고정확도 모드 - 고성능 추론 사용
        try:
            ocr = PaddleOCR(
                use_angle_cls=True,
                lang='korean',
                enable_hpi=True,  # 고성능 추론 활성화 (3.x의 새로운 기능)
            )
            print("🎯 고정확도 모드 (고성능 추론) 실행 중...")
        except Exception:
            # enable_hpi가 지원되지 않는 경우 기본 모드로 폴백
            ocr = PaddleOCR(use_angle_cls=True, lang='korean')
            print("⚡ 기본 모드로 실행 중... (고성능 추론 미지원)")
    else:
        # 기본 모바일 모델
        ocr = PaddleOCR(use_angle_cls=True, lang='korean')
        print("⚡ 기본 모드로 실행 중...")

    # OCR 실행
    print(f"이미지 분석 중: {processed_image_path}")
    raw_result = ocr.ocr(processed_image_path)

    # 텍스트 병합 및 통계 계산
    parsed_text: str = ""
    stats = {
        'total_blocks': 0,
        'avg_confidence': 0.0,
        'min_confidence': 1.0,
        'max_confidence': 0.0,
        'preprocessing': use_preprocess,
        'high_accuracy': high_accuracy
    }

    if raw_result and len(raw_result) > 0:
        result_data = raw_result[0]

        if 'rec_texts' in result_data:
            texts = result_data['rec_texts']
            scores = result_data.get('rec_scores', [])

            stats['total_blocks'] = len(texts)

            # 텍스트 병합
            for text in texts:
                if text and text.strip():
                    parsed_text += text + "\n"

            # 신뢰도 통계
            if scores:
                stats['avg_confidence'] = sum(scores) / len(scores)
                stats['min_confidence'] = min(scores)
                stats['max_confidence'] = max(scores)

    # 마지막 개행문자 제거
    parsed_text = parsed_text.rstrip("\n")

    # 전처리된 임시 파일 정리
    if use_preprocess and processed_image_path != image_path:
        try:
            os.remove(processed_image_path)
            print("🧹 임시 전처리 파일 정리 완료")
        except:
            pass

    return raw_result, parsed_text, stats

def main() -> None:
    """메인 함수 - 고급 모드"""

    if len(sys.argv) < 2:
        print("사용법: python ocr_advanced.py <이미지파일경로> [옵션]")
        print("옵션:")
        print("  --no-preprocess    : 이미지 전처리 비활성화")
        print("  --basic-params     : 기본 추론 사용 (빠름)")
        print("예시:")
        print("  python ocr_advanced.py sample.jpg")
        print("  python ocr_advanced.py sample.jpg --no-preprocess")
        print("  python ocr_advanced.py sample.jpg --basic-params")
        sys.exit(1)

    image_path = sys.argv[1]
    use_preprocess = '--no-preprocess' not in sys.argv
    high_accuracy = '--basic-params' not in sys.argv

    try:
        raw_result, parsed_text, stats = analyze_image_advanced(
            image_path, use_preprocess, high_accuracy
        )

        print("\n" + "="*50)
        print("🚀 고급 모드 분석 결과")
        print("="*50)

        print(f"\n📝 인식된 텍스트:")
        print(parsed_text)

        print(f"\n📊 분석 통계:")
        print(f"   • 인식된 텍스트 블록: {stats['total_blocks']}개")
        print(f"   • 평균 신뢰도: {stats['avg_confidence']:.1%}")
        print(f"   • 최고 신뢰도: {stats['max_confidence']:.1%}")
        print(f"   • 최저 신뢰도: {stats['min_confidence']:.1%}")
        print(f"   • 이미지 전처리: {'적용' if stats['preprocessing'] else '미적용'}")
        print(f"   • 모델 유형: {'고정확도 파라미터' if stats['high_accuracy'] else '기본 파라미터'}")

        # 결과 저장
        output_file: str = os.path.splitext(image_path)[0] + "_advanced_result.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== 고급 모드 OCR 분석 결과 ===\n\n")
            f.write(f"원본 파일: {image_path}\n")
            f.write(f"모드: 고급 (고정확도)\n")
            f.write(f"이미지 전처리: {'적용' if stats['preprocessing'] else '미적용'}\n")
            f.write(f"모델 유형: {'고성능 추론' if stats['high_accuracy'] else '기본 추론'}\n\n")
            f.write("분석 통계:\n")
            f.write(f"  - 텍스트 블록: {stats['total_blocks']}개\n")
            f.write(f"  - 평균 신뢰도: {stats['avg_confidence']:.1%}\n")
            f.write(f"  - 신뢰도 범위: {stats['min_confidence']:.1%} ~ {stats['max_confidence']:.1%}\n\n")
            f.write("인식된 텍스트:\n")
            f.write(parsed_text + "\n\n")
            f.write("Raw Result:\n")
            f.write(str(raw_result))

        print(f"\n💾 결과 저장: {output_file}")

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()