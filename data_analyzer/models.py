from django.db import models
from datetime import datetime


class FundInfo(models.Model):
    cik = models.IntegerField(primary_key=True)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fund_info'


class SecurityInfo(models.Model):
    cusip = models.CharField(primary_key=True, max_length=9)
    ticker = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    asset_class = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    exchange = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'security_info'
        

class PositionInfo(models.Model):
    infotable_sk = models.IntegerField(primary_key=True)
    accession_number = models.CharField(max_length=255, blank=True, null=True)
    cusip = models.ForeignKey('SecurityInfo', models.DO_NOTHING, db_column='cusip', blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    shares = models.IntegerField(blank=True, null=True)
    cik = models.ForeignKey(FundInfo, models.DO_NOTHING, db_column='cik', blank=True, null=True)
    filing_period = models.DateField(blank=True, null=True)

    @property
    def filing_date(self):
        if self.filing_period:
            return datetime.strptime(self.filing_period, '%d-%b-%Y').date()
        return None

    class Meta:
        managed = False
        db_table = 'position_info'