from django.shortcuts import render

# Create your views here.


def main_view(request):
    context_data = {}
    return render(request, "vacancies/index.html", context=context_data)


def company_view(request, name):
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
