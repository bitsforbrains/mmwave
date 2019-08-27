mmwave
======

A python module for capturing and processing streamed ethernet data from the Texas Instruments DCA1000EVM Radar Data
Capture Card.


Overview
--------
Currently, the available functionality includes:

* listen for streamed capture data on UDP port 4098
* save the binary data in an output file (raw data only, or as series of messages with the format sequence_number-payload_size-total_transfer_size)


Installation
------------

The current version is pre-alpha, and has not been packaged/deployed. To install it:

1.  clone this repo
2.  cd to the mmwave project root directory
3.  run 'python setup.py install' to install the module


Usage
-----

To use the module, create new instances of the Capture and FileWriter object classes. Configuration options can be set either using object properties or passing them in the object initialization:

.. code-block:: python

    from mmwave import Capture, FileWriter
    listener = Capture(source_format='RAW')
    filesink = FileWriter(overwrite=True)

    listener.output_format='RAW_NO_SEQ'
    filesink.output_filename='~/adc_raw_out.bin'

    listener.add_sink(filesink)  # register the output sink with the capture instance

    listener.start() # start listening for traffic on UDP port 4098

The listener will wait ad infinitum for the first packet, unless program execution is stopped. Once the first packet has been received, the listener will time out and clean up 1s after the last packet is received.
