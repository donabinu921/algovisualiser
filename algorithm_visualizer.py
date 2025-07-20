import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import time
import random
import copy

# Page configuration
st.set_page_config(
    page_title="Sorting Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS to make sidebar wider
st.markdown(
    """
<style>
    .css-1d391kg {
        width: 25rem;
    }
    .css-1lcbmhc {
        max-width: 25rem;
    }
    section[data-testid="stSidebar"] {
        width: 25rem !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .css-1d391kg {
        width: 25rem;
    }
    .css-1lcbmhc {
        max-width: 25rem;
    }
    section[data-testid="stSidebar"] {
        width: 25rem !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .algorithm-info {
        background-color: #2e3440;
        color: #d8dee9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .algorithm-info h4 {
        color: #88c0d0;
    }
    
    .stButton > button {
        width: 100%;
        margin: 0.25rem 0;
    }
    
    .stButton > button:hover {
        border-color: #28a745 !important;
        color: #28a745 !important;
    }
    
    .stButton > button:active, .stButton > button:focus {
        border-color: #28a745 !important;
        box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25) !important;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "array" not in st.session_state:
    st.session_state.array = [64, 34, 25, 12, 22, 11, 90]
if "original_array" not in st.session_state:
    st.session_state.original_array = copy.deepcopy(st.session_state.array)
if "is_sorting" not in st.session_state:
    st.session_state.is_sorting = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "algorithm_steps" not in st.session_state:
    st.session_state.algorithm_steps = []
if "comparing" not in st.session_state:
    st.session_state.comparing = []
if "sorted_indices" not in st.session_state:
    st.session_state.sorted_indices = []


# Algorithm implementations with step tracking
def bubble_sort_steps(arr):
    steps = []
    n = len(arr)
    arr_copy = arr.copy()

    for i in range(n):
        for j in range(0, n - i - 1):
            steps.append(
                {
                    "array": arr_copy.copy(),
                    "comparing": [j, j + 1],
                    "sorted_indices": list(range(n - i, n)),
                    "description": f"Comparing {arr_copy[j]} and {arr_copy[j + 1]}",
                }
            )

            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                steps.append(
                    {
                        "array": arr_copy.copy(),
                        "comparing": [j, j + 1],
                        "sorted_indices": list(range(n - i, n)),
                        "description": f"Swapped {arr_copy[j + 1]} and {arr_copy[j]}",
                    }
                )

    steps.append(
        {
            "array": arr_copy,
            "comparing": [],
            "sorted_indices": list(range(n)),
            "description": "Sorting complete!",
        }
    )

    return steps


def selection_sort_steps(arr):
    steps = []
    arr_copy = arr.copy()
    n = len(arr)

    for i in range(n):
        min_idx = i
        steps.append(
            {
                "array": arr_copy.copy(),
                "comparing": [i],
                "sorted_indices": list(range(i)),
                "description": f"Finding minimum from position {i}",
            }
        )

        for j in range(i + 1, n):
            steps.append(
                {
                    "array": arr_copy.copy(),
                    "comparing": [min_idx, j],
                    "sorted_indices": list(range(i)),
                    "description": f"Comparing {arr_copy[min_idx]} with {arr_copy[j]}",
                }
            )

            if arr_copy[j] < arr_copy[min_idx]:
                min_idx = j

        if min_idx != i:
            arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
            steps.append(
                {
                    "array": arr_copy.copy(),
                    "comparing": [i, min_idx],
                    "sorted_indices": list(range(i + 1)),
                    "description": f"Swapped {arr_copy[min_idx]} with {arr_copy[i]}",
                }
            )

    steps.append(
        {
            "array": arr_copy,
            "comparing": [],
            "sorted_indices": list(range(n)),
            "description": "Sorting complete!",
        }
    )

    return steps


def quick_sort_steps(arr):
    steps = []
    arr_copy = arr.copy()

    def partition(arr, low, high, steps):
        pivot = arr[high]
        i = low - 1

        steps.append(
            {
                "array": arr.copy(),
                "comparing": [high],
                "sorted_indices": [],
                "description": f"Pivot selected: {pivot} at index {high}",
            }
        )

        for j in range(low, high):
            steps.append(
                {
                    "array": arr.copy(),
                    "comparing": [j, high],
                    "sorted_indices": [],
                    "description": f"Comparing {arr[j]} with pivot {pivot}",
                }
            )

            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                if i != j:
                    steps.append(
                        {
                            "array": arr.copy(),
                            "comparing": [i, j],
                            "sorted_indices": [],
                            "description": f"Swapped {arr[j]} and {arr[i]}",
                        }
                    )

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(
            {
                "array": arr.copy(),
                "comparing": [i + 1, high],
                "sorted_indices": [],
                "description": f"Placed pivot {pivot} at correct position {i + 1}",
            }
        )

        return i + 1

    def quick_sort_recursive(arr, low, high, steps):
        if low < high:
            pi = partition(arr, low, high, steps)
            quick_sort_recursive(arr, low, pi - 1, steps)
            quick_sort_recursive(arr, pi + 1, high, steps)

    quick_sort_recursive(arr_copy, 0, len(arr_copy) - 1, steps)

    steps.append(
        {
            "array": arr_copy,
            "comparing": [],
            "sorted_indices": list(range(len(arr_copy))),
            "description": "Quick sort complete!",
        }
    )

    return steps


def merge_sort_steps(arr):
    steps = []
    arr_copy = arr.copy()

    def merge(arr, left, mid, right, steps):
        left_part = arr[left : mid + 1]
        right_part = arr[mid + 1 : right + 1]

        steps.append(
            {
                "array": arr.copy(),
                "comparing": list(range(left, right + 1)),
                "sorted_indices": [],
                "description": f"Merging subarrays [{left}:{mid}] and [{mid+1}:{right}]",
            }
        )

        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            steps.append(
                {
                    "array": arr.copy(),
                    "comparing": [left + i, mid + 1 + j],
                    "sorted_indices": [],
                    "description": f"Comparing {left_part[i]} and {right_part[j]}",
                }
            )

            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1

            steps.append(
                {
                    "array": arr.copy(),
                    "comparing": [k - 1],
                    "sorted_indices": [],
                    "description": f"Placed {arr[k-1]} at position {k-1}",
                }
            )

        while i < len(left_part):
            arr[k] = left_part[i]
            steps.append(
                {
                    "array": arr.copy(),
                    "comparing": [k],
                    "sorted_indices": [],
                    "description": f"Copying remaining {left_part[i]}",
                }
            )
            i += 1
            k += 1

        while j < len(right_part):
            arr[k] = right_part[j]
            steps.append(
                {
                    "array": arr.copy(),
                    "comparing": [k],
                    "sorted_indices": [],
                    "description": f"Copying remaining {right_part[j]}",
                }
            )
            j += 1
            k += 1

    def merge_sort_recursive(arr, left, right, steps):
        if left < right:
            mid = (left + right) // 2
            merge_sort_recursive(arr, left, mid, steps)
            merge_sort_recursive(arr, mid + 1, right, steps)
            merge(arr, left, mid, right, steps)

    merge_sort_recursive(arr_copy, 0, len(arr_copy) - 1, steps)

    steps.append(
        {
            "array": arr_copy,
            "comparing": [],
            "sorted_indices": list(range(len(arr_copy))),
            "description": "Merge sort complete!",
        }
    )

    return steps


def insertion_sort_steps(arr):
    steps = []
    arr_copy = arr.copy()
    n = len(arr)

    for i in range(1, n):
        key = arr_copy[i]
        j = i - 1

        steps.append(
            {
                "array": arr_copy.copy(),
                "comparing": [i],
                "sorted_indices": list(range(i)),
                "description": f"Inserting {key} into sorted portion",
            }
        )

        while j >= 0 and arr_copy[j] > key:
            steps.append(
                {
                    "array": arr_copy.copy(),
                    "comparing": [j, j + 1],
                    "sorted_indices": list(range(i)),
                    "description": f"Moving {arr_copy[j]} right",
                }
            )

            arr_copy[j + 1] = arr_copy[j]
            j -= 1

            steps.append(
                {
                    "array": arr_copy.copy(),
                    "comparing": [j + 1] if j + 1 >= 0 else [],
                    "sorted_indices": list(range(i)),
                    "description": f"Moved {arr_copy[j + 1]}",
                }
            )

        arr_copy[j + 1] = key
        steps.append(
            {
                "array": arr_copy.copy(),
                "comparing": [],
                "sorted_indices": list(range(i + 1)),
                "description": f"Placed {key} in correct position",
            }
        )

    steps.append(
        {
            "array": arr_copy,
            "comparing": [],
            "sorted_indices": list(range(n)),
            "description": "Sorting complete!",
        }
    )

    return steps


def heap_sort_steps(arr):
    steps = []
    arr_copy = arr.copy()
    n = len(arr_copy)

    def heapify(arr, n, i, steps):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        steps.append(
            {
                "array": arr.copy(),
                "comparing": [i]
                + ([left] if left < n else [])
                + ([right] if right < n else []),
                "sorted_indices": [],
                "description": f"Heapifying at index {i}",
            }
        )

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            steps.append(
                {
                    "array": arr.copy(),
                    "comparing": [i, largest],
                    "sorted_indices": [],
                    "description": f"Swapped {arr[largest]} and {arr[i]} in heap",
                }
            )
            heapify(arr, n, largest, steps)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr_copy, n, i, steps)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr_copy[0], arr_copy[i] = arr_copy[i], arr_copy[0]
        steps.append(
            {
                "array": arr_copy.copy(),
                "comparing": [0, i],
                "sorted_indices": list(range(i, n)),
                "description": f"Moved max element {arr_copy[i]} to sorted position",
            }
        )
        heapify(arr_copy, i, 0, steps)

    steps.append(
        {
            "array": arr_copy,
            "comparing": [],
            "sorted_indices": list(range(n)),
            "description": "Heap sort complete!",
        }
    )

    return steps


# Algorithm information
ALGORITHMS = {
    "Bubble Sort": {
        "function": bubble_sort_steps,
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)",
        "description": "Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
    },
    "Selection Sort": {
        "function": selection_sort_steps,
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)",
        "description": "Finds the minimum element and places it at the beginning, then repeats for the rest of the array.",
    },
    "Insertion Sort": {
        "function": insertion_sort_steps,
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)",
        "description": "Builds the final sorted array one item at a time by inserting each element into its correct position.",
    },
    "Quick Sort": {
        "function": quick_sort_steps,
        "time_complexity": "O(n log n) avg, O(n²) worst",
        "space_complexity": "O(log n)",
        "description": "Selects a pivot element and partitions the array around it, then recursively sorts the subarrays.",
    },
    "Merge Sort": {
        "function": merge_sort_steps,
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "description": "Divides the array into halves, recursively sorts them, and then merges the sorted halves back together.",
    },
    "Heap Sort": {
        "function": heap_sort_steps,
        "time_complexity": "O(n log n)",
        "space_complexity": "O(1)",
        "description": "Builds a max heap from the array, then repeatedly extracts the maximum element to build the sorted array.",
    },
}

# Main title
st.markdown(
    '<h1 class="main-header">🔍 Sorting Visualizer</h1>', unsafe_allow_html=True
)

# Sidebar controls
with st.sidebar:
    st.header("🎛️ Controls")

    # 1. Algorithm selection (TOP)
    st.subheader("🔧 Algorithm Selection")
    selected_algorithm = st.selectbox(
        "Choose Algorithm:", list(ALGORITHMS.keys()), index=0
    )

    st.divider()

    # 2. Animation controls (SECOND)
    st.subheader("⚡ Animation Controls")

    speed = st.slider("Speed (steps per second):", 0.5, 10.0, 2.0, 0.5)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Start Sorting"):
            if not st.session_state.algorithm_steps:
                algo_info = ALGORITHMS[selected_algorithm]
                st.session_state.algorithm_steps = algo_info["function"](
                    st.session_state.array
                )
            st.session_state.is_sorting = True

    with col2:
        if st.button("⏸️ Pause"):
            st.session_state.is_sorting = False

    col3, col4 = st.columns(2)

    with col3:
        if st.button("⏹️ Stop"):
            st.session_state.is_sorting = False
            st.session_state.current_step = 0
            st.session_state.array = copy.deepcopy(st.session_state.original_array)
            st.session_state.algorithm_steps = []

    with col4:
        if st.button("🔄 Reset"):
            st.session_state.array = copy.deepcopy(st.session_state.original_array)
            st.session_state.current_step = 0
            st.session_state.is_sorting = False
            st.session_state.algorithm_steps = []

    st.divider()

    # 3. Array input (THIRD)
    st.subheader("📝 Array Input")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎲 Generate Random"):
            size = st.session_state.get("array_size", 10)
            st.session_state.array = [random.randint(1, 100) for _ in range(size)]
            st.session_state.original_array = copy.deepcopy(st.session_state.array)
            st.session_state.current_step = 0
            st.session_state.algorithm_steps = []
            st.rerun()

    with col2:
        array_size = st.slider("Array Size:", 3, 20, 7, key="array_size")

    # Custom input
    custom_input = st.text_input(
        "Custom Array (comma-separated):",
        value=",".join(map(str, st.session_state.array)),
        help="Enter numbers separated by commas",
    )

    if st.button("✅ Apply Custom Array"):
        try:
            new_array = [int(x.strip()) for x in custom_input.split(",")]
            if len(new_array) > 0:
                st.session_state.array = new_array
                st.session_state.original_array = copy.deepcopy(st.session_state.array)
                st.session_state.current_step = 0
                st.session_state.algorithm_steps = []
                st.rerun()
        except ValueError:
            st.error("Please enter valid numbers separated by commas")

    st.divider()

    # 4. Algorithm information (BOTTOM)
    st.subheader("📚 Algorithm Info")
    algo_info = ALGORITHMS[selected_algorithm]
    st.markdown(
        f"""
    <div class="algorithm-info">
        <h4>{selected_algorithm}</h4>
        <p><strong>Time Complexity:</strong> {algo_info['time_complexity']}</p>
        <p><strong>Space Complexity:</strong> {algo_info['space_complexity']}</p>
        <p><strong>Description:</strong> {algo_info['description']}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Main visualization area
col1, col2 = st.columns([3, 1])

with col1:
    # Create visualization
    def create_bar_chart():
        if st.session_state.algorithm_steps and st.session_state.current_step < len(
            st.session_state.algorithm_steps
        ):
            step_data = st.session_state.algorithm_steps[st.session_state.current_step]
            array = step_data["array"]
            comparing = step_data.get("comparing", [])
            sorted_indices = step_data.get("sorted_indices", [])
        else:
            array = st.session_state.array
            comparing = []
            sorted_indices = []

        colors = []
        for i in range(len(array)):
            if i in sorted_indices:
                colors.append("#28a745")  # Green for sorted
            elif i in comparing:
                colors.append("#dc3545")  # Red for comparing
            else:
                colors.append("#007bff")  # Blue for unsorted

        fig = go.Figure(
            data=go.Bar(
                x=list(range(len(array))),
                y=array,
                marker=dict(color=colors),
                text=array,
                textposition="outside",
            )
        )

        fig.update_layout(
            title=dict(
                text=f"Current Array State - Step {st.session_state.current_step + 1}",
                x=0.5,
                font=dict(size=20),
            ),
            xaxis=dict(title="Index", showgrid=False),
            yaxis=dict(title="Value", showgrid=True, gridcolor="lightgray"),
            showlegend=False,
            height=400,
            plot_bgcolor="white",
        )

        return fig

    # Display chart
    chart_placeholder = st.empty()
    chart_placeholder.plotly_chart(create_bar_chart(), use_container_width=True)

with col2:
    # Status and information
    st.subheader("📊 Status")

    if st.session_state.algorithm_steps:
        progress = (st.session_state.current_step + 1) / len(
            st.session_state.algorithm_steps
        )
        st.progress(progress)
        st.write(
            f"Step: {st.session_state.current_step + 1} / {len(st.session_state.algorithm_steps)}"
        )

        if st.session_state.current_step < len(st.session_state.algorithm_steps):
            current_step_info = st.session_state.algorithm_steps[
                st.session_state.current_step
            ]
            st.info(current_step_info.get("description", ""))
    else:
        st.write("Click 'Start Sorting' to begin visualization")

    st.subheader("🎨 Legend")
    st.markdown(
        """
    - 🔵 **Blue**: Unsorted elements
    - 🔴 **Red**: Currently comparing
    - 🟢 **Green**: Sorted elements
    """
    )

# Animation loop
if st.session_state.is_sorting and st.session_state.algorithm_steps:
    if st.session_state.current_step < len(st.session_state.algorithm_steps) - 1:
        time.sleep(1.0 / speed)
        st.session_state.current_step += 1
        st.rerun()
    else:
        st.session_state.is_sorting = False
        st.success("🎉 Sorting completed!")
