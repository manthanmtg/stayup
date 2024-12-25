import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import signal
import pyautogui
from stayup.core import KeepAwake, format_duration

@pytest.fixture
def keep_awake():
    return KeepAwake(interval=5, duration=0.1, movement_distance=1, quiet=True)

def test_format_duration():
    """Test the format_duration utility function"""
    assert format_duration(3600) == "1:00:00"
    assert format_duration(3661) == "1:01:01"
    assert format_duration(60) == "0:01:00"

def test_init_default_values(keep_awake):
    """Test initialization with default values"""
    assert keep_awake.interval == 5
    assert keep_awake.duration == 0.1
    assert keep_awake.movement_distance == 1
    assert keep_awake.quiet is True
    assert keep_awake.running is True
    assert isinstance(keep_awake.start_time, datetime)
    assert keep_awake.end_time is None

@patch('signal.signal')
def test_signal_handlers(mock_signal):
    """Test that signal handlers are properly set"""
    keep_awake = KeepAwake()
    mock_signal.assert_any_call(signal.SIGINT, keep_awake.handle_shutdown)
    mock_signal.assert_any_call(signal.SIGTERM, keep_awake.handle_shutdown)

def test_handle_shutdown(keep_awake):
    """Test shutdown handler"""
    keep_awake.handle_shutdown(None, None)
    assert keep_awake.running is False

@patch('pyautogui.size')
@patch('pyautogui.position')
def test_get_safe_movement_center(mock_position, mock_size, keep_awake):
    """Test safe movement calculation when mouse is in center"""
    mock_size.return_value = (1000, 1000)
    mock_position.return_value = (500, 500)
    
    movement = keep_awake.get_safe_movement()
    assert movement == (1, 0)  # Default movement

@patch('pyautogui.size')
@patch('pyautogui.position')
def test_get_safe_movement_edges(mock_position, mock_size, keep_awake):
    """Test safe movement calculation near screen edges"""
    mock_size.return_value = (1000, 1000)
    
    # Test left edge
    mock_position.return_value = (5, 500)
    assert keep_awake.get_safe_movement() == (1, 0)
    
    # Test right edge
    mock_position.return_value = (995, 500)
    assert keep_awake.get_safe_movement() == (-1, 0)
    
    # Test top edge
    mock_position.return_value = (500, 5)
    assert keep_awake.get_safe_movement() == (0, 1)
    
    # Test bottom edge
    mock_position.return_value = (500, 995)
    assert keep_awake.get_safe_movement() == (0, -1)

@patch('pyautogui.moveRel')
def test_move_mouse(mock_moveRel, keep_awake):
    """Test mouse movement execution"""
    keep_awake.move_mouse()
    assert mock_moveRel.call_count == 2  # Move and move back

@patch('pyautogui.moveRel')
def test_move_mouse_error_handling(mock_moveRel, keep_awake):
    """Test error handling during mouse movement"""
    mock_moveRel.side_effect = Exception("Test error")
    keep_awake.move_mouse()  # Should not raise exception

def test_should_continue(keep_awake):
    """Test continuation logic"""
    assert keep_awake.should_continue() is True
    
    # Test with end time in future
    keep_awake.end_time = datetime.now() + timedelta(minutes=1)
    assert keep_awake.should_continue() is True
    
    # Test with end time in past
    keep_awake.end_time = datetime.now() - timedelta(minutes=1)
    assert keep_awake.should_continue() is False
    
    # Test when not running
    keep_awake.running = False
    assert keep_awake.should_continue() is False

def test_set_duration(keep_awake):
    """Test duration setting"""
    keep_awake.set_duration(60)
    assert isinstance(keep_awake.end_time, datetime)
    expected_end = keep_awake.start_time + timedelta(minutes=60)
    assert abs((keep_awake.end_time - expected_end).total_seconds()) < 1

@patch('time.time')
@patch('time.sleep')
def test_run_loop(mock_sleep, mock_time, keep_awake):
    """Test main run loop"""
    # Set up time.time() to simulate time passing
    # First call is for sleep_start, subsequent calls are for the while loop check
    mock_time.side_effect = [
        0,      # Initial sleep_start
        0.5,    # First while loop check
        1,      # Second while loop check
        5,      # Third while loop check (exceeds interval)
    ]
    
    # Set up to run for one iteration by setting end_time in the future
    keep_awake.end_time = datetime.now() + timedelta(seconds=10)
    keep_awake.interval = 5  # Set interval to 5 seconds
    
    # Mock should_continue to return True once then False to exit the loop
    original_should_continue = keep_awake.should_continue
    call_count = 0
    def mock_should_continue():
        nonlocal call_count
        call_count += 1
        if call_count <= 2:  # Allow two calls (one for main loop, one for sleep loop)
            return True
        return False
    keep_awake.should_continue = mock_should_continue
    
    try:
        keep_awake.run()
    finally:
        # Restore original method
        keep_awake.should_continue = original_should_continue
    
    # Should have attempted to sleep at least once
    mock_sleep.assert_called_with(1)
