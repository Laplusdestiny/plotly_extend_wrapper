# plotly_extend_wrapper

Extended Python library for Plotly

You can make plot simply

## Requirement

- Python >= 3.7
- Plotly >= 5.0.0
- kaleido = 0.2.1
- pandas >= 1.1.5

## Graph

- Pie(wrapper.Plot_pie)
- Sunburst(wrapper.Plot_sunburst)
- Bubble(wrapper.Plot_bubble_chart)
- Line with secondary y-axis(wrapper.Plot_line)
- Bubble with linear line(wrapper.Plot_bubble_with_line)

## Common function

- updater
  - Add options
  - Available options
    - x-axis title
    - y-axis title
    - secondary_y-axis title
    - show legend
    - height
    - width
    - marker size
- common
  - check_directory
    - Check directory with pathlib
    - Make directory if parent directory doesn't exist