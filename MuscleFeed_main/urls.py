from django.urls import path

from .views import *


def home_redirect(request):
    language = 'he'
    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user):
            language = Profile.objects.get(user=request.user).language
    request.session[settings.LANGUAGE_COOKIE_NAME] = language
    translation.activate(language)
    timezone.activate(pytz.timezone(settings.TIME_ZONE))
    return redirect('home', language)


urlpatterns = [
    path('<str:language>/signup/step-<int:step>/', signup,
         name='signup'),

    path('<str:language>/login/', login,
         name='login'),

    path('<str:language>/logout/', logout,
         name='logout'),

    path('<str:language>/resetpassword/step-<int:step>/', reset_password,
         name='reset-password'),

    path('<str:language>/language-change/', language_change,
         name='language-change'),

    path('<str:language>/reviews-show-all/', reviews_show_all,
         name='reviews-show-all'),

    path('<str:language>/write-review/', write_review,
         name='write-review'),

    path('<str:language>/call-me/', call_me,
         name='call-me'),

    path('<str:language>/make-order/', make_order,
         name='make-order'),

    path('<str:language>/user-<int:id>/', login_required(AccountPage.as_view()),
         name='account'),

    path('<str:language>/user-<int:id>/order-freeze/', account_order_freeze,
         name='order-freeze'),

    path('<str:language>/user-<int:id>/order-unfreeze/', account_order_unfreeze,
         name='order-unfreeze'),

    path('<str:language>/user-<int:id>/order-delete-freeze/', account_order_delete_freeze,
         name='order-delete-freeze'),

    path('<str:language>/user-<int:id>/load-orders/', account_load_orders,
         name='account-load-orders'),

    path('<str:language>/user-<int:id>/order-extend-load/', account_order_extend_load,
         name='account-order-extend-load'),

    path('<str:language>/user-<int:id>/order-extend/', account_order_extend,
         name='account-order-extend'),

    path('<str:language>/user-<int:id>/order-show-dishes/', account_order_show_dishes,
         name='account-order-show-dishes'),

    path('<str:language>/user-<int:id>/order-change-dish/', account_order_change_dish,
         name='account-order-change-dish'),

    path('<str:language>/user-<int:id>/order-change-menu-calculate/', account_order_change_menu_calculate,
         name='account-order-change-menu-calculate'),

    path('<str:language>/user-<int:id>/order-change-menu-submit/', account_order_change_menu_submit,
         name='account-order-change-menu-submit'),

    path('<str:language>/user-<int:id>/order-pay-info/', account_order_pay_info,
         name='account-order-pay-info'),

    path('<str:language>/user-<int:id>/change-password/', account_change_password,
         name='account-change-password'),

    path('<str:language>/user-<int:id>/changeemail/step-<int:step>/', account_change_email,
         name='account-change-email'),

    path('<str:language>/user-<int:id>/change-personal-data/', account_change_personal_data,
         name='account-change-personal-data'),

    path('<str:language>/user-<int:id>/fix-dishes/', moderator_account_fix_dishes,
         name='moderator-account-fix-dishes'),

    path('<str:language>/user-<int:id>/download-reports/', moderator_account_download_reports,
         name='moderator-account-download-reports'),

    path('<str:language>/user-<int:id>/download-reports-dishes/', moderator_account_download_reports_dishes,
         name='moderator-account-download-reports-dishes'),

    path('<str:language>/user-<int:id>/download-reports-orders/', moderator_account_download_reports_orders,
         name='moderator-account-download-reports-orders'),

    path('<str:language>/user-<int:id>/download-reports-delivery/', moderator_account_download_reports_delivery,
         name='moderator-account-download-reports-delivery'),

    path('<str:language>/user-<int:id>/make-order-payed/', moderator_account_make_order_payed,
         name='moderator-account-make-order-payed'),

    path('<str:language>/user-<int:id>/make-order-to-return-payed/', moderator_account_make_order_to_return_payed,
         name='moderator-account-make-order-to-return-payed'),

    path('<str:language>/user-<int:id>/change-request-delete/', moderator_account_change_request_delete,
         name='moderator-account-change-request-delete'),

    path('<str:language>/user-<int:id>/change-request-exec/', moderator_account_change_request_exec,
         name='moderator-account-change-request-exec'),

    path('<str:language>/user-<int:id>/order-complete-delete/', moderator_account_order_complete_delete,
         name='moderator-account-order-complete-delete'),

    path('<str:language>/user-<int:id>/order-complete-submit/', moderator_account_order_complete_submit,
         name='moderator-account-order-complete-submit'),

    path('<str:language>/user-<int:id>/call-request-load-price/', moderator_account_call_request_load_price,
         name='moderator-account-call-request-load-price'),

    path('<str:language>/user-<int:id>/call-request-delete/', moderator_account_call_request_delete,
         name='moderator-account-call-request-delete'),

    path('<str:language>/user-<int:id>/call-request-submit/', moderator_account_call_request_submit,
         name='moderator-account-call-request-submit'),

    path('<str:language>/user-<int:id>/review-request-delete/', moderator_account_review_request_delete,
         name='moderator-account-review-request-delete'),

    path('<str:language>/user-<int:id>/review-request-submit/', moderator_account_review_request_submit,
         name='moderator-account-review-request-submit'),

    path('<str:language>/user-<int:id>/download-backup/', moderator_account_download_backup,
         name='moderator-account-download-backup'),

    path('<str:language>/', HomePage.as_view(), name='home'),

    path('', home_redirect, name='home_redirect'),
]
