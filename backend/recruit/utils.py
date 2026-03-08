import feedparser
import requests
import re
from time import mktime
from datetime import datetime, date

# Django 관련 모듈 import
from django.utils import timezone
from .models import Job
from companies.models import Company


# 1. 헬퍼 함수들 (날짜 변환, 근무형태 분석)

def parse_deadline(date_str):
    """
    RSS의 '01/21(수)' 또는 '상시' 같은 문자열을 
    Django DB에 저장할 수 있는 datetime 객체로 변환
    """
    today = date.today()
    
    if "상시" in date_str or "채용" in date_str:
        return datetime(9999, 12, 31)

    try:
        match = re.search(r'(\d{1,2})/(\d{1,2})', date_str)
        if match:
            month, day = map(int, match.groups())
            year = today.year
            if today.month > month: 
                year += 1
            return datetime(year, month, day)
    except Exception:
        pass
        
    return datetime(9999, 12, 31)

def parse_job_type(title):
    if '계약직' in title:
        return '계약직'
    elif '임시직' in title:
        return '임시직'
    elif '인턴' in title:
        return '인턴'
    else:
        return '정규직'


# 2. RSS 데이터 크롤링 함수
def get_incruit_rss_data():
    rss_url = "https://www.incruit.com/rss/job.asp?jobtycd=1&today=y"
    headers = { "User-Agent": "Mozilla/5.0" }
    
    try:
        response = requests.get(rss_url, headers=headers)
        feed = feedparser.parse(response.content)
        
        jobs_data = []

        for entry in feed.entries:
            title = entry.get('title', '제목 없음')
            link = entry.get('link', '')
            company = entry.get('author', '회사명 없음')
            
            # 날짜 파싱
            published_at = timezone.now()
            if hasattr(entry, 'published_parsed'):
                dt = datetime.fromtimestamp(mktime(entry.published_parsed))
                published_at = timezone.make_aware(dt) if timezone.is_naive(dt) else dt

            # 상세 정보 파싱
            summary = entry.get('summary', '')
            
            career_match = re.search(r'경력 : (.*?)<br', summary)
            edu_match = re.search(r'학력 : (.*?)<br', summary)
            loc_match = re.search(r'지역 : (.*?)<br', summary)
            deadline_match = re.search(r'마감일 : (.*?)<br', summary)

            career = career_match.group(1).strip() if career_match else "정보 없음"
            education = edu_match.group(1).strip() if edu_match else "정보 없음"
            location = loc_match.group(1).strip() if loc_match else "정보 없음"
            deadline_str = deadline_match.group(1).strip() if deadline_match else "정보 없음"
            
            location = location.replace('|', '').replace('>', ' ')

            job_type = parse_job_type(title)

            jobs_data.append({
                "company": company,
                "title": title,
                "link": link,
                "published_at": published_at,
                "career": career,
                "education": education,
                "location": location,
                "deadline": deadline_str,
                "job_type": job_type
            })
            
        return jobs_data

    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []


# 3. DB 저장 및 관리 함수
def save_jobs_to_db():
    rss_data_list = get_incruit_rss_data()
    new_count = 0
    
    for item in rss_data_list:
        # A. 기업 정보
        company_obj, created = Company.objects.get_or_create(
            company_name=item['company'],
            defaults={
                'company_addr': item['location']
            }
        )

        # B. 중복 확인
        if Job.objects.filter(jobs_link=item['link']).exists():
            continue 

        # C. 마감일 변환
        deadline_dt = parse_deadline(item['deadline'])
        if timezone.is_naive(deadline_dt):
            deadline_dt = timezone.make_aware(deadline_dt)

        # D. 공고 저장
        Job.objects.create(
            company=company_obj,
            jobs_title=item['title'],
            jobs_link=item['link'],
            jobs_addr=item['location'],
            jobs_type=item['job_type'],
            jobs_date=deadline_dt,
            jobs_exp=item['career'],
            jobs_edu=item['education'],
        )
        new_count += 1

    print(f"=== [업데이트 완료] {new_count}개의 신규 공고 저장됨 ===")
    delete_expired_jobs()


def delete_expired_jobs():
    now = timezone.now()
    expired_jobs = Job.objects.filter(jobs_date__lt=now)
    count = expired_jobs.count()
    
    if count > 0:
        expired_jobs.delete()
        print(f"=== [청소 완료] 기한 만료된 공고 {count}개 삭제됨 ===")
    else:
        print("=== [청소 완료] 삭제할 만료 공고 없음 ===")