from ghapi.all import GhApi


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

    def _get_api_call_params(self, target=None):
        params = {
            'name': self.label_name,
        }
        if target:
            params['issue_number'] = target.number
        return params

    def _unset_label(self, api, **kwargs):
        params = self._get_api_call_params(**kwargs)
        try:
            api.issues.remove_label(**params)
        # TODO figure out the most precise error that is raised when the label cannot be removed because it doesn't exist
        except Exception as e:
            pass

    def _set_label(self, api, **kwargs):
        params = self._get_api_call_params(**kwargs)
        try:
            api.issues.add_label(**params)
        except Exception as e:
            pass

    def emit(self, api, target=None, reset_now=True):

        self._unset_label(api, target=target)
        self._set_label(api, target=target)
        if reset_now:
            self.reset(api, target=target)

    def reset(self, api, target=None):
        self._unset_label(api, target=target)
