from django.core.management.base import BaseCommand
from adminapp.models import SubscriptionPlan

class Command(BaseCommand):
    help = 'Seed subscription plans'

    def handle(self, *args, **options):
        plans = [
            # Assistant Plans
            {
                'name': 'Assistant Monthly',
                'plan_type': 'assistant',
                'duration': 'monthly',
                'price': 100,
                'features': 'Basic profile listing\nCustomer contact access\nUp to 10 service posts\nStandard support\nBasic analytics',
            },
            {
                'name': 'Assistant 6 Months',
                'plan_type': 'assistant',
                'duration': 'half_yearly',
                'price': 549,
                'features': 'Basic profile listing\nCustomer contact access\nUp to 10 service posts\nStandard support\nBasic analytics',
            },
            {
                'name': 'Assistant Yearly',
                'plan_type': 'assistant',
                'duration': 'yearly',
                'price': 999,
                'features': 'Basic profile listing\nCustomer contact access\nUp to 10 service posts\nStandard support\nBasic analytics',
            },
            # Professional Plans
            {
                'name': 'Professional Monthly',
                'plan_type': 'professional',
                'duration': 'monthly',
                'price': 99,
                'features': 'Enhanced profile visibility\nUnlimited service posts\nPriority customer matching\nAdvanced analytics & insights\n24/7 priority support\nLead generation tools\nPerformance dashboard',
            },
            {
                'name': 'Professional 6 Months',
                'plan_type': 'professional',
                'duration': 'half_yearly',
                'price': 499,
                'features': 'Enhanced profile visibility\nUnlimited service posts\nPriority customer matching\nAdvanced analytics & insights\n24/7 priority support\nLead generation tools\nPerformance dashboard',
            },
            {
                'name': 'Professional Yearly',
                'plan_type': 'professional',
                'duration': 'yearly',
                'price': 949,
                'features': 'Enhanced profile visibility\nUnlimited service posts\nPriority customer matching\nAdvanced analytics & insights\n24/7 priority support\nLead generation tools\nPerformance dashboard',
            },
        ]

        for plan in plans:
            SubscriptionPlan.objects.update_or_create(
                name=plan['name'],
                defaults=plan
            )
        self.stdout.write(self.style.SUCCESS('Subscription plans seeded successfully.'))