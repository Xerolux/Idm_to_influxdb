import math
import numpy as np
from idm_logger.ai.models import RollingWindowStats

class TestRollingWindowStats:
    def test_running_sum_logic(self):
        # Window size 5
        model = RollingWindowStats(window_size=5)

        # Add 3 items
        data = [1.0, 2.0, 3.0]
        for v in data:
            model.update({"s1": v})

        assert len(model.history["s1"]) == 3
        assert model.sums["s1"] == 6.0
        assert model.sq_sums["s1"] == 14.0 # 1+4+9

        # Add 2 more (full window)
        model.update({"s1": 4.0})
        model.update({"s1": 5.0})

        assert len(model.history["s1"]) == 5
        assert model.sums["s1"] == 15.0 # 1+2+3+4+5
        assert model.sq_sums["s1"] == 55.0 # 1+4+9+16+25

        # Add 6th item (should push out 1.0)
        model.update({"s1": 6.0})

        assert len(model.history["s1"]) == 5
        assert model.history["s1"][0] == 2.0
        assert model.history["s1"][-1] == 6.0

        expected_sum = 2+3+4+5+6 # 20
        expected_sq_sum = 4+9+16+25+36 # 90

        assert model.sums["s1"] == expected_sum
        assert model.sq_sums["s1"] == expected_sq_sum

    def test_detection_accuracy(self):
        # Compare running stats result with direct calculation
        model = RollingWindowStats(window_size=10)
        data = [10, 12, 23, 23, 16, 23, 21, 16]

        for v in data:
            model.update({"s1": float(v)})

        # Detect
        # Sensitivity low enough to ensure we get a calculation, high enough to not trigger?
        # Actually detect returns anomalies only if z_score > sensitivity.
        # But we can inspect internal state for test.

        # Manual calculation
        vals = np.array(data)
        expected_mean = np.mean(vals)
        expected_std = np.std(vals)

        n = len(data)
        calc_mean = model.sums["s1"] / n
        calc_var = (model.sq_sums["s1"] / n) - (calc_mean * calc_mean)
        calc_std = math.sqrt(calc_var)

        assert math.isclose(calc_mean, expected_mean, rel_tol=1e-9)
        assert math.isclose(calc_std, expected_std, rel_tol=1e-9)

    def test_save_load_state(self):
        model = RollingWindowStats(window_size=5)
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        for v in data:
            model.update({"s1": v})

        state = model.save_state()

        new_model = RollingWindowStats(window_size=5)
        new_model.load_state(state)

        assert len(new_model.history["s1"]) == 5
        assert new_model.sums["s1"] == 15.0
        assert new_model.sq_sums["s1"] == 55.0
