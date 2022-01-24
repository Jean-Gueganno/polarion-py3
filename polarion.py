
from __future__ import annotations

from time import time

from requests import exceptions as requests_exceptions
from zeep import exceptions as zeep_exceptions

from .polarion_access import PolarionAccess


class PolarionError(Exception):
    """A base class for Polarion-related issues."""


class InvalidWorkItem(PolarionError):
    """The Polarion work item provided is invalid."""


class SessionError(PolarionError):
    """The Polarion session is not active."""


class ComError(PolarionError):
    """The Polarion server is not reachable."""


class Polarion:
    """
        Polarion singleton
    """
    __instance = None
    _polarion_access: PolarionAccess = None
    project_id = ""
    project_prefix = ""

    @staticmethod
    def get_instance() -> Polarion:
        """
            Polarion accessor
            :return: Instance of Polarion if exist (Create singleton if not)
        """
        if Polarion.__instance is None:
            raise Exception("Polarion singleton class has to be initialize before it can be used")
        return Polarion.__instance

    def __init__(self, server, project_id, project_prefix, username, password):
        """
            Virtually private constructor
        """
        if Polarion.__instance is not None:
            raise Exception("Polarion class is a singleton, it should be instanced only once.")

        Polarion.__instance = self

        # Create polarion access instance
        self._polarion_access = PolarionAccess(server)
        self.project_id = project_id
        self.project_prefix = project_prefix

        # Log in to polarion using environment configuration
        self._polarion_access.log_in(username, password)
        # Get log-in time
        self._last_try_to_connect = time()

    @property
    def polarion_access(self) -> PolarionAccess:
        """
        Polarion connection status access property
        Catch network exceptions and try to reopen a new session in case of failure
        :return: Polarion access object
        """
        if self._polarion_access.is_connected:
            try:
                if self._polarion_access.session_is_logged_in:
                    # User is logged-in for the current session
                    return self._polarion_access
                else:
                    raise SessionError("Polarion session error: session is not active")

            except (requests_exceptions.ConnectionError, zeep_exceptions.Fault, SessionError) as exception:
                if time() - self._last_try_to_connect >= 60:
                    try:
                        self._last_try_to_connect = time()
                        # Try to reopen a new session
                        print("Try to reopen a new Polarion session")
                        self._polarion_access.connect()

                    except (requests_exceptions.ConnectionError, requests_exceptions.HTTPError, zeep_exceptions.Fault):
                        raise ComError(exception)

        return self._polarion_access
