from ansible.module_utils._text import to_text


class FilterModule(object):

    def filters(self):
        return {
            'project_name': self.project_name
        }

    def project_name(self, arg):
        """Extract name of a project from a GitHub reference
        of the form owner/repo.
        """
        return to_text(arg.split('/')[1])
