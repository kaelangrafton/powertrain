import os
import matplotlib.pyplot as plt
from pylatex import Document, Section, Subsection, Command, Figure, Tabular
from pylatex.utils import NoEscape
from main import main

def generate_report():
    data = main()  # Run the main script and get the data

    # Create a new LaTeX document
    doc = Document('report')
    doc.preamble.append(Command('title', 'Powertrain Analysis Report'))
    doc.preamble.append(Command('author', 'Your Name'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    # Add a section for Inputs
    with doc.create(Section('Inputs')):
        with doc.create(Tabular('l l')) as table:
            table.add_row("Battery Mass", f"{data['battery'].mass} kg")
            table.add_row("Specific Energy", f"{data['battery'].specific_energy} Wh/kg")
            table.add_row("Motor Power", f"{data['motor'].motor_power} W")
            table.add_row("Propeller Diameter", f"{data['propeller'].propeller_diameter} m")
            table.add_row("Hub Diameter", f"{data['propeller'].hub_diameter} m")
            table.add_row("Diffuser Expansion Ratio", f"{data['propeller'].diffuser_expansion_ratio}")

    # Add a section for Outputs
    with doc.create(Section('Outputs')):
        with doc.create(Tabular('l l')) as table:
            table.add_row("Total Runtime", f"{data['train'].runtime} hours")
            thrust = data['propeller'].static_thrust(data['motor'])
            table.add_row("Static Thrust", f"{thrust/9.81} kgf")
            table.add_row("Net Thrust", f"{data['train'].net_thrust/9.81} kgf")  # Access net thrust from train object

    # Add a section for Plots
    with doc.create(Section('Plots')):
        with doc.create(Subsection('Battery Capacity vs Time')):
            # Generate the plot
            plt.figure(figsize=(10, 6))
            times = data['train'].get_time_history()
            capacities = data['train'].capacity_history
            plt.plot(times, capacities, '-o', label='Battery Capacity')
            plt.title('Battery Capacity vs Time')
            plt.xlabel('Time (hours)')
            plt.ylabel('Battery Capacity (Wh)')
            plt.legend()
            plt.grid(True)
            plt.savefig('plot.png')

            # Add the plot to the LaTeX document
            with doc.create(Figure(position='h!')) as plot:
                plot.add_image('plot.png', width=NoEscape(r'0.8\textwidth'))
                plot.add_caption('Battery capacity over time.')
    

    # Insert a new page command
    doc.append(NoEscape(r'\newpage'))

    # Add an appendix for the class diagram
    with doc.create(Section('Appendix: Class Structure', numbering=False)):
        with doc.create(Figure(position='h!')) as diagram:
            diagram.add_image('class_diagram.png', width=NoEscape(r'0.8\textwidth'))
            diagram.add_caption('Class structure and relationships.')


    # Generate the LaTeX document
    doc.generate_pdf(clean_tex=True)

if __name__ == "__main__":
    generate_report()
    os.remove("plot.png")  # Clean up the plot image
