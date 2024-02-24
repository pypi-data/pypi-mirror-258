# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import logging
import smtplib
import ssl

from urllib.parse import unquote_plus

from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.pyson import Eval

logger = logging.getLogger(__name__)


class SmtpServer(ModelSQL, ModelView):
    'SMTP Servers'
    __name__ = 'smtp.server'
    name = fields.Char('Name', required=True)
    smtp_server = fields.Char('Server', required=True,
        states={
            'readonly': (Eval('state') != 'draft'),
            })
    smtp_timeout = fields.Integer('Timeout', required=True,
        states={
            'readonly': (Eval('state') != 'draft'),
            }, help="Time in secods")
    smtp_port = fields.Integer('Port', required=True,
        states={
            'readonly': (Eval('state') != 'draft'),
            })
    smtp_ssl = fields.Boolean('SSL',
        states={
            'readonly': (Eval('state') != 'draft'),
            })
    smtp_tls = fields.Boolean('TLS',
        states={
            'readonly': (Eval('state') != 'draft'),
            })
    ssl_verify = fields.Boolean('SSL Certificate Verification',
        states={
            'readonly': (Eval('state') != 'draft'),
            })
    smtp_user = fields.Char('User',
        states={
            'readonly': (Eval('state') != 'draft'),
            },
        help='The SMTP user, pay attention to correct '
        'URL-encoding, e.g. plus signs must be encoded.\n'
        's.a. https://meyerweb.com/eric/tools/dencoder/')
    smtp_password = fields.Char('Password', strip=False,
        states={
            'readonly': (Eval('state') != 'draft'),
            },
        help='The SMTP password, pay attention to correct '
        'URL-encoding, e.g. plus signs must be encoded.\n'
        's.a. https://meyerweb.com/eric/tools/dencoder/')
    smtp_use_email = fields.Boolean('Use email',
        states={
            'readonly': (Eval('state') != 'draft'),
            }, help='Force to send emails using this email')
    smtp_email = fields.Char('Email', required=True,
        states={
            'readonly': (Eval('state') != 'draft'),
            },
        help='Default From (if active this option) and Reply Email')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('done', 'Done'),
            ], 'State', readonly=True, required=True)
    default = fields.Boolean('Default')
    models = fields.Many2Many('smtp.server-ir.model',
            'server', 'model', 'Models',
        states={
            'readonly': Eval('state').in_(['done']),
            })

    @classmethod
    def __setup__(cls):
        super(SmtpServer, cls).__setup__()
        cls._buttons.update({
                'get_smtp_test': {},
                'draft': {
                    'invisible': Eval('state') == 'draft',
                    'depends': ['state'],
                    },
                'done': {
                    'invisible': Eval('state') == 'done',
                    'depends': ['state'],
                    },
                })

    @classmethod
    def check_xml_record(cls, records, values):
        return True

    @staticmethod
    def default_default():
        return True

    @staticmethod
    def default_smtp_timeout():
        return 60

    @staticmethod
    def default_smtp_ssl():
        return True

    @staticmethod
    def default_ssl_verify():
        return True

    @staticmethod
    def default_smtp_port():
        return 465

    @staticmethod
    def default_state():
        return 'draft'

    @classmethod
    @ModelView.button
    def draft(cls, servers):
        cls.write(servers, {
                'state': 'draft',
                })

    @classmethod
    @ModelView.button
    def done(cls, servers):
        cls.write(servers, {
                'state': 'done',
                })

    @classmethod
    @ModelView.button
    def get_smtp_test(cls, servers):
        """Checks SMTP credentials and confirms if outgoing connection works"""
        for server in servers:
            try:
                server.get_smtp_server()
            except Exception as message:
                logger.error('Exception getting smtp server: %s', message)
                raise UserError(gettext('smtp.smtp_test_details',
                    error=message))
            raise UserError(gettext('smtp.smtp_successful'))

    def get_smtp_server(self):
        """
        Instanciate, configure and return a SMTP or SMTP_SSL instance from
        smtplib.
        :return: A SMTP instance. The quit() method must be call when all
        the calls to sendmail() have been made.
        """
        ssl_context = ssl.create_default_context() if self.ssl_verify else None
        if self.smtp_ssl:
            smtp_server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port,
                timeout=self.smtp_timeout, context=ssl_context)
            uri = 'smtps'
        else:
            smtp_server = smtplib.SMTP(self.smtp_server, self.smtp_port,
                timeout=self.smtp_timeout)
            uri = 'smtp'

        if self.smtp_tls:
            smtp_server.starttls(context=ssl_context)
            uri += '+tls'

        if self.smtp_user and self.smtp_password:
            smtp_server.login(
                unquote_plus(self.smtp_user),
                unquote_plus(self.smtp_password)
                )
            uri += '%s:%s@' % (self.smtp_user, self.smtp_password)

        uri += '://%s' % self.smtp_server
        if self.smtp_port:
            uri += ':%s' % self.smtp_port

        smtp_server.uri = uri

        return smtp_server

    @classmethod
    def get_smtp_server_from_model(self, model):
        """
        Return Server from Models
        :param model: str Model name
        return object server
        """
        model = Pool().get('ir.model').search([('model', '=', model)])[0]
        servers = Pool().get('smtp.server-ir.model').search([
                ('model', '=', model),
                ], limit=1)
        if not servers:
            logger.warning('No SMTP server found for model %s' % model)
            raise UserError(gettext(
                'smtp.server_model_not_found', model=model.name))
        return servers[0].server

    def send_mail(self, from_, cc, email):
        try:
            smtp_server = self.get_smtp_server()
            issues = smtp_server.sendmail(from_, cc, email)
            smtp_server.quit()
            return True
        except smtplib.SMTPException as error:
            logger.error('SMTPException: %s', error)
            raise UserError(gettext('smtp.smtp_exception', error=error))
        except smtplib.socket.error as error:
            logger.error('socket.error: %s', error)
            raise UserError(gettext('smtp.smtp_server_error', error=error))
        except smtplib.SMTPRecipientsRefused as error:
            logger.error('socket.error: %s', error)
            raise UserError(gettext('smtp.smtp_server_error', error=error))
        return False


class SmtpServerModel(ModelSQL):
    'SMTP Server - Model'
    __name__ = 'smtp.server-ir.model'
    _table = 'smtp_server_ir_model'

    server = fields.Many2One('smtp.server', 'Server', ondelete='CASCADE',
        required=True)
    model = fields.Many2One('ir.model', 'Model', ondelete='RESTRICT',
        required=True)
