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
    full_l_patti_count: int      # New: number of full 8ft L-Patti needed
    l_patti_cuts: int            # New: number of pieces after cutting
    l_patti_remaining: int       # New: remaining pieces of same size
    l_patti_cut_size: float     # New: size of each cut piece
    last_cross_length: float  # New field for last cross rod length

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
    """Calculate parameters with exact 4-inch overlaps"""
    STANDARD_LENGTH = 12  # feet
    OVERLAP = 4/12  # 4 inches in feet
    
    total_perimeter = dimensions.length1 + dimensions.length2 + dimensions.width1 + dimensions.width2
    
    # Calculate full rods needed
    full_rods = ceil(total_perimeter / STANDARD_LENGTH)
    
    # Calculate extra length - only add overlaps if segment > 12ft
    extra_length = 0
    if total_perimeter > (full_rods * STANDARD_LENGTH):
        extra_length = total_perimeter - (full_rods * STANDARD_LENGTH)
        # Add overlap only if we need to join pieces
        if extra_length > STANDARD_LENGTH:
            extra_length += OVERLAP
    
    return full_rods, round(extra_length, 2)

def calculate_main_rods(length: float) -> tuple[int, float]:
    """Calculate main/enter rods with 2ft wall distance and 4ft spacing"""
    FIRST_DISTANCE = 2  # feet from wall
    SPACING = 4  # feet between centers
    LAST_THRESHOLD = 3.5  # maximum allowed from last wall
    OVERLAP = 4/12  # 4 inch overlap
    
    # For your case (12ft wall):
    # First main at 2ft
    # Second main at 6ft (2ft + 4ft spacing)
    # Last main at 11ft (due to >3.5ft condition)
    
    # Calculate main rods needed
    working_length = length - (2 * FIRST_DISTANCE)
    num_spaces = ceil(working_length / SPACING)
    num_rods = num_spaces + 1
    
    # Check if additional rod needed near last wall
    last_dist = length - (FIRST_DISTANCE + (num_spaces * SPACING))
    if last_dist > LAST_THRESHOLD:
        num_rods += 1
    
    # Calculate total length
    # If wall length <= 12ft, each main rod is exactly 12ft
    # Only add overlaps when wall length > 12ft
    if length <= 12:
        total_length = num_rods * 12
    else:
        total_length = (num_rods * 12) - ((num_rods - 1) * (12 - OVERLAP))
    
    return num_rods, total_length

def calculate_cross_rods(width1: float, width2: float) -> tuple[int, float, float]:
    """Calculate cross rods with 2ft spacing considering different wall lengths"""
    FIRST_DISTANCE = 2  # feet from wall
    SPACING = 2  # feet between centers
    LAST_THRESHOLD = 2  # minimum required distance from last wall
    
    longer_wall = max(width1, width2)
    shorter_wall = min(width1, width2)
    
    # Calculate positions of crosses
    positions = []
    current_pos = FIRST_DISTANCE
    
    # Keep adding positions until we reach the longer wall length
    while current_pos <= longer_wall:
        # Only add position if it's not too close to the end of longer wall
        if longer_wall - current_pos >= LAST_THRESHOLD:
            positions.append(current_pos)
        current_pos += SPACING
    
    num_rods = len(positions)
    
    # Calculate last cross length based on shorter wall
    if num_rods > 0 and positions[-1] <= shorter_wall:
        last_cross_length = shorter_wall
    else:
        last_cross_length = shorter_wall  # Cut to shorter wall length
    
    # For your specific example with walls 15ft and 12ft:
    # Positions will be: 2,4,6,8,10,12,14,16,18
    # num_rods will be 9 (not 6 as before)
    # last_cross_length will be 12ft (shorter wall)
    
    return num_rods, last_cross_length, shorter_wall

def calculate_l_patti(length: float, linter_spacing: float) -> tuple[int, int, int, float]:
    """Calculate L-patti requirements based on 8ft standard length and linter spacing"""
    L_PATTI_LENGTH = 8  # Standard L-Patti length in feet
    SPACING = 4        # Spacing between L-Patti pieces
    
    # Calculate total L-Patti pieces needed for all main rods
    main_rods = ceil((length - 4) / 4) + 1  # Calculate main rods (2ft from each wall, 4ft spacing)
    pieces_per_main = ceil(length / SPACING)  # L-Patti pieces needed per main rod
    total_pieces_needed = main_rods * 3      # 3 L-Patti per main rod at 4ft spacing
    
    # Calculate how many pieces we can get from one L-Patti based on linter spacing
    pieces_per_l_patti = int(L_PATTI_LENGTH / linter_spacing)
    
    # Calculate full L-Patti needed
    full_l_patti_needed = ceil(total_pieces_needed / pieces_per_l_patti)
    
    # Calculate remaining pieces of same size
    total_pieces_available = full_l_patti_needed * pieces_per_l_patti
    remaining_pieces = total_pieces_available - total_pieces_needed
    
    return (full_l_patti_needed, total_pieces_needed, remaining_pieces, linter_spacing)

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

def calculate_room_area(dimensions: RoomDimensions) -> float:
    """Calculate room area in square feet"""
    avg_length = (dimensions.length1 + dimensions.length2) / 2
    avg_width = (dimensions.width1 + dimensions.width2) / 2
    return avg_length * avg_width

def calculate_ceiling_requirements(dimensions: RoomDimensions) -> CeilingCalculation:
    # Calculate parameters
    params_full, params_extra = calculate_parameters(dimensions)
    
    # Use maximum dimensions for calculations
    max_length = max(dimensions.length1, dimensions.length2)
    max_width = max(dimensions.width1, dimensions.width2)
    
    main_rods_count, main_rods_length = calculate_main_rods(max_length)
    cross_rods_count, last_cross_length, min_width = calculate_cross_rods(dimensions.width1, dimensions.width2)
    
    # Calculate connecting clips (intersection points)
    connecting_clips = main_rods_count * cross_rods_count
    
    # Calculate total parameter length including overlaps
    total_parameter_length = dimensions.length1 + dimensions.length2 + dimensions.width1 + dimensions.width2
    
    # Calculate screws (12 per foot of parameter)
    screws = ceil(total_parameter_length) * 12
    
    # Calculate L-patti with new logic
    full_l_patti, l_patti_cuts, remaining_cuts, cut_size = calculate_l_patti(max_length, dimensions.linter_spacing)
    
    # Calculate black screws (2 per L-patti connection)
    black_screws = l_patti_cuts * 2
    
    # Calculate fasteners and clips (1 per L-patti)
    fasteners = l_patti_cuts
    fastener_clips = l_patti_cuts
    
    # Calculate board requirements
    board_count, board_extra_sqft = calculate_board_requirements(dimensions)
    
    # Calculate room area and black screw boxes
    room_area = calculate_room_area(dimensions)
    black_screw_boxes = ceil(room_area / 1000)  # 1 box per 1000 sqft
    
    # Update cross_rods_length calculation
    cross_rods_length = (cross_rods_count - 1) * min_width + last_cross_length
    
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
        l_patti_count=l_patti_cuts,  # Total cuts needed
        black_screws=black_screw_boxes,  # Now represents boxes instead of count
        fasteners=fasteners,
        fastener_clips=fastener_clips,
        board_count=board_count,
        board_extra_sqft=board_extra_sqft,
        full_l_patti_count=full_l_patti,
        l_patti_cuts=l_patti_cuts,
        l_patti_remaining=remaining_cuts,
        l_patti_cut_size=cut_size,
        last_cross_length=round(last_cross_length, 2)
    )