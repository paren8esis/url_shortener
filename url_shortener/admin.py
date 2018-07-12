from django.contrib import admin
from url_shortener.models import Letter, Word


class LetterAdmin(admin.ModelAdmin):
    list_display = ('letter', 'current_index', 'num_words')


class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'letter', 'word_id')


admin.site.register(Letter, LetterAdmin)
admin.site.register(Word, WordAdmin)
