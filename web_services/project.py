from zeep import Client


class ProjectWebService:
    """
    Class ProjectWebService
    This class gives access to ProjectWebService.wsdl description file
    """

    def __init__(self, polarion_access, server_prefix, session_header_element):
        self._polarion_access = polarion_access
        self.client = Client(server_prefix + 'ProjectWebService?wsdl')
        self.client.set_default_soapheaders([session_header_element])

    def get_project(self, project_id: str) -> object:
        """
        Method used to get project object using its ID
        :param project_id: the ID of the project to get
        :return: Project as an object
        """
        return self.client.service.getProject(project_id)

    def get_user(self, user_id: str) -> object:
        """
        Method used to get user object using its ID
        :param user_id: the ID of the user to get
        :return: User as an object
        """
        return self.client.service.getUser(user_id)
