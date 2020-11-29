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


def get_vacancy_info(vac_obj):
    return {
            "id": vac_obj.id,
            "title": vac_obj.title,
            "specialty": vac_obj.specialty.title,
            "skills": vac_obj.skills,
            "salary_min": vac_obj.salary_min,
            "salary_max": vac_obj.salary_max,
            "date": vac_obj.published_at,
            "company_logo": vac_obj.company.logo,
            "company_name": vac_obj.company.name
    }


def get_all_vacancies_info():
    info = [get_vacancy_info(vac) for vac in Vacancy.objects.all()]
    return {"vacancies": info, "total": len(info)}


def main_view(request):
    context_data = {**get_base_context(),
                    **get_company_preview_info(),
                    **get_vacancy_preview_info()}
    return render(request, "vacancies/index.html", context=context_data)


def company_view(request, company):
    context_data = {**get_base_context(),
                    **get_all_vacancies_info()}

    company = Company.objects.get(name=company)
    if company is None:
        raise Http404("404: Company doesn't exist.")
    company_info = {
            "name": company.name,
            "location": company.location,
            "logo": company.logo
    }
    print("Info: ", company_info)
    context_data.update(company_info)

    vacancy_info = [get_vacancy_info(vac)
                    for vac in Vacancy.objects.filter(company=company)]
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

    vacancy_info = [get_vacancy_info(vac) for vac in Vacancy.objects.filter(specialty=speciality)]
    context_data.update({
        "vacancies": vacancy_info,
        "spec": speciality.title,
        "total": len(vacancy_info)})

    return render(request, "vacancies/vacancy_category.html", context=context_data)


def vacancy_view(request, id):
    context_data = get_base_context()

    vacancy = Vacancy.objects.get(pk=id)
    if vacancy is None:
        raise Http404("404: Position doesn't exist.")
    
    context_data.update(get_vacancy_info(vacancy))

    return render(request, "vacancies/vacancy.html", context=context_data)
