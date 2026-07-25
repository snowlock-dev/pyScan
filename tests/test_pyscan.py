# test_pyscan.py

from unittest.mock import MagicMock, patch
from pyscan import run_scan, scan_port
import pytest


@pytest.mark.parametrize(
    "connect_value, expected_result",
    [
        (0, 80),          # Port is open
        (111, None),      # Connection refused (closed)
    ],
)
@patch("socket.socket")
def test_scan_port_success_or_closed(mock_socket, connect_value, expected_result):
    mock_instance = MagicMock()
    mock_instance.connect_ex.return_value = connect_value
    mock_socket.return_value.__enter__.return_value = mock_instance

    result = scan_port("127.0.0.1", 80)
    assert result == expected_result


@patch("socket.socket")
def test_scan_port_os_error(mock_socket):
    # Simulate an OSError (e.g., network unreachable or interface down)
    mock_socket.side_effect = OSError("Network is unreachable")

    result = scan_port("127.0.0.1", 80)
    assert result is None


@patch("pyscan.scan_port")
def test_run_scan_range(mock_scan_port):
    # Simulate ports 20 and 80 being open, others returning None within range 20 to 100
    mock_scan_port.side_effect = lambda host, port, timeout=1.0: port if port in [20, 80] else None

    open_ports = run_scan("127.0.0.1", start_port=20, end_port=100)

    assert sorted(open_ports) == [20, 80]
    assert mock_scan_port.call_count == 81


@patch("pyscan.scan_port")
def test_run_scan_invalid_range(mock_scan_port):
    # Edge Case: start_port greater than end_port should return an empty list immediately
    open_ports = run_scan("127.0.0.1", start_port=100, end_port=50)

    assert open_ports == []
    mock_scan_port.assert_not_called()


@patch("pyscan.scan_port")
def test_run_scan_boundary_clamping(mock_scan_port):
    # Edge Case: Ports out of TCP bounds (e.g., 0 or 70000) should be clamped to 1-65535
    mock_scan_port.return_value = None

    run_scan("127.0.0.1", start_port=-50, end_port=99999)

    # Max range allowed by clamp is 1 to 65535 (total 65535 calls)
    assert mock_scan_port.call_count == 65535
