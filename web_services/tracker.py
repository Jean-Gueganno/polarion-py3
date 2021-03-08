from zeep import Client


class TrackerWebService:
    def __init__(self, web_service_factory, server_prefix):
        self.web_service_factory = web_service_factory
        self.client = Client(server_prefix + 'TrackerWebService?wsdl')

    def create_workitem(self, project_id, type_id, title, description_content=""):
        """
        Function used to create a new workitem
        :param project_id: project id (string)
        :param type_id: workitem type id(string)
        :param title: workitem title (string)
        :param description_content: workitem description (string)
        :return: URI of created work item
        """

        # Create a new workitem
        workitem = self.client.type_factory('tns3:WorkItem')

        # Set project
        project = self.web_service_factory.project_web_service.client.service.getProject(project_id)
        workitem.project._uri = project._uri

        # Set type
        workitem.type = self.client.type_factory('tns3:EnumOptionId')
        workitem.type.id = type_id

        # Set title
        workitem.title = self.client.type_factory('xsd:string')
        workitem.title = title

        # Set description
        workitem.description = self.client.type_factory('tns2:Text')
        workitem.description.type = 'text/html'
        workitem.description.content = description_content.replace("\n", "<br>")
        workitem.description.contentLossy = False

        # Create the work item.
        return self.client.service.createWorkItem(workitem)

    def get_workitem_list(self, query, sort, fields):
        """
        Function used to get a list of workitems using Polarion query (can be found using filter option in Polarion)
        :param query:  (string) the lucene query to be used
        :param sort: (string) the field to be used for sorting
        :param fields: (string[]) the keys of the fields that should be filled.
        :return: the list of workitems
        """

        return self.client.service.queryWorkItems(query, sort, fields)

    def get_workitem_by_id(self, project_id, workitem_id):
        """
        Function used to get a workitem using project and workitem IDs
        :param project_id: the id of the project that contains the workitem to get
        :param workitem_id: the id of the work item to get
        :return:
        """

        return self.client.service.getWorkItemById(project_id, workitem_id)

    def get_custom_field(self, workitem_uri, custom_field_key):
        """
        Function used to get a custom field of a work item
        :param workitem_uri: the URI of the work item to get the custom field from
        :param custom_field_key: the key of the custom field
        :return:
        """

        return self.client.service.getCustomField(workitem_uri, custom_field_key)

    def add_comment(self, workitem_uri, title, comment):
        """

        :param workitem_uri:
        :param title:
        :param comment:
        :return:
        """
        comment_text = self.client.type_factory('tns2:Text')
        comment_text.type = 'text/html'
        comment_text.content = comment
        comment_text.contentLossy = False

        self.client.service.addComment(workitem_uri, title, comment_text)

    def set_status(self, project_id, workitem_id, value):
        workitem = self.get_workitem_by_id(project_id, workitem_id)
        workitem.status.id = value
        self.client.service.updateWorkItem(workitem)

    def set_severity(self, project_id, workitem_id, value):
        workitem = self.get_workitem_by_id(project_id, workitem_id)
        enum = self.client.type_factory('tns3:EnumOptionId')
        enum.id = value
        workitem.severity = enum
        self.client.service.updateWorkItem(workitem)

    def set_custom_field(self, workitem_uri, custom_field_key, value):
        """
        Function used to get a custom field of a work item
        :param workitem_uri: the URI of the work item to get the custom field from
        :param custom_field_key: the key of the custom field
        :param value: Value to set
        :return:
        """
        enum = self.client.type_factory('tns3:EnumOptionId')
        enum.id = value

        custom_field = self.client.type_factory('tns3:CustomField')

        custom_field.key = custom_field_key
        custom_field.parentItemURI = workitem_uri
        custom_field.value = enum

        return self.client.service.setCustomField(custom_field)

    def add_linked_item(self, project_id, workitem_uri_id, linked_workitem_uri_id, role):
        """
        Adds a linked work item
        :param project_id: project id
        :param workitem_uri_id: the ID of the work item to add the link to
        :param linked_workitem_uri_id: the ID of the target work item the link points to
        :param role: the role of the link to add
        :return: operation success
        """

        # Translate string into polarion type
        new_role = self.client.type_factory('tns3:EnumOptionId')
        new_role.id = role

        # Get the two concerned items
        workitem = self.get_workitem_by_id(project_id, workitem_uri_id)
        linked_workitem = self.get_workitem_by_id(project_id, linked_workitem_uri_id)

        # Set the link
        return self.client.service.addLinkedItem(workitem._uri, linked_workitem._uri, new_role)
