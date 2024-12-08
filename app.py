import streamlit as st
from decimal import Decimal, ROUND_HALF_UP

def convert_to_feet(value, unit='ft'):
    return value  # All inputs are assumed to be in feet now

def convert_result(value, to_unit):
    # Precise conversion factors
    conversion_factors = {
        'ft': Decimal('1.0'),
        'mm': Decimal('304.8'),  # Exact conversion factor for feet to mm
        'cm': Decimal('30.48')   # Exact conversion factor for feet to cm
    }
    
    # Convert to Decimal for precise calculation
    value = Decimal(str(value))
    result = value * conversion_factors[to_unit]
    # Round to 3 decimal places using ROUND_HALF_UP
    return float(result.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))

def main():
    st.title('Ceiling Rod Calculation')
    
    # Add unit selection at the top
    input_unit = st.selectbox(
        'Input measurements in:', 
        ['ft', 'mm', 'cm'],
        format_func=lambda x: {
            'ft': 'Feet (ft)',
            'mm': 'Millimeters (mm)',
            'cm': 'Centimeters (cm)'
        }[x],
        key="input_unit"
    )
    
    st.write("")  # Add spacing
    
    # Add default values and unique keys to input fields
    col1, col2 = st.columns(2)
    
    with col1:
        length1 = st.number_input(
            f'Length 1 ({input_unit})', 
            value=0.000,
            min_value=0.000,
            step=0.001 if input_unit == 'ft' else 1.0,
            format="%.3f" if input_unit == 'ft' else "%.1f",
            key="length1_input"
        )
        width1 = st.number_input(
            f'Width 1 ({input_unit})', 
            value=0.000,
            min_value=0.000,
            step=0.001 if input_unit == 'ft' else 1.0,
            format="%.3f" if input_unit == 'ft' else "%.1f",
            key="width1_input"
        )
    
    with col2:
        length2 = st.number_input(
            f'Length 2 ({input_unit})', 
            value=0.000,
            min_value=0.000,
            step=0.001 if input_unit == 'ft' else 1.0,
            format="%.3f" if input_unit == 'ft' else "%.1f",
            key="length2_input"
        )
        width2 = st.number_input(
            f'Width 2 ({input_unit})', 
            value=0.000,
            min_value=0.000,
            step=0.001 if input_unit == 'ft' else 1.0,
            format="%.3f" if input_unit == 'ft' else "%.1f",
            key="width2_input"
        )

    # Add some spacing
    st.write("")
    
    # Center the calculate button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        calculate_button = st.button('Calculate', key='calc_button')
    
    if calculate_button:
        try:
            # Convert inputs to feet first if needed
            conversion_to_ft = {
                'ft': 1.0,
                'mm': 0.00328084,
                'cm': 0.0328084
            }
            
            # Convert input values to feet
            conv_factor = conversion_to_ft[input_unit]
            length1_ft = Decimal(str(length1 * conv_factor))
            length2_ft = Decimal(str(length2 * conv_factor))
            width1_ft = Decimal(str(width1 * conv_factor))
            width2_ft = Decimal(str(width2 * conv_factor))
            
            # Calculate in feet using Decimal for precision
            horizontal_rods = max(length1_ft, length2_ft)
            vertical_rods = max(width1_ft, width2_ft)
            
            # Calculate number of rods (integer division)
            num_horizontal_rods = int(horizontal_rods / Decimal('2')) + 1
            num_vertical_rods = int(vertical_rods / Decimal('2')) + 1
            
            # Results section
            st.subheader('Results')
            
            result_unit = st.selectbox('Display results in:', 
                                     ['ft', 'mm', 'cm'],
                                     format_func=lambda x: {
                                         'ft': 'Feet (ft)',
                                         'mm': 'Millimeters (mm)',
                                         'cm': 'Centimeters (cm)'
                                     }[x])
            
            # Convert and display with proper precision
            horizontal_display = convert_result(float(horizontal_rods), result_unit)
            vertical_display = convert_result(float(vertical_rods), result_unit)
            
            st.write(f'Number of Horizontal Rods: {num_horizontal_rods}')
            st.write(f'Number of Vertical Rods: {num_vertical_rods}')
            st.write(f'Length of Horizontal Rods: {horizontal_display:.3f} {result_unit}')
            st.write(f'Length of Vertical Rods: {vertical_display:.3f} {result_unit}')
            
        except ValueError:
            st.error('Invalid input. Please enter numeric values.')

if __name__ == '__main__':
    main()