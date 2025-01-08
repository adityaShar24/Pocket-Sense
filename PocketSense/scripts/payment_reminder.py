from datetime import datetime , timedelta

from django.core.mail import send_mail
from django.db.models import Q
from django.conf import settings

from expenses.enums import (
    PaymentStatusEnum
)
from expenses.models import (
    Settlement,
)

def send_payment_reminders():
    reminder_date = datetime.now().date() + timedelta(days=3)

    pending_settlements = Settlement.objects.filter(
        Q(payment_status=PaymentStatusEnum.Pending.value) & Q(due_date=reminder_date)
    )

    if not pending_settlements.exists():
        print("No settlements require reminders for the given date.")
        return

    for settlement in pending_settlements:
        borrower = settlement.borrower
        lender = settlement.user
        amount = settlement.amount
        due_date = settlement.due_date

        subject = f"Payment Reminder: Settlement Due on {due_date}"
        message = (
            f"Dear {borrower.username},\n\n"
            f"This is a reminder that your payment of ₹{amount:.2f} "
            f"to {lender.username} is due on {due_date}.\n\n"
            f"Please ensure the payment is made on time to avoid further reminders.\n\n"
            f"Thank you!"
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [borrower.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            print(f"Payment reminder sent to {borrower.username} ({borrower.email}).")
        except Exception as e:
            print(f"Failed to send email to {borrower.username} ({borrower.email}): {e}")
            
def run():
    send_payment_reminders()