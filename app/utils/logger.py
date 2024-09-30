import logging
import coloredlogs

class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        frame = logging.currentframe().f_back.f_back
        class_name = frame.f_locals.get('self', None).__class__.__name__ if 'self' in frame.f_locals else ''
        return f'[{class_name}] {msg}', kwargs

coloredlogs.install(
    level='DEBUG',
    fmt='%(asctime)s %(filename)s %(funcName)s %(lineno)d [%(process)d] %(levelname)s %(message)s',
    level_styles = {
        'debug': {'color': 'green'},
        'info': {'color': 'blue'},
        'warning': {'color': 'yellow'},
        'error': {'color': 'red'},
        'critical': {'color': 'red', 'bold': True},
    },
    field_styles = {
        'asctime': {'color': 'magenta'},
        'hostname': {'color': 'cyan'},
        'levelname': {'color': 8, 'bold': True},
        'name': {'color': 'blue'},
        'programname': {'color': 'cyan'},
        'process': {'color': 'magenta'},
        'filename': {'color': 'green'},
        'funcname': {'color': 'yellow'},
        'lineno': {'color': 'cyan'},    
    }
)

log = logging.getLogger(__name__)