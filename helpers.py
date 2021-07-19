from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from pathlib import Path

import os

def getSubdirectories(path):
    results = []
    path = str(path)
    items = os.listdir(path)

    for item in items:
        fullPath = ('%s/' % path) + item if path[-1:] != '/' else path + item
        if os.path.isdir(fullPath):
            results.append({
                'name': item,
                'path': fullPath
            })

    return results

def getResultItem(itemData):
    return ExtensionResultItem(
        icon='images/directory.svg',
        name=itemData['name'],
        description='%s directory' % itemData['name'],
        on_enter=ExtensionCustomAction(itemData, keep_app_open=True)
    )

def getDefaultActions(data):
    actions = [
        ExtensionResultItem(
            icon='images/technology.svg',
            name=data['name'],
            description='Directory %s' % data['name'],
            on_enter=DoNothingAction()
        ),
        ExtensionResultItem(
            icon='images/icon.svg',
            name='Open in your editor',
            description='Open directory %s in your editor' % data['name'],
            on_enter=ExtensionCustomAction({
                'open_editor': True,
                'path': data['path']
            })
        )
    ]

    return actions

def getBackAction(currentTargetPath):
    targetPath = Path('%s/../' % currentTargetPath).resolve()
    return ExtensionResultItem(
        icon='images/back.svg',
        name='Go back',
        description='Go to previous directory',
        on_enter=RenderResultListAction(getDirectoryItems(targetPath))
    )

def getDirectoryItems(path):
    directories = getSubdirectories(path)
    results = []
    for directory in directories:
        item = getResultItem(directory)
        results.append(item)

    return results

def getResultItems(data):
    actions = getDefaultActions(data)
    actions.append(getBackAction(data['path']))
    items = getDirectoryItems('%s/' % data['path'])
    actions.extend(items)

    return actions
