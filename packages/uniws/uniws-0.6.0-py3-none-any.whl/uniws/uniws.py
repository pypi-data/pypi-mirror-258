# PYTHON_ARGCOMPLETE_OK

from .app import *


def uws() -> 'None':
    main(AppWorkspace())


def uhc() -> 'None':
    main(AppWare(
        ware=hardware(),
        name='connect',
        help='Connection to the hardware.',
    ))


def uhp() -> 'None':
    main(AppWare(
        ware=hardware(),
        name='power',
        help='Power state of the hardware.',
    ))


def uhu() -> 'None':
    main(AppWare(
        ware=hardware(),
        name='upload',
        help='Upload files to the hardware.',
    ))


def uhd() -> 'None':
    main(AppWare(
        ware=hardware(),
        name='download',
        help='Download files from the hardware.',
    ))


def uhs() -> 'None':
    main(AppWare(
        ware=hardware(),
        name='shell',
        help='Use the hardware shell.',
    ))


def uha() -> 'None':
    main(AppWare(
        ware=hardware(),
        name='action',
        help='Custom actions on the hardware.',
    ))


def usd() -> 'None':
    main(AppWare(
        ware=software(),
        name='download',
        help='Download the software sources.',
    ))


def usb() -> 'None':
    main(AppWare(
        ware=software(),
        name='build',
        help='Build the software.',
    ))


def usi() -> 'None':
    main(AppWare(
        ware=software(),
        name='install',
        help='Install the software.',
    ))


def ust() -> 'None':
    main(AppWare(
        ware=software(),
        name='test',
        help='Test the software.',
    ))


def usc() -> 'None':
    main(AppWare(
        ware=software(),
        name='clean',
        help='Clean the software.',
    ))


def usa() -> 'None':
    main(AppWare(
        ware=software(),
        name='action',
        help='Custom actions on the software.',
    ))
