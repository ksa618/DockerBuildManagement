from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

from .ArgumentHandler import ArgumentHandler

BUILD_KEY = 'build'
SAVE_IMAGES_KEY = 'saveImages'


def GetInfoMsg():
    infoMsg = "Build selections is configured by adding a 'build' property to the .yaml file.\r\n"
    infoMsg += "The 'build' property is a dictionary of build selections.\r\n"
    infoMsg += "Add '-build' to the arguments to build all selections in sequence, \r\n"
    infoMsg += "or add specific selection names to build those only.\r\n"
    infoMsg += "Example: 'dbm -build myBuildSelection'.\r\n"
    return infoMsg


def GetBuildSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    buildProperty = SwarmTools.GetProperties(arguments, BUILD_KEY, GetInfoMsg(), yamlData)
    if BuildTools.SELECTIONS_KEY in buildProperty:
        return buildProperty[BuildTools.SELECTIONS_KEY]
    return {}


def BuildSelections(selectionsToBuild, buildSelections):
    if len(selectionsToBuild) == 0:
        for buildSelection in buildSelections:
            BuildSelection(buildSelections[buildSelection], buildSelection)
    else:
        for selectionToBuild in selectionsToBuild:
            if selectionToBuild in buildSelections:
                BuildSelection(buildSelections[selectionToBuild], selectionToBuild)


def BuildSelection(buildSelection, selectionToBuild):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(buildSelection)
    BuildTools.HandleTerminalCommandsSelection(buildSelection)

    if BuildTools.FILES_KEY in buildSelection:
        composeFiles = buildSelection[BuildTools.FILES_KEY]
        buildComposeFile = 'docker-compose.build.' + selectionToBuild + '.yml'
        DockerComposeTools.MergeComposeFiles(composeFiles, buildComposeFile)
        DockerComposeTools.DockerComposeBuild([buildComposeFile])
        if BuildTools.ADDITIONAL_TAG_KEY in buildSelection:
            DockerComposeTools.TagImages(buildComposeFile, buildSelection[BuildTools.ADDITIONAL_TAG_KEY])
        if BuildTools.ADDITIONAL_TAGS_KEY in buildSelection:
            for tag in buildSelection[BuildTools.ADDITIONAL_TAGS_KEY]:
                DockerComposeTools.TagImages(buildComposeFile, tag)
        if SAVE_IMAGES_KEY in buildSelection:
            outputFolder = buildSelection[SAVE_IMAGES_KEY]
            DockerComposeTools.SaveImages(buildComposeFile, outputFolder)
            
    os.chdir(cwd)


def HandleBuildSelections(args):
    if args.build:
        return

    if args.help:
        print(GetInfoMsg())
        return

    selectionsToBuild = args.build_selections

    buildSelections = GetBuildSelections(args.all_arguments)
    BuildSelections(selectionsToBuild, buildSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleBuildSelections(ArgumentHandler.parse_arguments(arguments))
