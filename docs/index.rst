mmwave
======

A python module for capturing and processing streamed ethernet data from the Texas Instruments DCA1000EVM Radar Data
Capture Card.


Overview
--------
Currently, the available functionality includes:

- listen for streamed capture data on UDP port 4098 *(Capture module)*
- save the streamed data to an output file *(FileWriter output sink)*



Installation
------------

The current version is pre-alpha, and has not been packaged/deployed. To install it:

1.  clone this repo
2.  cd to the mmwave project root directory
3.  run 'python setup.py install' to install the module


Usage
-----

To use the module, create an instances of the Capture object class and an instance of one or more output sink objects. Configuration options can be set either using object properties or passing them in the object initialization:

.. code-block:: python

    from mmwave import Capture, FileWriter

    listener = Capture(source_format='RAW')
    filesink = FileWriter(overwrite=True)

    listener.output_format='RAW_NO_SEQ'
    filesink.output_filename='~/adc_raw_out.bin'

    listener.add_sink(filesink)  # register the output sink with the capture instance

    listener.start() # start listening for traffic on UDP port 4098

The listener will wait ad infinitum for the first packet, unless program execution is stopped. Once the first packet has been received, the listener will time out and clean up 1s after the last packet is received.


Capture Object Properties and Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Properties**

- bind_address (string, rw) - the address to bind the listener too *(default: '0.0.0.0')*
- source_format (string, rw) - the source format for the incoming stream, can be one of
  - RAW *(default)*
  - DATA_SEPARATED_MODE *(not yet implemented)*
- output_format (string, rw) - the output format to send to the sink, can be one of
  - RAW_NO_SEQ - output file only contains binary capture payload *(default)*
  - RAW_SEQ - output file contains binary capture payload prepended with message sequence number, message payload size, and total capture size
  - DATA_SEPARATED_NO_SEQ *(not yet implemented)*
  - DATA_SEPARATED_SEQ *(not yet implemented)*
- message_window_size (integer, rw) - the number of messages in the streaming window, valid range is 1-128 *(default is 16)*
- output_sinks (list of objects, ro) - returns all added output sinks
- stats (dictionary, ro) - returns execution stats
  - messages - the total number of messages processed
  - bytes - the total number of payload bytes received (actual)
  - out_of_order - count of out of order messages
  - missing - count of missing messages (gaps in sequence numbers)

**Methods**
- add_sink(<output-sink-instance>) - send an output stream to the specified output sink instance
- start() - start listening
