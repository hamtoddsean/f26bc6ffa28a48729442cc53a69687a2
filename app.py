import uuid
import time

import requests
from decimal import *
	
import re,os,zlib,json,time,csv

class Client(object):
    def __init__(self, url, public_key, secret):
        self.url = url + "/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)

    def get_symbol(self, symbol_code):
        """Get symbol."""
        return self.session.get("%s/public/symbol/%s" % (self.url, symbol_code)).json()

    def get_orderbook(self, symbol_code):
        """Get orderbook. """
        return self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()

    def tradehistory(self, clie):
        return self.session.get("%s/history/trades?symbol=%s" % (self.url, clie)).json()


    def get_address(self, currency_code):
        """Get address for deposit."""
        return self.session.get("%s/account/crypto/address/%s" % (self.url, currency_code)).json()

    def get_account_balance(self):
        """Get main balance."""
        return self.session.get("%s/account/balance" % self.url).json()

    def get_trading_balance(self):
        """Get trading balance."""
        return self.session.get("%s/trading/balance" % self.url).json()

    def transfer(self, currency_code, amount, to_exchange):
        return self.session.post("%s/account/transfer" % self.url, data={
                'currency': currency_code, 'amount': amount,
                'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
            }).json()

    def new_order(self, client_order_id, symbol_code, side, quantity, price=None):
        """Place an order."""
        data = {'symbol': symbol_code, 'side': side, 'type': 'market','timeInForce': 'FOK', 'quantity': quantity}

        if price is not None:
            data['price'] = price

        return self.session.put("%s/order/%s" % (self.url, client_order_id), data=data).json()

    def get_order(self, client_order_id, wait=None):
        """Get order info."""
        data = {'wait': wait} if wait is not None else {}

        return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()

    def cancel_order(self, client_order_id):
        """Cancel order."""
        return self.session.delete("%s/order/%s" % (self.url, client_order_id)).json()

    def withdraw(self, currency_code, amount, address, network_fee=None):
        """Withdraw."""
        data = {'currency': currency_code, 'amount': amount, 'address': address}

        if network_fee is not None:
            data['networkfee'] = network_fee

        return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()

    def get_transaction(self, transaction_id):
        """Get transaction info."""
        return self.session.get("%s/account/transactions/%s" % (self.url, transaction_id)).json()


    def reedt(timred):
        import re
        houra=''
        minb=''
        secgc=''
        reeta=''
        hourt=''
        rmo=re.compile(r'(\d+)-(\d+)-(\d+)(\D+)(\d+):(\d+):(\d+).(\d+)(\D+)')
        rba=rmo.findall(timred)
        houra=int(rba[0][4])*3600
        minb=int(rba[0][5])
        secgc=int(rba[0][6])
        minb=minb*60
        reeta=houra+minb+secgc
        hourt=int(rba[0][4])
        return [reeta,hourt]
        
    def tradebuy(self, trad, plistd):
        cite=''
        sumlist=[]
        sumprice=[]
        sqty=''
        sprice=''
        if trad[0]['side']== 'buy':
            for ite in range(1,100):
                cite= ite
                if trad[ite]['side']!= 'buy':
                    break
        for sumi in range(0,cite):
            sumlist.append(float(trad[sumi]['quantity']))
            sumprice.append(float(trad[sumi]['price']))
        sqty=float(sum(sumlist))
        sprice=float(max(sumprice))
    ###placebuy
        plistd['buyp'].append(sprice)
        plistd['BUY'].append(sprice)
        plistd['status']='sell'
        plistd['qty']=sqty
        self.totbuy(plistd)

    def tradestampbuy(self, trad):
        cite=''
        sumstamp=[]
        sqty=''
        sprice=''
        if trad[0]['side']== 'buy':
            for ite in range(1,100):
                cite= ite
                if trad[ite]['side']!= 'buy':
                    break
        for sumi in range(0,cite):
            sumstamp.append(trad[sumi]['timestamp'])
        return sumstamp[-1]



    def tbuyp(self,tbplistp,tbaskp):
        if tbplistp['lowert']!=[] and tbplistp['status']!='sell':
            if tbaskp> 0:
                if tbaskp> tbplistp['lowert'][1]:
                    placebuy=self.buy(float(tbplistp['qty'])+0.001,tbaskp)
                    if 'status' in placebuy:
                        if placebuy['status']=='filled':
                            tbplistp['buyp'].append(float(placebuy['sprice']))
                            tbplistp['BUY'].append(float(['sprice']))
                            tbplistp['status']='sell'
                            tbplistp['qty']=placebuy['sqty']
                            self.totbuy(tbplistp)
#########

    def totbuy(self,tutplist):
        bprc=''
        bpsprc=''
        bprc=tutplist['qty']/1
        bprc*=100
        bprc=bprc/100
        bprc*=tutplist['buyp'][-1]
        bpsprc=0.1/100
        bpsprc*=bprc
        bpsprc=float(bpsprc)
        tutplist['buyper'].append(bpsprc)

    def totsell(self,totsplist,totsbid,tssetamt,tssetamtt):
        sprc=''
        buyper=totsplist['buyper'][-1]
        buypr=totsplist['buyp'][-1]
        psprc=''
        sprc=totsplist['qty']/1
        sprc*=100
        sprc=sprc/100
        sprc*=totsbid
        psprc=0.1/100
        psprc*=sprc
        psprc=float(psprc)
        zprc= float(totsbid)-buypr
        zzprc=buyper/zprc
        zzprc*=100
        zzprc=float(zzprc)
        if zzprc>tssetamt and zzprc<= tssetamtt:
            self.tsellp(totsplist,totsbid)
        
    def tsellp(self,tsplistp,tsbidp):
        placesell=self.sell(float(tsplistp['qty'])+0.001,tsbidp)
        if 'status' in placesell:
            if placesell['status']=='filled':
                tsplistp['sellp'].append(float(placesell['sprice']))
                tsplistp['SELL'].append(float(placesell['sprice']))
                tsplistp['status']='buy'
                tsplistp['lower']=[]
                tsplistp['lowert']=[]
                tsplistp['w']=[]
                tsplistp['ww']=[]
                tsplistp['qty']=placesell['sqty']


####@@@@

####@@@@
    def gpricep():
        import requests
        rrt=''
        urltt='http://api.hitbtc.com/api/2/public/ticker/ETHUSD'
        rrt = requests.get(urltt).json()
        return rrt['timestamp']
        
    def abort(self,abcp,abtral,abplist,abbid):
        setamto=-500
        setamtt=1000000
        tutto=abcp[0]
        tuttw=abtral[0]
        if abcp[-1]< abtral[-1]:
            tutto+=24*3600
        if tutto-tuttw>= 1200:
            self.totsell(abplist,abbid,setamto,setamtt)
        
    def groupsell(self, gplist, gbid):
        gp= self.gpricep()
        cpg= self.reedt(gp)
        tdstamp=self.tradehistory()
        tradestamp= self.tradestampbuy(tdstamp)
        tralg= self.reedt(tradestamp)
        self.abort(cpg,tralg,gplist,gbid)


    def showtime(self,v):
        tva= 'Timer-'
        va= ''
        if v< 60:
            va= tva+str(v)+'-seconds'
        if v> 59 and v< 3600:
            v= v/60
            v= round(v,3)
            va= tva+str(v)+'-minutes'
        if v> 3599 and v< 86399:
            v= v/3600
            v= round(v,3)
            va= tva+str(v)+'-hours'
        if v> 86399:
            v= v/86400
            v= round(v,3)
            va= tva+str(v)+'-days'
        return va

    def talcal(self,t,p):
        qp=''
        pp=t-p
        if pp> 0:
            qp=pp/p
            qp=qp*100
        return qp


#########
####@@@@
    def tradesell(self, ttrad, splist):
        scite=''
        ssumlist=[]
        ssumprice=[]
        ssqty=''
        ssprice=''
        if ttrad[0]['side']== 'sell':
            for ssite in range(1,100):
                scite= ssite
                if ttrad[ssite]['side']!= 'sell':
                    break
        for ssumi in range(0,scite):
            ssumlist.append(float(ttrad[ssumi]['quantity']))
            ssumprice.append(float(ttrad[ssumi]['price']))
        ssqty=float(sum(ssumlist))
        ssprice=float(max(ssumprice))
#########

    ########sellll
        splist['sellp'].append(ssprice)
        splist['SELL'].append(ssprice)
        splist['status']='buy'            
        splist['qty']=ssqty

####@@@@

    def tradebuuy(self, butrad):
        bucite=''
        busumlist=[]
        busumprice=[]
        busqty=''
        busprice=''
        if butrad[0]['side']== 'buy':
            for buite in range(1,100):
                bucite= buite
                if butrad[buite]['side']!= 'buy':
                    break
        for busumi in range(0,bucite):
            busumlist.append(float(butrad[busumi]['quantity']))
            busumprice.append(float(butrad[busumi]['price']))
        busqty=float(sum(busumlist))
        busprice=float(max(busumprice))
        return [busqty,busprice]


    def tradeseell(self, kbutrad):
        kbucite=''
        kbusumlist=[]
        kbusumprice=[]
        kbusqty=''
        kbusprice=''
        if kbutrad[0]['side']== 'sell':
            for kbuite in range(1,100):
                kbucite= kbuite
                if kbutrad[kbuite]['side']!= 'sell':
                    break
        for kbusumi in range(0,kbucite):
            kbusumlist.append(float(kbutrad[kbusumi]['quantity']))
            kbusumprice.append(float(kbutrad[kbusumi]['price']))
        kbusqty=float(sum(kbusumlist))
        kbusprice=float(max(kbusumprice))
        return [kbusqty,kbusprice]


    def buy(self,aamt,abid):
        #import hitbtc
        import uuid
        import decimal
        abtc_usd= self.get_symbol('ETHUSD')
        aorder=''
        aclient_order_id = uuid.uuid4().hex
        abest = abid
        abet = None
        acamt = aamt
        nooz=''
        print('fetching buy order')
        aorder = self.new_order(aclient_order_id, 'ETHUSD', 'buy', aamt, abet)
        if 'error' in aorder:
            for iv in range(10):
                acamt=acamt-0.001
                round(acamt,3)
                aclient_order_idd = uuid.uuid4().hex
                aorder = self.new_order(aclient_order_idd, 'ETHUSD', 'buy', acamt, abet)
                if 'status' in aorder:
                    break
        if 'status' in aorder:
            if aorder['status']=='filled':
                tradhb=self.tradehistory('ETHUSD')
                sft=self.tradebuuy(tradhb)
                aorder['sqty']=sft[0]
                aorder['sprice']=sft[1]
        print('done')
        print(aorder)
        return aorder

    def sell(self,eamt,ebid):
        #import hitbtc
        import uuid
        import decimal
        ebtc_usd= self.get_symbol('ETHUSD')
        eorder=''
        eclient_order_id = uuid.uuid4().hex
        ebest = ebid
        ebet = None
        ecamt = eamt
        print('fetching sell order')
        eorder = self.new_order(eclient_order_id, 'ETHUSD', 'sell', eamt, ebet)
        if 'error' in eorder:
            for tfi in range(10):
                ecamt=ecamt-0.001
                round(ecamt,3)
                eclient_order_idd = uuid.uuid4().hex
                eorder = self.new_order(eclient_order_idd, 'ETHUSD', 'sell', ecamt, ebet)
                if 'status' in eorder:
                    break
        if 'status' in eorder:
            if eorder['status']=='filled':
                tradhs=self.tradehistory('ETHUSD')
                sfft=self.tradeseell(tradhs)
                eorder['sqty']=sfft[0]
                eorder['sprice']=sfft[1]

        print('done')
        print(eorder)
        return eorder

    def srun(self,juj,stoptime,plist):
        import os,zlib,json,time,csv,re,datetime
        time=datetime.datetime.now()
        time=str(time)
        mo=re.compile(r'(\d+-\d+-\d+)')
        ma=re.compile(r'(\d+):(\d+):(\d+)')
        mmo=re.compile(r'(\d+)(.)(\d+)')


        baa=ma.findall(time)
        aa=int(baa[0][0])
        bb=int(baa[0][1])
        cc=int(baa[0][2])
        aa=aa*3600
        bb=bb*60
        cc=aa+bb+cc

        ba=mo.findall(time)
        e=(str(ba[0]))
        kb=''
        bid=''
        ask=''
        bbid=''
        aask=''
        count=''
        dg=[]
        ded=1
        plist=''
        etddu='ETHUSD'
        stoptimee= stoptime
        
        if ded==1:
            cpl=juj
            if cpl['bid']!=None:
    
                bid=float(cpl['bid'])
                ask=float(cpl['ask'])
    
    # print(cpl)
                bbab=mmo.findall(str(bid))
                bbaa=mmo.findall(str(ask))
                bbid=float(bbab[0][0])
                aask=float(bbaa[0][0])
                        

                #plist=pathh
                if plist['buyp']==[] and plist['sellp']==[]:
                    tradh=self.tradehistory(etddu)
                    if tradh[0]['side']=='buy':
                        self.tradebuy(tradh,plist)
                    if tradh[0]['side']=='sell':
                        self.tradesell(tradh,plist)
                print(plist)
                
                count=len(plist['count'])

                if plist['list']==[]:
                    if ask-bid <=0.7:
                        plist['list']=[bid,ask]

                if plist['list'] !=[]:
                    if ask==float(plist['list'][1]):
                        if bid==float(plist['list'][0]):
                            plist['count'].append(1)
  
                if plist['list'] !=[]:
                    if ask<plist['list'][1] or ask>plist['list'][1]:
                        plist['list']=[bid,ask]
                        plist['count']=dg


                if plist['store']!=[]:
                    if plist['store'][-1]!= ask:
                        plist['store'].append(ask)
                if plist['store']==[]:
                    plist['store'].append(ask)

########

                if len(plist['store'])>= 20:
                    ab=len(plist['store'])- 20
                    slist=plist['store'][ab::]
                    for ji in range(0,len(slist)-1):
                        if plist['store'][ji]- plist['store'][ji+1]>= 25 or plist['store'][ji+1]- plist['store'][ji]<= -25:
                            plist['counter'].append(1)
                    if len(plist['counter'])>= 19:
                        plist['tab']=['switch']
                        plist['store']=slist
                    else:
                        plist['store']=[]
                        plist['tab']=['d']
                        plist['counter']=[]

################

                if plist['tab'][0]=='switch':

################
#watchdiff=''
                    if ask-bid>=25 and plist['status']!='sell':
                        plist['ww']=[bid,ask]
                        plist['w']=[bid,ask]
  
####fix lower
                    if ask- bid<=7:
                        if plist['ww']!=[]:
                            if ask<=plist['ww'][1]:
                                if count>1:
                                    plist['lowert']=[bid,ask]
                                    plist['lower']=[bid,ask]
####@#####

#####buy
                    if plist['ww']!=[] and plist['status']!='sell':
                        if ask<= plist['ww'][0]:
                            if ask- plist['ww'][1]>=25:
                                self.tbuyp(plist,ask)

#########
    ########sellll 1
                    if plist['status']=='sell':
                        if bid> plist['buyp'][-1]:
                            if bid-plist['buyp'][-1]>=25:
                                self.totsell(plist,bid,0,40)
                                self.groupsell(plist,bid)

###################



                else:
#watchdiff=''
                    if ask-bid>=0.7 and plist['status']!='sell':
                        plist['ww']=[bid,ask]
                        plist['w']=[bid,ask]
  
####fix lower
                    if ask- bid<=0.7 and plist['status']!= 'sell':
                        if plist['ww']!=[]:
                            if aask<=plist['ww'][1]:
                                if count>1:
                                    plist['lowert']=[bid,ask]
                                    plist['lower']=[bid,ask]

#####buy
                    if plist['lowert']!=[] and plist['status']!='sell':
                        if ask> 0:
                            if ask> plist['lowert'][1]:
    ###place buyorder
                                self.tbuyp(plist,ask)

#########

    ########sellll 1
                    if plist['status']=='sell':
                        if bid> plist['buyp'][-1]:
                            if bid-plist['buyp'][-1]> 0.9:
                                self.totsell(plist,bid,0,40)
                                self.groupsell(plist,bid)
                              

####@@@@
       
      #def


                if cc>= stoptimee:
                    stradeh= self.tradehistory('ETHUSD')
                    if stradeh[0]['type']=='sell':
                        plist['pleven']='yes'
                        print('over and out')
       #pleven='yes'
                    #pathh= plist
                    print('over and out')




if __name__ == "__main__":
    public_key = "cc2bf5e7ed2ba3dab76115b76d4ccbdc"
    secret = "14c806cfba09cdfbce048e7086232623"

    client = Client("https://api.hitbtc.com", public_key, secret)
    
    clist={'buyper':[],'keeprecord':[],'go':'','qty':'0.007','pleven':'','ggo':'yes','list':[],'buyp':[],'sellp':[],'BUY':[],'SELL':[],'even':'','count':[],'status':'','buy':[],'sell':[],'lower':[],'lowert':[],'uppert':[],'upper':[],'w':[],'ww':[],'counter':[],'store':[],'tab':['d'],'watch':''}
    url='http://api.hitbtc.com/api/2/public/ticker/ETHUSD'
    
    stoptime=431900
    showt= ''
    ss={}

    for vii in range(432000):
        time.sleep(1)
        showt= client.showtime(vii)
        print(showt)

        countpl=clist['pleven']


        if vii< stoptime or countpl != 'yes':
            r= client.get_orderbook('ETHUSD')
            ss['bid']=r['bid'][0]['price']
            ss['ask']=r['ask'][0]['price']
            r = requests.get(url)
            client.srun(ss,stoptime,clist)
            print(clist)

        else:
            print(showt)
            print('logged out')
            print(clist)
