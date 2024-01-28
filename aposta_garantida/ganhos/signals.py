from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from ganhos.models import Member, Saldo
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Member)
def novo_member_criado(sender, instance, created, **kwargs):
    if created:
        processar_nova_aposta(instance)

@receiver(post_save, sender=Member)
def member_atualizado(sender, instance, **kwargs):
    if instance.status == 'ganhou':
        processar_aposta_ganha(instance)
    elif instance.status == 'perdeu':
        processar_aposta_perdida(instance)
        
def processar_nova_aposta(member_instance):
    casa = member_instance.casa
    valor_aposta = member_instance.valor

    # Certifique-se de lidar com situações em que o Saldo para a casa ainda não existe
    saldo_casa, created = Saldo.objects.get_or_create(casa=casa)

    # Atualizar o saldo subtraindo o valor da aposta
    saldo_casa.valor -= valor_aposta
    saldo_casa.save()

    logger.info(f"Nova aposta criada: {member_instance} com valor: {valor_aposta}. Saldo atualizado para a casa {casa}: {saldo_casa.valor}")

def processar_aposta_ganha(member_instance):
    casa_ganhadora = member_instance.casa
    valor_ganho = member_instance.valor * member_instance.odd

    # Certifique-se de lidar com situações em que o Saldo para a casa ganhadora ainda não existe
    saldo_casa_ganhadora, created = Saldo.objects.get_or_create(casa=casa_ganhadora)

    # Atualizar o saldo adicionando o valor ganho
    saldo_casa_ganhadora.valor += valor_ganho
    saldo_casa_ganhadora.save()

    logger.info(f"Aposta ganha: {member_instance}. Saldo atualizado para a casa {casa_ganhadora}: {saldo_casa_ganhadora.valor}")
    
@receiver(pre_delete, sender=Member)
def member_deletado(sender, instance, **kwargs):
    if instance.status == 'ganhou':
        processar_exclusao_aposta_ganha(instance)

def processar_aposta_perdida(member_instance):
    # Supondo que 'Member' seja o modelo que você deseja excluir
    try:
        member_associado = Member.objects.get(pk=member_instance.pk)
        member_associado.delete()
        logger.info(f"Entrada em 'Member' excluída para a aposta perdida: {member_instance}")
    except Member.DoesNotExist:
        logger.warning(f"Nenhuma entrada em 'Member' encontrada para a aposta perdida: {member_instance}")

def processar_exclusao_aposta_ganha(member_instance):
    # Supondo que 'Member' seja o modelo que você deseja excluir
    try:
        member_associado = Member.objects.get(pk=member_instance.pk)
        member_associado.delete()
        logger.info(f"Entrada em 'Member' excluída para a aposta ganha excluída: {member_instance}")
    except Member.DoesNotExist:
        logger.warning(f"Nenhuma entrada em 'Member' encontrada para a aposta ganha excluída: {member_instance}")
