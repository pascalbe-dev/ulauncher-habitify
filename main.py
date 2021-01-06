import requests
import logging
from datetime import datetime
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def get_habits(self, token, only_pending):
        current_date = datetime.utcnow().isoformat()
        url = "https://api.habitify.me/habits?target_date=" + current_date

        if only_pending:
            url += "&status=pending"

        response = requests.get(url, headers={"Authorization": token})
        return response.json()

    def complete_habit(self, token, habit_id):
        current_date = datetime.utcnow().isoformat()
        url = "https://api.habitify.me/habits/" + habit_id + "/status"
        body = {
            "status": "completed",
            "target_date": current_date
        }

        response = requests.put(url, data=body, headers={
            "Authorization": token})

        logger.debug(response.content)

    def log_progress_for_habit(self, token, habit_id, progress_value, progress_unit):
        current_date = datetime.utcnow().isoformat()
        url = "https://api.habitify.me/habits/" + habit_id + "/logs"
        body = {
            "value": progress_value,
            "unit_type": progress_unit,
            "target_date": current_date
        }

        response = requests.post(url, data=body, headers={
            "Authorization": token})

        logger.debug(response.content)


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        token = extension.token
        if not token:
            return self.get_error_result()

        habits = extension.get_habits(token, extension.only_pending)
        items = []
        for habit in habits:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=habit.get('name'),
                                             description=habit.get('name'),
                                             on_enter=ExtensionCustomAction({'id': habit.get('id'), 'action': 'log'})))

        return RenderResultListAction(items)

    def get_error_result(self):
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name='Missing API Credential',
                                                           description='Did you provide one in the extension preferences?',
                                                           on_enter=HideWindowAction())])


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        action = data['action']
        habit_id = data['id']

        if action == 'complete':
            logger.info('Completing habit with ID ' + habit_id)
            extension.complete_habit(extension.token, habit_id)
        elif action == 'log':
            logger.info('Logging progress for habit with ID ' + habit_id)
            extension.log_progress_for_habit(
                extension.token, habit_id, "10", "min")


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        extension.token = event.preferences['api_credential']
        extension.only_pending = event.preferences['only_pending'] == 'True'


if __name__ == '__main__':
    DemoExtension().run()
