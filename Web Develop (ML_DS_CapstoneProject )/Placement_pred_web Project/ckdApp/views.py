from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
#from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import (View,TemplateView,
ListView,DetailView,
CreateView,DeleteView,
UpdateView)
from . import models
from .forms import *
from django.core.files.storage import FileSystemStorage
#from topicApp.Topicfun import Topic
#from ckdApp.funckd import ckd
#from sklearn.tree import export_graphviz #plot tree
#from sklearn.metrics import roc_curve, auc #for model evaluation
#from sklearn.metrics import classification_report #for model evaluation
##from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(df2.drop('classification_yes', 1), df2['classification_yes'], test_size = .2, random_state=10)

import time
import pandas as pd
import numpy as np
#from sklearn.preprocessing import StandardScaler
#from sklearn.feature_selection import SelectKBest
#from sklearn.feature_selection import chi2
#from sklearn.model_selection import train_test_split
#from sklearn.decomposition import PCA
#from sklearn.feature_selection import RFE
#from sklearn.linear_model import LogisticRegression
import joblib
import matplotlib.pyplot as plt
#import eli5 #for purmutation importance
#from eli5.sklearn import PermutationImportance
#import shap #for SHAP values
#from pdpbox import pdp, info_plots #for partial plots
np.random.seed(123) #ensure reproduc
class dataUploadView(View):
    form_class = ckdForm
    success_url = reverse_lazy('success')
    template_name = 'create.html'
    failure_url= reverse_lazy('fail')
    filenot_url= reverse_lazy('filenot')
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        #print('inside post')
        form = self.form_class(request.POST, request.FILES)
        #print('inside form')
        if form.is_valid():
            form.save()
            data_ssc_p = request.POST.get('ssc_p')
            data_hsc_p = request.POST.get('hsc_p')
            data_degree_p = request.POST.get('degree_p')
            data_etest_p = request.POST.get('etest_p')
            data_mba_p = request.POST.get('mba_p')

            data_gender_M = request.POST.get('gender_M')
            data_ssc_b_Others = request.POST.get('ssc_b_Others')
            data_hsc_b_Others = request.POST.get('hsc_b_Others')
            data_hsc_s_Commerce = request.POST.get('hsc_s_Commerce')
            data_hsc_s_Science = request.POST.get('hsc_s_Science')
            data_degree_t_Others = request.POST.get('degree_t_Others')
            data_degree_t_Sci_Tech = request.POST.get('degree_t_Sci_Tech')
            data_workex_Yes = request.POST.get('workex_Yes')
            data_specialisation_Mkt_HR = request.POST.get('specialisation_Mkt_HR')
            #print (data)
            #dataset1=pd.read_csv("prep.csv",index_col=None)
            dicc={'yes':1,'no':0}
            filename = 'final_model.pkl'
            classifier = joblib.load("final_model.pkl")

            data = [[
                        float(data_ssc_p),
                        float(data_hsc_p),
                        float(data_degree_p),
                        float(data_etest_p),
                        float(data_mba_p),
                        int(bool(data_gender_M)),
                        int(bool(data_ssc_b_Others)),
                        int(bool(data_hsc_b_Others)),
                        int(bool(data_hsc_s_Commerce)),
                        int(bool(data_hsc_s_Science)),
                        int(bool(data_degree_t_Others)),
                        int(bool(data_degree_t_Sci_Tech)),
                        int(bool(data_workex_Yes)),
                        int(bool(data_specialisation_Mkt_HR))]]
            #sc = StandardScaler()
            #data = sc.fit_transform(data.reshape(-1,1))
            prediction = classifier.predict(data)
            out = prediction[0]
# providing an index
            #ser = pd.DataFrame(data, index =['bgr','bu','sc','pcv','wbc'])

            #ss=ser.T.squeeze()
#data_for_prediction = X_test1.iloc[0,:].astype(float)

#data_for_prediction =obj.pca(np.array(data_for_prediction),y_test)
            #obj=ckd()
            ##plt.savefig("static/force_plot.png",dpi=150, bbox_inches='tight')





            return render(request, "succ_msg.html", {
                'ssc_p': data_ssc_p,
                'hsc_p': data_hsc_p,
                'degree_p': data_degree_p,
                'etest_p': data_etest_p,
                'mba_p': data_mba_p,
                'gender_M': data_gender_M,
                'ssc_b_Others': data_ssc_b_Others,
                'hsc_b_Others': data_hsc_b_Others,
                'hsc_s_Commerce': data_hsc_s_Commerce,
                'hsc_s_Science': data_hsc_s_Science,
                'degree_t_Others': data_degree_t_Others,
                'degree_t_Sci_Tech': data_degree_t_Sci_Tech,
                'workex_Yes': data_workex_Yes,
                'specialisation_Mkt_HR': data_specialisation_Mkt_HR,
                'out': out
            })



        else:
            return redirect(self.failure_url)
