from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from pathlib import Path

import os

def getSubdirectories(path):
    results = []
    items = os.listdir(path)

    for item in items:
        fullPath = '%s/' % path + item if path[-1] != '/' else path + item
        print(fullPath)
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

def getDefaultActions(data, workspaceRoot):
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
            on_enter=ExtensionCustomAction(
                {
                    'open_editor': True,
                    'path': data['path']
                },
                keep_app_open=True
            )
        )
    ]

    return actions

# def getDirectoryItems(root, workspaceRoot, avoid_loop=False):
#     root = '%s/' % os.path.realpath(root)
#     directories = getSubdirectories(root)
#     results = []
#     if root != workspaceRoot and not avoid_loop:
#         results.append(ExtensionResultItem(
#             icon='images/back.svg',
#             name='Go back',
#             description='Go back to parent directory',
#             on_enter=RenderResultListAction(getDirectoryItems('%s/../' % root, workspaceRoot, not avoid_loop))
#         ))
# 
#     for directory in directories:
#         item = getResultItem(directory)
#         results.append(item)
# 
#     return results

def getDirectoryItems(path):
    directories = getSubdirectories(path)
    results = []
    for directory in directories:
        item = getResultItem(directory)
        results.append(item)

    return results

def getResultItems(data, workspaceRoot):
    actions = getDefaultActions(data, workspaceRoot)

    targetPath = Path('%s/../' % data['path'])
    if (targetPath.resolve() != workspaceRoot):
        backActions = []
        backActions.extend(getDefaultActions(
            { 'name': targetPath.name, 'path': targetPath.resolve() },
            workspaceRoot
        ))
        actions.append(
            ExtensionResultItem(
                icon='images/back.svg',
                name='Go back',
                description='Go back to parent directory',
                on_enter=RenderResultListAction(getDirectoryItems(targetPath.resolve))
            )
        )
        backActions.extend(getDirectoryItems(targetPath.resolve))

    items = getDirectoryItems('%s/' % data['path'])
    actions.extend(items)

    return actions
