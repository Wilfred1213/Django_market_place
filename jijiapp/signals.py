from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from jijiapp.models import ConversationMessage,send_notification_email
from jijiapp.models import ConversationCount
from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

@receiver(post_save, sender=ConversationMessage)
def send_notification_email_handler(sender, instance, created, **kwargs):
    if created:
        send_notification_email(sender, instance, created, **kwargs)
        
# @receiver(post_save, sender=ConversationMessage)
# @receiver(post_delete, sender=ConversationMessage)
# def update_conversation_message_count(sender, instance, **kwargs):
#     conversation = instance.conversation
#     conversation_count, created = ConversationCount.objects.get_or_create(conversation=conversation)
#     conversation_count.message_count = conversation.messages.count()
#     conversation_count.save()
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=ConversationMessage)
@receiver(post_delete, sender=ConversationMessage)
def update_conversation_message_count(sender, instance, **kwargs):
    try:
        conversation = getattr(instance, 'conversation', None)
        
        if conversation is None:
            return  # Skip further processing if the conversation is not available
        
        conversation_count, created = ConversationCount.objects.get_or_create(conversation=conversation)
        conversation_count.message_count = conversation.messages.count()
        conversation_count.save()
    except ObjectDoesNotExist:
        pass

 # Broadcast the updated message count to the relevant WebSocket group
    # channel_layer = get_channel_layer()
    # group_name = f'inbox_{conversation.members.first().id}'
    # async_to_sync(channel_layer.group_send)(
    #     group_name,
    #     {
    #         'type': 'message.count',
    #         'count': conversation_count.message_count
    #     }
    # )