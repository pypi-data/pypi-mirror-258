__version__ = "0.0.16.dev1"


def dash_board():
    """Launches the dash board."""
    from .dashBoard import main
    dashBoard.main()


def getShipments():
    """getShipments."""
    from .getShipments import main
    main()


def glueWeight():
    """glue weight."""
    from .GlueWeight import main
    main()


def groundVITests():
    """GND/VI tests."""
    from .groundVITests import main
    main()


def sendShipments():
    """Send items."""
    from .sendShipments import main
    main()


def uploadTest():
    """Upload tests."""
    from .uploadTest import main
    main()


def uploadMultipleTests():
    """Upload multiple tests."""
    from .uploadMultipleTests import main
    main()

def uploadIVfiles():
    """Upload IV files of single and double modules"""
    from .uploadIVfiles import main
    main()
