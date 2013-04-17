import netsnmp, sys
from cStringIO import StringIO
from nswrapper.types import get_datatype

class Snmp(object):
    
    class ConnectionError(Exception):
        pass
    
    def __init__(self,host='localhost',version=2,community='public', **kwargs):
        kwargs['DestHost'] = host
        kwargs['Community'] = community
        kwargs['Version'] = version
        
        self.session = netsnmp.Session(**kwargs)
        if self.session.sess_ptr == 0:
            m = "Unable to connect to host %s" % host
            raise self.ConnectionError(m)
    
    def get(self, oids):
        if not type(oids) == list and not type(oids) == tuple:
            oids = (oids,)
        
        varlist = []
        for oid in oids:
            varlist.append(netsnmp.Varbind(oid))
        varlist = netsnmp.VarList(*varlist)
        
        self.session.get(varlist)
        
        for var in varlist:
            yield get_datatype(var)
    
    
    def walk(self, oid):
        varlist = netsnmp.VarList(netsnmp.Varbind(oid))
        self.session.walk(varlist)
        for var in varlist:
            yield get_datatype(var)
