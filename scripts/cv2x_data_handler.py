import pandas as pd
import numpy as np
import os

class Cv2xDataHandler:
    def __init__(self):
        self.__parameters_name = 'parameters.csv'
        self.__sf_period = 1
        self.__BPS_TO_MBPS = 1000000
        self.__US_TO_SEC = 1000000
        self.__US_TO_MS = 1000
        self.__valid_mcs_idx = [5,6,7,11]
    
    
    def getConfigurations(self, 
                        pIn:str,
                        pck_len=None,
                        prio=None,
                        resv=None,
                        ipg=None)->pd.DataFrame:
        conf = pd.read_csv(os.path.join(pIn,self.__parameters_name))
        if pck_len is not None:
            conf = conf[conf['packet_size'] == pck_len]
        if prio is not None:
            conf = conf[conf['priority'] == prio]
        if resv is not None:
            conf = conf[conf['revervation_period'] == resv]
        if ipg is not None:
            conf = conf[conf['interval'] == ipg]
        return conf
    
    def getRxTracesByConfiguration(self,
                                    path,
                                    pck_len=None,
                                    prio=None,
                                    resv=None,
                                    ipg=None)->dict:
        conf = self.getConfigurations(path, pck_len, prio, resv, ipg)
        ret = {}
        isRxLog = lambda x: x.split('_')[0] == 'rx'
        whichRx = lambda x: x.split('_')[1]
        whichTx = lambda x: x.split('_')[-1].split('.')[0]
        for inx, row in conf.iterrows():
            pTemp = os.path.join(path,str(row['id']))
            files = os.listdir(pTemp)
            for f in files:
                if isRxLog(f):
                    if(whichRx(f) not in ret):
                        ret[whichRx(f)] = {whichTx(f):[os.path.join(pTemp,f)]}
                    else:
                        if(whichTx(f) not in ret[whichRx(f)]):
                            ret[whichRx(f)][whichTx(f)] = [os.path.join(pTemp,f)]
                        else:
                            ret[whichRx(f)][whichTx(f)].append(
                                os.path.join(pTemp,f))
        return ret
    
    def getRxTracesByApp(self,
                          path:str,
                          name:str,
                          app:str):
        pScene = os.path.join(path,name)
        ret = {}
        isRxLog = lambda x: x.split('_')[0] == 'rx'
        whichRx = lambda x: x.split('_')[1]
        whichTx = lambda x: x.split('_')[-2].split('.')[0]
        whichApp = lambda x: x.split('_')[-1].split('.')[0]
        for log in os.listdir(pScene):
            if isRxLog(log) and app == whichApp(log):
                if(whichRx(log) not in ret):
                    ret[whichRx(log)] = {whichTx(log):[os.path.join(pScene,log)]}
                else:
                    if(whichTx(log) not in ret[whichRx(log)]):
                        ret[whichRx(log)][whichTx(log)] = [os.path.join(pScene,log)]
                    else:
                        ret[whichRx(log)][whichTx(log)].append(
                            os.path.join(pScene,log))
        return ret
    
    def getSCIByConfiguration(self,
                            path,
                            pck_len=None,
                            prio=None,
                            resv=None,
                            ipg=None)->list:
        conf = self.getConfigurations(path, pck_len, prio, resv, ipg)
        isSCI = lambda x: x=='sci.csv'
        ret = []
        for inx, row in conf.iterrows():
            pTemp = os.path.join(path,str(row['id']))
            files = os.listdir(pTemp)
            for f in files:
                if isSCI(f):
                    ret.append(os.path.join(pTemp,f))
        return ret
        
        
    def getPacketSizeFromRxLog(self,data:pd.DataFrame)->int:
        return data['packet_length'].iloc[0]
    
    def getRxAvg100msMetrics(self,data:pd.DataFrame)->pd.DataFrame:
        data = data[data['extra']==1]
        data = data[['avg_throughput(100ms)','avg_packet_loss(100ms)']]
        data.dropna(inplace=True)
        data.reset_index(inplace=True,drop=True)
        return data
    
    def getRxAvg10msMetrics(self,data:pd.DataFrame)->pd.DataFrame:
        data = data[data['extra']==1]
        data = data[['avg_throughput(10ms)','avg_packet_loss(10ms)']]
        data.dropna(inplace=True)
        data.reset_index(inplace=True,drop=True)
        return data
    
    def getRxLatencyMetrics(self,data:pd.DataFrame)->pd.DataFrame:
        data = data[data['extra']==0]
        data = data[['latency (ms)']]
        data.dropna(inplace=True)
        data.reset_index(inplace=True,drop=True)
        return data
    
    def calculateAvgThroughput(self, 
                               data:pd.DataFrame)->float:
        pck_len = self.getPacketSizeFromRxLog(data)
        data = data[data['extra']==0]
        total_bits = 8 * int(pck_len) * len(data)
        dfTime = data.get('rx_timestamp (us)')
        total_time = (dfTime.iloc[-1] - dfTime.iloc[0])/self.__US_TO_SEC
        return total_bits/total_time/self.__BPS_TO_MBPS
    
    
    def calculateAvgLoss(self,
                         data:pd.DataFrame)->float:
        data = data[data['extra']==0]
        return data.get('per_ue_loss_pct (%)').iloc[-1]
    
    def calculateAvgLatency(self,
                            data:pd.DataFrame)->float:
        data = data[data['extra']==0]
        dfLatency = data.get('latency (ms)')
        return np.mean(dfLatency)
    
    def createRBListByMCS(self,path:str):
        data = pd.read_csv(path)
        data.drop(data.tail(5).index,inplace=True) 
        data_time = data['rx_timestamp_us']
        start_time = data_time.get(0)

        ret={}

        grouped_sci = {mcs_idx: group for mcs_idx, 
                group in data.groupby('mcs_idx')}
        for mcs_idx, sci_df in grouped_sci.items():
            if mcs_idx not in self.__valid_mcs_idx:
                continue
            sf_list=[]
            sf_right_list=[]
            rb_start_list=[]
            rb_end_list=[]
            for _,sf in sci_df.iterrows():
                sf_index = int((sf['rx_timestamp_us']-start_time)/self.__US_TO_MS)
                sf_list.append(sf_index)
                sf_right_list.append(sf_index+self.__sf_period)
                sf_rb_start = sf['pssch_start_idx']-2
                rb_start_list.append(sf_rb_start)
                rb_end_list.append(sf_rb_start + sf['nof_prb_pssch']+2)
            ret[mcs_idx]= [sf_list,sf_right_list,rb_start_list,rb_end_list]
        return ret
        
cv2xDataHandler = Cv2xDataHandler()