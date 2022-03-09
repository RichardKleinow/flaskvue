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

# ToDo: Serve Production Version from nginx

#############
# PYADS AREA
#############
class BC9000:
    def __init__(self, connection_string: pyads.Connection, offset=0):
        self.conn = connection_string
        # Connection area
        if not self.conn.is_open:
            self.conn.open()
        # Memory area
        self.cmd = self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset, plc_datatype=pyads.PLCTYPE_INT)
        self.targetpos = self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset+4, plc_datatype=pyads.PLCTYPE_DINT)
        self.actpos = self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset+8, plc_datatype=pyads.PLCTYPE_DINT)
        self.state = self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset+16, plc_datatype=pyads.PLCTYPE_INT)
        self.error = self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset+18, plc_datatype=pyads.PLCTYPE_SINT)
        self.virtposlim = self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset+50, plc_datatype=pyads.PLCTYPE_DINT)
        self.virtneglim = self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset+54, plc_datatype=pyads.PLCTYPE_DINT)
        self.config = self.conn.get_symbol(index_group=pyads.INDEXGROUP_MEMORYBYTE, index_offset=offset+58, plc_datatype=pyads.PLCTYPE_INT)
        # State area
        self.running = False
        if self.conn.read_state()[0] == 6:
            self.running = True

    def get_initial_values(self):
        self.Dvalues = {}
        self.Dvalues['command'] = self.cmd.read()
        self.Dvalues['targetpos'] = self.targetpos.read()
        self.Dvalues['actpos'] = self.actpos.read()
        self.Dvalues['state'] = self.state.read()
        self.Dvalues['error'] = self.error.read()
        self.Dvalues['virtposlim'] = self.virtposlim.read()
        self.Dvalues['virtneglim'] = self.virtneglim.read()
        self.Dvalues['config'] = self.config.read()
        self.Dvalues['running'] = self.running
        return self.Dvalues


    def connect_event_handler(self):
        self.cmd.clear_device_notifications()
        self.cmd.add_device_notification(self.notify_frontend)
        #self.targetpos.add_device_notification(self.notify_frontend)
        #self.actpos.add_device_notification(self.notify_frontend)
        #self.state.add_device_notification(self.notify_frontend)
        #self.error.add_device_notification(self.notify_frontend)
        #self.virtposlim.add_device_notification(self.notify_frontend)
        #self.virtneglim.add_device_notification(self.notify_frontend)
        #self.config.add_device_notification(self.notify_frontend)


    def notify_frontend(self, args):
        print(args)
        pass



#############
# FLASK AREA
#############
class Appl:
    def __init__(self):
        app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
        app.config['SECRET_KEY'] = 'secret!'
        self.app = app      # Save app for decorator usage
        self.socketio = SocketIO(app, cors_allowed_origins='*')
        self.socketio.on_namespace(CustomMethods())
        self._port = 5000
        self._debug = True

        # Routing
        @app.route('/', defaults={'path':''})
        @app.route('/<path:path>')
        def catch_all(path):
            return render_template("index.html")

    def run(self):
        self.socketio.run(self.app,debug=self._debug, host='0.0.0.0', port=int(self._port))


class CustomMethods(Namespace):
    def random_number(self):
        return randint(1,100)

    def on_connect(self):
        logging.info('socket connected')

    def on_disconnect(self):
        logging.info('socket disconnected')


###############
# RUNTIME AREA
###############
class Runtime:
    def __init__(self):
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
        self.add_route_beckhoff()
        self.check_connection()


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
                self.dInitValues = self.dev.get_initial_values()

                # ToDo: Send init values to Frontend
                self.dev.connect_event_handler()
                while True:
                    print(self.dInitValues)
                    time.sleep(1)
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
    App = Appl()
    rt = Runtime()
    # Move Runtime to another Thread
    app_thread = threading.Thread(target=rt.run)
    app_thread.start()
    App.run()







