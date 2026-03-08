from django.db import models
from companies.models import Company

# 채용공고 테이블
class Job(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        db_column='company_id', # DB에는 'company_id'라는 컬럼명으로 저장됨
        related_name='jobs'     # company.jobs.all() 로 해당 기업의 공고 조회 가능
    )
    
    jobs_title = models.CharField(max_length=100)
    jobs_link = models.URLField(unique=True, max_length=500) 
    jobs_addr = models.CharField(max_length=100)
    jobs_type = models.CharField(max_length=100)
    jobs_date = models.DateTimeField()
    jobs_exp = models.CharField(max_length=100)
    jobs_edu = models.CharField(max_length=100)

    def __str__(self):
        return self.jobs_title