from django.db.models import Count
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.shortcuts import render
from accounts.models import LsSettings , LsUser
from wishlist.models import LsWishlist
from emails.models import LsEmailForSend
from orders.models import LsOrder,LsOrderItems
from products.models import LsCategoryes,LsProduct,lsProductImage
from datetime import datetime
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import email.message
from django.template.loader import render_to_string
import smtplib
from luckhunter import settings
# Create your views here.

@csrf_exempt
def test_email(request):
    status = send_email_for_winner_information()
    status = send_email_for_order_booking()
    status = send_email_for_register_user()
    status = send_email_for_booking_start_notification()
    
    
   
    return HttpResponse("test")



def send_email_for_winner_information():
    if LsEmailForSend.objects.filter(Email_status=False).exists():
        get_system_info = LsSettings.objects.all().first()
        get_emails = LsEmailForSend.objects.filter(Email_status=False)[0:2]
        for item in get_emails:
            ################################################ EMAL SEND CODE START ##############
            if item.email_id == "":
                test = ""
            else:    
                content = {'get_system_info': get_system_info, "yourname": item.user.name, "BASE_URL": settings.BASE_URL,"get_emails": item}
                email_content = render_to_string("email_template/email_send_for_winners.html", content)
                msg = email.message.Message()
                msg['Subject'] = 'Winner'+get_system_info.Title
                msg['From'] = settings.EMAIL_HOST_USER
                msg['To'] = item.email_id
                password =settings.EMAIL_HOST_PASSWORD
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(email_content)
                s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                s.starttls()
                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string())
            LsEmailForSend.objects.filter(id=item.id).update(Email_status=True)
            ################################################ EMAL SEND CODE END ##############
    return True

def send_email_for_order_booking():
    if LsOrder.objects.filter(Mail_send_status=False).filter(payment_status=True).exists():
        get_system_info = LsSettings.objects.all().first()
        get_content =  LsOrder.objects.filter(Mail_send_status=False).filter(payment_status=True)[0:2]
        print(get_content)
        for item in get_content:
            get_user_info = get_object_or_404(LsUser, id=item.user.id)
            get_item_of_this_order = None
            if LsOrderItems.objects.filter(order_id=item).exists():
                get_item_of_this_order = LsOrderItems.objects.filter(order_id=item)
            ################################################ EMAL SEND CODE START ##############
            if get_user_info.user.email == "":
                test = ""
            else:    
                content = {'get_system_info': get_system_info, "yourname": get_user_info.name,"BASE_URL": settings.BASE_URL, "get_orders": item,"get_item_of_this_order": get_item_of_this_order}
                email_content = render_to_string("email_template/email_send_for_ordeer_statement.html", content)
                msg = email.message.Message()
                msg['Subject'] = 'Order summary'
                msg['From'] = settings.EMAIL_HOST_USER
                msg['To'] = get_user_info.user.email
                password = settings.EMAIL_HOST_PASSWORD
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(email_content)
                s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                s.starttls()
                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string())
            LsOrder.objects.filter(id=item.id).update(Mail_send_status=True, update_date=datetime.now())
            ################################################ EMAL SEND CODE END ##############
    return True


def send_email_for_booking_start_notification():
    if LsWishlist.objects.values('user').annotate(total=Count('user')).exists():
        get_system_info = LsSettings.objects.all().first()
        get_users = LsWishlist.objects.values('user').annotate(total=Count('user'))
        if get_users:
            for user_id in get_users:
                get_user_info = get_object_or_404(LsUser , id=user_id["user"])
                if LsWishlist.objects.filter(user_id=user_id["user"]).filter(Wishlist_mail_status=False).filter(Product__Ticket_booking_start__lte=datetime.today()).filter(Product__winner_status=False).exists():
                    
                    if get_user_info.user.email == "":
                        test = ""    
                    else:
                        get_product = LsWishlist.objects.filter(user_id=user_id["user"]).filter(Wishlist_mail_status=False).filter(Product__Ticket_booking_start__lte=datetime.today()).filter(Product__winner_status=False)
                        print(get_product)
                        ################################################ EMAL SEND CODE START ##############
                        content = {'get_system_info': get_system_info, "yourname": get_user_info.name,"BASE_URL": settings.BASE_URL, "get_product": get_product}
                        email_content = render_to_string("email_template/email_send_for_booking_start_notification.html", content)
                        msg = email.message.Message()
                        msg['Subject'] = 'Booking Start'
                        msg['From'] = settings.EMAIL_HOST_USER
                        msg['To'] = get_user_info.user.email
                        password = settings.EMAIL_HOST_PASSWORD
                        msg.add_header('Content-Type', 'text/html')
                        msg.set_payload(email_content)
                        s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                        s.starttls()
                        s.login(msg['From'], password)
                        s.sendmail(msg['From'], [msg['To']], msg.as_string())
                    LsWishlist.objects.filter(user_id=user_id["user"]).filter(Wishlist_mail_status=False).filter(Product__Ticket_booking_start__lte=datetime.today()).filter(Product__winner_status=False).update(Wishlist_mail_status=True,Update_date=datetime.now())
                    ################################################ EMAL SEND CODE END ##############
    return True



def send_email_for_register_user():
    ################################################ EMAL SEND CODE START ##############
    if LsUser.objects.filter(status=True).filter(Mail_status=False).exists():
        today = date.today()
        month = today.month
        get_product = None
        if LsProduct.objects.filter(Status=True).filter(winner_status=False).filter(Ticket_open_date__month=month).exists() or LsProduct.objects.filter(Ticket_booking_start__month=month).filter(winner_status=False).filter(Status=True).exists():
            get_product = LsProduct.objects.filter(Status=True).order_by("Publich_date").filter(winner_status=False).filter(Ticket_open_date__month=month) | LsProduct.objects.filter(Ticket_booking_start__month=month).filter(winner_status=False).filter(Status=True)[0:4]
        get_system_info = LsSettings.objects.all().first()
        get_user = LsUser.objects.filter(status=True).filter(Mail_status=False)[0:2]
        for user in get_user:
            if user.user.email == "":
                test = ""
            else:    
                content = {'get_system_info':get_system_info,"yourname":user.name,"BASE_URL":settings.BASE_URL,"get_product":get_product}
                email_content = render_to_string("email_template/email_send_for_create_new_account.html",content)
                msg = email.message.Message()
                msg['Subject'] = 'Account Create successfully'
                msg['From'] = settings.EMAIL_HOST_USER
                msg['To'] = user.user.email
                password = settings.EMAIL_HOST_PASSWORD
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(email_content)
                s = smtplib.SMTP(settings.EMAIL_HOST , settings.EMAIL_PORT)
                s.starttls()
                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string())
            LsUser.objects.filter(id=user.id).update(Mail_status=True)
    ################################################ EMAL SEND CODE END ##############
    return True