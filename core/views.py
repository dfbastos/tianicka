from django.shortcuts import render, redirect
from django.views import View
from .models import Turmas, Alunos, Estrelas

# Create your views here.

class Core(View):
    def get(self, *args, **kwargs):

        #Captura possíveis variáveis de cadastro de turmas
        try:
            statusTurma = self.request.session['statusTurma']
            msgTurma = self.request.session['msgTurma']
            del self.request.session['statusTurma']
            del self.request.session['msgTurma']
        except:
            statusTurma = None
            msgTurma = None

        #captura possíveis variáveis de cadastro de alunos
        try:
            statusAluno = self.request.session['statusAluno']
            msgAluno = self.request.session['msgAluno']
            del self.request.session['statusAluno']
            del self.request.session['msgAluno']
        except:
            statusAluno = None
            msgAluno = None

        #Captura possíveis variáveis de inclusão/exclusao de estrelas
        try:
            statusEstrelinhas = self.request.session['statusEstrelinhas']
            msgEstrelinhas = self.request.session['msgEstrelinhas']
            del self.request.session['statusEstrelinhas']
            del self.request.session['msgEstrelinhas']
        except:
            statusEstrelinhas = None
            msgEstrelinhas = None

        #Consulta as turmas cadastradas
        turmas = Turmas.objects.all().order_by('turma')

        #Consulta os alunos cadastrados
        alunos = Alunos.objects.all().order_by('nome')

        #Consulta todas as estrelinhas
        estrelas = Estrelas.objects.all()

        #Define as mensagens
        mensagensEstrelas = {
            0: 'Vamos colecionar?',
            1: 'Oba!',
            2: 'É isso aí!',
            3: 'Continue assim!',
            4: 'Maravilha!',
            5: 'Perfeito',
            6: 'Sensacional!',
            7: 'Fantástico!',
            8: 'Excelente!',
            9: 'Parabéns!',
            10: 'Você é 10!'
        }

        alunosEstrelas = []

        id = 0

        for dado in alunos:
            est = estrelas.filter(aluno=dado.id).count()
            if est is None:
                est = 0
            if est > 10:
                est = 10
            count = []
            while len(count) < est:
                count.append(0)
            alunosEstrelas.append({
                'id': id,
                'nome': dado.nome,
                'turma': dado.turma.turma,
                'estrelas': est,
                'estrelasMaximas': 10,
                'msg': mensagensEstrelas[est],
                'count': count
            })
            id += 1

        return render(self.request, 'index.html', {
            'statusTurma': statusTurma,
            'msgTurma': msgTurma,
            'statusAluno': statusAluno,
            'msgAluno': msgAluno,
            'statusEstrelinhas': statusEstrelinhas,
            'msgEstrelinhas': msgEstrelinhas,
            'turmas': turmas,
            'alunos': alunos,
            'alunosEstrelas': alunosEstrelas
        })


    def post(self, *args, **kwargs):
        acao = self.request.POST['acao']

        if acao == 'cadastrarTurma':
            #Cadastrar Turma
            db = Turmas()
            retorno = db.criar(self.request.POST['turma'])
            self.request.session['statusTurma'] = retorno['status']
            self.request.session['msgTurma'] = retorno['msg']
            return redirect('/')

        elif acao == 'cadastrarAluno':
            #Cadastrar Aluno
            db = Alunos()
            retorno = db.criar(self.request.POST['aluno'], self.request.POST['turma'])
            self.request.session['statusAluno'] = retorno['status']
            self.request.session['msgAluno'] = retorno['msg']
            return redirect('/')

        elif acao == 'cadastrarEstrelinha':
            #Incluir estrelinha
            db = Estrelas()
            retorno = db.adicionar(self.request.POST['aluno'])
            self.request.session['statusEstrelinhas'] = retorno['status']
            self.request.session['msgEstrelinhas'] = retorno['msg']
            return redirect('/')