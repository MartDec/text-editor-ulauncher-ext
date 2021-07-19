import gi
gi.require_version('Gdk', '3.0')

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from helpers import *
import subprocess

class EditorExtension(Extension):

    def __init__(self):
        super(EditorExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = getDirectoryItems(extension.preferences['workspace_path'])
        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()

        if 'open_editor' in data:
            subprocess.run([extension.preferences['application_bin'], data['path']])
        else:
            actions = getResultItems(data)
            return RenderResultListAction(actions)


if __name__ == '__main__':
    EditorExtension().run()
