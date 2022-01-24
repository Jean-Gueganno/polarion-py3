

import re
from .comment import CommentsTree
from ..polarion import Polarion, InvalidWorkItem


def clean_html(string_to_clean):
    """
    Method to remove HTML & non ASCII characters formatting from input
    """
    string_to_clean = re.sub(r'[^\x00-\x7F]+', ' ', string_to_clean)
    clean_string = re.sub('<[^<]+?>', '', string_to_clean)
    return clean_string


class PolarionWorkitem:
    """
    Class PolarionWorkitem
    """
    WORKITEM_TYPE = ""

    def __init__(self, arg):
        self.polarion_instance = Polarion.get_instance()

        self._workitem = None
        self._comments = None

        if isinstance(arg, str):
            workitem_id = self.polarion_instance.project_prefix + arg if re.search("^\\d+$", arg) else arg

            self._workitem = self.polarion_instance.polarion_access.tracker.get_workitem_by_id(
                self.polarion_instance.project_id, workitem_id)
        else:
            self._workitem = arg

        if self._workitem.type:
            if self._workitem.type.id != self.WORKITEM_TYPE:
                raise InvalidWorkItem(f"Polarion workitem {self._workitem.type.id} is not an {self.WORKITEM_TYPE}.")

            self._initialization()

        else:
            raise InvalidWorkItem("Polarion workitem has not been found.")

    def _initialization(self) -> None:
        """
        Protected method used to finalize the object instantiation
        :return: None
        """
        self._comments = CommentsTree(self.workitem)

    @property
    def uri(self):
        return self._workitem.uri

    @property
    def comments(self) -> object:
        """
        Property used to get comments linked to the workitem
        :return: Comments object
        """
        return self._comments

    @property
    def workitem(self):
        """
        Property used to get workitem object
        :return: Workitem object or raise exception if there is a polarion connexion issue
        """
        return self._workitem

    @property
    def id(self) -> str:
        """
        Property used to get workitem id
        :return: workitem id
        """
        return self.workitem.id

    @property
    def author(self):
        """
        Property used to get workitem author
        :return: workitem id
        """
        return self.workitem.author.name

    @property
    def status(self) -> str:
        """
        Property used to get workitem workflow status
        :return: Workflow status of the workitem
        """
        return self.workitem.status.id

    @property
    def severity(self) -> str:
        """
        Property used to get workitem severity
        :return: Severity of the workitem
        """
        return self.workitem.severity.id

    @property
    def title(self) -> str:
        """
        Property used to get workitem title
        :return: workitem title
        """
        return self.workitem.title

    @property
    def description(self) -> str:
        """
        Property used to get workitem description
        :return: workitem description
        """
        return self.workitem.description.content

    @property
    def url(self) -> str:
        """
        Property used to get the url of the workitem
        :return: Workitem url
        """
        hostname = Polarion.get_instance().polarion_access.hostname
        return "https://" + hostname + "/polarion/#/project/" + self.workitem.project.id + "/workitem?id=" \
               + self.workitem.id

    def get_comment_by_uri(self, uri: str) -> object or None:
        """
        Method used to get specific comment using its URI
        :param uri: URI of the comment
        :return: Comment object if exist, else None
        """
        if self.workitem.comments:
            for comment in self.workitem.comments.Comment:
                if comment.uri == uri:
                    return comment
        return None

    def get_custom_field_value(self, custom_field_id: str) -> object or None:
        """
        Method used to get a specific custom field value within a list of custom fields
        :param custom_field_id: Custom field id corresponding value to return
        :return: Value or None if custom field doesn't exist
        """
        if self.workitem.customFields is None:
            return None

        custom_fields_list = self.workitem.customFields["Custom"]

        for custom_field in custom_fields_list:
            if custom_field["key"] == custom_field_id:
                return custom_field["value"]

        return None
