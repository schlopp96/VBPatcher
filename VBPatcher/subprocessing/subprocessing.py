from subprocess import TimeoutExpired, call
from sys import exit as ex
from time import sleep
from typing import NoReturn

import applogger.applogger
import globalvars.globalvars
from PyLoadBar import load

logger = applogger.applogger._LogGenerator(globalvars.globalvars._logFile)

def _startPrompt() -> NoReturn | None:
    """Prompt user to decide whether to start Valheim immediately after program exit or not.

    ---

    :return: display user prompt.
    :rtype: NoReturn | None
    """
    while True:
        logger.info('Displaying start game prompt...')
        startPrompt: str = input(
            f'\nStart Game?\n\n> Enter [y] or [n]:\n{globalvars.globalvars._textborder}\n> ')
        match startPrompt.lower():
            case 'y'|'yes':
                _openValheim()
                return _exitPatcher()
            case 'n'|'no':
                logger.info('Patching process successfully completed!\n>> Preparing to exit...\n')
                load('\nPatching process successfully completed',
                     '\nPreparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{startPrompt}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                print(f'\nERROR: Invalid Input\n\n>> Your Entry: "{startPrompt}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
                sleep(1.250)
                continue


def _openValheim() -> int | None:
    """Calls command to open "Valheim" within Steam client.
    - Will raise `TimeoutExpired` exception if executable doesn't start within 10 seconds.
        - Prevents program from freezing due to any errors encountered during launch process.

    - Steam must be running to properly initialize launch process.

    ---

    :return: Start game client.
    :rtype: int | None
    """
    try:
        logger.info('Starting Valheim...\n\n')
        load("\nStarting Game", "Opening Valheim...")
        return call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 892970", timeout=10)
    except TimeoutExpired as exp:
        logger.error(f'Something went wrong... Having trouble starting game...\n>> {exp}\n')
        print(f'Something went wrong... Having trouble starting game...\n>> {exp}\n')
        return _exitPatcher()


def _exitPatcher() -> None | NoReturn:
    """Exit the application and finalize log.

    ---

    :return: Exits application.
    :rtype: None | NoReturn
    """
    logger.info(f'Exiting patcher...\n\n>> End of log...\n\n{globalvars.globalvars._textborder}\n')
    return ex()