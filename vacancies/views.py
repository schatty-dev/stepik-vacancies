from collections import Counter
from django.shortcuts import render

from vacancies.models import Company, Vacancy, Speciality


def get_vacancy_preview_info():
    specs = [vac.specialty.title for vac in Vacancy.objects.all()]
    specs_cnt = dict(Counter(specs))
    return {"specialties": specs_cnt}


def get_company_preview_info():
    companies = [vac.company.name for vac in Vacancy.objects.all()]
    company_cnt = Counter(companies)
    company_logos = {}
    for company in Company.objects.all():
        num = company_cnt[company.name]
        if num:
            company_logos[company.logo] = num
    return {"companies": company_logos}


def main_view(request):
    context_data = {**{},
                    **get_company_preview_info(),
                    **get_vacancy_preview_info()}
    return render(request, "vacancies/index.html", context=context_data)


def company_view(request, company):
    context_data = {}
    return render(request, "vacancies/company.html", context=context_data)


def vacancies(request):
    context_data = {}
    return render(request, "vacancies/vacancies.html", context=context_data)


def vacancy_category(request, category):
    context_data = {}
    return render(request, "vacancies/vacancy_category.html", context=context_data)


def vacancy_view(request, id):
    context_data = {}
    return render(request, "vacancies/vacancy.html", context=context_data)
