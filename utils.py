from dataclasses import dataclass
from math import ceil
from decimal import Decimal, ROUND_HALF_UP

@dataclass
class RoomDimensions:
    length1: float
    length2: float
    width1: float
    width2: float
    linter_spacing: float  # New field for linter/chad height

@dataclass
class CeilingCalculation:
    parameters_full: int
    parameters_extra: float
    main_rods: int
    cross_rods: int
    connecting_clips: int
    screws: int
    total_parameter_length: float
    main_rods_length: float
    cross_rods_length: float
    l_patti_count: int  # New field
    black_screws: int   # New field
    fasteners: int      # New field
    fastener_clips: int # New field
    board_count: float  # New field
    board_extra_sqft: float  # New field

def calculate_rod_length_with_overlap(length: float, standard_length: float = 12.0, overlap: float = 4/12) -> tuple[int, float]:
    """Calculate number of rods needed and extra length including overlaps"""
    if length <= standard_length:
        return 1, length
    
    # Calculate full rods needed accounting for overlaps
    full_rods = ceil((length - overlap) / (standard_length - overlap))
    # Calculate total length including overlaps
    total_length = length + ((full_rods - 1) * overlap)
    
    return full_rods, total_length

def calculate_parameters(dimensions: RoomDimensions) -> tuple[int, float]:
    """Calculate parameters needed for the perimeter including 4 inch overlaps"""
    STANDARD_LENGTH = 12  # feet
    OVERLAP = 4/12  # 4 inches in feet
    
    # Calculate perimeter using average of lengths and widths
    total_perimeter = dimensions.length1 + dimensions.length2 + dimensions.width1 + dimensions.width2
    full_rods, total_length = calculate_rod_length_with_overlap(total_perimeter, STANDARD_LENGTH, OVERLAP)
    
    extra_length = total_length % STANDARD_LENGTH
    if extra_length > 0:
        extra_length = round(extra_length + OVERLAP, 2)  # Add overlap for the extra piece
    
    return full_rods, extra_length

def calculate_main_rods(length: float) -> tuple[int, float]:
    """Calculate main rods with 4ft spacing and 2ft from walls"""
    FIRST_ROD_DISTANCE = 2  # feet from wall
    ROD_SPACING = 4  # feet between rods
    LAST_WALL_THRESHOLD = 3.5  # maximum allowed distance from last wall
    
    usable_length = length - (2 * FIRST_ROD_DISTANCE)
    num_spaces = ceil(usable_length / ROD_SPACING)
    num_rods = num_spaces + 1
    
    # Check if additional rod needed near last wall
    last_distance = length - (FIRST_ROD_DISTANCE + (num_spaces * ROD_SPACING))
    if last_distance > LAST_WALL_THRESHOLD:
        num_rods += 1
        
    return num_rods, length

def calculate_cross_rods(width: float) -> tuple[int, float]:
    """Calculate cross rods with 2ft spacing and 2ft from walls"""
    FIRST_ROD_DISTANCE = 2  # feet from wall
    ROD_SPACING = 2  # feet between centers
    
    # Calculate number of spaces between rods
    usable_width = width - (2 * FIRST_ROD_DISTANCE)
    num_spaces = ceil(usable_width / ROD_SPACING)
    num_rods = num_spaces + 1
    
    # Calculate total length needed including overlaps
    rods, total_length = calculate_rod_length_with_overlap(width)
    
    return num_rods, total_length

def calculate_l_patti(length: float) -> int:
    """Calculate L-patti count with 3ft from first wall and 4ft spacing"""
    FIRST_PATTI_DISTANCE = 3  # feet from wall
    PATTI_SPACING = 4  # feet between L-patti
    LAST_WALL_THRESHOLD = 3.5  # maximum allowed distance from last wall
    
    usable_length = length - (2 * FIRST_PATTI_DISTANCE)
    num_spaces = ceil(usable_length / PATTI_SPACING)
    num_patti = num_spaces + 1
    
    # Check if additional L-patti needed near last wall
    last_distance = length - (FIRST_PATTI_DISTANCE + (num_spaces * PATTI_SPACING))
    if last_distance > LAST_WALL_THRESHOLD:
        num_patti += 1
    
    return num_patti

def calculate_board_requirements(dimensions: RoomDimensions) -> tuple[float, float]:
    """Calculate plywood board requirements"""
    BOARD_LENGTH = 6  # feet
    BOARD_WIDTH = 4   # feet
    BOARD_AREA = BOARD_LENGTH * BOARD_WIDTH  # 24 sqft
    
    room_area = ((dimensions.length1 + dimensions.length2) / 2) * ((dimensions.width1 + dimensions.width2) / 2)
    boards_needed = room_area / BOARD_AREA
    full_boards = int(boards_needed)
    extra_sqft = round((boards_needed - full_boards) * BOARD_AREA, 2)
    
    return full_boards, extra_sqft

def calculate_ceiling_requirements(dimensions: RoomDimensions) -> CeilingCalculation:
    # Calculate parameters
    params_full, params_extra = calculate_parameters(dimensions)
    
    # Use maximum dimensions for calculations
    max_length = max(dimensions.length1, dimensions.length2)
    max_width = max(dimensions.width1, dimensions.width2)
    
    main_rods_count, main_rods_length = calculate_main_rods(max_length)
    cross_rods_count, cross_rods_length = calculate_cross_rods(max_width)
    
    # Calculate connecting clips (intersection points)
    connecting_clips = main_rods_count * cross_rods_count
    
    # Calculate total parameter length including overlaps
    total_parameter_length = dimensions.length1 + dimensions.length2 + dimensions.width1 + dimensions.width2
    
    # Calculate screws (12 per foot of parameter)
    screws = ceil(total_parameter_length) * 12
    
    # Calculate L-patti
    l_patti_count = calculate_l_patti(max_length)
    
    # Calculate black screws (2 per L-patti connection)
    black_screws = l_patti_count * 2
    
    # Calculate fasteners and clips (1 per L-patti)
    fasteners = l_patti_count
    fastener_clips = l_patti_count
    
    # Calculate board requirements
    board_count, board_extra_sqft = calculate_board_requirements(dimensions)
    
    return CeilingCalculation(
        parameters_full=params_full,
        parameters_extra=round(params_extra, 2),
        main_rods=main_rods_count,
        cross_rods=cross_rods_count,
        connecting_clips=connecting_clips,
        screws=screws,
        total_parameter_length=round(total_parameter_length, 2),
        main_rods_length=round(main_rods_length, 2),
        cross_rods_length=round(cross_rods_length, 2),
        l_patti_count=l_patti_count,
        black_screws=black_screws,
        fasteners=fasteners,
        fastener_clips=fastener_clips,
        board_count=board_count,
        board_extra_sqft=board_extra_sqft
    )