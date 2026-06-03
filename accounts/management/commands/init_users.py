from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import User

UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Initialize default users for the system'

    def handle(self, *args, **options):
        # Create admin user
        if not UserModel.objects.filter(username='admin').exists():
            admin = UserModel.objects.create_superuser(
                username='admin',
                email='admin@edupresence.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                role=User.Role.ADMIN
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin (password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Create coordinator user
        if not UserModel.objects.filter(username='coordenador').exists():
            coordinator = UserModel.objects.create_user(
                username='coordenador',
                email='coordenador@edupresence.com',
                password='coord123',
                first_name='João',
                last_name='Coordenador',
                role=User.Role.COORDENADOR
            )
            self.stdout.write(self.style.SUCCESS(f'Created coordinator user: coordenador (password: coord123)'))
        else:
            self.stdout.write(self.style.WARNING('Coordinator user already exists'))

        # Create teacher user
        if not UserModel.objects.filter(username='professor').exists():
            teacher = UserModel.objects.create_user(
                username='professor',
                email='professor@edupresence.com',
                password='prof123',
                first_name='Maria',
                last_name='Silva',
                role=User.Role.PROFESSOR
            )
            self.stdout.write(self.style.SUCCESS(f'Created teacher user: professor (password: prof123)'))
        else:
            self.stdout.write(self.style.WARNING('Teacher user already exists'))

        self.stdout.write(self.style.SUCCESS('User initialization complete!'))
