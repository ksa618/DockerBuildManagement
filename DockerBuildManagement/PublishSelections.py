from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

from .ArgumentHandler import ArgumentHandler

PUBLISH_KEY = 'publish'
CONTAINER_ARTIFACT_KEY = 'containerArtifact'

def GetInfoMsg():
    infoMsg = "Publish selections is configured by adding a 'publish' property to the .yaml file.\r\n"
    infoMsg += "The 'publish' property is a dictionary of publish selections.\r\n"
    infoMsg += "Add '-publish' to the arguments to publish all selections in sequence, \r\n"
    infoMsg += "or add specific selection names to publish those only.\r\n"
    infoMsg += "Example: 'dbm -publish myPublishSelection'.\r\n"
    return infoMsg


def GetPublishSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    publishProperty = SwarmTools.GetProperties(arguments, PUBLISH_KEY, GetInfoMsg(), yamlData)
    if BuildTools.SELECTIONS_KEY in publishProperty:
        return publishProperty[BuildTools.SELECTIONS_KEY]
    return {}


def PublishSelections(selectionsToPublish, publishSelections):
    if len(selectionsToPublish) == 0:
        for publishSelection in publishSelections:
            PublishSelection(publishSelections[publishSelection], publishSelection)
    else:
        for selectionToPublish in selectionsToPublish:
            if selectionToPublish in publishSelections:
                PublishSelection(publishSelections[selectionToPublish], selectionToPublish)


def PublishSelection(publishSelection, publishSelectionKey):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(publishSelection)
    BuildTools.HandleTerminalCommandsSelection(publishSelection)

    if BuildTools.FILES_KEY in publishSelection:
        if BuildTools.TryGetFromDictionary(publishSelection, CONTAINER_ARTIFACT_KEY, True):
            PublishContainerSelection(publishSelection, publishSelectionKey)
        else:
            PublishArtifactSelection(publishSelection)

        BuildTools.HandleCopyFromContainer(publishSelection)
    
    os.chdir(cwd)


def PublishContainerSelection(publishSelection, publishSelectionKey):
    composeFiles = publishSelection[BuildTools.FILES_KEY]
    publishComposeFile = 'docker-compose.publish.' + publishSelectionKey + '.yml'
    DockerComposeTools.MergeComposeFiles(composeFiles, publishComposeFile)
    DockerComposeTools.PublishDockerImages(publishComposeFile)
    if BuildTools.ADDITIONAL_TAG_KEY in publishSelection:
        DockerComposeTools.PublishDockerImagesWithNewTag(publishComposeFile, publishSelection[BuildTools.ADDITIONAL_TAG_KEY])
    if BuildTools.ADDITIONAL_TAGS_KEY in publishSelection:
        for tag in publishSelection[BuildTools.ADDITIONAL_TAGS_KEY]:
            DockerComposeTools.PublishDockerImagesWithNewTag(publishComposeFile, tag)


def PublishArtifactSelection(publishSelection):
    DockerComposeTools.DockerComposeBuild(
        publishSelection[BuildTools.FILES_KEY])
    DockerComposeTools.DockerComposeUp(
        publishSelection[BuildTools.FILES_KEY], False)


def HandlePublishSelections(args):
    if not args.publish:
        return

    if args.help:
        print(GetInfoMsg())
        return

    selectionsToPublish = args.publish_selections

    publishSelections = GetPublishSelections(args.all_arguments)
    PublishSelections(selectionsToPublish, publishSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandlePublishSelections(ArgumentHandler.parse_arguments(arguments))
