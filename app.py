import streamlit as st
from itertools import permutations
from typing import List, Tuple

def can_fit(container: Tuple[int, int], truck: Tuple[int, int]) -> bool:
    return container[0] <= truck[0] and container[1] <= truck[1]

def check_fit(containers: List[Tuple[int, int]], truck: Tuple[int, int]) -> bool:
    # Start by sorting the containers by the largest to smallest based on area.
    containers = sorted(containers, key=lambda x: x[0] * x[1], reverse=True)

    # The used_space list will keep track of the (length, width) of the placed containers.
    used_space = []

    for container in containers:
        placed = False

        # Try to place the container in the existing rows.
        for idx, space in enumerate(used_space):
            if can_fit(container, (truck[0] - space[0], space[1])) or can_fit((container[1], container[0]), (truck[0] - space[0], space[1])):
                # If it fits, update the used space for that row.
                used_space[idx] = (space[0] + min(container), max(space[1], max(container)))
                placed = True
                break
        
        # If the container has not been placed in the existing rows, try to create a new row.
        if not placed:
            if can_fit(container, (truck[0], truck[1] - sum([s[1] for s in used_space]))) or can_fit((container[1], container[0]), (truck[0], truck[1] - sum([s[1] for s in used_space]))):
                # If a new row can be created, add it to the used space.
                used_space.append((min(container), max(container)))
                placed = True

        # If the container couldn't be placed, return False.
        if not placed:
            return False

    # If all containers have been placed, return True.
    return True

# Initialize session state variables if they don't exist
if 'truck_length' not in st.session_state:
    st.session_state.truck_length = 600
if 'truck_width' not in st.session_state:
    st.session_state.truck_width = 235

# Streamlit UI
st.title('Truck Load Calculator')

# Define the container dimensions
container_dimensions = {
    "Frame": (229, 108),
    "Stillage": (102, 79),
    "Travel Cage": (141, 103),
    "Row (15kg)": (222, 29),
    "Row (18kg)": (231, 33)
}

# Initialize session state variables for truck dimensions if they don't exist
if 'truck_length' not in st.session_state:
    st.session_state['truck_length'] = 600  # Example default value
if 'truck_width' not in st.session_state:
    st.session_state['truck_width'] = 230  # Example default value

# Input for truck dimensions
st.subheader('Enter the Truck Dimensions:')
truck_length = st.number_input('Length (cm)', min_value=0, value=st.session_state['truck_length'], key='truck_length')
truck_width = st.number_input('Width (cm)', min_value=0, value=st.session_state['truck_width'], key='truck_width')

# Define the calculation function
def calculate_load():
    containers_list = []
    for container_name, dimensions in container_dimensions.items():
        quantity = st.session_state[container_name]  # Get the current quantity from session state
        for _ in range(quantity):
            containers_list.append(container_dimensions[container_name])

    truck_size = (st.session_state['truck_length'], st.session_state['truck_width'])
    can_fit_in_truck = check_fit(containers_list, truck_size)  # Note the variable name change to avoid conflict

    if can_fit_in_truck:
        st.success("All containers can fit in the truck!")
    else:
        st.error("Containers won't fit in the truck.")

st.subheader('Enter the Container Quantities:')
for container_name, dimensions in container_dimensions.items():
    # Containers are keyed by their name, their quantities are updated in session state
    st.number_input(f'{container_name} {dimensions[0]} x {dimensions[1]} Quantity', min_value=0, key=container_name)

# Listen for changes in each input, if any input changes, recalculate the load
for container_name in container_dimensions.keys():
    if st.session_state[container_name]:
        calculate_load()
        break

# If the page is being loaded for the first time, perform an initial calculation
if 'init_calc_done' not in st.session_state:
    st.session_state['init_calc_done'] = True
    calculate_load()