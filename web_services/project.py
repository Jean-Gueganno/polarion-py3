from zeep import Client


class ProjectWebService:
    def __init__(self, web_service_factory, server_prefix):
        self.web_service_factory = web_service_factory
        self.client = Client(server_prefix + 'ProjectWebService?wsdl')

    def get_project(self, project_id):
        """
        Gets a project
        :param project_id: the ID of the project to get
        :return: project
        """
        return self.client.service.getProject(project_id)
