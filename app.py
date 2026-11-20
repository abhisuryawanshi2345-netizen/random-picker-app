import re
import secrets
import time
import streamlit as st

st.set_page_config(page_title="Random Picker", page_icon="🎲", layout="centered")

st.title("🎲 Random Picker")
st.write("Enter names, games, or any list of items below and pick one at random.")

# Initialize pick history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Optional category label
category = st.selectbox(
    "What are you picking?",
    ["Person Name", "Game Name", "Movie / Show", "Custom Item"],
)

# Input box (supports one item per line or comma-separated)
raw_input = st.text_area(
    f"Enter {category.lower()}s (one per line or separated by commas):",
    height=180,
    placeholder="Example:\nRahul\nSneha\nAmit\nPriya",
)

no_repeat = st.checkbox("Don't repeat items already picked", value=False)

# Parse and clean the list
items = [item.strip() for item in re.split(r"[,\n]+", raw_input) if item.strip()]

col1, col2 = st.columns([2, 1])

with col1:
    pick_clicked = st.button("🎯 Pick Random Result", type="primary", use_container_width=True)

with col2:
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Handle the random pick
if pick_clicked:
    if len(items) < 2:
        st.warning("Please enter at least 2 items to pick from.")
    else:
        pool = [i for i in items if i not in st.session_state.history] if no_repeat else items

        if not pool:
            st.info("Every item in your list has already been picked! Click **Clear History** to reset.")
        else:
            # Quick shuffle animation
            slot = st.empty()
            for _ in range(12):
                slot.markdown(f"### Rolling... **{secrets.choice(pool)}**")
                time.sleep(0.06)

            winner = secrets.choice(pool)
            st.session_state.history.append(winner)

            slot.empty()
            st.success(f"### 🎉 Selected {category}: **{winner}**")
            st.balloons()

# Show previous picks
if st.session_state.history:
    st.divider()
    st.subheader("Previous Picks")
    for idx, picked in enumerate(reversed(st.session_state.history), start=1):
        st.write(f"{idx}. {picked}")
