import requests
from datetime import datetime
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        token = extension.token
        if not token:
            return self.get_error_result()

        habits = self.get_habits(token)
        items = []
        for habit in habits:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=habit.get('name'),
                                             description=habit.get('name'),
                                             on_enter=HideWindowAction()))

        return RenderResultListAction(items)

    def get_habits(self, token):
        current_date = datetime.now().isoformat()
        response = requests.get(
            "https://api.habitify.me/habits?target_date=" + current_date, headers={"Authorization": token})
        return response.json()

    def get_error_result(self):
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name='Missing API Credential',
                                                           description='Did you provide one in the extension preferences?',
                                                           on_enter=HideWindowAction())])


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        extension.token = event.preferences['api_credential']


if __name__ == '__main__':
    DemoExtension().run()
