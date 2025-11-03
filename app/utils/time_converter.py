"""
USA Swimming Time Conversion Factors
Based on USA Swimming's official conversion factors
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Tuple
from enum import Enum

class SwimmingCourse(str, Enum):
    SCY = "SCY"  # Short Course Yards (25 yards)
    SCM = "SCM"  # Short Course Meters (25 meters)
    LCM = "LCM"  # Long Course Meters (50 meters)

# USA Swimming Conversion Factors (2024 version)
# Format: (from_course, to_course, event) -> factor
CONVERSION_FACTORS = {
    # LCM to SCY conversions (what Spanish swimmers need most)
    ("LCM", "SCY", "50_free"): 0.8644,
    ("LCM", "SCY", "100_free"): 0.8644,
    ("LCM", "SCY", "200_free"): 0.8644,
    ("LCM", "SCY", "400_free"): 0.8655,  # 500 yards equivalent
    ("LCM", "SCY", "800_free"): 0.8655,  # 1000 yards equivalent
    ("LCM", "SCY", "1500_free"): 0.8658,  # 1650 yards equivalent
    
    ("LCM", "SCY", "50_back"): 0.8560,
    ("LCM", "SCY", "100_back"): 0.8560,
    ("LCM", "SCY", "200_back"): 0.8560,
    
    ("LCM", "SCY", "50_breast"): 0.8496,
    ("LCM", "SCY", "100_breast"): 0.8496,
    ("LCM", "SCY", "200_breast"): 0.8496,
    
    ("LCM", "SCY", "50_fly"): 0.8644,
    ("LCM", "SCY", "100_fly"): 0.8644,
    ("LCM", "SCY", "200_fly"): 0.8644,
    
    ("LCM", "SCY", "200_im"): 0.8560,
    ("LCM", "SCY", "400_im"): 0.8560,
    
    # SCY to LCM conversions (reverse)
    ("SCY", "LCM", "50_free"): 1.1566,
    ("SCY", "LCM", "100_free"): 1.1566,
    ("SCY", "LCM", "200_free"): 1.1566,
    ("SCY", "LCM", "500_free"): 1.1553,  # 400m equivalent
    ("SCY", "LCM", "1000_free"): 1.1553,  # 800m equivalent
    ("SCY", "LCM", "1650_free"): 1.1549,  # 1500m equivalent
    
    ("SCY", "LCM", "50_back"): 1.1682,
    ("SCY", "LCM", "100_back"): 1.1682,
    ("SCY", "LCM", "200_back"): 1.1682,
    
    ("SCY", "LCM", "50_breast"): 1.1773,
    ("SCY", "LCM", "100_breast"): 1.1773,
    ("SCY", "LCM", "200_breast"): 1.1773,
    
    ("SCY", "LCM", "50_fly"): 1.1566,
    ("SCY", "LCM", "100_fly"): 1.1566,
    ("SCY", "LCM", "200_fly"): 1.1566,
    
    ("SCY", "LCM", "200_im"): 1.1682,
    ("SCY", "LCM", "400_im"): 1.1682,
    
    # LCM to SCM conversions
    ("LCM", "SCM", "all"): 1.0,  # Add small factor for turns
    
    # SCM to LCM conversions
    ("SCM", "LCM", "all"): 1.0,  # Add small factor for fewer turns
    
    # SCM to SCY conversions
    ("SCM", "SCY", "50_free"): 0.8712,
    ("SCM", "SCY", "100_free"): 0.8712,
    ("SCM", "SCY", "200_free"): 0.8712,
    ("SCM", "SCY", "400_free"): 0.8712,
    ("SCM", "SCY", "800_free"): 0.8712,
    ("SCM", "SCY", "1500_free"): 0.8712,
    
    # SCY to SCM conversions
    ("SCY", "SCM", "50_free"): 1.1478,
    ("SCY", "SCM", "100_free"): 1.1478,
    ("SCY", "SCM", "200_free"): 1.1478,
    ("SCY", "SCM", "500_free"): 1.1478,
    ("SCY", "SCM", "1000_free"): 1.1478,
    ("SCY", "SCM", "1650_free"): 1.1478,
}

# Event distance mappings
EVENT_MAPPINGS = {
    "400_free": "500_free",  # 400m LCM -> 500y SCY
    "800_free": "1000_free",  # 800m LCM -> 1000y SCY
    "1500_free": "1650_free",  # 1500m LCM -> 1650y SCY
    "500_free": "400_free",  # 500y SCY -> 400m LCM
    "1000_free": "800_free",  # 1000y SCY -> 800m LCM
    "1650_free": "1500_free",  # 1650y SCY -> 1500m LCM
}

# Altitude adjustment factors (for locations like Colorado Springs)
ALTITUDE_FACTORS = {
    "freestyle": 0.985,
    "backstroke": 0.985,
    "breaststroke": 0.988,
    "butterfly": 0.985,
    "im": 0.986
}

class USASwimmingConverter:
    """
    Time converter using USA Swimming's official conversion factors
    """
    
    @staticmethod
    def time_to_seconds(time_str: str) -> float:
        """
        Convert time string (MM:SS.HH or SS.HH) to seconds
        """
        if ':' in time_str:
            parts = time_str.split(':')
            minutes = int(parts[0])
            seconds = float(parts[1])
            return minutes * 60 + seconds
        else:
            return float(time_str)
    
    @staticmethod
    def seconds_to_time(seconds: float) -> str:
        """
        Convert seconds to time string (MM:SS.HH)
        """
        minutes = int(seconds // 60)
        secs = seconds % 60
        
        if minutes > 0:
            return f"{minutes}:{secs:05.2f}"
        else:
            return f"{secs:.2f}"
    
    @staticmethod
    def get_stroke_from_event(event: str) -> str:
        """
        Extract stroke type from event name
        """
        if "free" in event.lower():
            return "freestyle"
        elif "back" in event.lower():
            return "backstroke"
        elif "breast" in event.lower():
            return "breaststroke"
        elif "fly" in event.lower():
            return "butterfly"
        elif "im" in event.lower():
            return "im"
        else:
            return "freestyle"
    
    @classmethod
    def convert_time(
        cls,
        time_input: str,
        event: str,
        from_course: str,
        to_course: str,
        altitude_adjustment: bool = False
    ) -> Dict:
        """
        Convert swimming time using USA Swimming factors
        
        Args:
            time_input: Time as string (e.g., "23.45" or "1:23.45")
            event: Event name (e.g., "100_free", "200_fly")
            from_course: Source course (LCM, SCM, or SCY)
            to_course: Target course (LCM, SCM, or SCY)
            altitude_adjustment: Apply altitude correction
        
        Returns:
            Dictionary with original time, converted time, and metadata
        """
        
        # Convert time to seconds
        time_seconds = cls.time_to_seconds(time_input)
        
        # Handle same course "conversion"
        if from_course == to_course:
            return {
                "original_time": time_input,
                "converted_time": time_input,
                "original_seconds": time_seconds,
                "converted_seconds": time_seconds,
                "factor": 1.0,
                "event": event,
                "from_course": from_course,
                "to_course": to_course,
                "altitude_adjusted": False
            }
        
        # Check for event distance mapping
        mapped_event = event
        if from_course == "LCM" and to_course == "SCY":
            if event in EVENT_MAPPINGS:
                mapped_event = EVENT_MAPPINGS[event]
        elif from_course == "SCY" and to_course == "LCM":
            if event in EVENT_MAPPINGS:
                mapped_event = EVENT_MAPPINGS[event]
        
        # Get conversion factor
        factor_key = (from_course, to_course, event)
        
        # Try specific event factor first
        if factor_key in CONVERSION_FACTORS:
            factor = CONVERSION_FACTORS[factor_key]
        # Try general factor for the course combination
        elif (from_course, to_course, "all") in CONVERSION_FACTORS:
            factor = CONVERSION_FACTORS[(from_course, to_course, "all")]
        else:
            # Calculate composite factor if needed (e.g., SCM -> LCM -> SCY)
            if from_course == "SCM" and to_course == "SCY":
                # Use SCM to SCY directly if available
                factor = CONVERSION_FACTORS.get(
                    (from_course, to_course, event),
                    0.8712  # Default SCM to SCY
                )
            elif from_course == "SCY" and to_course == "SCM":
                factor = CONVERSION_FACTORS.get(
                    (from_course, to_course, event),
                    1.1478  # Default SCY to SCM
                )
            else:
                factor = 1.0
        
        # Apply conversion
        converted_seconds = time_seconds * factor
        
        # Apply altitude adjustment if needed
        altitude_factor_applied = 1.0
        if altitude_adjustment:
            stroke = cls.get_stroke_from_event(event)
            altitude_factor_applied = ALTITUDE_FACTORS.get(stroke, 1.0)
            converted_seconds *= altitude_factor_applied
        
        # Round to hundredths
        converted_seconds = float(
            Decimal(str(converted_seconds)).quantize(
                Decimal('0.01'), 
                rounding=ROUND_HALF_UP
            )
        )
        
        return {
            "original_time": time_input,
            "converted_time": cls.seconds_to_time(converted_seconds),
            "original_seconds": time_seconds,
            "converted_seconds": converted_seconds,
            "factor": factor,
            "event": event,
            "mapped_event": mapped_event,
            "from_course": from_course,
            "to_course": to_course,
            "altitude_adjusted": altitude_adjustment,
            "altitude_factor": altitude_factor_applied if altitude_adjustment else None
        }
    
    @classmethod
    def batch_convert(
        cls,
        times: list,
        from_course: str,
        to_course: str,
        altitude_adjustment: bool = False
    ) -> list:
        """
        Convert multiple times at once
        
        Args:
            times: List of dictionaries with 'time' and 'event' keys
            from_course: Source course
            to_course: Target course
            altitude_adjustment: Apply altitude correction
        
        Returns:
            List of conversion results
        """
        results = []
        for item in times:
            result = cls.convert_time(
                item['time'],
                item['event'],
                from_course,
                to_course,
                altitude_adjustment
            )
            results.append(result)
        return results
    
    @classmethod
    def get_ncaa_standards(cls, event: str, gender: str = "men") -> Dict:
        """
        Get NCAA qualifying standards for an event
        Returns times in SCY format
        """
        # These would be updated annually from NCAA
        # Example standards (2024-2025 season)
        standards = {
            "men": {
                "50_free": {
                    "d1_a": "19.05",
                    "d1_b": "19.85",
                    "d2": "20.29",
                    "d3_a": "20.45",
                    "d3_b": "21.19"
                },
                "100_free": {
                    "d1_a": "42.05",
                    "d1_b": "43.79",
                    "d2": "44.69",
                    "d3_a": "45.09",
                    "d3_b": "46.69"
                },
                # Add all other events...
            },
            "women": {
                "50_free": {
                    "d1_a": "21.73",
                    "d1_b": "22.63",
                    "d2": "23.09",
                    "d3_a": "23.29",
                    "d3_b": "24.19"
                },
                # Add all other events...
            }
        }
        
        return standards.get(gender, {}).get(event, {})