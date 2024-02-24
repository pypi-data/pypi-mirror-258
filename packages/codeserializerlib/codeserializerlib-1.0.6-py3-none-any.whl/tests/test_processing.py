from codeserializerlib import processing
from codeserializerlib.models.code import code
from codeserializerlib.models.code_type import code_type



# define the code list for testing
codes = [
    code(hash="IEH79A04", code_type=code_type.store_credit, shop_name="Ola Kala", value=100),
    code(hash="IEH291F4", code_type=code_type.store_credit, shop_name="Ola Kala", value=100),
    code(hash="IEH261C1", code_type=code_type.store_credit, shop_name="Ola Kala", value=100),
]

def test_process_message():
    ret_codes = processing.process_message("Ola Kala", "Hier habt ihr nochmal 3x100€ Gutscheine.\nIEH79A04\nIEH291F4\nIEH261C1")

    assert len(ret_codes) == len(codes)
    assert [code.to_dict() for code in ret_codes] == [code.to_dict() for code in codes]

def test_process_message_no_codes():
    ret_codes = processing.process_message("Ola Kala", "Hier habt ihr nochmal Gutscheine.")
    assert len(ret_codes) == 0

def test_process_message_one_code():
    ret_codes = processing.process_message("Ola Kala", "Hier habt ihr nochmal 1x100€ Gutscheine.\nIEH79A04")
    assert len(ret_codes) == 1
    assert ret_codes[0].to_dict() == codes[0].to_dict()