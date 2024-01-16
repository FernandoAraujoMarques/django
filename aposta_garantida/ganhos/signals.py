from django.db.models.signals import post_save
from django.dispatch import receiver
from ganhos.models import Member, Saldo 

@receiver(post_save, sender=Member)
def novo_member_criado(sender, instance, created, **kwargs):
    if created:
        # Subtrair o valor da aposta do saldo da casa
        casa = instance.casa
        valor_aposta = instance.valor
        status = instance.status

        # Certifique-se de lidar com situações em que o Saldo para a casa ainda não existe
        saldo_casa, created = Saldo.objects.get_or_create(casa=casa)

        # Atualizar o saldo subtraindo o valor da aposta
        saldo_casa.valor -= valor_aposta
        saldo_casa.save()

        #print(f"Novo Member criado: {instance} com valor de aposta: {valor_aposta}. Saldo atualizado para a casa {casa}: {saldo_casa.valor}")


