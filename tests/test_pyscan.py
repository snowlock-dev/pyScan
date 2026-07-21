# test_pyscan.py

from unittest.mock import MagicMock, patch
import pytest

from pyscan import run_scan, scan_port


@patch("socket.socket")
def test_scan_port_open(mock_socket):
    mock_instance = MagicMock()
    mock_instance.connect_ex.return_value = 0
    mock_socket.return_value.__enter__.return_value = mock_instance

    result = scan_port("127.0.0.1", 80)
    assert result == 80


@patch("socket.socket")
def test_scan_port_closed(mock_socket):
    mock_instance = MagicMock()
    mock_instance.connect_ex.return_value = 111  # Connection refused
    mock_socket.return_value.__enter__.return_value = mock_instance

    result = scan_port("127.0.0.1", 80)
    assert result is None


@patch("pyscan.scan_port")
def test_run_scan_range(mock_scan_port):
    # Simulate port 22 and 80 being open, others returning None
    mock_scan_port.side_effect = lambda host, port: port if port in [20, 80] else None

    open_ports = run_scan("127.0.0.1", 20, 100)

    assert open_ports == [20, 80]
    assert mock_scan_port.call_count == 81
