from django.contrib import admin
from .models import Alunos, Turmas, Estrelas

# Register your models here.

class Aluno(admin.ModelAdmin):
    list_display = ['nome', 'turma']
    search_fields = []


class Turma(admin.ModelAdmin):
    list_display = ['turma']
    search_fields = []


class Estrela(admin.ModelAdmin):
    list_display = ['data', 'aluno']
    search_fields = []


admin.site.register(Alunos, Aluno)
admin.site.register(Turmas, Turma)
admin.site.register(Estrelas, Estrela)