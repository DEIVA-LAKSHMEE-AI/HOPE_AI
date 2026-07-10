from django import forms
from .models import ckdModel


class ckdForm(forms.ModelForm):

    class Meta:
        model = ckdModel

        fields = [
            'ssc_p',
            'hsc_p',
            'degree_p',
            'etest_p',
            'mba_p',
            'gender_M',
            'ssc_b_Others',
            'hsc_b_Others',
            'hsc_s_Commerce',
            'hsc_s_Science',
            'degree_t_Others',
            'degree_t_Sci_Tech',
            'workex_Yes',
            'specialisation_Mkt_HR',
        ]

        labels = {
            'ssc_p': 'SSC Percentage',
            'hsc_p': 'HSC Percentage',
            'degree_p': 'Degree Percentage',
            'etest_p': 'Employability Test Percentage',
            'mba_p': 'MBA Percentage',
            'gender_M': 'Male',
            'ssc_b_Others': 'SSC Board (Others)',
            'hsc_b_Others': 'HSC Board (Others)',
            'hsc_s_Commerce': 'Commerce',
            'hsc_s_Science': 'Science',
            'degree_t_Others': 'Other Degree',
            'degree_t_Sci_Tech': 'Science & Technology',
            'workex_Yes': 'Work Experience',
            'specialisation_Mkt_HR': 'Marketing & HR',
        }
