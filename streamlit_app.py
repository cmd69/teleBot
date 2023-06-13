import streamlit as st
from streamlit_elements import elements, mui, html
from streamlit_elements import nivo
import pandas as pd
from dotenv import load_dotenv
from streamlit_elements import dashboard
from telebot import chartsGenerator



def main():

    # PAGE CONFIG
    st.set_page_config(page_title="Portfolio Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide"
    )
    st.title("Main Page")
    st.sidebar.success("Select a page")
    
    
    categories_checkbox = chartsGenerator.generate_categories_checkbox(None)

    # SIDEBAR
    with st.sidebar:
        st.data_editor(
                    categories_checkbox,
                    column_config={
                        "selected": st.column_config.CheckboxColumn(
                            "Your favorite?",
                            help="Select your **favorite** widgets",
                            default=True,
                        )
                    },
                    disabled=["widgets"],
                    hide_index=True,
                    key="third-element"
                )

    # SETUP DASHBOARD
    with elements("dashboard"):

        layout = [
            dashboard.Item("first_item", 0, 0, 5, 3),
            dashboard.Item("second_item", 5, 0, 7, 3),
            dashboard.Item("third_item", 0, 2, 12, 3),
        ]

        def handle_layout_change(updated_layout):
            # You can save the layout in a file, or do anything you want with it.
            # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
            return updated_layout

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            with mui.Box(key="first_item"):
                chartsGenerator.generate_expenses_piechart(None)
            with mui.Box(key="second_item"):
                chartsGenerator.generate_general_linechart(None)
            with mui.Box(key="third_item"):
                chartsGenerator.generate_general_linechart(None)

                
# Run the app
if __name__ == "__main__":
   main()