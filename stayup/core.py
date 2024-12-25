import time
import signal
import pyautogui
from datetime import datetime, timedelta

def format_duration(seconds):
    """Format duration in seconds to a readable string"""
    return str(timedelta(seconds=seconds))

class KeepAwake:
    def __init__(self, interval=60, duration=0.1, movement_distance=1, quiet=False):
        self.interval = interval
        self.duration = duration
        self.movement_distance = movement_distance
        self.quiet = quiet
        self.running = True
        self.start_time = datetime.now()
        self.end_time = None
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
    
    def handle_shutdown(self, signum, frame):
        print("\nShutting down gracefully...")
        self.running = False
    
    def get_safe_movement(self):
        """Determine safe movement direction based on current mouse position"""
        screen_width, screen_height = pyautogui.size()
        current_x, current_y = pyautogui.position()
        
        # Define margins for edge detection
        margin = 10
        
        # Check if near edges and determine safe movement direction
        if current_x <= margin:  # Near left edge
            return (self.movement_distance, 0)  # Move right
        elif current_x >= screen_width - margin:  # Near right edge
            return (-self.movement_distance, 0)  # Move left
        elif current_y <= margin:  # Near top edge
            return (0, self.movement_distance)  # Move down
        elif current_y >= screen_height - margin:  # Near bottom edge
            return (0, -self.movement_distance)  # Move up
        else:
            # Default movement pattern (right and back)
            return (self.movement_distance, 0)
    
    def move_mouse(self):
        """Perform a small mouse movement in a safe direction"""
        try:
            # Get safe movement direction
            dx, dy = self.get_safe_movement()
            
            # Move mouse in safe direction and back
            pyautogui.moveRel(dx, dy, duration=self.duration)
            pyautogui.moveRel(-dx, -dy, duration=self.duration)
            
        except Exception as e:
            print(f"\nError moving mouse: {e}")
    
    def should_continue(self):
        """Check if the script should continue running"""
        if not self.running:
            return False
        
        if self.end_time:
            return datetime.now() < self.end_time
            
        return True
    
    def set_duration(self, minutes):
        """Set the total duration to run"""
        if minutes:
            self.end_time = self.start_time + timedelta(minutes=minutes)
            if not self.quiet:
                print(f"Script will run until: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def run(self):
        """Main loop to keep the system awake"""
        if not self.quiet:
            print(f"Starting keep-awake script. Press Ctrl+C to exit.")
            print(f"Moving mouse every {format_duration(self.interval)}")
        
        movements = 0
        while self.should_continue():
            self.move_mouse()
            movements += 1
            
            runtime = datetime.now() - self.start_time
            if not self.quiet:
                remaining = ""
                if self.end_time:
                    remaining = f" | Remaining: {format_duration(int((self.end_time - datetime.now()).total_seconds()))}"
                
                print(f"\rRunning for {format_duration(int(runtime.total_seconds()))} | "
                      f"Movements: {movements}{remaining}", end='', flush=True)
            
            # Sleep in smaller intervals to allow for more responsive shutdown
            sleep_start = time.time()
            while time.time() - sleep_start < self.interval and self.should_continue():
                time.sleep(1)
        
        if not self.quiet:
            print(f"\nScript ran for {format_duration(int(runtime.total_seconds()))} "
                  f"with {movements} mouse movements")
