from collections import Counter

from django.http import Http404, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

from vacancies.models import Company, Vacancy, Speciality
from data import WEBSITE_TITLE


def get_base_context():
    """Get context that every page uses. """
    return {
            'website_title': WEBSITE_TITLE,
    }


def get_vacancy_preview_info():
    """Get info for previewing positions per specialty for main page. """
    specs = [vac.specialty.code for vac in Vacancy.objects.all()]
    specs_cnt = dict(Counter(specs))

    specs_info = []
    for spec_code, spec_num in specs_cnt.items():
        # Assume the object exists (!)
        name = Speciality.objects.get(code=spec_code).title
        specs_info.append({'code': spec_code, 'name': name, "num": spec_num})

    return {"specialties": specs_info}


def get_company_preview_info():
    """Get info for previewing positions per company for main page. """
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


''' ------ Views ------- '''


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        return get_base_context()


class BaseDetailView(DetailView):
    """A base view for a single object + base context. """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update(get_base_context())
        return self.render_to_response(context)


class MainView(BaseView):
    template_name = "vacancies/index.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context.update(get_company_preview_info())
        context.update(get_vacancy_preview_info())
        return context


class CompanyView(BaseView):
    template_name = "vacancies/company.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        try:
            company = kwargs.get("company")
            company = Company.objects.get(name=company)
            if company is None:
                raise Http404("404: Company doesn't exist.")
        except Exception as e:
            raise HttpResponse(e, status=500)

        company_info = {
                "name": company.name,
                "location": company.location,
                "logo": company.logo
        }
        context.update(company_info)

        vacancies = Vacancy.objects.filter(company=company)
        context.update({"vacancies": vacancies, "total": len(vacancies)})

        return context


class AllPositionsView(BaseView):
    template_name = "vacancies/vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(AllPositionsView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        context['title'] = "All Positions"
        return context


class SpecialtyPositionsView(BaseView):
    """View for 'Positions for Category' """
    template_name = "vacancies/vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(SpecialtyPositionsView, self).get_context_data(**kwargs)

        try:
            specialty = kwargs.get("specialty")
            spec_obj = Speciality.objects.get(code=specialty)
            if spec_obj is None:
                raise Http404("404: Category doesn't exist.")
        except Exception as e:
            raise HttpResponse(e, status=500)

        context.update({
            "vacancies": Vacancy.objects.filter(specialty=spec_obj),
            "title": spec_obj.title,
        })
        return context


class PositionView(BaseDetailView):
    """View for 'Single Position' page. """

    template_name = "vacancies/vacancy.html"
    model = Vacancy
