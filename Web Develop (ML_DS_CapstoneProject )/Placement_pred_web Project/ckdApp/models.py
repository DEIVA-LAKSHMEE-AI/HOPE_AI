from django.db import models

class ckdModel(models.Model):
    ssc_p = models.FloatField()
    hsc_p = models.FloatField()
    degree_p = models.FloatField()
    etest_p = models.FloatField()
    mba_p = models.FloatField()

    gender_M = models.BooleanField(default=False)
    ssc_b_Others = models.BooleanField(default=False)
    hsc_b_Others = models.BooleanField(default=False)
    hsc_s_Commerce = models.BooleanField(default=False)
    hsc_s_Science = models.BooleanField(default=False)
    degree_t_Others = models.BooleanField(default=False)
    degree_t_Sci_Tech = models.BooleanField(default=False)
    workex_Yes = models.BooleanField(default=False)
    specialisation_Mkt_HR = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ssc_p}"
