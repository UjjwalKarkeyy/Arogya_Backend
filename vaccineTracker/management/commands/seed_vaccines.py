from django.core.management.base import BaseCommand
from vaccineTracker.models import Vaccine

class Command(BaseCommand):
    help = "Seed the database with initial vaccine records"

    def handle(self, *args, **kwargs):
        vaccines_data = [
            {"name": "BCG", "manufacturer": "Serum Institute", "max_doses": 1, "dose_interval_days": 0},
            {"name": "OPV", "manufacturer": "GlaxoSmithKline", "max_doses": 3, "dose_interval_days": 28},
            {"name": "Pentavalent", "manufacturer": "Sanofi Pasteur", "max_doses": 3, "dose_interval_days": 28},
            {"name": "Measles", "manufacturer": "Serum Institute", "max_doses": 2, "dose_interval_days": 28},
            {"name": "MR (Measles-Rubella)", "manufacturer": "Serum Institute", "max_doses": 2, "dose_interval_days": 28},
            {"name": "Hepatitis B", "manufacturer": "GSK", "max_doses": 3, "dose_interval_days": 30},
            {"name": "Hib", "manufacturer": "Sanofi", "max_doses": 3, "dose_interval_days": 28},
            {"name": "PCV (Pneumococcal)", "manufacturer": "Pfizer", "max_doses": 3, "dose_interval_days": 28},
            {"name": "DTP", "manufacturer": "Serum Institute", "max_doses": 3, "dose_interval_days": 28},
            {"name": "DTaP", "manufacturer": "Sanofi", "max_doses": 3, "dose_interval_days": 28},
            {"name": "Influenza (Flu)", "manufacturer": "Sanofi", "max_doses": 1, "dose_interval_days": 0},
            {"name": "COVID-19 (Covishield)", "manufacturer": "Serum Institute", "max_doses": 2, "dose_interval_days": 90},
            {"name": "COVID-19 (Pfizer)", "manufacturer": "Pfizer", "max_doses": 2, "dose_interval_days": 90},
            {"name": "COVID-19 (Moderna)", "manufacturer": "Moderna", "max_doses": 2, "dose_interval_days": 90},
            {"name": "Typhoid Conjugate", "manufacturer": "Bharat Biotech", "max_doses": 1, "dose_interval_days": 0},
            {"name": "Hepatitis A", "manufacturer": "GSK", "max_doses": 2, "dose_interval_days": 180},
            {"name": "Varicella (Chickenpox)", "manufacturer": "Merck", "max_doses": 2, "dose_interval_days": 28},
            {"name": "HPV", "manufacturer": "Merck", "max_doses": 2, "dose_interval_days": 180},
            {"name": "Rabies", "manufacturer": "GSK", "max_doses": 3, "dose_interval_days": 7},
            {"name": "Japanese Encephalitis", "manufacturer": "Bharat Biotech", "max_doses": 2, "dose_interval_days": 28},
            {"name": "Polio IPV", "manufacturer": "Sanofi", "max_doses": 1, "dose_interval_days": 0},
            {"name": "Meningococcal", "manufacturer": "GSK", "max_doses": 2, "dose_interval_days": 28},
            {"name": "Rotavirus", "manufacturer": "GSK", "max_doses": 2, "dose_interval_days": 28},
            {"name": "Hepatitis E", "manufacturer": "China National Biotec", "max_doses": 2, "dose_interval_days": 28},
            {"name": "Td (Tetanus-diphtheria booster)", "manufacturer": "Serum Institute", "max_doses": 1, "dose_interval_days": 0},
            {"name": "Tetanus (TT)", "manufacturer": "Sanofi", "max_doses": 2, "dose_interval_days": 28},
            {"name": "BCG Revaccination", "manufacturer": "Serum Institute", "max_doses": 1, "dose_interval_days": 0},
            {"name": "Influenza (H1N1)", "manufacturer": "Sanofi", "max_doses": 1, "dose_interval_days": 0},
            {"name": "COVID-19 (Johnson & Johnson)", "manufacturer": "J&J", "max_doses": 1, "dose_interval_days": 0},
            {"name": "COVID-19 (Sinopharm)", "manufacturer": "Sinopharm", "max_doses": 2, "dose_interval_days": 28},
        ]

        for vaccine in vaccines_data:
            Vaccine.objects.update_or_create(name=vaccine['name'], defaults=vaccine)

        self.stdout.write(self.style.SUCCESS("Successfully seeded 30 vaccines."))
