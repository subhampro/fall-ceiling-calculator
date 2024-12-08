import streamlit as st

def convert_to_feet(value, unit='ft'):
    return value  # All inputs are assumed to be in feet now

def convert_result(value, to_unit):
    conversion_factors = {
        'ft': 1,
        'mm': 304.8,
        'cm': 30.48
    }
    return value * conversion_factors[to_unit]

def main():
    st.title('Ceiling Rod Calculation')
    
    # All inputs are in feet
    length1 = st.number_input('Length 1 (ft)', min_value=0.0)
    length2 = st.number_input('Length 2 (ft)', min_value=0.0)
    width1 = st.number_input('Width 1 (ft)', min_value=0.0)
    width2 = st.number_input('Width 2 (ft)', min_value=0.0)
    
    if st.button('Calculate'):
        try:
            # Calculate everything in feet
            horizontal_rods = max(length1, length2)
            vertical_rods = max(width1, width2)
            num_horizontal_rods = int(horizontal_rods / 2) + 1
            num_vertical_rods = int(vertical_rods / 2) + 1

            # Results section
            st.subheader('Results')
            
            # Unit conversion selector for results
            result_unit = st.selectbox('Display results in:', 
                                     ['ft', 'mm', 'cm'],
                                     format_func=lambda x: {'ft': 'Feet', 
                                                          'mm': 'Millimeters', 
                                                          'cm': 'Centimeters'}[x])
            
            # Convert measurements to selected unit
            horizontal_display = convert_result(horizontal_rods, result_unit)
            vertical_display = convert_result(vertical_rods, result_unit)

            # Display results
            st.write(f'Number of Horizontal Rods: {num_horizontal_rods}')
            st.write(f'Number of Vertical Rods: {num_vertical_rods}')
            st.write(f'Length of Horizontal Rods: {horizontal_display:.2f} {result_unit}')
            st.write(f'Length of Vertical Rods: {vertical_display:.2f} {result_unit}')
            
        except ValueError:
            st.error('Invalid input. Please enter numeric values.')

if __name__ == '__main__':
    main()