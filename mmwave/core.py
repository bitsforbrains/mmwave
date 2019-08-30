import socket
import struct
import logging
from .dataformats import VALID_SOURCE_FORMATS, VALID_OUTPUT_FORMATS


class Capture(object):

    def __init__(self, bind_address='0.0.0.0', source_format='RAW', message_window_size=16):
        self._logger = logging.getLogger(__name__)
        self._bind_address = bind_address
        self._source_format = source_format
        self._output_sinks = []
        self._message_window_size = message_window_size
        self._kill = False
        self._listening = False
        self._currentseq = 0
        self._stats = {'messages': 0, 'bytes': 0, 'out_of_order': 0, 'missing': 0}

    def _bind(self):
        self._logger.debug('Starting listener')
        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.settimeout(1)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udp_socket.bind((self.bind_address, 4098))
            self._listening = True
            return udp_socket
        except:
            self._logger.error('Unhandled exception binding to socket')
            self._listening = False
            return None

    @staticmethod
    def process_message(sock):
        buf = sock.recv(8192)
        seq_num = buf[:4]
        capture_size = buf[4:10]
        payload = buf[10:]
        payload_size = len(payload)
        return payload, seq_num, payload_size, capture_size

    def _store_message(self, message_window, message):
        if len(message_window) == 0:
            message_window.append(message)
        else:
            if message['seq_num'] <= message_window[-1]['seq_num']:
                self._logger.warning('Message seq_num {0} received out of order'.format(message['seq_num']))
                self._stats['out_of_order'] += 1
                index = -1
                for msg in message_window:
                    index += 1
                    if message['seq_num'] > msg['seq_num']:
                        message_window.insert(index + 1, message)
            else:
                message_window.append(message)

        if len(message_window) >= self.message_window_size:
            self._process_message_window(message_window)

    def _process_message_window(self, message_window):
        msg = message_window.pop(0)
        if msg['seq_num'] - self._currentseq != 1:
            self._logger.warning('Missing sequence number (curr={0}, next={1})'
                                 .format(self._currentseq, msg['seq_num']))
            self._stats['missing'] += 1
        self._currentseq = msg['seq_num']
        # dump to all sinks
        for sink in self.output_sinks:
            if self.source_format not in VALID_OUTPUT_FORMATS[sink.output_format]['valid_sources']:
                self._logger.warn('output format {0} configured for {1} is not compatible with {2} source type'
                                  .format(sink.output_format, sink.name(), self.source_format))
            else:
                data = b''
                for field in VALID_OUTPUT_FORMATS[sink.output_format]['fields']:
                    data += msg[field]
                sink.receive(data)

    def _flush_window(self, message_window):
        while len(message_window) > 0:
            self._process_message_window(message_window)

    def add_sink(self, output_sink):
        try:
            if output_sink not in self._output_sinks:
                self._output_sinks.append(output_sink)
            return True
        except:
            self._logger.error('Unhandled exception adding output sink')
            return False

    def start(self):
        message_window = []
        self._currentseq = 0
        self._stats = {'messages': 0, 'bytes': 0, 'out_of_order': 0, 'missing': 0}

        if self.output_sinks is []:
            self._logger.warn("No output sinks registered")

        listener_socket = self._bind()
        if listener_socket is not None:
            print('Bound to port 4098')
        else:
            print('Could not bind to UDP port')
        while self._kill is False:
            try:
                payload_size = 0
                payload, raw_seq, payload_size, raw_capture_size = self.process_message(listener_socket)
            except socket.timeout:
                if self._currentseq > 0:
                    listener_socket.close()
                    self._flush_window(message_window)
                    self._kill = True
                else:
                    self._logger.info('Listener timed out waiting for data')
                    continue
            if payload_size > 0:
                seq_num, = struct.unpack('<L', raw_seq)
                print('Processing message with sequence number {0}'.format(seq_num))
                capture_size, = struct.unpack('<Q', raw_capture_size + b'\x00\x00')

                self._logger.debug('Received message (seq/payload-size/total-capture-size):',
                                   seq_num, payload_size, capture_size)
                raw_payload_size = struct.pack('<L', len(payload))

                message = {'seq_num': seq_num, 'raw_seq': raw_seq, 'raw_payload_size': raw_payload_size,
                           'raw_capture_size': raw_capture_size, 'payload': payload}
                self._store_message(message_window, message)
                self._stats['bytes'] += payload_size
                self._stats['messages'] += 1


    @property
    def bind_address(self):
        return self._bind_address

    @bind_address.setter
    def bind_address(self, value):
        try:
            socket.inet_pton(socket.AF_INET, value)
            self._bind_address = value
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, value)
                self._bind_address = value
            except socket.error:
                raise ValueError('source format invalid (must be RAW or DATA_SEPARATED)')

    @property
    def source_format(self):
        return self._source_format

    @source_format.setter
    def source_format(self, value):
        if value not in VALID_SOURCE_FORMATS:
            raise ValueError('source format invalid')
        self._source_format = value

    @property
    def message_window_size(self):
        return self._message_window_size

    @message_window_size.setter
    def message_window_size(self, value):
        if value < 1 or value > 128:
            raise ValueError('message_window_size value is invalid (must be between 1 and 128)')
        self._message_window_size = value

    @property
    def output_sinks(self):
        return self._output_sinks

    @property
    def stats(self):
        return self._stats
