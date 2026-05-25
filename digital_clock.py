#!/usr/bin/env python3
"""Digital Clock - Displays current time in multiple time zones"""

import tkinter as tk
from tkinter import font
from datetime import datetime
import pytz
from typing import List, Tuple


class DigitalClock:
    """A digital clock displaying time in multiple time zones."""

    def __init__(self, root, time_zones: List[str] = None):
        """Initialize the digital clock.
        
        Args:
            root: Tkinter root window
            time_zones: List of timezone strings (e.g., ['UTC', 'US/Eastern', 'Europe/Berlin'])
        """
        self.root = root
        self.root.title("Digital Clock - Multiple Time Zones")
        self.root.geometry("800x400")
        self.root.configure(bg='#1a1a1a')
        
        # Default time zones if none provided
        self.time_zones = time_zones or [
            'UTC',
            'US/Eastern',
            'Europe/Berlin',
            'Asia/Tokyo',
            'Australia/Sydney',
            'US/Pacific'
        ]
        
        # Configure fonts
        self.title_font = font.Font(family='Courier New', size=14, weight='bold')
        self.time_font = font.Font(family='Courier New', size=48, weight='bold')
        self.zone_font = font.Font(family='Courier New', size=12)
        
        self.setup_ui()
        self.update_clock()

    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(
            main_frame,
            text="⏰ Digital Clock - Multiple Time Zones",
            font=self.title_font,
            bg='#1a1a1a',
            fg='#00ff00'
        )
        title.pack(pady=20)
        
        # Create a frame for each timezone
        self.clock_frames = {}
        self.time_labels = {}
        self.zone_labels = {}
        
        # Create 2 rows, 3 columns grid
        clock_container = tk.Frame(main_frame, bg='#1a1a1a')
        clock_container.pack(fill=tk.BOTH, expand=True)
        
        for idx, timezone in enumerate(self.time_zones):
            # Calculate grid position
            row = idx // 3
            col = idx % 3
            
            # Create frame for this timezone
            tz_frame = tk.Frame(
                clock_container,
                bg='#2a2a2a',
                relief=tk.RAISED,
                bd=2
            )
            tz_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Configure grid weights
            clock_container.grid_rowconfigure(row, weight=1)
            clock_container.grid_columnconfigure(col, weight=1)
            
            # Timezone name
            zone_label = tk.Label(
                tz_frame,
                text=timezone,
                font=self.zone_font,
                bg='#2a2a2a',
                fg='#ffaa00'
            )
            zone_label.pack(pady=10)
            
            # Time display
            time_label = tk.Label(
                tz_frame,
                text='--:--:--',
                font=self.time_font,
                bg='#2a2a2a',
                fg='#00ff00'
            )
            time_label.pack(pady=20)
            
            self.clock_frames[timezone] = tz_frame
            self.time_labels[timezone] = time_label
            self.zone_labels[timezone] = zone_label
        
        # Footer with current local time
        footer_frame = tk.Frame(main_frame, bg='#1a1a1a')
        footer_frame.pack(pady=20)
        
        self.local_time_label = tk.Label(
            footer_frame,
            text='Local Time: ',
            font=self.zone_font,
            bg='#1a1a1a',
            fg='#0088ff'
        )
        self.local_time_label.pack()

    def update_clock(self):
        """Update all clock displays."""
        # Get current UTC time
        now = datetime.now(pytz.UTC)
        
        # Update each timezone
        for timezone in self.time_zones:
            try:
                # Convert to timezone
                tz = pytz.timezone(timezone)
                local_time = now.astimezone(tz)
                
                # Format time
                time_str = local_time.strftime('%H:%M:%S')
                date_str = local_time.strftime('%Y-%m-%d')
                
                # Update label
                self.time_labels[timezone].config(text=time_str)
                
                # Update zone label with date
                self.zone_labels[timezone].config(
                    text=f"{timezone}\n{date_str}"
                )
            except Exception as e:
                self.time_labels[timezone].config(text='ERROR')
                print(f"Error updating {timezone}: {e}")
        
        # Update local time
        local_now = datetime.now()
        local_time_str = local_now.strftime('%Y-%m-%d %H:%M:%S')
        self.local_time_label.config(text=f'Local Time: {local_time_str}')
        
        # Schedule next update (every 1000ms = 1 second)
        self.root.after(1000, self.update_clock)

    def add_timezone(self, timezone: str):
        """Add a new timezone to the display.
        
        Args:
            timezone: Timezone string (e.g., 'Europe/Paris')
        """
        if timezone not in self.time_zones:
            self.time_zones.append(timezone)
            print(f"Added timezone: {timezone}")

    def remove_timezone(self, timezone: str):
        """Remove a timezone from the display.
        
        Args:
            timezone: Timezone string to remove
        """
        if timezone in self.time_zones:
            self.time_zones.remove(timezone)
            print(f"Removed timezone: {timezone}")

    def get_available_timezones(self) -> List[str]:
        """Get all available timezones.
        
        Returns:
            List of all available timezone strings
        """
        return sorted(pytz.all_timezones)


class DigitalClockApp:
    """Main application class."""

    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        
        # Custom timezones
        custom_zones = [
            'UTC',
            'US/Eastern',
            'US/Central',
            'US/Mountain',
            'US/Pacific',
            'Europe/London',
            'Europe/Berlin',
            'Europe/Paris',
            'Asia/Tokyo',
            'Asia/Shanghai',
            'Asia/Hong_Kong',
            'Australia/Sydney',
        ]
        
        self.clock = DigitalClock(self.root, custom_zones)

    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = DigitalClockApp()
    app.run()


if __name__ == '__main__':
    main()
