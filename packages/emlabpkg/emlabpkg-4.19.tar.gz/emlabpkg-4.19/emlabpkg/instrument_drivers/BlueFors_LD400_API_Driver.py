import requests
import os
import pandas as pd
import numpy as np
import datetime as dt
from typing import Optional, Callable
from qcodes import InstrumentChannel
from qcodes.instrument.base import Instrument
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time

class BlueFors(Instrument):

    def __init__(self, name      : str, 
                 folder_path     : Optional[str] = 'C:/Users/EMLab/Dropbox/BF1/BF1 logs/', 
                 api_port        : Optional[int] = 49098,
                 api_key         : Optional[str] = 'cb966295-68e4-4ef3-b1e9-8a8bad2f6b4b',
                 **kwargs):

        super().__init__(name = name, **kwargs)
        self.connect_message()

        self._folder_path = os.path.abspath(folder_path)
        
        self._scheme = 'https'
        self._authority = f'localhost:{api_port}'
        self._query = f'key={api_key}'

        self._api_url = BlueForsAPIURL(parent=self, scheme=self._scheme, authority=self._authority, query=self._query)

        self._pressure_channels = BlueForsPressureChannels(parent=self,
                                                    channel_vacuum_can=1, channel_pumping_line=2, channel_compressor_outlet=3, 
                                                    channel_compressor_inlet=4, channel_mixture_tank=5, channel_venting_line=6)
        self._temperature_channels = BlueForsTemperatureChannels(parent=self,
                                                    channel_50k_plate=1, channel_4k_plate=2, channel_magnet=3, 
                                                    channel_still=5, channel_mixing_chamber=6, channel_fse=9)
        self._heater_channels = BlueForsHeaterChannels(parent=self, channel_still_heater=3, channel_mxc_heater=4, channel_fse_heater=4)

        self._initialize_submodules()

    def get_idn(self):
        idn = {"vendor": 'BlueFors', "model": 'LD400', "serial": '49098', "firmware": None}
        return idn

    def _initialize_submodules(self):
        api = BlueForsAPI(parent=self, 
                          api_url=self._api_url, 
                          bf_pres_channels=self._pressure_channels, bf_temp_channels=self._temperature_channels, 
                          bf_heater_channels=self._heater_channels)
        self.add_submodule('api', api)

class BlueForsAPIURL(InstrumentChannel):

    def __init__(self, parent       : BlueFors, 
                       scheme       : str,
                       authority    : str,
                       query        : str,
                       **kwargs):
    
        super().__init__(parent=parent, name='BlueForsPressureChannels', **kwargs)

        self._scheme = scheme
        self._authority = authority
        self._query = query

class BlueForsPressureChannels(InstrumentChannel):

    def __init__(self, parent                      : BlueFors, 
                       channel_vacuum_can          : int,
                       channel_pumping_line        : int,
                       channel_compressor_outlet   : int,
                       channel_compressor_inlet    : int,
                       channel_mixture_tank        : int,
                       channel_venting_line        : int,
                       **kwargs):
    
        super().__init__(parent=parent, name='BlueForsPressureChannels', **kwargs)

        self._channel_vacuum_can = channel_vacuum_can
        self._channel_pumping_line = channel_pumping_line
        self._channel_compressor_outlet = channel_compressor_outlet
        self._channel_compressor_inlet = channel_compressor_inlet
        self._channel_mixture_tank = channel_mixture_tank
        self._channel_venting_line = channel_venting_line

class BlueForsTemperatureChannels(InstrumentChannel):

    def __init__(self, parent                  : BlueFors, 
                       channel_50k_plate       : int,
                       channel_4k_plate        : int,
                       channel_magnet          : int,
                       channel_still           : int,
                       channel_mixing_chamber  : int,
                       channel_fse             : int,
                       **kwargs):
    
        super().__init__(parent=parent, name='BlueForsTemperatureChannels', **kwargs)

        self._channel_50k_plate = channel_50k_plate
        self._channel_4k_plate = channel_4k_plate
        self._channel_magnet = channel_magnet
        self._channel_still = channel_still
        self._channel_mixing_chamber = channel_mixing_chamber
        self._channel_fse = channel_fse

class BlueForsHeaterChannels(InstrumentChannel):

    def __init__(self, parent                  : BlueFors, 
                       channel_still_heater    : int,
                       channel_mxc_heater      : int,
                       channel_fse_heater      : Optional[int] = None,
                       **kwargs):
    
        super().__init__(parent=parent, name='BlueForsHeaterChannels', **kwargs)

        self._channel_still_heater = channel_still_heater
        self._channel_mxc_heater = channel_mxc_heater
        self._channel_fse_heater = channel_fse_heater

class BlueForsAPI(InstrumentChannel):
    
    def __init__(self, parent                  : BlueFors, 
                       api_url                 : BlueForsAPIURL,
                       bf_pres_channels        : BlueForsPressureChannels,
                       bf_temp_channels        : BlueForsTemperatureChannels,
                       bf_heater_channels      : BlueForsHeaterChannels,
                       **kwargs):

        super().__init__(parent=parent, name='BlueForsAPI', **kwargs)
        
        self._api_url = api_url

        self._temperature_channels_sensors_api_mapping = {bf_temp_channels._channel_50k_plate: 't50k', 
                                                          bf_temp_channels._channel_4k_plate: 't4k', 
                                                          bf_temp_channels._channel_still: 'tstill', 
                                                          bf_temp_channels._channel_mixing_chamber: 'tmixing', 
                                                          bf_temp_channels._channel_magnet: 'tmagnet', 
                                                          bf_temp_channels._channel_fse : 'tfse'}

        
        self._pressure_channels_api_mapping = {bf_pres_channels._channel_vacuum_can: 'vacuum can', 
                                               bf_pres_channels._channel_pumping_line: 'pumping line', 
                                               bf_pres_channels._channel_compressor_outlet: 'compressot outlet', 
                                               bf_pres_channels._channel_compressor_inlet: 'compressot inlet', 
                                               bf_pres_channels._channel_mixture_tank: 'mixture tank', 
                                               bf_pres_channels._channel_venting_line: 'venting line'}

        self._valves = list(range(1, 24))
        
        self._pumps = ['scroll1', 'scroll2', 'turbo1', 'turbo2', 'compressor']
        
        self._channel1_heaters = ['mxc', 'still']
        self._channel1_heater_channels_api_mapping = {'mxc' : bf_heater_channels._channel_mxc_heater, 
                                                      'still' : bf_heater_channels._channel_still_heater}
        
        if bf_heater_channels._channel_fse_heater is not None:
            self._channel2_heaters = ['fse']
            self._channel2_heater_channels_api_mapping = {'fse': bf_heater_channels._channel_fse_heater}

        self.add_parameter(name       = 'flow',
                           unit       = 'mmol/s',
                           get_parser = float,
                           get_cmd    = lambda: self._get_flow(),
                           docstring  = f'Flow of mixture',
                           )
        
        self._initialize_submodules()

    def _initialize_submodules(self):

        for channel_num, name in self._temperature_channels_sensors_api_mapping.items():
            
            self.add_parameter(name   = f'{name}',
                           unit       = 'K',
                           get_parser = float,
                           get_cmd    = lambda channel_num=channel_num: self._get_temperature(channel_num),
                           docstring  = f'Temperature of the {name}',
                           )

        for channel_num, name in self._pressure_channels_api_mapping.items():
            
            self.add_parameter(name   = f'p{channel_num}',
                           unit       = 'Bar',
                           get_parser = float,
                           get_cmd    = lambda channel_num=channel_num: self._get_pressure(channel_num),
                           docstring  = f'Pressure of the {name}',
                           )

        for valve_num in self._valves:

            valve_submodule = BlueForsAPIPValve(parent=self, num=valve_num)
            self.add_submodule(f'v{valve_num}', valve_submodule)

        for pump in self._pumps:

            pump_submodule = BlueForsAPIPump(parent=self, name=pump)
            self.add_submodule(pump, pump_submodule)

        for heater in self._channel1_heaters:

            heater_submodule = BlueForsAPIHeater(parent=self, num=self._channel1_heater_channels_api_mapping[heater], channel_temp_ctrl=1)
            self.add_submodule(f'{heater}_heater', heater_submodule)

        for heater in self._channel2_heaters:

            heater_submodule = BlueForsAPIHeater(parent=self, num=self._channel2_heater_channels_api_mapping[heater], channel_temp_ctrl=2)
            self.add_submodule(f'{heater}_heater', heater_submodule)

        cpa_submodule = BlueForsAPICPA(parent=self)
        self.add_submodule('cpa', cpa_submodule)

    def _get_temperature(self, channel: int):

        endpoint = self._temperature_channels_sensors_api_mapping[channel]

        path = f'values/mapper/bf/temperatures/{endpoint}'
        temperature_sensor_api_path = f'{self._api_url._scheme}://{self._api_url._authority}/{path}/?{self._api_url._query}'
        mapping = f'mapper.bf.temperatures.{endpoint}'

        value = self._get_response_value_from_api(api_path=temperature_sensor_api_path, mapping=mapping)
        
        return value

    def _get_pressure(self, channel: int):

        path = f'values/mapper/bf/pressures/p{channel}'
        pressure_guage_api_path = f'{self._api_url._scheme}://{self._api_url._authority}/{path}/?{self._api_url._query}'
        mapping = f'mapper.bf.pressures.p{channel}'

        value = self._get_response_value_from_api(api_path=pressure_guage_api_path, mapping=mapping)

        return value

    def _get_flow(self):
        path = f'values/mapper/bf/flow'
        flowmeter_api_path = f'{self._api_url._scheme}://{self._api_url._authority}/{path}/?{self._api_url._query}'
        mapping = f'mapper.bf.flow'

        value = self._get_response_value_from_api(api_path=flowmeter_api_path, mapping=mapping)

        return value

    def _get_response_value_from_api(self, api_path: str, mapping: str, parser: Optional[Callable] = None):
        
        response = requests.get(api_path, verify=False)
        value = self._measurement_parser(response, mapping)

        if parser is not None:
            value = parser(value)
            
        return value

    def _measurement_parser(self, response: requests.Response, mapping: str):

        latest_value = response.json()['data'][mapping]['content']['latest_value']
        
        value = latest_value['value']
        outdated = latest_value['outdated']
        date_time = time.ctime(float(latest_value['date']) / 1000)
        status = latest_value['status']        
        exception = latest_value['exception']

        if status in ['SYNCHRONIZED', 'INDEPENDENT', 'QUEUED']:
            return float(value)
        elif status in ['INVALID', 'DISCONNECTED']:
            return np.nan
        else:
            raise ValueError(f'Unrecognized measurement status: {status}. Check measurement and data.')

    def _get_state_parser(self, state: int):

        if state == 0:
            return False
        elif state == 1:
            return True
        else:
            raise ValueError(f'Unrecognized state: {state}. Check measurement and data.')

    def _set_state_parser(self, state: int):

        if type(state) == bool:
            if state:
                return 1
            elif not state:
                return 0
        else:
            raise ValueError(f'Unrecognized state: {state}. Check measurement and data.')

    def _convert_kelvin_to_celsius(self, value: float):

        return (value - 273.15)

    def _post_data_to_api(self, api_path_data: str, mapping_data: str, value_data: str, 
                          push_func_api_path: Optional[str] = None, push_func_mapping: Optional[str] = None):
        
        data = {
            'data': {
                mapping_data: {
                    'content': {
                        'value': value_data
                    }
                }
            }
        }
        
        json_responses = []
        
        response = requests.post(api_path_data, json=data, verify=False)
        json_responses.append(response.json())

        if push_func_api_path is not None:

            push_func_data = {
                'data': {
                    push_func_mapping: {
                        'content': {
                            'call': 1
                        }
                    }
                }
            }
            
            response = requests.post(push_func_api_path, json=push_func_data, verify=False)
            json_responses.append(response.json())

        for json_response in json_responses:
            if 'error' in json_response.keys():
                error = json_response['error']
                print(error)
                raise ValueError('Error while posting data. See printed dictionary for more information.')
            
class BlueForsAPIPValve(InstrumentChannel):

    def __init__(self, parent      : BlueForsAPI,
                       num         : int,
                       **kwargs):

        super().__init__(parent=parent, name=f'BlueForsAPI_valve_{num}', **kwargs)
        
        self._api_url = self.parent._api_url
        self._valve_num = num
        
        self.add_parameter(name   = f'state',
                       get_parser = bool,
                       get_cmd    = lambda valve_num=self._valve_num: self._get_valve_state(valve_num),
                       docstring  = f'State of valve {self._valve_num}',
                       )

    def _get_valve_state(self, valve_num: int):

        path = f'values/mapper/bf/valves/v{valve_num}'
        valve_api_path = f'{self._api_url._scheme}://{self._api_url._authority}/{path}/?{self._api_url._query}'
        mapping = f'mapper.bf.valves.v{valve_num}'

        value = self.parent._get_response_value_from_api(api_path=valve_api_path, mapping=mapping, parser=self.parent._get_state_parser)

        return value
    
class BlueForsAPIPump(InstrumentChannel):

    def __init__(self, parent      : BlueForsAPI,
                       name        : str,
                       **kwargs):

        super().__init__(parent=parent, name=f'BlueForsAPI_{name}', **kwargs)
        
        self._api_url = self.parent._api_url
        self._pump_name = name
        
        self.add_parameter(name   = f'state',
                       get_parser = bool,
                       get_cmd    = lambda pump_name=self._pump_name: self._get_pump_state(pump_name),
                       docstring  = f'State of {self._pump_name}',
                       )

    def _get_pump_state(self, pump: str):

        path = f'values/mapper/bf/pumps/{pump}'
        pump_api_path = f'{self._api_url._scheme}://{self._api_url._authority}/{path}/?{self._api_url._query}'
        mapping = f'mapper.bf.pumps.{pump}'

        value = self.parent._get_response_value_from_api(api_path=pump_api_path, mapping=mapping, parser=self.parent._get_state_parser)

        return value
    
class BlueForsAPIHeater(InstrumentChannel):

    def __init__(self, parent                : BlueForsAPI,
                       num                   : int,
                       channel_temp_ctrl     : int,
                       **kwargs):

        super().__init__(parent=parent, name=f'BlueForsAPI_heater_{num}', **kwargs)
        
        self._api_url = self.parent._api_url
        self._heater_num = num
        if channel_temp_ctrl == 1:
            self._channel_temp_ctrl = ''
        else:
            self._channel_temp_ctrl = channel_temp_ctrl
        
        self.add_parameter(name   = f'state',
                       get_parser = bool,
                       get_cmd    = lambda heater_num=self._heater_num: self._get_heater_state(heater_num),
                       set_cmd    = lambda state, heater_num=self._heater_num: self._set_heater_state(heater_num, state),
                       set_parser = self.parent._set_state_parser,
                       docstring  = f'State of heater_{self._heater_num}',
                       )

        self.add_parameter(name   = f'power',
                       unit       = 'Watt',
                       get_cmd    = lambda heater_num=self._heater_num: self._get_heater_power(heater_num),
                       set_cmd    = lambda power, heater_num=self._heater_num: self._set_heater_power(heater_num, power),
                       docstring  = f'Power of heater_{self._heater_num}',
                       )

    def _get_heater_state(self, heater_num: int):

        path = f'values/driver/bftc{self._channel_temp_ctrl}/data/heaters/heater_{heater_num}/active'
        heater_api_path = f'{self._api_url._scheme}://{self._api_url._authority}/{path}/?{self._api_url._query}'
        mapping = f'driver.bftc{self._channel_temp_ctrl}.data.heaters.heater_{heater_num}.active'

        value = self.parent._get_response_value_from_api(api_path=heater_api_path, mapping=mapping, parser=self.parent._get_state_parser)

        return value

    def _set_heater_state(self, heater_num: int, state: bool):

        path_data = f'values/driver/bftc{self._channel_temp_ctrl}/data/heaters/heater_{heater_num}/active'
        heater_api_path_data = f'{self._api_url._scheme}://{self._api_url._authority}/{path_data}/?{self._api_url._query}'
        mapping_data = f'driver.bftc{self._channel_temp_ctrl}.data.heaters.heater_{heater_num}.active'
        
        path_push = f'values/driver/bftc{self._channel_temp_ctrl}/data/heaters/heater_{heater_num}/write'
        heater_api_path_push = f'{self._api_url._scheme}://{self._api_url._authority}/{path_push}/?{self._api_url._query}'
        mapping_push = f'driver.bftc{self._channel_temp_ctrl}.data.heaters.heater_{heater_num}.write'

        self.parent._post_data_to_api(api_path_data=heater_api_path_data, mapping_data=mapping_data, value_data=state, 
                               push_func_api_path=heater_api_path_push, push_func_mapping=mapping_push)

    def _get_heater_power(self, heater_num: int):

        path = f'values/driver/bftc{self._channel_temp_ctrl}/data/heaters/heater_{heater_num}/power'
        heater_api_path = f'{self._api_url._scheme}://{self._api_url._authority}/{path}/?{self._api_url._query}'
        mapping = f'driver.bftc{self._channel_temp_ctrl}.data.heaters.heater_{heater_num}.power'

        value = self.parent._get_response_value_from_api(api_path=heater_api_path, mapping=mapping)

        return value

    def _set_heater_power(self, heater_num: int, power: bool):

        path_data = f'values/driver/bftc{self._channel_temp_ctrl}/data/heaters/heater_{heater_num}/power'
        heater_api_path_data = f'{self._api_url._scheme}://{self._api_url._authority}/{path_data}/?{self._api_url._query}'
        mapping_data = f'driver.bftc{self._channel_temp_ctrl}.data.heaters.heater_{heater_num}.power'

        path_push = f'values/driver/bftc{self._channel_temp_ctrl}/data/heaters/heater_{heater_num}/write'
        heater_api_path_push = f'{self._api_url._scheme}://{self._api_url._authority}/{path_push}/?{self._api_url._query}'
        mapping_push = f'driver.bftc{self._channel_temp_ctrl}.data.heaters.heater_{heater_num}.write'

        self.parent._post_data_to_api(api_path_data=heater_api_path_data, mapping_data=mapping_data, value_data=power, 
                               push_func_api_path=heater_api_path_push, push_func_mapping=mapping_push)
        
class BlueForsAPICPA(InstrumentChannel):

    def __init__(self, parent: BlueForsAPI, **kwargs):

        super().__init__(parent=parent, name=f'BlueForsAPI_CPA', **kwargs)
        
        self._api_url = self.parent._api_url

        self._cpa_temperatures_api_mapping = {'Water_In': 'coolant_in_temperature', 'Water_Out': 'coolant_out_temperature', 
                                              'Oil': 'oil_temperature', 'Helium': 'helium_temperature'}
    
        self.add_parameter(name   = f'state',
                       get_parser = bool,
                       get_cmd    = lambda: self._get_cpa_state(),
                       docstring  = f'State of CPA',
                       )
        for name, api_name in self._cpa_temperatures_api_mapping.items():
            
            self.add_parameter(name   = f'{name.lower()}_temperature',
                           unit       = 'C',
                           get_parser = float,
                           get_cmd    = lambda api_name=api_name: self._get_cpa_temp(api_name),
                           docstring  = f'Temperature of {name.replace("_", " ")}',
                           )

    def _get_cpa_state(self):

        path = f'values/driver/cpa/compressor_running_status'
        cpa_api_path = f'{self._api_url._scheme}://{self._api_url._authority}/{path}/?{self._api_url._query}'
        mapping = f'driver.cpa.compressor_running_status'

        value = self.parent._get_response_value_from_api(api_path=cpa_api_path, mapping=mapping, parser=self.parent._get_state_parser)

        return value

    def _get_cpa_temp(self, api_name: str):

        path = f'values/driver/cpa/{api_name}'
        cpa_api_path = f'{self._api_url._scheme}://{self._api_url._authority}/{path}/?{self._api_url._query}'
        mapping = f'driver.cpa.{api_name}'

        value = self.parent._get_response_value_from_api(api_path=cpa_api_path, mapping=mapping, parser=self.parent._convert_kelvin_to_celsius)

        return value