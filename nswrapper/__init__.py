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
    
    def prepare(self, *attrs):
        varlist = []
        for attr in attrs:
            # attr is a varlist
            if isinstance(attr, netsnmp.VarList):
                varlist = varlist + attr.varbinds
            
            # attr is a list of oids or varbinds
            elif type(attr) == list or type(attr) == tuple:
                for oid in attr:
                    if isinstance(oid, netsnmp.Varbind):
                        varlist.append(oid)
                    else:
                        varlist.append(netsnmp.Varbind(oid))
            
            # attr is an oid or a varbind
            else:
                if isinstance(attr, netsnmp.Varbind):
                    varlist.append(attr)
                else:
                    varlist.append(netsnmp.Varbind(attr))
        
        return netsnmp.VarList(*varlist)
    
    def get(self, *oids):
        varlist = self.prepare(oids)
        self.session.get(varlist)
        for var in varlist:
            yield get_datatype(var)
    
    def getbulk(self, offset, repeat, *oids):
        varlist = self.prepare(oids)
        self.session.getbulk(offset, repeat, varlist)
        for var in varlist:
            yield get_datatype(var)
    
    def getnext(self, *oids):
        varlist = self.prepare(oids)
        self.session.getnext(varlist)
        for var in varlist:
            yield get_datatype(var)
    
    def walk(self, *oids):
        varlist = self.prepare(oids)
        if len(varlist) > 1:
            m = "Only one oid or varbind must be specified"
            raise Exception(m)
        self.session.walk(varlist)
        for var in varlist:
            yield get_datatype(var)
