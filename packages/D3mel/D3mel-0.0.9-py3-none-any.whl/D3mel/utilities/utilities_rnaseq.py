#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 18:00:38 2024

@author: javicolors
"""

import pandas as pd

#%%

class UtilitiesRNAseq():
    
    def __init__(self, fbd):
        self.fbd = fbd       
        self.Seq_Gene_Expression = None
        
    def get_proyects(self, matriz = None):
        if matriz is None and self.Seq_Gene_Expression is None:
            print("Set a Seq gene expression matrix first")
            return None
        elif self.Seq_Gene_Expression is None:
            self.Seq_Gene_Expression = matriz
        return list(self.Seq_Gene_Expression['Parent_library_name'].unique())
    

    def RNA_by_proyect(self, g, proyects, matriz = None):
        
        if matriz is None:
            matriz = self.Seq_Gene_Expression
        
        try:
            g = list(g)
            if proyects is None:
                proyects = self.get_proyects()
            else:
                proyects = list(proyects)
            dict_df = {}
            for proyect in proyects:
                df = matriz[matriz['Parent_library_name'] == proyect]
                df_v = pd.pivot_table(df, index='FBgn#', columns='RNASource_name', values='RPKM_value', aggfunc='mean')
                dict_df[proyect] = df_v[df_v.index.isin(g)].dropna()
            return dict_df
        except:
            print("Something didn't go as expected. Please check your inputs")

