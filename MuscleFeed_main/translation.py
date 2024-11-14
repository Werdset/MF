from modeltranslation.translator import register, TranslationOptions

from .models import *


@register(Fixed)
class FixedTranslationOptions(TranslationOptions):
    fields = (
        'open_graph_site_name',
        'open_graph_title',
        'open_graph_description',
        'open_graph_image',
        'site_description',
        'phone_number',
    )


@register(WrapperTranslations)
class WrapperTranslationsTranslationOptions(TranslationOptions):
    fields = (
        'logout',
        'login',
        'logging_in',
        'user_login',
        'password',
        'remember_me',
        'forget_password',
        'registration',
        'user_name',
        'user_surname',
        'user_phone',
        'signup_by_email',
        'signup_by_phone',
        'error_phone_russia',
        'error_phone_short',
        'error_email_exists',
        'error_phone_exists',
        'error_no_register_data',
        'next',
        'user_sex',
        'repeat_password',
        'agreed',
        'reset_password',
        'user_agreement',
        'privacy_policy',
        'language',
        'email_confirmed',
        'please_login',
        'success',
        'wait_a_second',
        'error',
        'try_again',
        'confirm_instruction',
        'agreed_error',
        'no_such_email',
        'bad_key',
        'key_resented',
        'key_info',
        'resend_key',
        'personal_account',
        'wrong_password',
        'user_address',
        'why_us',
        'our_menu',
        'reviews',
        'questions',
        'call',
        'call_me',
        'form_fail_info',
        'call_me_success_info',
        'name_and_surname',
        'send',
        'order_created',
        'order_success',
        'unique_order_number',
        'to_pay',
        'order_success_info',
        'order_not_created',
        'code',
        'email',
        'footer_info1',
        'footer_info2',
        'info_video',
        'phone_10_error',
        'calories_short_start',
        'calories_short',
        'payment_type',
        'card_phone',
        'card_delivery',
        'cash_delivery',
    )


@register(PrivacyPolicy)
class PrivacyPolicyTranslationOptions(TranslationOptions):
    fields = (
        'content',
    )


@register(UserAgreement)
class UserAgreementTranslationOptions(TranslationOptions):
    fields = (
        'content',
    )


@register(Dish)
class DishTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )


@register(MenuType)
class MenuTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'short_description',
        'extra_short_description',
        'description',
    )


@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )


@register(HomePageSettings)
class HomePageSettingsTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'meta_description',
        'meta_keywords',
        'open_graph_title',
        'open_graph_description',
        'open_graph_image',
        'slider_title',
        'slider_description',
        'pluses1_title',
        'pluses1_description',
        'pluses2_title',
        'pluses2_description',
        'pluses3_title',
        'pluses3_description',
        'new_order',
        'call_us',
        'select_menu',
        'select_your_aim',
        'select',
        'selected',
        'monday_short',
        'tuesday_short',
        'wednesday_short',
        'thursday_short',
        'friday_short',
        'saturday_short',
        'sunday_short',
        'want_this_menu',
        'order',
        'meal_days_1',
        'meal_days_2',
        'meal_days_4',
        'meal_days_6',
        'meal_days_14',
        'meal_days_26',
        'your_profit',
        'phone_info',
        'comment',
        'show_all',
        'write_review',
        'often_questions',
        'review',
        'contact_link',
        'contact_link_info',
        'select_dish',
        'back',
        'write_review_success_info',
        'drink',
        'breakfast',
        'second_breakfast',
        'lunch',
        'high_tea',
        'dinner',
        'replace',
        'gram_short',
        'summary',
        'proteins',
        'fats',
        'carbohydrates',
        'to_price',
        'from_price',
        'changed_dishes',
        'reset',
        'per_day',
        'all_days',
        'order_failure',
        'order_failure_info_1',
        'order_failure_info_2',
        'reload_page',
        'delivery_map',
        'free_delivery',
        'free_delivery_text_1',
        'free_delivery_text_2',
        'select_days',
        'select_plan1',
        'select_plan2',
        'calculate_calories',
        'calories_calculator',
        'age',
        'height',
        'weight',
        'sex',
        'male',
        'female',
        'physical_activities',
        'physical_activities1',
        'physical_activities2',
        'physical_activities3',
        'purpose',
        'purpose1',
        'purpose2',
        'purpose3',
        'you_need_calories',
        'recommended_menus',
        'result',
        'promocode',
    )


@register(AccountPageSettings)
class AccountPageSettingsTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'personal_info',
        'my_profile',
        'hello',
        'save_btn',
        'changes_saved',
        'changes_saved_info',
        'old_password',
        'change_password',
        'new_password',
        'new_password_repeat',
        'change_email',
        'change_address',
        'change_phone',
        'add_phone',
        'new_phone',
        'add_email',
        'new_email',
        'change_name',
        'change_surname',
        'change_personal_data',
        'change_personal_data_success',
        'change_personal_data_info',
        'orders',
        'load_more',
        'extend_order',
        'days',
        'active_t',
        'completed',
        'not_payed',
        'pay',
        'all',
        'active_pl',
        'completed_pl',
        'not_payed_pl',
        'no_orders',
        'make_order',
        'price',
        'plan_changed',
        'plan_changed_info',
        'home',
        'show_dishes',
        'change_menu',
        'meal_days',
        'you_need_to_pay',
        'freeze_info',
        'freeze_info_link',
        'freeze',
        'unfreeze',
        'frozen',
        'will_be_frozen',
        'will_be_unfrozen',
        'order_freeze_info',
        'get_promocode',
        'get_promocode_info',
        'copy_referral_link',
        'referral_link_copy_success',
        'referral_link_copy_success_info',
    )


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = (
        'question',
        'answer',
    )


@register(QuestionBlock)
class QuestionBlockTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'content',
    )
