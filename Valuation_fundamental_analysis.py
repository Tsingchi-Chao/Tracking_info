#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from iFinDPy import *
plt.rc("font",family='YouYuan')
plt.style.use('grayscale')
import warnings
warnings.filterwarnings("ignore")
THS_iFinDLogin('cjhx333','415032')


# In[80]:


class Valuation:
    """Valuation
    Valuation is used to track the valuation of major index、sector and stock.
    """
    def __init__(self,code:str,start_date:str,end_date:str,name:str,object_type:str='index',tick_fontsize:int=16):
        """
        Args:
            code(str):The code of the object,like 000300.SH represents HS300.
            start_date(str):The start date of the period.
            end_date(str):The end date of the period,always it's the latest date.
            name(str):The name of the code, like"食品饮料".
            object_type(str):The type of the object,which can be "index" and "stock".
            tick_fontsize(str):The fontsize of the tick of the picture.
        """
        self.code=code
        self.start_date=start_date
        self.end_date=end_date
        self.object_type=object_type
        self.df=pd.DataFrame()
        self.name=name
        self.tick_fontsize=tick_fontsize
        
    def get_THS_Data(self)->pd.DataFrame:
        """
        Returns:data(pd.DataFrame):The data of the pe,the index is datetime,and 'PE_TTM' is PE_TTM,'时间加权历史分位数' is the quuntile
        """
        if self.object_type=='index':
            THS_Data=THS_DS(self.code,'ths_pe_ttm_index','100,100','block:history',self.start_date,self.end_date)
        elif self.object_type=='stock':
            THS_Data=THS_DS(self.code,'ths_pe_ttm_stock','100','',self.start_date,self.end_date)
        data=THS_Data.data
        data=data.set_index('time')
        data.index=pd.to_datetime(data.index)
        data.columns=['code','PE_TTM']
        size=len(data['PE_TTM'])-1
        data['时间加权历史分位数']=data['PE_TTM'].rank().apply(lambda x:100*(x-1)/size)#对历史数据排序，计算当前排名所处分位数
        self.df=data
        return data
    
    def show_valuation(self):
        """
        Draw the picture of the valuation,here we use PE to represent the valuation of company.
        """
        if self.df.empty==True:
            Valuation.get_THS_Data(self)
        data=self.df.copy()
        fig = plt.figure(figsize=[10,12])
        ax1= fig.add_subplot(2, 1, 1)
        ax1.plot(data['时间加权历史分位数'],c='r',label='时间加权历史分位数')
        ax1.axhline(50,c='b')
        ax1.legend()
        ax1.set_xlabel('时间')
        ax1.set_ylabel('分位数')
        ax1.set_title(self.name+'估值所处历史分位数')
        for label in ax1.get_xticklabels()+ax1.get_yticklabels():
            label.set_fontsize(self.tick_fontsize)
            

        ax2=fig.add_subplot(2, 1, 2)
        ax2.plot(data['PE_TTM'],c='r',label='PE_TTM')
        ax2.legend()
        ax2.set_xlabel('时间')
        ax2.set_ylabel('PE')
        ax2.set_title(self.name+'估值水平变化')
        for label in ax2.get_xticklabels()+ax2.get_yticklabels():
            label.set_fontsize(self.tick_fontsize)


# In[85]:


class Fundamental_Analysis:
    """Fundamental_Analysis
    This class is used to do analysis about the fundamental of the sector or stock.
    """
    def __init__(self,code:str,start_date:str,end_date:str,name:str,object_type:str='index',tick_fontsize:int=14):
        """
        Args:
            code(str):The code of the object,like 000300.SH represents HS300.
            start_date(str):The start date of the period.
            end_date(str):The end date of the period,always it's the latest date.
            name(str):The name of the code, like"食品饮料".
            tick_fontsize(str):The fontsize of the tick of the picture.
        """
        self.code=code
        self.start_date=start_date
        self.end_date=end_date
        self.name=name
        self.df=pd.DataFrame()
        self.object_type=object_type
        self.tick_fontsize=tick_fontsize
        
    def get_THS_Data(self)->pd.DataFrame:
        """
        Returns:data(pd.DataFrame):The fundamental data about the index or the stock.
        """
        if self.object_type=='index':
            THS_Data=THS_DS(self.code,'ths_roe_ttm_index;ths_sale_net_rate_ttm_index;ths_total_revenue_yoy_index;ths_total_np_yoy_index;ths_roa_ttm_index',
                            '100;100;;;100','Days:Alldays,Fill:Blank,Interval:Q,block:history',self.start_date,self.end_date)
        elif self.object_type=='stock':
            THS_Data=THS_DS(self.code,'ths_roe_ttm_stock;ths_sales_gir_ttm_stock;ths_operating_revenue_yoy_stock;ths_np_yoy_stock;ths_roa_ttm_stock',
                            '100;100;;;100','Days:Alldays,Fill:Blank,Interval:Q,block:latest',self.start_date,self.end_date)
        data=THS_Data.data
        data=data.set_index('time')
        data.index=pd.to_datetime(data.index)
        data.columns=['code','ROE_TTM','销售净利率_TTM','营业收入同比','净利润同比','ROA_TTM']
        self.df=data
        return data

        
    def show_fundamental(self):
        """
        Show the picture about the fundamental data of the index or the stock.
        """
        if self.df.empty==True:
            Fundamental_Analysis.get_THS_Data(self)
        data=self.df.copy()
        fig = plt.figure(figsize=[20,12])
        ax1= fig.add_subplot(2, 2, 1)
        ax1.plot(data['ROE_TTM'],c='r',label='ROE_TTM')
        ax1.legend()
        ax1.set_xlabel('时间')
        ax1.set_ylabel('ROE_TTM')
        ax1.set_title(self.name+'ROE_TTM')
        for label in ax1.get_xticklabels()+ax1.get_yticklabels():
            label.set_fontsize(self.tick_fontsize)
        
        ax2=fig.add_subplot(2, 2, 2)
        ax2.plot(data['营业收入同比'],c='b',label='营业收入同比')
        ax2.legend()
        ax2.set_xlabel('时间')
        ax2.set_ylabel('营业收入同比')
        ax2.set_title(self.name+'营业收入同比')
        for label in ax2.get_xticklabels()+ax2.get_yticklabels():
            label.set_fontsize(self.tick_fontsize)
        
        ax3=fig.add_subplot(2, 2, 3)
        ax3.plot(data['净利润同比'],c='b',label='净利润同比')
        ax3.legend()
        ax3.set_xlabel('时间')
        ax3.set_ylabel('净利润同比')
        ax3.set_title(self.name+'净利润同比')
        for label in ax3.get_xticklabels()+ax3.get_yticklabels():
            label.set_fontsize(self.tick_fontsize)
        
        ax4=fig.add_subplot(2, 2, 4)
        ax4.plot(data['ROA_TTM'],c='r',label='ROA_TTM')
        ax4.legend()
        ax4.set_xlabel('时间')
        ax4.set_ylabel('ROA_TTM')
        ax4.set_title(self.name+'ROA_TTM')
        for label in ax4.get_xticklabels()+ax4.get_yticklabels():
            label.set_fontsize(self.tick_fontsize)


# In[93]:


def main():
    #计算古井贡酒的估值信息并展示
    value=Valuation('000596.SZ','2016-01-01','2021-03-09','古井贡酒','stock')
    value.show_valuation()
    #展示古井贡酒的基本面信息
    fda=Fundamental_Analysis('000596.SZ','2016-01-01','2020-12-09','古井贡酒','stock')
    fda.show_fundamental()
    
if __name__=='__main__':
    main()

