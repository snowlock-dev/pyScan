# test_pyscan.py

import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from pyscan import run_scan, scan_port


@pytest.mark.parametrize(
    "side_effect, expected_result",
    [
        ("open_port", 80),                            # Port is open
        (OSError(111, "Connection refused"), None),   # Connection refused (closed)
    ],
)
@pytest.mark.asyncio
@patch("pyscan.asyncio.open_connection", new_callable=AsyncMock)
async def test_scan_port_success_or_closed(mock_open_conn, side_effect, expected_result):
    
    if isinstance(side_effect, Exception):
        # For errors, just assign the side_effect
        mock_open_conn.side_effect = side_effect
    else:
        # For open ports, mock the reader and writer
        reader = MagicMock()
        writer = MagicMock()
        writer.wait_closed = AsyncMock() 
        
        mock_open_conn.return_value = (reader, writer)

    result = await scan_port("127.0.0.1", 80)
    assert result == expected_result


@pytest.mark.asyncio
@patch("pyscan.asyncio.open_connection", new_callable=AsyncMock)
async def test_scan_port_timeout(mock_open_conn):
    # Simulate a firewall silently dropping packets (Timeout)
    mock_open_conn.side_effect = asyncio.TimeoutError()

    result = await scan_port("127.0.0.1", 80)
    assert result is None


@pytest.mark.asyncio
@patch("pyscan.asyncio.open_connection", new_callable=AsyncMock)
async def test_scan_port_os_error(mock_open_conn):
    # Simulate a real network error (e.g, network unreachable)
    mock_open_conn.side_effect = OSError("Network is unreachable")

    result = await scan_port("127.0.0.1", 80)
    assert result is None


@pytest.mark.asyncio
@patch("pyscan.scan_port", new_callable=AsyncMock)
async def test_run_scan_range(mock_scan_port):
    mock_scan_port.side_effect = lambda host, port, timeout=1.0: port if port in [20, 80] else None

    open_ports = await run_scan("127.0.0.1", start_port=20, end_port=100)

    assert sorted(open_ports) == [20, 80]
    assert mock_scan_port.call_count == 81


@pytest.mark.asyncio
@patch("pyscan.scan_port", new_callable=AsyncMock)
async def test_run_scan_invalid_range(mock_scan_port):
    open_ports = await run_scan("127.0.0.1", start_port=100, end_port=50)

    assert open_ports == []
    mock_scan_port.assert_not_called()


@pytest.mark.asyncio
@patch("pyscan.scan_port", new_callable=AsyncMock)
async def test_run_scan_boundary_clamping(mock_scan_port):
    mock_scan_port.return_value = None

    await run_scan("127.0.0.1", start_port=-50, end_port=99999)

    # Max range allowed by clamp is 1 to 65535 (total 65535 calls)
    assert mock_scan_port.call_count == 65535
