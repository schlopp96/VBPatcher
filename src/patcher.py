#!/usr/bin/env python3
#@ ====================================================================================================== @#
#> Valheim BepInEx Patcher <#
#< Est. 10/24/21 >#
#@ ====================================================================================================== @#
#$ ====================================================================================================== $#
from os import chdir
from os.path import dirname
from shutil import copytree
from subprocess import call
from sys import exit as ex
from time import sleep
from typing import Any, NoReturn

from icecream import ic
from loadSequence import load

#$ ====================================================================================================== $#

#> Set working directory to location containing root VBP repository folder.
chdir(dirname(dirname(dirname(__file__))))

textborder: str = '=================================================='

#@ Declare variables containing patch files directory and destination:
patch_stable = "VBP\patch\stable"
patch_latest = r"VBP\patch\bleeding-edge"
build_Stable = "v5.18.00"
build_BleedingEdge = "e21677f"
patchDestination = "C:\Program Files (x86)\Steam\steamapps\common\Valheim"

def main() -> None | NoReturn:
    """Patcher for BepInEx, a modding console for Valheim.

    - User may choose between several patch installion options:
        - Latest stable build.
        - Latest bleeding-edge (beta) build.
        - Latest stable build, then latest bleeding-edge build afterwards.

    :return: patch BepInEx to chosen build.
    :rtype: None | NoReturn
    """

    while True:
        choosePatch: str = input(
            f"Which patch build would you like to install?\n[1.] Stable Release: {build_Stable}\n[2.] Bleeding-Edge Build: {build_BleedingEdge}\n[3.] Full build upgrade (apply both patches in order of release): {build_Stable} then {build_BleedingEdge}\n[4.] Exit Program\n\n> "
        )
        match choosePatch:
            case '1': stable_patch()
            case '2': BE_patch()
            case '3': full_patch()
            case '4':
                print('\nBepInEx patching process cancelled...')
                sleep(0.5)
                return exitPatcher()
            case _:
                print('\n\t- ERROR: Invalid Input -\n')
                ic(choosePatch)
                sleep(0.750)
                print(
                    f'\n==> Must ONLY enter [1] for stable release {build_Stable}, [2] for bleeding-edge build {build_BleedingEdge}, [3] for FULL upgrade (apply both patches in order), or [4] to exit program <==\n\n'
                )
                sleep(1.250)
                continue

        return exitPatcher()


def stable_patch() -> None:
    """Install latest BepInEx stable-build patch version to local directory.

    :return: Installs BepInEx patch.
    :rtype: None
    """

    while True:
        confirmStable: str = input(
            f'\nReally patch BepInEx to latest stable-build {build_Stable} in location:\n\n====> "{patchDestination}"?\n\n> Enter [y] or [n]:\n{textborder}\n> '
        )
        match confirmStable.lower():
            case 'yes'|'y':
                patch(patch_stable, patchDestination, build_Stable)
                promptStart()
            case 'n'|'no':
                load('\nBepInEx patching process cancelled', '\nClosing window...',
                False)
                break
            case _:
                print('\n\t- ERROR: Invalid Input -\n')
                ic(confirmStable)
                sleep(0.750)
                print(
                    '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
                )
                sleep(1.250)
                continue


def BE_patch() -> None:
    """Install latest BepInEx bleeding-edge patch version to local directory.

    :return: Install bleeding-edge patch to BepInEx directory.
    :rtype: None
    """
    while True:
        confirmLatest: str = input(
            f'\nReally patch BepInEx to the latest bleeding-edge beta build {build_BleedingEdge} in location:\n\n====> "{patchDestination}"?\n\n> Enter [y] or [n]:\n{textborder}\n> '
        )
        match confirmLatest.lower():
            case 'yes'|'y':
                patch(patch_stable, patchDestination, build_BleedingEdge)
                promptStart()
            case 'n'|'no':
                load('\nBepInEx patching process cancelled', '\nClosing window...',
                False)
                break
            case _:
                print('\n\t- ERROR: Invalid Input -\n')
                ic(confirmLatest)
                sleep(0.750)
                print(
                    '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
                )
                sleep(1.250)
                continue


def full_patch() -> None:
    """Install both latest BepInEx stable patch, before then installing bleeding-edge beta patch.

    :return: Install both stable and bleeding edge patch builds in order of release to BepInEx directory.
    :rtype: None
    """
    while True:
        confirmFull: str = input(
            f'\nReally install latest stable patch {build_Stable} then apply latest "bleeding-edge" build {build_BleedingEdge}?\n> Enter [y] or [n]:\n{textborder}\n> '
        )
        match confirmFull.lower():
            case 'yes'|'y':
                patch(patch_stable, patchDestination, build_Stable)
                patch(patch_stable, patchDestination, build_BleedingEdge)
                promptStart()
            case 'n'|'no':
                load('\nBepInEx patching process cancelled', '\nClosing window...',
                 False)
                break
            case _:
                print('\n\t- ERROR: Invalid Input -\n')
                ic(confirmFull)
                sleep(0.750)
                print(
                    '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
                )
                sleep(1.250)
                continue


def promptStart() -> NoReturn | None:
    """Prompt user to choose whether or not to start the game post patching.

    :return: Exits program or starts game.
    :rtype: NoReturn | None
    """
    while True:
        startPrompt: str = input(
            f'\nStart Game?\n\n> Enter [y] or [n]:\n{textborder}\n> ')
        match startPrompt:
            case 'y'|'yes':
                openValheim()
                return ex()
            case 'n'|'no':
                load('\nPatching process successfully completed',
                     '\nClosing window...', False)
                return ex()
            case _:
                print('\n\t- ERROR: Invalid Input -\n')
                ic(startPrompt)
                sleep(0.750)
                print(
                    '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
                )
                sleep(1.250)
                continue


def openValheim() -> int:
    """Calls command to open "Valheim".

    :return: Starts game.
    :rtype: int
    """
    load("\nStarting Game", "Opening Valheim...")
    return call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 892970")


def patch(patchFile: Any, patchLocation: Any, patchTitle: Any) -> Any:
    """Patch BepInEx according to provided parameter values.

    :param patchFile: Directory containing patch files.
    :type patchFile: Any
    :param patchLocation: Location of BepInEx install directory to install files.
    :type patchLocation: Any
    :param patchTitle: Build title of patch to be installed.
    :type patchTitle: Any
    :return: Patch BepInEx with desired version build.
    :rtype: Any
    """
    load(
        f'\nPatching BepInEx version/build {patchTitle} to location: {patchLocation}',
        f'\nPatch version/build {patchTitle} successfully installed!')
    return copytree(patchFile, patchLocation, dirs_exist_ok=True)


def exitPatcher() -> NoReturn:
    input('\nPress [ENTER] to exit...')
    ex()


if __name__ == '__main__':
    main()
