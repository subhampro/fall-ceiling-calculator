import streamlit as st

def convert_to_feet(value, unit):
    conversion_factors = {
        'cm': 0.0328084,
        'mm': 0.00328084,
        'inches': 0.0833333,
        'ft': 1,
        'm': 3.28084,
        'yd': 3
    }
    return value * conversion_factors[unit]

def convert_from_feet(value, unit):
    conversion_factors = {
        'cm': 30.48,
        'mm': 304.8,
        'inches': 12,
        'ft': 1,
        'm': 0.3048,
        'yd': 0.333333
    }
    return value * conversion_factors[unit]

def main():
    st.title('Ceiling Rod Calculation')
    
    # Input fields
    length1 = st.number_input('Length 1', min_value=0.0)
    length2 = st.number_input('Length 2', min_value=0.0)
    width1 = st.number_input('Width 1', min_value=0.0)
    width2 = st.number_input('Width 2', min_value=0.0)
    
    unit = st.selectbox('Unit', 
                       ['cm', 'mm', 'inches', 'ft', 'm', 'yd'])
    
    if st.button('Calculate'):
        try:
            length1_in_feet = convert_to_feet(length1, unit)
            length2_in_feet = convert_to_feet(length2, unit)
            width1_in_feet = convert_to_feet(width1, unit)
            width2_in_feet = convert_to_feet(width2, unit)

            horizontal_rods = max(length1_in_feet, length2_in_feet)
            vertical_rods = max(width1_in_feet, width2_in_feet)
            num_horizontal_rods = int(horizontal_rods / 2) + 1
            num_vertical_rods = int(vertical_rods / 2) + 1

            horizontal_rods = convert_from_feet(horizontal_rods, unit)
            vertical_rods = convert_from_feet(vertical_rods, unit)

            st.subheader('Results')
            st.write(f'Number of Horizontal Rods: {num_horizontal_rods}')
            st.write(f'Number of Vertical Rods: {num_vertical_rods}')
            st.write(f'Length of Horizontal Rods: {horizontal_rods:.2f} {unit}')
            st.write(f'Length of Vertical Rods: {vertical_rods:.2f} {unit}')
            
        except ValueError:
            st.error('Invalid input. Please enter numeric values.')

if __name__ == '__main__':
    main()