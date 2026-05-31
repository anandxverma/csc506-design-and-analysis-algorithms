# Milestone 2 — Search Algorithms

Implements and benchmarks **Binary Search** and **Linear Search** with a CLI benchmark script and an interactive Streamlit UI.

## Files

| File | Description |
|---|---|
| [search_algorithms.py](search_algorithms.py) | Core algorithm implementations (`binary_search`, `linear_search`, `time_search`) |
| [test_search_algorithms.py](test_search_algorithms.py) | CLI benchmark script — prints timing results to the terminal |
| [search_ui.py](search_ui.py) | Interactive Streamlit app with Search and Benchmark pages |

## Prerequisites

Python 3.8+ is required. Install dependencies with:

```bash
pip install streamlit pandas
```

## Running the CLI Benchmark

From the `ms2/` directory:

```bash
python test_search_algorithms.py
```

The script runs both algorithms against randomly generated sorted arrays of sizes 100, 1 000, and 10 000. Each configuration is repeated 5 times. Output is printed as a table:

```
Size       Algorithm        Target   Result     Avg (ms)       Min (ms)       Max (ms)
--------------------------------------------------------------------------------
100        binary_search    hit      42         0.001234       0.001100       0.001500
100        binary_search    miss     -1         0.000987       0.000900       0.001100
...
```

**Columns:**

- **Size** — number of elements in the array
- **Algorithm** — `binary_search` or `linear_search`
- **Target** — `hit` (target exists in array) or `miss` (target is `-1`, not present)
- **Result** — index returned by the algorithm (`-1` means not found)
- **Avg / Min / Max (ms)** — timing across 5 runs in milliseconds

## Running the Interactive UI

From the `ms2/` directory:

```bash
streamlit run search_ui.py
```

Streamlit will open the app in your browser (default: `http://localhost:8501`).

### Search page

1. Enter a comma-separated list of integers in the **Input Array** field.
2. Select **Binary Search** or **Linear Search** from the sidebar.
3. Enter a **Target value** and click **Search**.
4. The result index is highlighted visually in the array display.

> Binary Search automatically sorts the input array.

### Benchmark page

1. Select one or more **array sizes** (100, 1 000, 10 000, 100 000).
2. Adjust the **Runs per configuration** slider (1–20).
3. Click **Run Benchmark**.
4. Results are shown in three tabs: **Table**, **Line Chart**, and **Bar Chart**.
