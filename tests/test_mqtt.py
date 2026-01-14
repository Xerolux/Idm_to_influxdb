import pytest
from unittest.mock import MagicMock, patch
from idm_logger.mqtt import MQTTPublisher

@pytest.fixture
def mock_mqtt_client():
    """Fixture to mock the paho.mqtt.client."""
    with patch('paho.mqtt.client.Client') as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        yield mock_client_instance

@pytest.fixture
def publisher(mock_mqtt_client):
    """Fixture to create an MQTTPublisher instance with a mocked client."""
    # Mock config to enable MQTT
    with patch('idm_logger.mqtt.config') as mock_config:
        mock_config.get.side_effect = lambda key, default=None: {
            "mqtt.enabled": True,
            "mqtt.topic_prefix": "idm/heatpump",
            "mqtt.qos": 1,
        }.get(key, default)

        p = MQTTPublisher()
        p.client = mock_mqtt_client
        p.connected = True
        yield p

def test_publish_data_handles_flat_dictionary(publisher, mock_mqtt_client):
    """
    Verify that publish_data correctly processes a flat dictionary,
    creates the correct JSON payloads, and publishes to the right topics.
    """
    # Sample data mimicking the output of modbus.read_sensors()
    test_data = {
        "temp_outside": 12.5,
        "op_mode": 1,
        "op_mode_str": "Heating",
        "fault_active": False,
    }

    # Call the method under test
    publisher.publish_data(test_data)

    # --- Assertions ---

    # 1. Check calls for individual sensor topics
    calls = mock_mqtt_client.publish.call_args_list

    # Expected calls: temp_outside, op_mode, fault_active, and the /state topic
    assert len(calls) == 4

    # Check temp_outside
    temp_call = next(c for c in calls if c.args[0] == 'idm/heatpump/temp_outside')
    assert temp_call is not None
    assert '"value": 12.5' in temp_call.args[1]

    # Check op_mode (raw value and _str value)
    op_mode_call = next(c for c in calls if c.args[0] == 'idm/heatpump/op_mode')
    assert op_mode_call is not None
    assert '"value": 1' in op_mode_call.args[1]
    assert '"value_str": "Heating"' in op_mode_call.args[1]

    # Check fault_active
    fault_call = next(c for c in calls if c.args[0] == 'idm/heatpump/fault_active')
    assert fault_call is not None
    assert '"value": false' in fault_call.args[1]

    # 2. Verify that _str topics are NOT created
    for call in calls:
        assert not call.args[0].endswith("_str")

    # 3. Check the combined state topic
    state_call = next(c for c in calls if c.args[0] == 'idm/heatpump/state')
    assert state_call is not None
    assert state_call.args[1] == '{"temp_outside": 12.5, "op_mode": 1, "op_mode_str": "Heating", "fault_active": false}'
