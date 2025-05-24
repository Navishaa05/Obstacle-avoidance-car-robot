import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read data from Excel
file_path = 'Delay_vs_Dist.xlsx'  # Replace with your Excel file path
data = pd.read_excel(file_path)

# Extract data
delays = data['Delay (ms)'].values
distances = data['Distance (cm)'].values

# Perform linear regression
coefficients = np.polyfit(delays, distances, 1)  # Linear fit (degree 1)
line_fit = np.poly1d(coefficients)  # Generate the polynomial function
line_distances = line_fit(delays)   # Generate line values

# Plot the data and the best-fit line
plt.figure(figsize=(8, 6))
plt.plot(delays, distances, 'bo-', label='Original Data')  # Original data
plt.plot(delays, line_distances, 'r--', label=f'Best-Fit Line: y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}')  # Fitted line

# Add labels, title, and legend
plt.title('Distance vs Delay with Best-Fit Line', fontsize=14)
plt.xlabel('Delay (ms)', fontsize=12)
plt.ylabel('Distance (cm)', fontsize=12)
plt.grid(True)
plt.legend(fontsize=12)
plt.tight_layout()

# Show the plot
plt.show()
