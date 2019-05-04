from SwarmManagement import SwarmTools, SwarmManager
from DockerBuildManagement import BuildTools
import sys
import os

from .ArgumentHandler import ArgumentHandler

SWARM_KEY = 'swarm'
PROPERTIES_KEY = 'properties'


def GetInfoMsg():
    infoMsg = "Swarm selections is configured by adding a 'swarm' property to the .yaml file.\r\n"
    infoMsg += "The 'swarm' property is a dictionary of swarm selections.\r\n"
    infoMsg += "Add '-swarm -start' to the arguments to initiate all swarm selections, \r\n"
    infoMsg += "or add specific selection names to start those only.\r\n"
    infoMsg += "Add '-swarm -stop' to the arguments to stop all swarm selections, \r\n"
    infoMsg += "or add specific selection names to stop those only.\r\n"
    infoMsg += "Add '-swarm -restart' to the arguments to restart all swarm selections, \r\n"
    infoMsg += "or add specific selection names to restart those only.\r\n"
    infoMsg += "Example: 'dbm -swarm -start mySwarmSelection'.\r\n"
    infoMsg += "Example: 'dbm -swarm -stop mySwarmSelection'.\r\n"
    infoMsg += "Example: 'dbm -swarm -restart mySwarmSelection'.\r\n"
    return infoMsg


def GetSwarmSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    swarmProperty = SwarmTools.GetProperties(arguments, SWARM_KEY, GetInfoMsg(), yamlData)
    if BuildTools.SELECTIONS_KEY in swarmProperty:
        return swarmProperty[BuildTools.SELECTIONS_KEY]
    return {}


def DeploySwarmSelections(swarmSelectionsToDeploy, swarmSelections, prefix):
    if len(swarmSelectionsToDeploy) == 0:
        for swarmSelection in swarmSelections:
            DeploySwarmSelection(swarmSelections[swarmSelection], prefix)
    else:
        for swarmSelectionToDeploy in swarmSelectionsToDeploy:
            if swarmSelectionToDeploy in swarmSelections:
                DeploySwarmSelection(swarmSelections[swarmSelectionToDeploy], prefix)


def DeploySwarmSelection(swarmSelection, prefix):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(swarmSelection)
    BuildTools.HandleTerminalCommandsSelection(swarmSelection)
    SwarmManager.HandleManagement(
        [prefix] + BuildSwarmManagementFilesRow(swarmSelection) + BuildSwarmManagementPropertiesRow(swarmSelection))
    os.chdir(cwd)


def BuildSwarmManagementFilesRow(swarmSelection):
    swarmManagementFiles = []
    if not(BuildTools.FILES_KEY in swarmSelection):
        return swarmManagementFiles
    for swarmManagementFile in swarmSelection[BuildTools.FILES_KEY]:
        swarmManagementFiles += ['-f', swarmManagementFile]
    return swarmManagementFiles


def BuildSwarmManagementPropertiesRow(swarmSelection):
    swarmManagementProperties = []
    if not(PROPERTIES_KEY in swarmSelection):
        return swarmManagementProperties
    for swarmManagementProperty in swarmSelection[PROPERTIES_KEY]:
        swarmManagementProperties += str.split(swarmManagementProperty)
    return swarmManagementProperties


def GetSwarmCommand(args):
    if args.start is not None:
        return '-start'
    if args.stop is not None:
        return '-stop'
    if args.restart is not None:
        return '-restart'
    return ''


def CheckSwarmCommandInArguments(args):
    if GetSwarmCommand(args) == '':
        return False
    return True


def CheckSwarmInArguments(arguments):
    if '-swarm' in arguments or '-s' in arguments:
        return True
    return False


def HandleSwarmSelections(args):
    if not args.swarm and not CheckSwarmCommandInArguments(args):
        return

    if args.help:
        print(GetInfoMsg())
        return

    if args.swarm and not CheckSwarmCommandInArguments(arguments):
        print(GetInfoMsg())

    swarmSelectionsToDeploy = args.swarm_selections

    if not args.swarm and CheckSwarmCommandInArguments(arguments):
        swarmSelectionsToDeploy += args.start_selections
        swarmSelectionsToDeploy += args.stop_selections
        swarmSelectionsToDeploy += args.restart_selections

    swarmSelections = GetSwarmSelections(args.all_arguments)
    DeploySwarmSelections(swarmSelectionsToDeploy, swarmSelections, GetSwarmCommand(arguments))


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleSwarmSelections(ArgumentHandler.parse_arguments(arguments))
