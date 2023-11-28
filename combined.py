from predefined_main import *
from defined_main import *

def get_results(num_data_items, num_transactions):
    defined_good_nonflagged, defined_good_flagged, defined_bad_nonflagged, defined_bad_flagged = defined_results(num_data_items=num_data_items, num_transactions=num_transactions)
    predefined_good_nonflagged, predefined_good_flagged, predefined_bad_nonflagged, predefined_bad_flagged = predefined_results(num_data_items=num_data_items, num_transactions=num_transactions)
    return dict(defined_good_nonflagged=defined_good_nonflagged, defined_good_flagged=defined_good_flagged, defined_bad_nonflagged=defined_bad_nonflagged, defined_bad_flagged=defined_bad_flagged, predefined_good_nonflagged=predefined_good_nonflagged, predefined_good_flagged=predefined_good_flagged,predefined_bad_nonflagged=predefined_bad_nonflagged,predefined_bad_flagged=predefined_bad_flagged)

def get_values_for_key(list_of_dicts, key):
    return [d[key] for d in list_of_dicts if key in d]