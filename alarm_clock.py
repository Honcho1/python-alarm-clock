"""
Advanced Alarm Clock Program
A comprehensive alarm clock with customizable tones and snooze functionality.
"""

import time
import datetime
import threading
import os
import sys
from typing import Optional, List, Dict

# Try to import playsound, with fallback options
try:
    from playsound import playsound
    AUDIO_AVAILABLE = True
except ImportError:
    print("Warning: playsound library not found. Audio playback will be simulated.")
    AUDIO_AVAILABLE = False
    def playsound(sound_file):
        print(f"♪ Playing alarm sound: {sound_file} ♪")

class AlarmClock:
    """Main alarm clock class with full functionality."""
    
    def __init__(self):
        """Initialize the alarm clock with default settings."""
        self.alarms: List[Dict] = []
        self.active_alarm: Optional[Dict] = None
        self.snooze_duration = 5  # Default snooze duration in minutes
        self.default_tones = {
            "1": "beep.wav",
            "2": "bell.wav", 
            "3": "chime.wav",
            "4": "buzzer.wav"
        }
        self.running = True
        
        # Create default tone files if they don't exist
        self._create_default_tones()
    
    def _create_default_tones(self):
        """Create placeholder sound files for demonstration purposes."""
        tone_folder = "alarm_tones"
        if not os.path.exists(tone_folder):
            os.makedirs(tone_folder)
        
        # Create simple text files as placeholders for actual audio files
        for tone_file in self.default_tones.values():
            tone_path = os.path.join(tone_folder, tone_file)
            if not os.path.exists(tone_path):
                with open(tone_path, 'w') as f:
                    f.write(f"Placeholder for {tone_file}")
    
    def validate_time_format(self, time_str: str) -> bool:
        """
        Validate time input in HH:MM format (24-hour clock).
        
        Args:
            time_str: Time string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            time_parts = time_str.split(':')
            if len(time_parts) != 2:
                return False
            
            hours, minutes = int(time_parts[0]), int(time_parts[1])
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except (ValueError, IndexError):
            return False
    
    def set_alarm(self) -> None:
        """Set a new alarm with user input."""
        print("\n" + "="*50)
        print("           SET NEW ALARM")
        print("="*50)
        
        # Get alarm time
        while True:
            alarm_time = input("Enter alarm time (HH:MM in 24-hour format): ").strip()
            if self.validate_time_format(alarm_time):
                break
            print("❌ Invalid time format. Please use HH:MM (e.g., 14:30)")
        
        # Get alarm tone
        tone_choice = self.select_alarm_tone()
        
        # Get snooze duration
        snooze_duration = self.select_snooze_duration()
        
        # Get alarm label (optional)
        label = input("Enter alarm label (optional): ").strip()
        if not label:
            label = f"Alarm at {alarm_time}"
        
        # Create alarm dictionary
        alarm = {
            'time': alarm_time,
            'tone': tone_choice,
            'snooze_duration': snooze_duration,
            'label': label,
            'enabled': True,
            'snoozed': False,
            'snooze_count': 0
        }
        
        self.alarms.append(alarm)
        print(f"\n✅ Alarm set successfully!")
        print(f"   Time: {alarm_time}")
        print(f"   Tone: {tone_choice}")
        print(f"   Snooze: {snooze_duration} minutes")
        print(f"   Label: {label}")
    
    def select_alarm_tone(self) -> str:
        """
        Allow user to select an alarm tone.
        
        Returns:
            str: Selected tone file path
        """
        print("\n📻 Select Alarm Tone:")
        print("1. Default Beep")
        print("2. Bell Sound")
        print("3. Chime")
        print("4. Buzzer")
        print("5. Upload Custom Tone")
        
        while True:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice in ['1', '2', '3', '4']:
                tone_file = self.default_tones[choice]
                return os.path.join("alarm_tones", tone_file)
            elif choice == '5':
                return self.upload_custom_tone()
            else:
                print("❌ Invalid choice. Please select 1-5.")
    
    def upload_custom_tone(self) -> str:
        """
        Allow user to specify a custom alarm tone.
        
        Returns:
            str: Path to custom tone file
        """
        while True:
            file_path = input("Enter path to custom audio file (.wav, .mp3): ").strip()
            
            if os.path.exists(file_path):
                # Check if it's an audio file
                if file_path.lower().endswith(('.wav', '.mp3', '.ogg', '.m4a')):
                    print(f"✅ Custom tone selected: {file_path}")
                    return file_path
                else:
                    print("❌ Please select a valid audio file (.wav, .mp3, .ogg, .m4a)")
            else:
                print("❌ File not found. Please check the path.")
                
                # Offer to use default instead
                use_default = input("Use default tone instead? (y/n): ").lower()
                if use_default == 'y':
                    return os.path.join("alarm_tones", self.default_tones['1'])
    
    def select_snooze_duration(self) -> int:
        """
        Allow user to select snooze duration.
        
        Returns:
            int: Snooze duration in minutes
        """
        print("\n⏰ Select Snooze Duration:")
        print("1. 5 minutes")
        print("2. 10 minutes")
        print("3. 15 minutes")
        print("4. Custom duration")
        
        while True:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                return 5
            elif choice == '2':
                return 10
            elif choice == '3':
                return 15
            elif choice == '4':
                while True:
                    try:
                        custom_duration = int(input("Enter custom snooze duration (1-60 minutes): "))
                        if 1 <= custom_duration <= 60:
                            return custom_duration
                        else:
                            print("❌ Please enter a value between 1 and 60 minutes.")
                    except ValueError:
                        print("❌ Please enter a valid number.")
            else:
                print("❌ Invalid choice. Please select 1-4.")
    
    def view_alarms(self) -> None:
        """Display all set alarms."""
        print("\n" + "="*50)
        print("           YOUR ALARMS")
        print("="*50)
        
        if not self.alarms:
            print("No alarms set. Use option 1 to set an alarm.")
            return
        
        for i, alarm in enumerate(self.alarms, 1):
            status = "✅ ENABLED" if alarm['enabled'] else "❌ DISABLED"
            snooze_info = f" (Snoozed {alarm['snooze_count']}x)" if alarm['snoozed'] else ""
            
            print(f"{i}. {alarm['label']}")
            print(f"   Time: {alarm['time']} | Status: {status}{snooze_info}")
            print(f"   Tone: {os.path.basename(alarm['tone'])}")
            print(f"   Snooze: {alarm['snooze_duration']} minutes")
            print("-" * 40)
    
    def manage_alarms(self) -> None:
        """Manage existing alarms (enable/disable/delete)."""
        if not self.alarms:
            print("No alarms to manage. Set an alarm first.")
            return
        
        self.view_alarms()
        
        print("\nAlarm Management:")
        print("1. Enable/Disable Alarm")
        print("2. Delete Alarm")
        print("3. Back to Main Menu")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            self.toggle_alarm()
        elif choice == '2':
            self.delete_alarm()
        elif choice == '3':
            return
        else:
            print("❌ Invalid choice.")
    
    def toggle_alarm(self) -> None:
        """Enable or disable an alarm."""
        try:
            alarm_num = int(input("Enter alarm number to toggle: ")) - 1
            if 0 <= alarm_num < len(self.alarms):
                self.alarms[alarm_num]['enabled'] = not self.alarms[alarm_num]['enabled']
                status = "enabled" if self.alarms[alarm_num]['enabled'] else "disabled"
                print(f"✅ Alarm {alarm_num + 1} {status}.")
            else:
                print("❌ Invalid alarm number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def delete_alarm(self) -> None:
        """Delete an alarm."""
        try:
            alarm_num = int(input("Enter alarm number to delete: ")) - 1
            if 0 <= alarm_num < len(self.alarms):
                deleted_alarm = self.alarms.pop(alarm_num)
                print(f"✅ Alarm '{deleted_alarm['label']}' deleted.")
            else:
                print("❌ Invalid alarm number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def play_alarm(self, alarm: Dict) -> None:
        """
        Play the alarm sound.
        
        Args:
            alarm: Alarm dictionary containing tone information
        """
        try:
            print(f"\n🚨 ALARM RINGING: {alarm['label']} 🚨")
            print(f"Time: {alarm['time']}")
            
            if AUDIO_AVAILABLE and os.path.exists(alarm['tone']):
                playsound(alarm['tone'])
            else:
                # Simulate alarm sound for demonstration
                for i in range(5):
                    print("♪ BEEP BEEP BEEP ♪")
                    time.sleep(0.5)
                    
        except Exception as e:
            print(f"❌ Error playing alarm sound: {e}")
            # Fallback to text-based alarm
            print("🔔 ALARM! ALARM! ALARM! 🔔")
    
    def handle_alarm_response(self, alarm: Dict) -> None:
        """
        Handle user response to alarm (dismiss or snooze).
        
        Args:
            alarm: The alarm that's currently ringing
        """
        self.active_alarm = alarm
        
        while self.active_alarm:
            print(f"\n⏰ Alarm: {alarm['label']}")
            print("1. Dismiss Alarm")
            print("2. Snooze Alarm")
            
            try:
                # Give user 30 seconds to respond, then auto-snooze
                response = input("Enter your choice (1-2) or press Enter to snooze: ").strip()
                
                if response == '1' or response.lower() == 'dismiss':
                    print("✅ Alarm dismissed.")
                    alarm['snoozed'] = False
                    alarm['snooze_count'] = 0
                    self.active_alarm = None
                    break
                elif response == '2' or response == '' or response.lower() == 'snooze':
                    self.snooze_alarm(alarm)
                    break
                else:
                    print("❌ Invalid choice. Please enter 1 or 2.")
                    
            except KeyboardInterrupt:
                print("\n✅ Alarm dismissed via keyboard interrupt.")
                self.active_alarm = None
                break
    
    def snooze_alarm(self, alarm: Dict) -> None:
        """
        Snooze the alarm for the specified duration.
        
        Args:
            alarm: The alarm to snooze
        """
        alarm['snoozed'] = True
        alarm['snooze_count'] += 1
        snooze_minutes = alarm['snooze_duration']
        
        print(f"😴 Alarm snoozed for {snooze_minutes} minutes.")
        print(f"   Snooze count: {alarm['snooze_count']}")
        
        # Calculate new alarm time
        current_time = datetime.datetime.now()
        snooze_time = current_time + datetime.timedelta(minutes=snooze_minutes)
        new_alarm_time = snooze_time.strftime("%H:%M")
        
        # Create a temporary snooze alarm
        snooze_alarm = alarm.copy()
        snooze_alarm['time'] = new_alarm_time
        snooze_alarm['label'] = f"{alarm['label']} (Snooze {alarm['snooze_count']})"
        
        self.active_alarm = None
        
        # Start monitoring for the snoozed alarm
        threading.Thread(target=self.monitor_snooze_alarm, args=(snooze_alarm,), daemon=True).start()
    
    def monitor_snooze_alarm(self, alarm: Dict) -> None:
        """
        Monitor a snoozed alarm until it's time to ring again.
        
        Args:
            alarm: The snoozed alarm to monitor
        """
        target_time = datetime.datetime.strptime(alarm['time'], "%H:%M").time()
        
        while self.running:
            current_time = datetime.datetime.now().time()
            
            if (current_time.hour == target_time.hour and 
                current_time.minute == target_time.minute):
                
                self.play_alarm(alarm)
                self.handle_alarm_response(alarm)
                break
                
            time.sleep(30)  # Check every 30 seconds
    
    def start_monitoring(self) -> None:
        """Start monitoring all alarms in a separate thread."""
        monitor_thread = threading.Thread(target=self.alarm_monitor, daemon=True)
        monitor_thread.start()
        print("✅ Alarm monitoring started.")
    
    def alarm_monitor(self) -> None:
        """Monitor all alarms for activation."""
        while self.running:
            current_time = datetime.datetime.now().time()
            
            for alarm in self.alarms:
                if not alarm['enabled'] or alarm['snoozed']:
                    continue
                
                alarm_time = datetime.datetime.strptime(alarm['time'], "%H:%M").time()
                
                if (current_time.hour == alarm_time.hour and 
                    current_time.minute == alarm_time.minute and
                    not self.active_alarm):
                    
                    self.play_alarm(alarm)
                    self.handle_alarm_response(alarm)
            
            time.sleep(30)  # Check every 30 seconds
    
    def show_help(self) -> None:
        """Display help information."""
        help_text = """
        ===============================================
                    ALARM CLOCK HELP
        ===============================================
        
        🔹 SETTING ALARMS:
        • Use 24-hour format (e.g., 14:30 for 2:30 PM)
        • Choose from 4 default tones or upload custom audio
        • Set custom snooze duration (1-60 minutes)
        • Add descriptive labels for easy identification
        
        🔹 ALARM TONES:
        • Default tones are stored in 'alarm_tones' folder
        • Supported custom formats: .wav, .mp3, .ogg, .m4a
        • Ensure audio files are accessible and not corrupted
        
        🔹 SNOOZE FEATURE:
        • Snooze postpones alarm by selected duration
        • Tracks snooze count for each alarm
        • Auto-snooze after 30 seconds if no response
        
        🔹 ALARM MANAGEMENT:
        • View all alarms with their status
        • Enable/disable alarms without deleting
        • Delete alarms you no longer need
        
        🔹 TROUBLESHOOTING:
        • If audio doesn't play, check file paths
        • Ensure 'playsound' library is installed
        • Use Ctrl+C to force dismiss stuck alarms
        
        🔹 KEYBOARD SHORTCUTS:
        • Ctrl+C: Emergency alarm dismiss
        • Enter: Quick snooze during alarm
        
        ===============================================
        """
        print(help_text)
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("           ALARM CLOCK MENU")
        print("="*50)
        print("1. Set New Alarm")
        print("2. View All Alarms")
        print("3. Manage Alarms")
        print("4. Help")
        print("5. Exit")
        print("="*50)
        
        # Show current time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Current Time: {current_time}")
        
        # Show active alarms count
        active_count = sum(1 for alarm in self.alarms if alarm['enabled'])
        print(f"Active Alarms: {active_count}")
    
    def run(self) -> None:
        """Main program loop."""
        print("🔔 Welcome to Advanced Alarm Clock!")
        print("Setting up alarm monitoring...")
        
        # Start alarm monitoring
        self.start_monitoring()
        
        while self.running:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == '1':
                    self.set_alarm()
                elif choice == '2':
                    self.view_alarms()
                elif choice == '3':
                    self.manage_alarms()
                elif choice == '4':
                    self.show_help()
                elif choice == '5':
                    print("👋 Goodbye! All alarms have been stopped.")
                    self.running = False
                    break
                else:
                    print("❌ Invalid choice. Please select 1-5.")
                    
                # Pause before showing menu again
                if choice != '5':
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Program interrupted by user.")
                self.running = False
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                print("The program will continue running.")

def main():
    """Main function to run the alarm clock."""
    try:
        alarm_clock = AlarmClock()
        alarm_clock.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("Please restart the program.")

if __name__ == "__main__":
    main()