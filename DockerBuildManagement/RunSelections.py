from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

from .ArgumentHandler import ArgumentHandler

RUN_KEY = 'run'
ABORT_ON_CONTAINER_EXIT_KEY = 'abortOnContainerExit'
DETACHED_KEY = 'detached'

def GetInfoMsg():
    infoMsg = "Run selections is configured by adding a 'run' property to the .yaml file.\r\n"
    infoMsg += "The 'run' property is a dictionary of run selections.\r\n"
    infoMsg += "Add '-run' to the arguments to run all runnable selections in sequence, \r\n"
    infoMsg += "or add specific selection names to run those only.\r\n"
    infoMsg += "Example: 'dbm -run myRunnableSelection'.\r\n"
    return infoMsg


def GetRunSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    runProperty = SwarmTools.GetProperties(arguments, RUN_KEY, GetInfoMsg(), yamlData)
    if BuildTools.SELECTIONS_KEY in runProperty:
        return runProperty[BuildTools.SELECTIONS_KEY]
    return {}


def RunSelections(selectionsToRun, runSelections):
    if len(selectionsToRun) == 0:
        for runSelection in runSelections:
            RunSelection(runSelections[runSelection])
    else:
        for selectionToRun in selectionsToRun:
            if selectionToRun in runSelections:
                RunSelection(runSelections[selectionToRun])


def RunSelection(runSelection):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(runSelection)
    BuildTools.HandleTerminalCommandsSelection(runSelection)

    if BuildTools.FILES_KEY in runSelection:
        DockerComposeTools.DockerComposeUp(
            runSelection[BuildTools.FILES_KEY],
            BuildTools.TryGetFromDictionary(runSelection, ABORT_ON_CONTAINER_EXIT_KEY, True),
            BuildTools.TryGetFromDictionary(runSelection, DETACHED_KEY, False))

        BuildTools.HandleCopyFromContainer(runSelection)
    
    os.chdir(cwd)


def HandleRunSelections(args):
    if not args.run:
        return

    if args.help:
        print(GetInfoMsg())
        return

    selectionsToRun = args.run_selections

    runSelections = GetRunSelections(args.all_arguments)
    RunSelections(selectionsToRun, runSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleRunSelections(ArgumentHandler.parse_arguments(arguments))
