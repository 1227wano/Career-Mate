import os
import json
import requests
import PyPDF2
from django.conf import settings

class GeminiRecommender:
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', '')
        
        # 도메인 풀네임을 적어야 GMS가 길을 열어준다!
        
        base_url = "https://gms.ssafy.io/gmsapi/generativelanguage.googleapis.com"
        
        self.api_url = f"{base_url}/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"

    def extract_text_from_pdf(self, pdf_path):
        """PDF 파일 경로를 받아 텍스트만 추출합니다."""
        text = ""
        try:
            # 파일이 존재하는지 먼저 확인
            if not os.path.exists(pdf_path):
                return "파일 없음"

            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                # 페이지가 0개이거나 암호화된 경우 대비
                if len(reader.pages) == 0:
                    return "빈 PDF 파일"
                    
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                        
        except Exception as e:
            print(f"📄 [WARNING] PDF 읽기 실패 (파일 깨짐 가능성): {e}")
            return "" # 에러나면 빈 문자열 반환 (서버 멈춤 방지)
            
        return text

    def get_recommendations(self, file_path, job_list_text):
        
        # 1. PDF 텍스트 추출
        resume_text = self.extract_text_from_pdf(file_path)
        
        # ⚠️ PDF가 깨져서 못 읽었을 경우를 대비한 가짜 데이터
        if not resume_text or len(resume_text.strip()) < 10:
            print("⚠️ PDF 내용이 없거나 깨져있습니다. 테스트를 위해 더미 데이터를 사용합니다.")
            resume_text = "이 지원자는 성실하며 웹 개발 경험(Vue.js, Django)이 있습니다."

        example_data = """
        [합격 매칭 예시 1]
        지원자 스펙: 정보처리기사, Java, Spring 프로젝트 경험 2회
        추천 공고: (주)아이티 - 백엔드 개발자 (자격요건: Spring 숙련자 우대)
        매칭 이유: 지원자의 Spring 프로젝트 경험과 자격증이 해당 공고의 기술 스택과 일치함.

        [합격 매칭 예시 2]
        지원자 스펙: JLPT N1, 일본어 통번역 경험, 컴퓨터공학 복수전공
        추천 공고: 글로벌솔루션 - 일본 해외 영업 및 기술지원
        매칭 이유: IT 지식과 수준급 일본어 능력을 동시에 갖추어 해당 직무에 최적임.
        """

        # 2. 프롬프트 작성 (예시 데이터 포함)
        prompt = f"""
        너는 채용 전문가 AI야. 
        먼저 아래 [참고: 합격 매칭 예시]를 읽고, 어떤 기준으로 사람과 공고를 매칭했는지 학습해.
        그 다음 [이력서]와 [채용공고 목록]을 분석해서 가장 적합한 공고 3개를 추천해줘.
        
        JSON 포맷을 엄격히 지켜.

        ---
        [참고: 합격 매칭 예시 (Few-shot Learning)]
        {example_data}
        ---

        [이력서 요약]
        {resume_text[:3000]}

        [채용공고 목록]
        {job_list_text}

        ---
        [응답 양식 - JSON Only]
        {{
            "recommendations": [
                {{
                    "job_id": "공고ID(숫자)",
                    "match_reason": "한국어로 된 추천 사유"
                }}
            ]
        }}
        """

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        headers = {'Content-Type': 'application/json'}

        # 3. GMS 요청 보내기
        try:
            print(f"🚀 [GMS 요청] 보내는 곳: {self.api_url}")
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=120)
            
            if response.status_code != 200:
                print(f"❌ API 에러 응답: {response.status_code} - {response.text}")
                return {"error": f"GMS Error {response.status_code}", "detail": response.text}

            # 4. 결과 파싱
            result_json = response.json()
            try:
                ai_text = result_json['candidates'][0]['content']['parts'][0]['text']
                ai_text = ai_text.replace("```json", "").replace("```", "").strip()
                return json.loads(ai_text)
            except Exception as e:
                print(f"⚠️ 파싱 에러: {e}")
                return {"error": "AI 응답 형식이 이상함", "raw": str(result_json)}

        except Exception as e:
            print(f"❌ 연결 실패: {e}")
            return {"error": str(e)}