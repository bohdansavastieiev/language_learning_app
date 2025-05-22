# language_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Language, UserProfile, Dictionary, Word

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_native_language')

    def get_native_language(self, instance):
        return instance.profile.native_language if hasattr(instance, 'profile') else 'N/A'
    get_native_language.short_description = 'Native Language'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# --- Register your custom models ---

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)

@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'user__username', 'language__name')
    list_filter = ('language', 'user')

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'translation', 'dictionary', 'created_at', 'updated_at')
    search_fields = ('text', 'translation', 'example_sentence', 'dictionary__name', 'dictionary__user__username')
    list_filter = ('dictionary__language', 'dictionary__user', 'dictionary')
