#!/usr/bin/python3

import os
import sys
import logging
import time
import pyads
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send, emit, Namespace
from random import randint
import threading
from queue import Queue


# ToDo: Serve Production Version from nginx

#############
# PYADS AREA
#############
class BC9000:
    def __init__(self, connection_string: pyads.Connection, offset=0):
        self.conn = connection_string
        self.deviceName = 'BC9000'
        # 66 Byte Struct
        offset = offset * 66
        # Connection area
        if not self.conn.is_open:
            self.conn.open()
        # Memory area
        self.dValues = {'command': self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset, plc_datatype=pyads.PLCTYPE_INT),
                        'targetpos': self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset + 4, plc_datatype=pyads.PLCTYPE_DINT),
                        'actpos': self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset + 8, plc_datatype=pyads.PLCTYPE_DINT),
                        'state': self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset + 16, plc_datatype=pyads.PLCTYPE_INT),
                        'error': self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset + 18, plc_datatype=pyads.PLCTYPE_SINT),
                        'virtposlim': self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset + 50, plc_datatype=pyads.PLCTYPE_DINT),
                        'virtneglim': self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset + 54, plc_datatype=pyads.PLCTYPE_DINT),
                        'config': self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset + 58, plc_datatype=pyads.PLCTYPE_INT)
                        }


    def get_values(self):
        if not self.conn.is_open:
            self.conn.open()
        self.dEmitter = {key: self.dValues[key].read() for key in self.dValues}
        self.dEmitter['plc_running'] = True if self.conn.read_state()[1] == 0 else False
        return self.dEmitter


#############
# FLASK AREA
#############
class Appl:
    def __init__(self, queue: Queue):
        app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
        app.config['SECRET_KEY'] = 'secret!'
        self.app = app  # Save app for decorator usage
        self.socketio = SocketIO(app, cors_allowed_origins='*')
        self.queue = queue
        self.socketio.on_namespace(CustomMethods(self.queue))
        self._port = 5000
        self._debug = True

        # Routing
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def catch_all(path):
            return render_template("index.html")

    def run(self):
        self.socketio.run(self.app, debug=self._debug, host='0.0.0.0', port=int(self._port))


class CustomMethods(Namespace):
    def __init__(self, workQ:Queue):
        Namespace.__init__(self)
        self.workQ = workQ
        self.dTransfer = {}

    def on_req_DeviceType(self):
        self.dTransfer = self.workQ.queue[0]
        logging.info(f'Device Type requested. Returning {self.dTransfer["DeviceType"]}')
        return self.dTransfer['DeviceType']

    def on_connect(self):
        logging.info('socket connected')

    def on_disconnect(self):
        logging.info('socket disconnected')


###############
# RUNTIME AREA
###############
class Runtime(threading.Thread):
    def __init__(self, workQ:Queue, socket:SocketIO):
        threading.Thread.__init__(self)
        self.workQ = workQ
        self.dTransfer = {
            'DeviceType': ''
        }
        self.workQ.put(self.dTransfer)
        self.dev = None
        self.socket = socket
        self.SENDER_AMS = '192.168.178.56.1.1'
        self.PLC_AMS = '192.168.178.200.1.1'
        self.PLC_IP = '192.168.178.200'
        self.PLC_USERNAME = 'pi'
        self.PLC_PASSWORD = 'raspberry'
        self.ROUTE_NAME = 'RouteToPC '
        self.HOSTNAME = '192.168.178.56'
        self._isWin = False
        if os.name == 'nt':
            self._isWin = True

    def run(self):
        # Loop
        #       Detect Connection state
        #       get type
        #       pull initial values
        #       connect on-change handlers
        #       write values from Frontend
        while self.dev is None:
            self.check_connection()
            self.add_route_beckhoff()

        while True:
            self.send_data()
            time.sleep(1)


    def send_data(self):
        with self.plc:
            if self.dev is not None:
                self.socket.emit('update_values', self.dev.get_values())
            else:
                logging.error('Device got overwritten')

    # Create Route on PLC Side
    def add_route_beckhoff(self):
        if self._isWin:
            return
        pyads.open_port()
        pyads.set_local_address(self.SENDER_AMS)
        pyads.add_route_to_plc(self.SENDER_AMS, self.HOSTNAME, self.PLC_IP, self.PLC_USERNAME, self.PLC_PASSWORD, route_name=self.ROUTE_NAME)
        pyads.close_port()

    def check_connection(self):
        # Create Route on Client Side -> Win: Route has to be added via TwinCatRouter,
        # Linux Route is added on first connection
        # Todo: Add Routine to change ports on failure (pyads.TC2_PLC1 f.e.)
        pyads.PORT_BC = 800
        if self._isWin:
            self.plc = pyads.Connection(self.PLC_AMS, pyads.PORT_BC)
        else:
            self.plc = pyads.Connection(self.PLC_AMS, pyads.PORT_BC, self.PLC_IP)
        with self.plc as plc:
            if plc.read_device_info()[0] == 'COUPLER_PLC':
                self.dev = BC9000(plc)
                self.dTransfer['DeviceType'] = self.dev.deviceName
            else:
                logging.error('Device type not implemented yet')


###############
# GENERAL AREA
###############
def init_logging():
    log_format = f"%(asctime)s [%(processName)s] [%(name)s] [%(levelname)s] %(message)s"
    log_level = logging.DEBUG
    if getattr(sys, 'frozen', False):
        folder = os.path.dirname(sys.executable)
    else:
        folder = os.path.dirname(os.path.abspath(__file__))
    # noinspection PyArgumentList
    logging.basicConfig(
        format=log_format,
        level=log_level,
        force=True,
        handlers=[
            logging.FileHandler(filename=f'{folder}\\debug.log', mode='w', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ])


if __name__ == "__main__":
    init_logging()
    q = Queue()
    App = Appl(q)
    rt = Runtime(q, App.socketio)
    rt.daemon = True
    rt.start()
    # Move Runtime to another Thread
    App.run()
