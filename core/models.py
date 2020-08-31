from django.db import models
from datetime import date

# Create your models here.


class Turmas(models.Model):
    turma = models.CharField(max_length=50, unique=True)


    def criar(self, turma):
        try:
            db = Turmas()
            db.turma = turma.strip()
            db.save()
        except:
            return {
                'status': False,
                'msg': f'Esta turma ({turma}) já foi adicionada, não pode haver duas turmas com o mesmo nome'
            }
        return {
            'status': True,
            'msg': f'{turma} cadastrado(a)'
        }


class Alunos(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    nome = models.CharField(max_length=100)
    turma = models.ForeignKey(Turmas, on_delete=models.CASCADE)


    def criar(self, nome, turma):
        nome = nome.strip().upper()
        turma = Turmas.objects.get(id=turma)
        try:
            db = Alunos()
            db.id = str(nome) + ' - ' + str(turma.turma)
            db.nome = nome
            db.turma = turma
            db.save()
        except Exception as erro:
            return {
                'status': False,
                'msg': f'{nome} já foi cadastrado em {turma.turma}'
            }
        return {
            'status': True,
            'msg': f'{nome} cadastrado com sucesso em {turma.turma}'
        }


class Estrelas(models.Model):
    data = models.DateField()
    aluno = models.ForeignKey(Alunos, on_delete=models.CASCADE)


    def adicionar(self, aluno):
        aluno = Alunos.objects.get(id=aluno)
        db = Estrelas()
        db.data = date.today()
        db.aluno = aluno
        db.save()
        return {
            'status': True,
            'msg': f'Estrelinha para {aluno.nome} adicionada'
        }


    def remover(self, aluno):
        Estrelas.objects.filter(id=aluno).last().delete()
        return {
            'status': True,
            'msg': 'Estrelinha removida'
        }


    def zerar(self, aluno):
        Estrelas.objects.filter(aluno=aluno).delete()