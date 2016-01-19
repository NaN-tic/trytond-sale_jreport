# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import Model, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all_ = ['Configuration', 'SaleConfigurationCompany']
__metaclass__ = PoolMeta


class Configuration:
    __name__ = 'sale.configuration'

    sale_qty_decimal = fields.Function(fields.Boolean(
            'Sale Qty Decimal', help='Show qty with or without decimals'),
        'get_company_config', 'set_company_config')

    @classmethod
    def get_company_config(cls, configs, names):
        pool = Pool()
        CompanyConfig = pool.get('sale.configuration.company')

        company_id = Transaction().context.get('company')
        company_configs = CompanyConfig.search([
                ('company', '=', company_id),
                ])

        res = {}
        for fname in names:
            res[fname] = {
                configs[0].id: None,
                }
            if company_configs:
                val = getattr(company_configs[0], fname)
                if isinstance(val, Model):
                    val = val.id
                res[fname][configs[0].id] = val
        return res

    @classmethod
    def set_company_config(cls, configs, name, value):
        pool = Pool()
        CompanyConfig = pool.get('sale.configuration.company')

        company_id = Transaction().context.get('company')
        company_configs = CompanyConfig.search([
                ('company', '=', company_id),
                ])
        if company_configs:
            company_config = company_configs[0]
        else:
            company_config = CompanyConfig(company=company_id)
        setattr(company_config, name, value)
        company_config.save()


class SaleConfigurationCompany(ModelSQL):
    'Sale Configuration per Company'
    __name__ = 'sale.configuration.company'

    company = fields.Many2One('company.company', 'Company', required=True,
        ondelete='CASCADE', select=True)
    sale_qty_decimal = fields.Boolean('Sale Qty Decimal')
