VALID_SOURCE_FORMATS = {'RAW': {'description': 'Raw mode data format'},
                        'DATA_SEPARATED': {'description': 'Data separated mode data format'}}

VALID_OUTPUT_FORMATS = {'RAW_SEQ':
                            {'description': 'Raw mode with message sequence numbers',
                             'fields': ['raw_seq', 'raw_payload_size', 'raw_capture_size', 'payload'],
                             'valid_sources': ['RAW']},
                        'RAW_NO_SEQ':
                            {'description': 'Raw mode (payload only)',
                             'fields': ['payload'],
                             'valid_sources': ['RAW']},
                        'DATA_SEPARATED_SEQ':
                            {'description': '',
                             'fields': [],
                             'valid_sources': ['DATA_SEPARATED']},
                        'DATA_SEPARATED_NO_SEQ':
                            {'description': '',
                             'fields': [],
                             'valid_sources': ['DATA_SEPARATED']}}
