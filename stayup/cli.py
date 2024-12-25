import argparse
import subprocess
import pyautogui
from .core import KeepAwake

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='''Keep system awake by simulating small mouse movements.
        
Examples:
    # Run with default settings (5 minute intervals)
    stayup
    
    # Run for 2 hours
    stayup --run-for 120
    
    # Run until a specific command completes
    stayup --wait-cmd "pip install large-package"
    
    # Move mouse every 2 minutes with 0.2s movement duration
    stayup --interval 120 --duration-movement 0.2
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--run-for',
        type=float,
        help='Run the script for specified number of minutes'
    )
    group.add_argument(
        '--wait-cmd',
        type=str,
        help='Run until the specified command completes'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Interval between mouse movements in seconds (default: 60)'
    )
    parser.add_argument(
        '--duration-movement',
        type=float,
        default=0.1,
        help='Duration of mouse movement in seconds (default: 0.1)'
    )
    parser.add_argument(
        '--disable-failsafe',
        action='store_true',
        help='Disable the failsafe feature (moving mouse to corner won\'t stop the script)'
    )
    parser.add_argument(
        '--movement-distance',
        type=int,
        default=1,
        help='Distance in pixels for mouse movement (default: 1)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Reduce output verbosity'
    )
    
    return parser.parse_args()

def run_command(cmd):
    """Run a command and return its exit code"""
    try:
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
        return process.returncode
    except Exception as e:
        print(f"Error running command: {e}")
        return 1

def main():
    try:
        args = parse_arguments()
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = not args.disable_failsafe
        
        keep_awake = KeepAwake(
            interval=args.interval,
            duration=args.duration_movement,
            movement_distance=args.movement_distance,
            quiet=args.quiet
        )
        
        if args.run_for:
            keep_awake.set_duration(args.run_for)
            keep_awake.run()
        elif args.wait_cmd:
            if not args.quiet:
                print(f"Running command: {args.wait_cmd}")
            exit_code = run_command(args.wait_cmd)
            if not args.quiet:
                print(f"Command completed with exit code: {exit_code}")
        else:
            keep_awake.run()
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()
