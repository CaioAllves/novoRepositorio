from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Tarefa
from django.db.models import Min,Max

# Create your views here.

def home(request):
    tarefas = Tarefa.objects.all().order_by('ordemApresentacao')
    return render(request, "index.html", {"tarefas": tarefas})

def salvar(request):
    nomeTarefa = request.POST.get("nomeTarefa")
    custo = request.POST.get("custo")
    dataLimite = request.POST.get("dataLimite")
    if nomeTarefa and custo and dataLimite and float(custo) <= 999999.99:
        try:         
            Tarefa.objects.create(nomeTarefa = nomeTarefa, custo = custo, dataLimite = dataLimite)
            return redirect(home)
        except IntegrityError as e:
                error_message = "Erro! Nome da tarefa já existe."
                return render(request, 'incluir.html', {'error_message': error_message})
    elif float(custo) > 999999.99:
        error_message = "Erro ao salvar a tarefa, custo excede limite."
        return render(request, 'incluir.html', {'error_message': error_message})
    else:
        error_message = "Erro ao salvar a tarefa, todos os campos devem ser preenchidos."
        return render(request, 'incluir.html', {'error_message': error_message})

def incluir(request):
    return render(request, "incluir.html")

def pagInicial(request):
    return home(request)

def edit(request,id):
    tarefas = Tarefa.objects.get(id=id)
    return render(request,"update.html", {"tarefas" : tarefas})

def update(request,id):
    nomeTarefa = request.POST.get("nomeTarefa")
    custo = request.POST.get("custo")
    dataLimite = request.POST.get("dataLimite")
    
    if Tarefa.objects.filter(nomeTarefa=nomeTarefa).exclude(id=id).exists():
        error_message = "Erro ao salvar a tarefa, nomes iguais."
        tarefas = Tarefa.objects.get(id=id)
        return render(request, 'update.html', {"tarefas" : tarefas, 'error_message': error_message})
    elif float(custo) > 999999.99:
        error_message = "Erro ao salvar a tarefa, custo excede limite."
        tarefas = Tarefa.objects.get(id=id)
        return render(request, 'update.html', {"tarefas" : tarefas, 'error_message': error_message})

    if nomeTarefa and custo and dataLimite:
        tarefa = Tarefa.objects.get(id=id)
        tarefa.nomeTarefa = nomeTarefa
        tarefa.custo = custo
        tarefa.dataLimite = dataLimite
        tarefa.save()
        return redirect(home)
    else:
        error_message = "Erro ao salvar a tarefa, todos os campos devem estar preenchidos."
        tarefas = Tarefa.objects.get(id=id)
        return render(request, 'update.html', {"tarefas" : tarefas, 'error_message': error_message})
        
def delete(request,id):
    tarefa = Tarefa.objects.get(id=id)
    tarefa.delete()
    return redirect(home)

def subir(request, ordemApresentacao):
    tarefa = Tarefa.objects.get(ordemApresentacao=ordemApresentacao)
    primeiraTarefa = Tarefa.objects.aggregate(Min('ordemApresentacao'))['ordemApresentacao__min']
    if tarefa.ordemApresentacao == primeiraTarefa:
        return redirect(home)

    tarefaAcima = Tarefa.objects.filter(ordemApresentacao__lt=ordemApresentacao).order_by('-ordemApresentacao').first()

    if not tarefaAcima:
        return redirect(home)
    
    tarefaAcima.ordemApresentacao = 0
    tarefa.ordemApresentacao = ordemApresentacao-1

    tarefaAcima.save()
    tarefa.save()

    tarefaAcima.ordemApresentacao = ordemApresentacao

    tarefaAcima.save()

    return redirect(home)


def descer(request, ordemApresentacao):
    tarefa = Tarefa.objects.get(ordemApresentacao=ordemApresentacao)
    ultimaTarefa = Tarefa.objects.aggregate(Max('ordemApresentacao'))['ordemApresentacao__max']
    if tarefa.ordemApresentacao == ultimaTarefa:
        return redirect(home)

    tarefaAbaixo = Tarefa.objects.filter(ordemApresentacao__gt=ordemApresentacao).order_by('ordemApresentacao').first()

    if not tarefaAbaixo:
        return redirect(home)
    
    tarefaAbaixo.ordemApresentacao = 0
    tarefa.ordemApresentacao = ordemApresentacao +1

    tarefaAbaixo.save()
    tarefa.save()

    tarefaAbaixo.ordemApresentacao = ordemApresentacao

    tarefaAbaixo.save()

    return redirect(home)
