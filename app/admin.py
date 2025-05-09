from django.contrib import admin
from .models import User, Admin, Exploiter, Country, Genre, Company, Actor, Film, Comment, Rating

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = ('username', 'email', 'password', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_per_page = 25
    ordering = ('username',)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'addres')
    list_filter = ('phone_number',)
    search_fields = ('user__username', 'phone_number', 'addres')
    fields = ('user', 'phone_number', 'addres')
    raw_id_fields = ('user',)
    list_per_page = 25
    ordering = ('user__username',)

@admin.register(Exploiter)
class ExploiterAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    list_filter = ('phone_number',)
    search_fields = ('user__username', 'phone_number')
    fields = ('user', 'phone_number')
    raw_id_fields = ('user',)
    list_per_page = 25
    ordering = ('user__username',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'flag_image')
    search_fields = ('name',)
    fields = ('name', 'flag_image')
    list_per_page = 25
    ordering = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)
    list_per_page = 25
    ordering = ('name',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    fields = ('name', 'description')
    list_per_page = 25
    ordering = ('name',)

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date')
    list_filter = ('birth_date',)
    search_fields = ('first_name', 'last_name')
    fields = ('first_name', 'last_name', 'birth_date', 'photo')
    list_per_page = 25
    ordering = ('first_name', 'last_name')

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'views', 'get_genres', 'get_countries')
    list_filter = ('genres', 'company', 'countries')
    search_fields = ('name',)
    fields = ('name', 'video', 'genres', 'company', 'actors', 'countries', 'views')
    filter_horizontal = ('genres', 'actors', 'countries')
    raw_id_fields = ('company',)
    list_per_page = 25
    ordering = ('name',)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Janrlar'

    def get_countries(self, obj):
        return ", ".join([country.name for country in obj.countries.all()])
    get_countries.short_description = 'Davlatlar'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'text_preview', 'created_at')
    list_filter = ('created_at', 'user', 'film')
    search_fields = ('user__username', 'film__name', 'text')
    fields = ('user', 'film', 'text', 'created_at')
    raw_id_fields = ('user', 'film')
    readonly_fields = ('created_at',)
    list_per_page = 25
    ordering = ('-created_at',)

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Izoh matni'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'score', 'created_at')
    list_filter = ('score', 'created_at', 'user', 'film')
    search_fields = ('user__username', 'film__name')
    fields = ('user', 'film', 'score', 'created_at')
    raw_id_fields = ('user', 'film')
    readonly_fields = ('created_at',)
    list_per_page = 25
    ordering = ('-created_at',)