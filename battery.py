import numpy as np
from scipy.integrate import ode
from powertrain_components import EnergySource

class Battery(EnergySource):
    """
    A detailed battery model based on the concepts from "Battery Knockdown Factors for Conceptual Design"
    by Robert A. McDonald.

    This model captures the non-linear behavior of battery voltage and resistance with respect to
    depth of discharge (DOD), as well as the effects of capacity fade and resistance growth over time.

    Attributes:
        cell_config (dict): Configuration parameters for a single cell.
        num_cells_series (int): Number of cells in series.
        num_cells_parallel (int): Number of cells in parallel.
        Q (float): Pack capacity in Amp-hours.
        Vcharge (float): Pack charge voltage in Volts.
        Vcutoff (float): Pack cutoff voltage in Volts.
        Irated (float): Pack rated current in Amps.
        k_Q (float): Capacity fade parameter.
        k_R (float): Resistance growth parameter.
        dod (float): Current depth of discharge.
    """

    def __init__(self, cell_config, num_cells_series, num_cells_parallel):
        """
        Initialize the battery pack with the given cell configuration and pack layout.

        Args:
            cell_config (dict): Configuration parameters for a single cell.
            num_cells_series (int): Number of cells in series.
            num_cells_parallel (int): Number of cells in parallel.
        """
        self.cell_config = cell_config
        self.num_cells_series = num_cells_series
        self.num_cells_parallel = num_cells_parallel
        self.initialize()

    def initialize(self):
        """Initialize battery parameters based on the cell configuration and pack layout."""
        self.Q = self.cell_config['Q'] * self.num_cells_parallel  # Pack capacity (Ah)
        self.Vcharge = self.cell_config['Vcharge'] * self.num_cells_series  # Pack charge voltage (V)
        self.Vcutoff = self.cell_config['Vcutoff'] * self.num_cells_series  # Pack cutoff voltage (V)
        self.Irated = self.cell_config['Irated'] * self.num_cells_parallel  # Pack rated current (A)
        self.k_Q = 1.0  # Capacity fade parameter
        self.k_R = 1.0  # Resistance growth parameter
        self.dod = 0.0  # Initial depth of discharge

    def OCV(self, dod):
        """
        Calculate the Open Circuit Voltage (OCV) as a function of Depth of Discharge (DOD).

        This function implements the OCV curve fit from the paper, scaled to the pack voltage.

        Args:
            dod (float): Depth of Discharge, between 0 and 1.

        Returns:
            float: Open Circuit Voltage of the battery pack.
        """
        return self.num_cells_series * (
            self.cell_config['Vlin0'] + 
            self.cell_config['K'] * dod + 
            self.cell_config['A'] * np.exp(-self.cell_config['B'] * dod) + 
            self.cell_config['E'] * np.sin(self.cell_config['F'] * dod - self.cell_config['G']) * 
            np.exp(-self.cell_config['H'] * dod) + 
            self.cell_config['D'] * (dod / (self.cell_config['C'] + 1.0 - dod))
        )

    def Rss(self, dod):
        """
        Calculate the series resistance as a function of Depth of Discharge (DOD).

        This function implements the resistance model from the paper, scaled to the pack configuration.

        Args:
            dod (float): Depth of Discharge, between 0 and 1.

        Returns:
            float: Series resistance of the battery pack.
        """
        return (self.k_R * (
            self.cell_config['R0'] + 
            self.cell_config['Rslope'] * dod + 
            self.cell_config['RA'] * np.exp(-self.cell_config['RB'] * (1.0 - dod))
        ) * self.num_cells_series / self.num_cells_parallel)

    def V(self, dod, I):
        """
        Calculate the terminal voltage as a function of Depth of Discharge (DOD) and current.

        Args:
            dod (float): Depth of Discharge, between 0 and 1.
            I (float): Current draw from the battery, positive for discharge.

        Returns:
            float: Terminal voltage of the battery pack.
        """
        return self.OCV(dod) - self.Rss(dod) * I

    def update(self, t, I):
        """
        Update the battery state based on the time step and current draw.

        Args:
            t (float): Time step in seconds.
            I (float): Current draw from the battery, positive for discharge.
        """
        dod_rate = I / (self.k_Q * self.Q * 3600)  # DOD change rate
        self.dod += dod_rate * t
        self.dod = np.clip(self.dod, 0, 1)  # Ensure DOD stays between 0 and 1

    def get_output(self):
        """
        Get the current output voltage and current of the battery.

        Returns:
            tuple: (voltage, current) at the current state.
        """
        return self.V(self.dod, self.Irated), self.Irated

    def get_energy_remaining(self):
        """
        Calculate the remaining energy in the battery.

        Returns:
            float: Remaining energy in Watt-hours.
        """
        return (1 - self.dod) * self.Q * self.Vcharge

    def get_power_available(self):
        """
        Calculate the available power from the battery.

        Returns:
            float: Available power in Watts.
        """
        V, I = self.get_output()
        return V * I

    def set_aging_parameters(self, k_Q, k_R):
        """
        Set the aging parameters for the battery.

        Args:
            k_Q (float): Capacity fade parameter.
            k_R (float): Resistance growth parameter.
        """
        self.k_Q = k_Q
        self.k_R = k_R

    def get_state(self):
        """
        Get the current state of the battery.

        Returns:
            dict: Current state including voltage, current, and DOD.
        """
        V, I = self.get_output()
        return {
            'voltage': V,
            'current': I,
            'dod': self.dod,
            'energy_remaining': self.get_energy_remaining(),
            'power_available': self.get_power_available()
        }