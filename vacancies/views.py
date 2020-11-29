from collections import Counter
from django.shortcuts import render
from django.http import Http404

from vacancies.models import Company, Vacancy, Speciality

from data import WEBSITE_TITLE


def get_base_context():
    return {
            'website_title': WEBSITE_TITLE,
    }


def get_vacancy_preview_info():
    specs = [vac.specialty.code for vac in Vacancy.objects.all()]
    specs_cnt = dict(Counter(specs))

    specs_info = []
    for spec_code, spec_num in specs_cnt.items():
        # Assume the object exists (!)
        name = Speciality.objects.get(code=spec_code).title
        specs_info.append({'code': spec_code, 'name': name, "num": spec_num})
 
    return {"specialties": specs_info}


def get_company_preview_info():
    companies = [vac.company.name for vac in Vacancy.objects.all()]
    company_cnt = Counter(companies)
    company_info = []
    for company in Company.objects.all():
        num = company_cnt[company.name]
        if not num:
            continue
        company_info.append({
            "name": company.name,
            "logo": company.logo,
            "num": num
        })
    return {"companies": company_info}


def get_all_vacancies_info():
    info = [{
            "id": vac.id,
            "title": vac.title,
            "specialty": vac.specialty.title,
            "skills": vac.skills,
            "salary_min": vac.salary_min,
            "salary_max": vac.salary_max,
            "date": vac.published_at,
            "company_logo": vac.company.logo} for vac in Vacancy.objects.all()]
    return {"vacancies": info, "total": len(info)}


def main_view(request):
    context_data = {**get_base_context(),
                    **get_company_preview_info(),
                    **get_vacancy_preview_info()}
    return render(request, "vacancies/index.html", context=context_data)


def company_view(request, company):
    context_data = {**get_base_context(),
                    **get_all_vacancies_info()}

    print("Company: ", company)
    company = Company.objects.get(name=company)
    if company is None:
        raise Http404("404: Company doesn't exist.")
    company_info = {
            "name": company.name,
            "location": company.location,
            "logo": company.logo
    }
    context_data.update(company_info)

    vacancy_info = []
    for vac in Vacancy.objects.filter(company=company):
            vacancy_info.append({
                "id": vac.id,
                "title": vac.title,
                "specialty": vac.specialty.title,
                "skills": vac.skills,
                "salary_min": vac.salary_min,
                "salary_max": vac.salary_max,
                "date": vac.published_at,
                "company_logo": vac.company.logo})
    context_data.update({"vacancies": vacancy_info, "total": len(vacancy_info)})

    return render(request, "vacancies/company.html", context=context_data)


def vacancies(request):
    context_data = {**get_base_context(),
                    **get_all_vacancies_info()}
    return render(request, "vacancies/vacancies.html", context=context_data)


def vacancy_category(request, category):
    context_data = get_base_context()

    speciality = Speciality.objects.get(code=category)
    if speciality is None:
        raise Http404("404: Category doesn't exist.")
  
    vacancy_info = []
    for vac in Vacancy.objects.all():
        if vac.specialty == speciality:
            vacancy_info.append({
                "id": vac.id,
                "title": vac.title,
                "specialty": vac.specialty.title,
                "skills": vac.skills,
                "salary_min": vac.salary_min,
                "salary_max": vac.salary_max,
                "date": vac.published_at,
                "company_logo": vac.company.logo}
            )

    context_data.update({"vacancies": vacancy_info, "spec": speciality.title, "total": len(vacancy_info)})

    return render(request, "vacancies/vacancy_category.html", context=context_data)


def vacancy_view(request, id):
    context_data = get_base_context()

    vacancy = Vacancy.objects.get(pk=id)
    if vacancy is None:
        raise Http404("404: Position doesn't exist.")
    
    vacancy_info = {
            "title": vacancy.title,
            "spec": vacancy.specialty.title,
            "salary_min": vacancy.salary_min,
            "salary_max": vacancy.salary_max,
            "skills": vacancy.skills,
            "text": vacancy.text,
            "company_name": vacancy.company.name,
            "company_logo": vacancy.company.logo,
    }
    context_data.update(vacancy_info)

    return render(request, "vacancies/vacancy.html", context=context_data)
