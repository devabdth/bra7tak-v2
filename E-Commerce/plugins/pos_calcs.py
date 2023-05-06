class POSCalculations:
    def __init__(self, db):
        self.db = db

    def report(self, start_date=0, end_date=999999999999999999):
        return {
            'OVERVIEW': self.generate_overview(),
            'CONVERSION_RATE': self.calculate_margins(),
            'ROI': self.calculate_roi()
        }

    def generate_overview(self, start_date=0, end_date=999999999999999999):
        report = {}
        report['INPUTS'] = {}
        report['OUTPUTS'] = {}

        report['INPUTS']['ORDERS'] = self.db.pos.inputs.loc[self.db.pos.inputs['date'] > start_date]
        report['INPUTS']['ORDERS'] = report['INPUTS']['ORDERS'].loc[report['INPUTS']
                                                                    ['ORDERS']['date'] < end_date]
        report['INPUTS']['ORDERS'] = report['INPUTS']['ORDERS'].loc[report['INPUTS']
                                                                    ['ORDERS']['direction'].str.contains('Order')]
        report['INPUTS']['ORDERS'] = sum(report['INPUTS']['ORDERS']['amount'])

        report['INPUTS']['DEALS'] = self.db.pos.inputs.loc[self.db.pos.inputs['date'] > start_date]
        report['INPUTS']['DEALS'] = report['INPUTS']['DEALS'].loc[report['INPUTS']
                                                                  ['DEALS']['date'] < end_date]
        report['INPUTS']['DEALS'] = report['INPUTS']['DEALS'].loc[report['INPUTS']
                                                                  ['DEALS']['direction'].str.contains('Deal')]
        report['INPUTS']['DEALS'] = sum(report['INPUTS']['DEALS']['amount'])

        report['OUTPUTS']['STOCK'] = self.db.pos.outputs.loc[self.db.pos.outputs['date'] > start_date]
        report['OUTPUTS']['STOCK'] = report['OUTPUTS']['STOCK'].loc[report['OUTPUTS']
                                                                    ['STOCK']['date'] < end_date]
        report['OUTPUTS']['STOCK'] = report['OUTPUTS']['STOCK'].loc[report['OUTPUTS']
                                                                    ['STOCK']['direction'].str.contains('Stock')]
        report['OUTPUTS']['STOCK'] = sum(report['OUTPUTS']['STOCK']['amount'])

        report['OUTPUTS']['SALARIES'] = self.db.pos.outputs.loc[self.db.pos.outputs['date'] > start_date]
        report['OUTPUTS']['SALARIES'] = report['OUTPUTS']['SALARIES'].loc[report['OUTPUTS']
                                                                          ['SALARIES']['date'] < end_date]
        report['OUTPUTS']['SALARIES'] = report['OUTPUTS']['SALARIES'].loc[report['OUTPUTS']
                                                                          ['SALARIES']['direction'].str.contains('Salary')]
        report['OUTPUTS']['SALARIES'] = sum(
            report['OUTPUTS']['SALARIES']['amount'])

        report['OUTPUTS']['BILLS'] = self.db.pos.outputs.loc[self.db.pos.outputs['date'] > start_date]
        report['OUTPUTS']['BILLS'] = report['OUTPUTS']['BILLS'].loc[report['OUTPUTS']
                                                                    ['BILLS']['date'] < end_date]
        report['OUTPUTS']['BILLS'] = report['OUTPUTS']['BILLS'].loc[report['OUTPUTS']
                                                                    ['BILLS']['direction'].str.contains('Bills')]
        report['OUTPUTS']['BILLS'] = sum(report['OUTPUTS']['BILLS']['amount'])

        report['OUTPUTS']['INVESTMENTS'] = self.db.pos.outputs.loc[self.db.pos.outputs['date'] > start_date]
        report['OUTPUTS']['INVESTMENTS'] = report['OUTPUTS']['INVESTMENTS'].loc[report['OUTPUTS']
                                                                                ['INVESTMENTS']['date'] < end_date]
        report['OUTPUTS']['INVESTMENTS'] = report['OUTPUTS']['INVESTMENTS'].loc[report['OUTPUTS']
                                                                                ['INVESTMENTS']['direction'].str.contains('Investment')]
        report['OUTPUTS']['INVESTMENTS'] = sum(
            report['OUTPUTS']['INVESTMENTS']['amount'])

        return report

    def calculate_margins(self, start_date=0, end_date=999999999999999999):
        report = {}
        report['TOTAL_INPUTS'] = self.db.pos.inputs.loc[self.db.pos.inputs['date'] > start_date]
        report['TOTAL_INPUTS'] = report['TOTAL_INPUTS'].loc[report['TOTAL_INPUTS']
                                                            ['date'] < end_date]
        report['TOTAL_INPUTS'] = sum(report['TOTAL_INPUTS']['amount'])

        report['TOTAL_OUTPUTS'] = self.db.pos.outputs.loc[self.db.pos.outputs['date'] > start_date]
        report['TOTAL_OUTPUTS'] = report['TOTAL_OUTPUTS'].loc[report['TOTAL_OUTPUTS']
                                                              ['date'] < end_date]
        report['TOTAL_OUTPUTS'] = sum(report['TOTAL_OUTPUTS']['amount'])

        report['PROFIT_MARGIN'] = report['TOTAL_INPUTS'] - \
            report['TOTAL_OUTPUTS']
        if report['TOTAL_INPUTS'] == 0:
            report['PROFIT_MARGIN_PRECENTAGE']= 0
        else:
            report['PROFIT_MARGIN_PRECENTAGE'] = (report['PROFIT_MARGIN'] * 100) / report['TOTAL_INPUTS']

        return report

    def calculate_roi(self, start_date=0, end_date=999999999999999999):
        investments = self.db.pos.outputs.loc[self.db.pos.outputs['date'] > start_date]
        investments = investments.loc[investments['date'] < end_date]
        investments = investments.loc[self.db.pos.outputs['direction'].str.contains(
            'Investment')]
        investments = sum(investments['amount'])
        if investments == 0:
            return 0

        profit = sum(self.db.pos.inputs['amount']) - \
            sum(self.db.pos.outputs['amount'])

        return profit/investments
