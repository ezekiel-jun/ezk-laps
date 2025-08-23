#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR 테스트 프로그램 - 기본/고급 모드 테스트 함수
"""

import sys
import os

# 현재 디렉토리를 Python path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ocr_basic import analyze_image_basic
from ocr_advanced import analyze_image_advanced

def test_basic_mode(image_path: str):
    """기본 모드 테스트"""
    print("🟢 기본 모드 테스트")
    print("=" * 50)

    try:
        raw_result, parsed_text = analyze_image_basic(image_path)

        print(f"\n📝 인식된 텍스트:")
        print(parsed_text)

        # 기본 통계
        if raw_result and len(raw_result) > 0:
            result_data = raw_result[0]
            if 'rec_texts' in result_data:
                print(f"\n📊 인식된 텍스트 블록 수: {len(result_data['rec_texts'])}개")

                # 각 텍스트별 신뢰도 표시
                if 'rec_scores' in result_data:
                    print("\n각 텍스트와 신뢰도:")
                    for i, (text, score) in enumerate(zip(result_data['rec_texts'], result_data['rec_scores'])):
                        if text and text.strip():
                            print(f"  {i+1}. '{text}' (신뢰도: {score:.1%})")

        print("\n✅ 기본 모드 테스트 완료")

    except FileNotFoundError:
        print(f"❌ 파일이 없습니다: {image_path}")
    except Exception as e:
        print(f"❌ 기본 모드 오류: {e}")

def test_advanced_mode(image_path: str):
    """고급 모드 테스트"""
    print("\n🔥 고급 모드 테스트")
    print("=" * 50)

    # 여러 고급 모드 옵션 테스트
    test_configs = [
        {"name": "전처리 + 고성능 추론", "preprocess": True, "accuracy": True, "emoji": "🔥"},
        {"name": "고성능 추론만", "preprocess": False, "accuracy": True, "emoji": "🎯"},
        {"name": "전처리만", "preprocess": True, "accuracy": False, "emoji": "🔧"},
    ]

    results = []

    for config in test_configs:
        print(f"\n{config['emoji']} {config['name']} 테스트 중...")
        print("-" * 40)

        try:
            raw_result, parsed_text, stats = analyze_image_advanced(
                image_path,
                use_preprocess=config['preprocess'],
                high_accuracy=config['accuracy']
            )

            print(f"\n📝 인식된 텍스트:")
            print(parsed_text)

            print(f"\n📊 분석 통계:")
            print(f"   • 텍스트 블록: {stats['total_blocks']}개")
            print(f"   • 평균 신뢰도: {stats['avg_confidence']:.1%}")
            print(f"   • 신뢰도 범위: {stats['min_confidence']:.1%} ~ {stats['max_confidence']:.1%}")

            results.append({
                'name': config['name'],
                'avg_confidence': stats['avg_confidence'],
                'total_blocks': stats['total_blocks'],
                'success': True
            })

        except FileNotFoundError:
            print(f"❌ 파일이 없습니다: {image_path}")
            results.append({'name': config['name'], 'success': False})
        except Exception as e:
            print(f"❌ {config['name']} 오류: {e}")
            results.append({'name': config['name'], 'success': False})

    # 결과 비교
    print(f"\n🏆 고급 모드 결과 비교")
    print("=" * 50)
    print(f"{'모드':<25} {'신뢰도':<10} {'텍스트 블록'}")
    print("-" * 45)

    for result in results:
        if result['success']:
            print(f"{result['name']:<25} {result['avg_confidence']:<9.1%} {result['total_blocks']}개")
        else:
            print(f"{result['name']:<25} {'실패':<10} -")

    print("\n✅ 고급 모드 테스트 완료")

def test_comparison(image_path: str):
    """기본 vs 고급 모드 비교 테스트"""
    print("\n⚡ vs 🔥 기본 모드 vs 고급 모드 비교")
    print("=" * 50)

    print("1️⃣ 기본 모드 실행 중...")
    try:
        basic_result, basic_text = analyze_image_basic(image_path)
        basic_success = True
        basic_blocks = 0
        if basic_result and len(basic_result) > 0:
            result_data = basic_result[0]
            if 'rec_texts' in result_data:
                basic_blocks = len(result_data['rec_texts'])
    except Exception as e:
        print(f"❌ 기본 모드 오류: {e}")
        basic_success = False

    print("\n2️⃣ 고급 모드 (최고 성능) 실행 중...")
    try:
        advanced_result, advanced_text, advanced_stats = analyze_image_advanced(
            image_path, use_preprocess=True, high_accuracy=True
        )
        advanced_success = True
    except Exception as e:
        print(f"❌ 고급 모드 오류: {e}")
        advanced_success = False

    # 비교 결과
    print(f"\n🔍 비교 결과")
    print("=" * 50)

    if basic_success and advanced_success:
        print(f"{'항목':<20} {'기본 모드':<15} {'고급 모드'}")
        print("-" * 50)
        print(f"{'처리 시간':<20} {'빠름':<15} {'느림'}")
        print(f"{'모델 크기':<20} {'작음':<15} {'큼'}")
        print(f"{'텍스트 블록 수':<20} {basic_blocks:<15} {advanced_stats['total_blocks']}")
        print(f"{'평균 신뢰도':<20} {'-':<15} {advanced_stats['avg_confidence']:.1%}")
        print(f"{'전처리 적용':<20} {'없음':<15} {'있음' if advanced_stats['preprocessing'] else '없음'}")

        print(f"\n💡 권장사항:")
        if advanced_stats['avg_confidence'] > 0.9:
            print("   🔥 고급 모드: 높은 신뢰도가 필요한 경우")
        print("   ⚡ 기본 모드: 빠른 처리가 필요한 경우")
    else:
        print("❌ 비교 테스트 실행 실패")

def test_all(image_path: str):
    """모든 테스트를 순차 실행"""
    print("🔍 PaddleOCR 전체 테스트 프로그램")
    print("=" * 50)

    # 이미지 파일 존재 확인
    if not os.path.exists(image_path):
        print(f"⚠️  테스트 이미지가 없습니다: {image_path}")
        print("테스트를 위해 이미지 파일을 준비해주세요.")
        return

    print(f"🖼️  테스트 이미지: {image_path}")

    # 1. 기본 모드 테스트
    test_basic_mode(image_path)

    # 2. 고급 모드 테스트
    test_advanced_mode(image_path)

    # 3. 비교 테스트
    test_comparison(image_path)

    print(f"\n🎉 모든 테스트가 완료되었습니다!")
    print("=" * 50)

def main():
    """메인 함수 - 개별 테스트 선택 실행"""

    # 기본 이미지 파일 경로
    image_path = "images/ocr_test_01.png"

    # 개별 테스트 함수들 (주석을 해제하여 실행)

    # 1. 기본 모드만 테스트
    # test_basic_mode(image_path)

    # 2. 고급 모드만 테스트
    test_advanced_mode(image_path)

    # 3. 비교 테스트만 실행
    # test_comparison(image_path)

    # 4. 모든 테스트 실행
    # test_all(image_path)

if __name__ == "__main__":
    main()