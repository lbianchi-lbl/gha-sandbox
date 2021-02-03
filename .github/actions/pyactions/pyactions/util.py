from ghapi.all import GhApi

from .actions import Logger


_log = Logger()


class CILabels:
    run_integration = 'CI:run-integration'


class Trigger:

    def emit(self, api, **kwargs):
        ...

    def reset(self, api, **kwargs):
        ...


class LabelAddTrigger(Trigger):
    """
    run_integration_trigger = LabelTrigger(CILabels.run_integration)
    for pr in api.pulls.get():
        run_integration_trigger.emit(api, target=pr, reset_now=True)

    run_integration_trigger.reset(api, target=pr)

    """
    def __init__(self, label_name):
        self.label_name = label_name

    def _unset_label(self, api, target=None):
        params = dict(name=self.label_name)
        if target:
            params.update(issue_number=target.number)

        try:
            api.issues.remove_label(**params)
        # TODO figure out the most precise error that is raised when the label cannot be removed because it doesn't exist
        except Exception as e:
            _log.exception(e)

    def _set_label(self, api, target=None):
        params = dict(labels=[self.label_name])
        if target:
            params.update(issue_number=target.number)

        try:
            api.issues.add_labels(**params)
        except Exception as e:
            _log.exception(e)

    def emit(self, api, target=None, reset_now=True):

        self._unset_label(api, target=target)
        self._set_label(api, target=target)
        if reset_now:
            self.reset(api, target=target)

    def reset(self, api, target=None):
        self._unset_label(api, target=target)
