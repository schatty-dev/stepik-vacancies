from copy import copy
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
import django
django.setup()
import argparse

from vacancies.models import Speciality, Company, Vacancy
from data import jobs, companies, specialties


def fill_db():
    print("Jobs: ", len(jobs))
    print("Companies: ", len(companies))
    print("Specialities: ", len(specialties))

    for company in companies:
        try:
            Company.objects.create(**company)
        except Exception as e:
            print(f"Failed to load object {company['id']}: {e}")
    else:
        print("Companies added.")

    for spec in specialties:
        try:
            Speciality.objects.create(**spec)
        except Exception as e:
            print(f"Failed to load object {spec['id']}: {e}")
    else:
        print("Specialities added.")

    for job in jobs:
        try:
            # Find fk objects
            company = Company.objects.get(pk=job["company"])
            specialty = Speciality.objects.get(code=job["specialty"])

            # Prepare valid object with foreign keys
            vacancy = copy(job)
            vacancy["company"] = company
            vacancy["specialty"] = specialty
            vacancy["text"] = job["description"]
            del vacancy["description"]
            Vacancy.objects.create(**vacancy)
        except Exception as e:
            print(f"Failed to load object {job['id']}: {e}")
    else:
        print("Vacancies added.")


def clean_db():
    Vacancy.objects.all().delete()
    Company.objects.all().delete()
    Speciality.objects.all().delete()
    print("All DB data removed.")


parser = argparse.ArgumentParser(description='Run training')
parser.add_argument("--clear", default=False, action="store_true",
                    help="Command to clean DB instead of filling it.")


if __name__ == "__main__":
    args = parser.parse_args()
    print("Args: ", args)

    if args.clear:
        clean_db()
    else:
        fill_db()
