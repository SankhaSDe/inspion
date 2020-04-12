import sys
sys.path.append('../')

import json
import pytest
import logging
from server.messages import *
from server.data import *

def test_handle_message_duplicateInit():
  """
  sending ClientToServer_INIT_LOCATION message two times
  """
  payload = {'ip':'1.0.0.1','port':76001,'msg':[1,0,111111111111,185185130,185185132,1234567890]}
  result = handle_message(ip=payload['ip'], port=payload['port'], msg=payload['msg'])
  payload = {'ip':'1.0.0.1','port':76001,'msg':[1,0,111111111111,185185133,185185134,1234567891]}
  result = handle_message(ip=payload['ip'], port=payload['port'], msg=payload['msg'])
  assert len(data._location_data)==1 and len(data._data_index)==1 \
      and data._location_data[0][4]==1234567891 and data._data_index[111111111111]==0 \
      and result[0][0]=='1.0.0.1' and result[0][1]==76001 and '[2, 0]' in result[0][2]

def test_handle_message_secondClient():
  """
  new ClientToServer_INIT_LOCATION message
  """
  payload = {'ip':'1.0.0.2','port':76002,'msg':[1,0,111111111112,185185135,185185136,1234567892]}
  result = handle_message(ip=payload['ip'],port=payload['port'],msg=payload['msg'])
  assert len(data._location_data)==2 and len(data._data_index)==2 \
      and data._location_data[0][4]==1234567891 and data._data_index[111111111111]==0 \
      and data._location_data[1][4]==1234567892 and data._data_index[111111111112]==1 \
      and len(result)==2 \
      and result[0][0]=='1.0.0.2' and result[0][1]==76002 and '[2, 1' in result[0][2] \
      and result[1][0]=='1.0.0.1' and result[1][1]==76001 and '[4, ' in result[1][2]

def test_handle_message_initClientAck():
  payload = {'ip':'1.0.0.1','port':76001,'msg':[3,0,111111111111,185185137,185185139,1234567893]}
  result = handle_message(ip=payload['ip'],port=payload['port'],msg=payload['msg'])
  payload = {'ip':'1.0.0.2','port':76002,'msg':[3,0,111111111112,185185140,185185141,1234567894]}
  result = handle_message(ip=payload['ip'],port=payload['port'],msg=payload['msg'])
  assert result == None and len(data._location_data)==2 and len(data._data_index)==2 \
      and data._location_data[0][4]==1234567893 and data._data_index[111111111111]==0 \
      and data._location_data[1][4]==1234567894 and data._data_index[111111111112]==1 \

def test_handle_message_updateLocation():
  """
  new ClientToServer_UPDATE_LOCATION ( 5 )
  """
  payload = {'ip':'1.0.0.1','port':76001,'msg':[5,0,111111111111,185185137,185185139,1234567893]}
  result = handle_message(ip=payload['ip'],port=payload['port'],msg=payload['msg'])
  assert len(data._location_data)==2 and len(data._data_index)==2 \
      and data._location_data[0][4]==1234567893 and data._data_index[111111111111]==0 \
      and data._location_data[1][4]==1234567894 and data._data_index[111111111112]==1 \
      and len(result)==1 \
      and result[0][0]=='1.0.0.1' and result[0][1]==76001 \
      and '[6, 1, 0, 111111111112, 185185140, 185185141, 1234567894, -1, "1.0.0.2", 76002]' in result[0][2]

