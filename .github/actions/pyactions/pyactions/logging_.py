import traceback


class ActionsLogger:
    "Pseudo-logging.Logger compatible with GitHub Actions workflow commands output format"

    def debug(self, msg):
        print(f"::debug::{msg}")

    def info(self, msg):
        print(msg)

    def warning(self, msg):
        print(f"::warning::{msg}")

    def error(self, msg):
        print(f"::error::{msg}")

    def critical(self, msg):
        self.error(f"CRITICAL: {msg}")

    @contextlib.contextmanager
    def group(self, title):
        print(f"::group::{title}")
        yield
        print(f"::endgroup::")

    def _display_exception(self, e):
        with self.group(title=str(e)):
            self.info(f'{type(e)=}')
            traceback.print_exc()

    def exception(self, e):
        self._display_exception(e)

    def _display_pr(self, pr, title=None):
        title = title or f'PR #{pr.number} - {pr.title}'
        with self.group(title):
            print(pr)

    def _display_generic(self, obj, title=None):
        title = title or str(type(obj))
        with self.group(title):
            print(obj)

    def display(
            self,
            obj=None, title=None,
            **kwargs
        ):
        if obj is not None:
            self._display_generic(title=title)

        for key, obj_to_display in kwargs.items():
            if key in {'pr', 'pull', 'pull_request'}:
                self._display_pr(pr, title=title)
            else:
                title = title or _varname_to_dotted(key)
                self._display_generic(obj_to_display, title=title)


def _varname_to_dotted(s: str, sep='__'):
    return s.replace(sep, '.')


def get_logger(*args, **kwargs):
    return ActionsLogger()
