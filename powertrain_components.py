from abc import ABC, abstractmethod

class PowertrainComponent(ABC):
    """
    Abstract base class for all powertrain components.
    
    This class defines the common interface that all powertrain components must implement.
    """
    
    @abstractmethod
    def initialize(self):
        """Initialize component parameters."""
        pass
    
    @abstractmethod
    def update(self, t, *args):
        """
        Update component state.
        
        Args:
            t (float): Time step.
            *args: Additional arguments specific to the component.
        """
        pass
    
    @abstractmethod
    def get_output(self):
        """
        Get component output.
        
        Returns:
            The output of the component, which may vary depending on the specific component.
        """
        pass

class EnergySource(PowertrainComponent):
    """
    Abstract base class for energy sources (e.g., batteries, fuel tanks).
    
    This class extends PowertrainComponent with methods specific to energy sources.
    """
    
    @abstractmethod
    def get_energy_remaining(self):
        """
        Get remaining energy in the source.
        
        Returns:
            float: Remaining energy in the appropriate units (e.g., Wh for batteries, kg for fuel).
        """
        pass
    
    @abstractmethod
    def get_power_available(self):
        """
        Get available power from the source.
        
        Returns:
            float: Available power in Watts.
        """
        pass

class PowerConverter(PowertrainComponent):
    """
    Abstract base class for power converters (e.g., electric motors, engines).
    
    This class extends PowertrainComponent with methods specific to power converters.
    """
    
    @abstractmethod
    def get_efficiency(self):
        """
        Get current efficiency of the converter.
        
        Returns:
            float: Efficiency as a value between 0 and 1.
        """
        pass
    
    @abstractmethod
    def get_power_output(self):
        """
        Get current power output of the converter.
        
        Returns:
            float: Power output in Watts.
        """
        pass

class Propulsor(PowertrainComponent):
    """
    Abstract base class for propulsors (e.g., ducted fans, propellers).
    
    This class extends PowertrainComponent with methods specific to propulsors.
    """
    
    @abstractmethod
    def get_thrust(self):
        """
        Get current thrust output.
        
        Returns:
            float: Thrust in Newtons.
        """
        pass
    
    @abstractmethod
    def get_power_required(self):
        """
        Get current power required.
        
        Returns:
            float: Power required in Watts.
        """
        pass