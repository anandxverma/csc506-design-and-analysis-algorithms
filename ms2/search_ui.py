import random
import streamlit as st
import pandas as pd
from search_algorithms import binary_search, linear_search, time_search

st.title("Search Algorithm Visualizer")

st.sidebar.header("Navigation")
page = st.sidebar.radio("", ["Search", "Benchmark"], label_visibility="collapsed")

algorithm = "Binary Search"
if page == "Search":
    st.sidebar.divider()
    st.sidebar.header("Configuration")
    algorithm = st.sidebar.radio("Algorithm", ["Binary Search", "Linear Search"])


# ── Search page ──────────────────────────────────────────────────────────────
if page == "Search":
    st.subheader("Input Array")
    array_input = st.text_input(
        "Enter comma-separated numbers",
        value="1, 3, 5, 7, 9, 11, 13, 15",
    )

    try:
        arr = [int(x.strip()) for x in array_input.split(",") if x.strip()]
    except ValueError:
        st.error("Please enter valid integers separated by commas.")
        st.stop()

    if algorithm == "Binary Search":
        arr = sorted(arr)
        st.caption("Array is sorted automatically for binary search.")

    st.write("Array:", arr)

    target = st.number_input("Target value to search", value=7, step=1)

    if st.button("Search"):
        fn = binary_search if algorithm == "Binary Search" else linear_search
        result, elapsed_ms, _, _ = time_search(fn, arr, int(target))
        st.caption(f"Search completed in **{elapsed_ms:.4f} ms**")

        if result == -1:
            st.warning(f"Target **{int(target)}** was not found in the array.")
        else:
            st.success(f"Target **{int(target)}** found at index **{result}**.")

        st.subheader("Array with result highlighted")
        cols = st.columns(len(arr))
        for i, val in enumerate(arr):
            with cols[i]:
                if i == result:
                    st.markdown(
                        f"<div style='background:#2ecc71;color:white;border-radius:6px;"
                        f"padding:8px;text-align:center;font-weight:bold'>{val}<br>"
                        f"<small>idx {i}</small></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div style='background:#ecf0f1;border-radius:6px;"
                        f"padding:8px;text-align:center'>{val}<br>"
                        f"<small>idx {i}</small></div>",
                        unsafe_allow_html=True,
                    )

    st.divider()
    with st.expander("Algorithm info"):
        if algorithm == "Binary Search":
            st.markdown(
                "**Binary Search** requires a sorted array and repeatedly halves the "
                "search range.  \nTime complexity: **O(log n)**"
            )
        else:
            st.markdown(
                "**Linear Search** checks each element one by one from left to right.  \n"
                "Time complexity: **O(n)**"
            )


# ── Benchmark page ────────────────────────────────────────────────────────────
else:
    st.subheader("Benchmark Tests")
    st.caption(
        "Reproduces the test_search_algorithms.py benchmark across array sizes "
        "100, 1 000, and 10 000."
    )

    sizes_options = st.multiselect(
        "Array sizes to benchmark",
        options=[100, 1_000, 10_000, 100_000],
        default=[100, 1_000, 10_000],
    )
    runs = st.slider("Runs per configuration (averaged)", min_value=1, max_value=20, value=5)

    if st.button("Run Benchmark"):
        if not sizes_options:
            st.warning("Select at least one array size.")
            st.stop()

        rows = []
        with st.spinner("Running benchmarks..."):
            for size in sorted(sizes_options):
                arr_bench = sorted(random.sample(range(size * 10), size))
                target_hit = random.choice(arr_bench)
                target_miss = -1

                for target, label in [(target_hit, "hit"), (target_miss, "miss")]:
                    for name, fn in [("binary_search", binary_search), ("linear_search", linear_search)]:
                        result, avg, lo, hi = time_search(fn, arr_bench, target, runs=runs)
                        rows.append({
                            "Size": size,
                            "Algorithm": name,
                            "Target": label,
                            "Result": result,
                            "Avg Time (ms)": round(avg, 6),
                            "Min Time (ms)": round(lo, 6),
                            "Max Time (ms)": round(hi, 6),
                        })

        df = pd.DataFrame(rows)

        tab_table, tab_line, tab_bar = st.tabs(["Table", "Line Chart", "Bar Chart"])

        with tab_table:
            st.dataframe(df, use_container_width=True)

        pivot = df.pivot_table(
            index="Size",
            columns=["Algorithm", "Target"],
            values="Avg Time (ms)",
        )
        pivot.columns = [f"{alg} ({lbl})" for alg, lbl in pivot.columns]

        with tab_line:
            st.subheader("Avg Execution Time by Array Size")
            st.line_chart(pivot)

        with tab_bar:
            st.subheader("Avg Execution Time per Configuration")
            bar_df = df.copy()
            bar_df["Config"] = bar_df["Algorithm"] + " (" + bar_df["Target"] + ")"
            bar_pivot = bar_df.pivot_table(
                index="Config", columns="Size", values="Avg Time (ms)"
            )
            st.bar_chart(bar_pivot)
