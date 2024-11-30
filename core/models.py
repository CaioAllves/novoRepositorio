from django.db import models

# Create your models here.

class Tarefa(models.Model):
    nomeTarefa = models.CharField(max_length=40,unique=True)
    custo = models.DecimalField(max_digits=8,decimal_places=2)
    dataLimite = models.DateField()
    ordemApresentacao = models.IntegerField(unique=True,blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.ordemApresentacao is None:
            max_ordem = Tarefa.objects.aggregate(models.Max('ordemApresentacao'))['ordemApresentacao__max'] or 0
            self.ordemApresentacao = max_ordem + 1 if max_ordem > 0 else 1
        super().save(*args, **kwargs)


    def __str__(self):
        return self.nomeTarefa
