from django.apps import AppConfig
import posthog

class HomeAppConfig(AppConfig):
    name = "home"

    def ready(self):
        posthog.api_key = 'phc_zjhMXcYodTdsui69Src7Y133OnOx5tPmmR55K7qLFZv'
        posthog.host = 'https://app.posthog.com'