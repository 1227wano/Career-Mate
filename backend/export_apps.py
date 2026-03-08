import json
import os
import subprocess
import sys

# 앱 이름만 적는 대신, (저장할_파일명, 추출할_구체적_모델명) 형식으로 변경
TARGET_INFO = [
    # (파일명, 앱이름.모델명)
    ('companies', 'companies.Company'),
    ('recruit', 'recruit.Job'),
]

def export_apps_to_json():
    # 현재 실행 중인 Python의 경로 (가상환경의 python.exe)
    python_executable = sys.executable 

    for app_name, target_model in TARGET_INFO:
        output_file = f"{app_name}.json"
        print(f"[{target_model}] 데이터를 {output_file}로 추출 중입니다...")

        try:
            # dumpdata 뒤에 앱 이름 대신 구체적인 모델명(target_model)을 넣음
            result = subprocess.run(
                [python_executable, '-Xutf8', 'manage.py', 'dumpdata', target_model, '--indent', '2'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                print(f"{target_model} 추출 실패: {result.stderr}")
                continue

            # 결과가 비어있는 경우 처리
            if not result.stdout.strip():
                print(f"주의: {target_model}에 대한 데이터가 없습니다.")
                continue

            data = json.loads(result.stdout)

            # PK 순으로 정렬
            data.sort(key=lambda x: x['pk'])

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"저장 완료: {output_file} (데이터: {len(data)}개)")

        except Exception as e:
            print(f"오류 발생 ({target_model}): {str(e)}")

if __name__ == "__main__":
    export_apps_to_json()