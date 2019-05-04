import sys

from SwarmManagement import SwarmTools

from DockerBuildManagement import ChangelogSelections, BuildSelections, PublishSelections, RunSelections, \
    SwarmSelections, TestSelections, BuildTools
from .ArgumentHandler import ArgumentHandler


def GetInfoMsg():
    infoMsg = "Docker Build Management\r\n\r\n"
    infoMsg += "Run:\r\n"
    infoMsg += RunSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Build:\r\n"
    infoMsg += BuildSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Publish:\r\n"
    infoMsg += PublishSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Test:\r\n"
    infoMsg += TestSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Swarm Deployment of Domain Services:\r\n"
    infoMsg += SwarmSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Export Version From Changelog:\r\n"
    infoMsg += ChangelogSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Additional Info:\r\n"
    infoMsg += BuildTools.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Add '-help' to arguments to print this info again.\r\n\r\n"
    return infoMsg
    
    
def HandleManagement(arguments):
    if len(arguments) == 0:
        print(GetInfoMsg())
        return

    args = ArgumentHandler.parse_arguments(arguments)

    if args.help in args and len(arguments) == 1:
        print(GetInfoMsg())
        return
    
    SwarmTools.LoadEnvironmentVariables(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    SwarmTools.HandleDumpYamlData(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    ChangelogSelections.HandleChangelogSelections(arguments)
    SwarmSelections.HandleSwarmSelections(arguments)
    BuildSelections.HandleBuildSelections(arguments)
    TestSelections.HandleTestSelections(arguments)
    RunSelections.HandleRunSelections(arguments)
    PublishSelections.HandlePublishSelections(arguments)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleManagement(ArgumentHandler.parse_arguments(arguments))
