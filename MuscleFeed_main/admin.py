from django.contrib import admin

from .models import *

def dublicate_entry(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
dublicate_entry.short_description = "Дублировать запись"


def register_models(models_list):
    for model, fields in models_list.items():
        model_fields = ()
        for field in model._meta.fields:
            if field.name in fields:
                model_fields = (field.name, *model_fields)

        class Admin(admin.ModelAdmin):
            list_display = ('__str__', *model_fields)
            list_filter = model_fields
            search_fields = model_fields
            actions = [dublicate_entry]
            if model == Order:
                def save_model(self, request, obj, form, change):
                    order = obj.save()['order']
                    form.cleaned_data['dishes_day1'] = order.dishes_day1.all()
                    form.cleaned_data['dishes_day2'] = order.dishes_day2.all()
                    form.cleaned_data['dishes_day3'] = order.dishes_day3.all()
                    form.cleaned_data['dishes_day4'] = order.dishes_day4.all()
                    form.cleaned_data['dishes_day5'] = order.dishes_day5.all()
                    form.cleaned_data['dishes_day6'] = order.dishes_day6.all()
                    form.cleaned_data['dishes_day7'] = order.dishes_day7.all()
                    form.cleaned_data['dishes_day8'] = order.dishes_day8.all()
                    form.cleaned_data['dishes_day9'] = order.dishes_day9.all()
                    form.cleaned_data['dishes_day10'] = order.dishes_day10.all()
                    form.cleaned_data['dishes_day11'] = order.dishes_day11.all()
                    form.cleaned_data['dishes_day12'] = order.dishes_day12.all()
                    form.cleaned_data['dishes_day13'] = order.dishes_day13.all()
                    form.cleaned_data['dishes_day14'] = order.dishes_day14.all()
                    form.cleaned_data['dishes_day15'] = order.dishes_day15.all()
                    form.cleaned_data['dishes_day16'] = order.dishes_day16.all()
                    form.cleaned_data['dishes_day17'] = order.dishes_day17.all()
                    form.cleaned_data['dishes_day18'] = order.dishes_day18.all()
                    form.cleaned_data['dishes_day19'] = order.dishes_day19.all()
                    form.cleaned_data['dishes_day20'] = order.dishes_day20.all()
                    form.cleaned_data['dishes_day21'] = order.dishes_day21.all()
                    form.cleaned_data['dishes_day22'] = order.dishes_day22.all()
                    form.cleaned_data['dishes_day23'] = order.dishes_day23.all()
                    form.cleaned_data['dishes_day24'] = order.dishes_day24.all()
                    form.cleaned_data['dishes_day25'] = order.dishes_day25.all()
                    form.cleaned_data['dishes_day26'] = order.dishes_day26.all()
                    super().save_model(request, obj, form, change)
        admin.site.register(model, Admin)


register_models({
    Fixed: [],
    Video: [],
    WrapperTranslations: [],
    Dish: ['name', 'admin_name', 'type', 'price'],
    MenuType: [],
    Menu: [],
    HomePageSettings: [],
    Question: [],
    QuestionBlock: [],
    Review: ['name', 'created', 'is_moderated'],
    PrivacyPolicy: [],
    UserAgreement: [],
    Profile: ['name', 'surname', 'status', 'phone', 'is_moderator'],
    EmailVerification: ['user__email', 'user__first_name', 'user__last_name' 'new_email', 'key', 'created'],
    ResetPasswordVerification: ['user', 'key', 'created'],
    CallRequest: ['name', 'phone', 'created'],
    Order: ['id', 'phone', 'name', 'address', 'email', 'payment_type', 'menu__name', 'menu__type', 'price', 'days', 'is_completed', 'created'],
    AccountPageSettings: [],
    OrderFreeze: [],
    PromoCode: [],
})


