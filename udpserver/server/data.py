__all__ = ['data']

from server.serverlog import debug,error

class Data:
    """
    [ _data_index ]
         ------------------------
         |     cid    |  index  |
         ------------------------
         | 1234567890 |    1    |
         | 1234567891 |    2    |

    [ _location_data ] internal data storage is a 2D array(list of lists) that
    holds information in below format:
         -----------------------------------------------------------------------
         |ctype|   cid    |   lat   |   lon   |  update  |is_udp|   ip  | port |
         -----------------------------------------------------------------------
       1 | 1   |1234567890|185185133|185185133|1234567890|   0  |x.x.x.x|765430|
       2 | 1   |1234567891|185185133|185185133|1234567890|   0  |x.x.x.x|765430|
         -----------------------------------------------------------------------
    """

    def __init__(self):
        self._location_data = []
        self._data_index = {}

    def insert(self,ctype,cid,lat,lon,update,is_udp,ip,port):
        #TODO - validate input
        if cid in self._data_index:
            index = self._data_index.get(cid)
            self._location_data[index] = [ctype,cid,lat,lon,update,is_udp,ip,port]
        else:
            self._location_data.append([ctype,cid,lat,lon,update,is_udp,ip,port])
            self._data_index[cid] = len(self._location_data)-1

    def search_nearby(self,cid,lat,lon):
        return [x for x in data._location_data if (x[1]!=cid)]

    def __str__(self):
        return str(self._location_data)

data = Data()
