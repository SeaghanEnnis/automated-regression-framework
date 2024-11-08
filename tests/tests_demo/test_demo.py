import pytest

def test_show_pass():
    assert 1 == 1, "Demo Success"
    
def test_show_failure():
    assert 1 == 2, "Demo Failure"
    
def test_show_failure_exception(unfufilled_param):
     assert 1 == 1, "Demo Exception"
     
     
@pytest.mark.skip(reason="skipped test example")
def test_show_skip():
    assert 1 == 1, "Demo Success"