from src.detect import is_azerbaijani

def test_true():
	assert is_azerbaijani("salam")

def test_false():
	assert is_azerbaijani("hello")
