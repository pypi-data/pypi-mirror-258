from agogos.refiner import Refiner
import pytest

class TestRefiner:

    def test_refine(self):
        
        class refinerInstance(Refiner):
            def predict(self, predictions):
                return predictions
            
        refiner = refinerInstance()

        assert refiner.predict([1, 2, 3]) == [1, 2, 3]

    def test_refine_abstract(self):
        with pytest.raises(TypeError):
            Refiner()