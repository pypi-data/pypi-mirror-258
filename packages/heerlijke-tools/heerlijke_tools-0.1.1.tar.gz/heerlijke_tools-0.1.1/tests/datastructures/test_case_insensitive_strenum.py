import pytest


class TestCaseInsensitiveStrenum:
    class TestAuto:            
        def test_str_equality(self, input_enum):
            assert input_enum.FIRST == "FIRST"
            assert input_enum.FIRST == "First"
            assert input_enum.FIRST == "first"
            assert input_enum.FIRST == "fIrST"
            assert input_enum.SECOND == "SECOND"
            assert input_enum.SECOND == "Second"
            assert input_enum.SECOND == "second"
            assert input_enum.SECOND == "sEcOnD"
            assert input_enum.THIRD == "THIRD"
            assert input_enum.THIRD == "Third"
            assert input_enum.THIRD == "third"
            assert input_enum.THIRD == "tHiRD"
            
        def test_creation(self, input_enum):
            assert input_enum.FIRST == input_enum("FIRST")
            assert input_enum.FIRST == input_enum("First")
            assert input_enum.FIRST == input_enum("first")
            assert input_enum.FIRST == input_enum("fIrST")
            assert input_enum.SECOND == input_enum("SECOND")
            assert input_enum.SECOND == input_enum("Second")
            assert input_enum.SECOND == input_enum("second")
            assert input_enum.SECOND == input_enum("sEcOnD")
            assert input_enum.THIRD == input_enum("THIRD")
            assert input_enum.THIRD == input_enum("Third")
            assert input_enum.THIRD == input_enum("third")
            assert input_enum.THIRD == input_enum("tHiRD")
    
        def test_raises_value_error_if_incorrect(self, input_enum):
            with pytest.raises(ValueError):
                input_enum("Does_not_exist")
