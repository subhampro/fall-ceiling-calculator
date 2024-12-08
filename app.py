import streamlit as st
import pandas as pd
from utils import RoomDimensions, calculate_ceiling_requirements
from decimal import Decimal
import base64
from io import BytesIO

def convert_to_feet(value, unit):
    conversion = {
        'ft': 1.0,
        'mm': 0.00328084,
        'cm': 0.0328084,
        'inches': 0.0833333,
        'm': 3.28084,
        'yd': 3
    }
    return value * conversion[unit]

def generate_excel_download(calc_results):
    df = pd.DataFrame({
        'Item': [
            'Parameters (Full 12ft)',
            'Parameters (Extra Length)',
            'Main Rods',
            'Cross Rods',
            'Connecting Clips',
            'Screws',
            'Total Parameter Length'
        ],
        'Quantity': [
            calc_results.parameters_full,
            f"{calc_results.parameters_extra:.2f} ft",
            calc_results.main_rods,
            calc_results.cross_rods,
            calc_results.connecting_clips,
            calc_results.screws,
            f"{calc_results.total_parameter_length:.2f} ft"
        ]
    })
    
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Ceiling Calculation')
    
    return buffer.getvalue()

def main():
    st.title('False Ceiling Calculator')
    
    unit = st.selectbox(
        'Select measurement unit:',
        ['ft', 'mm', 'cm', 'inches', 'm', 'yd']
    )
    
    # Add Linter Spacing input at the top
    linter_spacing = st.number_input(
        f'Linter Spacing (Chad to Main Rod Height) ({unit})',
        min_value=0.0,
        help="Distance from Chad to the starting width of Main/Enter"
    )
    
    st.subheader('Room Measurements')
    col1, col2 = st.columns(2)
    
    with col1:
        length1 = st.number_input(f'Wall 1 Length ({unit})', min_value=0.0)
        width1 = st.number_input(f'Width 1 ({unit})', min_value=0.0)
    
    with col2:
        length2 = st.number_input(f'Wall 2 Length ({unit})', min_value=0.0)
        width2 = st.number_input(f'Width 2 ({unit})', min_value=0.0)

    if st.button('Calculate'):
        dimensions = RoomDimensions(
            convert_to_feet(length1, unit),
            convert_to_feet(length2, unit),
            convert_to_feet(width1, unit),
            convert_to_feet(width2, unit),
            convert_to_feet(linter_spacing, unit)
        )
        
        results = calculate_ceiling_requirements(dimensions)
        
        st.subheader('Calculation Results')
        
        # Parameters
        st.write("### Steel Parameters (1 inch × 1 inch)")
        st.write(f"Room Perimeter: {results.total_parameter_length:.2f} ft")
        param_text = f"{results.parameters_full} full rods (12ft each)"
        if results.parameters_extra > 0:
            param_text += f" + {results.parameters_extra:.2f} ft extra (including 4 inch overlap)"
        st.write(f"Parameters needed: {param_text}")
        
        # Main/Enter Details
        st.write("### Main/Enter Rods (1 inch × 2 inch)")
        st.write(f"Main rods needed: {results.main_rods}")
        if results.main_rods_length > (results.main_rods * 12):
            extra_length = results.main_rods_length - (results.main_rods * 12)
            st.write(f"Extra length needed: {extra_length:.2f} ft (with 4 inch overlaps)")
        st.write("Spacing: 2ft from walls, 4ft between rods")
        
        # Cross Rod Details
        st.write("### Cross Rods (3 inch × 1 inch)")
        st.write(f"Cross rods needed: {results.cross_rods}")
        if results.cross_rods_length > (results.cross_rods * 12):
            extra_length = results.cross_rods_length - (results.cross_rods * 12)
            st.write(f"Extra length needed: {extra_length:.2f} ft (with 4 inch overlaps)")
        st.write("Spacing: 2ft from walls to center, 2ft between centers")
        
        # Support Materials with detailed counts
        st.write("### Support Materials")
        st.write(f"L-patti required: {results.l_patti_count}")
        st.write(f"Fasteners needed: {results.fasteners} (1 per L-patti)")
        st.write(f"Fastener clips needed: {results.fastener_clips} (1 per fastener)")
        st.write(f"Connecting clips needed: {results.connecting_clips} (at Main-Cross intersections)")
        
        # Screws with specific counts
        st.write("### Screws")
        st.write(f"Regular screws: {results.screws} (1ft spacing on parameters)")
        st.write(f"Black screws: {results.black_screws} (2 per L-patti)")
        
        # Detailed Board Requirements
        st.write("### Plywood Boards (6ft × 4ft × 0.5inch)")
        if results.board_extra_sqft > 0:
            st.write(f"Full boards needed: {int(results.board_count)}")
            st.write(f"Extra area needed: {results.board_extra_sqft:.2f} sqft ({results.board_extra_sqft/24:.2f} boards)")
        else:
            st.write(f"Full boards needed: {int(results.board_count)}")

if __name__ == '__main__':
    main()