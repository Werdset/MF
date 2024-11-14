

def duplicate_entry(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate_entry.short_description = "Duplicate selected record"
