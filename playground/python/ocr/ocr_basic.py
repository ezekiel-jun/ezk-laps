#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaddleOCR 기본 모드 - 빠른 인식
Python 3.11+ 필수
"""

from typing import Tuple, Optional
import os
import sys
from paddleocr import PaddleOCR

def analyze_image_basic(image_path: str) -> Tuple[Optional[list], str]:
    """
    기본 모드로 이미지에서 텍스트 분석

    Args:
        image_path (str): 분석할 이미지 파일 경로

    Returns:
        Tuple[Optional[list], str]: (raw_result, parsed_text)
    """

    # 파일 존재 여부 확인
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {image_path}")

    # PaddleOCR 초기화 (기본 모바일 모델)
    ocr = PaddleOCR(use_angle_cls=True, lang='korean')
    print("⚡ 기본 모드로 실행 중... (빠른 인식)")

    # OCR 실행
    print(f"이미지 분석 중: {image_path}")
    raw_result = ocr.ocr(image_path)

    # 텍스트 병합 (PaddleOCR 3.x 구조)
    parsed_text: str = ""
    if raw_result and len(raw_result) > 0:
        result_data = raw_result[0]

        if 'rec_texts' in result_data:
            texts = result_data['rec_texts']
            for text in texts:
                if text and text.strip():
                    parsed_text += text + "\n"

    # 마지막 개행문자 제거
    parsed_text = parsed_text.rstrip("\n")

    return raw_result, parsed_text

def main() -> None:
    """메인 함수 - 기본 모드"""

    if len(sys.argv) != 2:
        print("사용법: python ocr_basic.py <이미지파일경로>")
        print("예시: python ocr_basic.py sample.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        raw_result, parsed_text = analyze_image_basic(image_path)

        print("\n" + "="*50)
        print("📋 기본 모드 분석 결과")
        print("="*50)

        print(f"\n📝 인식된 텍스트:")
        print(parsed_text)

        # 기본 통계
        if raw_result and len(raw_result) > 0:
            result_data = raw_result[0]
            if 'rec_texts' in result_data:
                print(f"\n📊 인식된 텍스트 블록 수: {len(result_data['rec_texts'])}")

        # 결과 저장
        output_file: str = os.path.splitext(image_path)[0] + "_basic_result.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== 기본 모드 OCR 분석 결과 ===\n\n")
            f.write(f"원본 파일: {image_path}\n")
            f.write(f"모드: 기본 (빠른 인식)\n\n")
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