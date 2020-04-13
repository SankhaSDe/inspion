__all__ = ['local_data']

from server.serverlog import debug,error

class LocalData:
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
         |ctype|   cid    |   lat   |   lon   |   ip  | port |  update  |  udp |
         -----------------------------------------------------------------------
       1 | 1   |1234567890|185185133|185185133|x.x.x.x|   0  |1234567890|765430|
       2 | 1   |1234567891|185185133|185185133|x.x.x.x|   0  |1234567890|765430|
         -----------------------------------------------------------------------
    """

    def __init__(self):
        self._location_data = []
        self._data_index = {}

    def insert(self, ctype, cid, lat, lon, ip, port, update, udp):
        # TODO - validate input
        client_info = [ctype, cid, lat, lon, ip, port, update, udp]
        if cid in self._data_index:
            index = self._data_index.get(cid)
            old_info = self._location_data[index]
            if client_info[6] > old_info[6]: # 6 -> update
                self._location_data[index] = client_info
        else:
            self._location_data.append(client_info)
            self._data_index[cid] = len(self._location_data)-1

    def search(self, lat, lon):
        # TODO - implement nearby logic
        return [x for x in self._location_data]

    def clean(self):
        # TODO - delete old data based on config.DATA_EXPIRATION_TIME
        pass

    def __str__(self):
        return str(self._location_data)

local_data = LocalData()
