

from string import Template
from requests import exceptions as requests_exceptions
from zeep import exceptions as zeep_exceptions
from .workitem import PolarionWorkitem
from ..polarion import PolarionError


class PolarionTestCase(PolarionWorkitem):
    """
    PolarionTestCase
    """

    def __init__(self, test_case_id, workitem_type: str = None):

        if workitem_type:
            self.WORKITEM_TYPE = workitem_type

        try:
            PolarionWorkitem.__init__(self, test_case_id)
        except (requests_exceptions.ConnectionError, zeep_exceptions.Fault, PolarionError, AttributeError) as exception:
            raise PolarionError(f"Failed to create PolarionEcuTestCase object (error = {exception})") from exception

    @property
    def linked_defect_url(self) -> str:
        """
        Property used to get URL of linked defect
        :return: URL of linked defects
        """
        hostname = self.polarion_instance.polarion_access.hostname
        return "https://" + hostname + "/polarion/#/project/" + self.polarion_instance.project_id + \
               "/workitems/defect?query=linkedWorkItems:" + self.id

    def nb_steps(self):
        """
        Returns all steps
        returns: list of steps
        """
        steps_list = self.polarion_instance.polarion_access.test_management.get_test_steps(self.uri)
        nb_step = len(steps_list.steps.TestStep)
        return nb_step

    def get_steps(self):
        """
        Returns all steps
        returns: list of steps
        """
        steps_list = self.polarion_instance.polarion_access.test_management.get_test_steps(self.uri)
        return steps_list.steps.TestStep

    def get_step(self, index):

        steps_list = self.get_steps()
        step = steps_list[index].values
        return step

    def get_step_column_content(self, index, column) -> str:

        content = self.get_step(index).Text[column].content
        return content
