# files/management/commands/notify_expired_files.py
from collections import defaultdict
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

from files.models import Arquivo

# Define the notification thresholds (in days)
THRESHOLDS = [7, 3, 0]  # 7 days left, 3 days left, and expiration day


class Command(BaseCommand):
    help = "Notify company representatives and admin about files nearing or at expiration."

    def handle(self, *args, **options):
        today = timezone.now().date()
        notifications = defaultdict(list)  # {empresa: [(arquivo, days_left), ...]}

        # For each threshold, query the Arquivo objects that hit the target date.
        for days in THRESHOLDS:
            target_date = today + timedelta(days=days)
            arquivos = Arquivo.objects.filter(validade=target_date)
            for arquivo in arquivos:
                notifications[arquivo.cliente].append((arquivo, days))

        if not notifications:
            self.stdout.write("No files meet the notification criteria today.")
            return

        # Send notifications per Empresa (i.e. company)
        for empresa, arquivo_list in notifications.items():
            # Get all representatives (via the "workers" related name)
            representantes = empresa.workers.all()
            rep_emails = [rep.email for rep in representantes if rep.email]
            if rep_emails:
                subject = "Alert: Files Approaching Expiration"
                message_lines = [
                    f"Dear representative of {empresa.nome_fantasia},",
                    "",
                    "The following files are nearing or have reached their expiration date:",
                    "",
                ]
                for arquivo, days_left in arquivo_list:
                    if days_left == 7:
                        status = "will expire in 7 days"
                    elif days_left == 3:
                        status = "will expire in 3 days"
                    elif days_left == 0:
                        status = "expires today"
                    else:
                        status = f"expires in {days_left} days"
                    message_lines.append(
                        f" - {arquivo.nome} (Uploaded: {arquivo.data_upload.date()}, Expiration: {arquivo.validade}) → {status}"
                    )
                message_lines.append("")
                message_lines.append("Please log in to the portal for more details.")
                message = "\n".join(message_lines)

                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        rep_emails,
                        fail_silently=False,
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f"Notification sent to representatives of {empresa.nome_fantasia}: {rep_emails}"
                    ))
                except Exception as e:
                    self.stderr.write(f"Error sending email to {empresa.nome_fantasia}: {e}")

        # Notify admin using a dedicated admin email setting (e.g. settings.EXPIRATION_NOTIFICATION_ADMIN)
        admin_email = getattr(settings, "EXPIRATION_NOTIFICATION_ADMIN", None)
        if admin_email:
            subject = "Daily Report: Files Approaching Expiration"
            message_lines = [
                "Dear Admin,",
                "",
                "The following files have reached one of the notification thresholds today:",
                "",
            ]
            # For admin, we can list all files across companies.
            for empresa, arquivo_list in notifications.items():
                for arquivo, days_left in arquivo_list:
                    if days_left == 7:
                        status = "7 days left"
                    elif days_left == 3:
                        status = "3 days left"
                    elif days_left == 0:
                        status = "expires today"
                    else:
                        status = f"{days_left} days left"
                    message_lines.append(
                        f" - {arquivo.nome} (Company: {empresa.nome_fantasia}, Uploaded: {arquivo.data_upload.date()}, Expiration: {arquivo.validade}) → {status}"
                    )
            message = "\n".join(message_lines)
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS("Admin notification sent."))
            except Exception as e:
                self.stderr.write(f"Error sending admin email: {e}")
        else:
            self.stdout.write("No EXPIRATION_NOTIFICATION_ADMIN email configured in settings.")
