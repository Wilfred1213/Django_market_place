from django.apps import AppConfig



class JijiappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jijiapp'
    
    # this is signal from models.py
    def ready(self):
        # import jijiapp.signals
        
        from . import signals
