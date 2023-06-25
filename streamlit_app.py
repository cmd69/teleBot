import streamlit as st
from streamlit_elements import elements, mui
from streamlit_elements import dashboard
from telebot import chartsGenerator
from PIL import Image



def main():

    # User data validation
    if (st.experimental_get_query_params().get("access_token") == None):
        access_token = 0
    else:
        access_token = st.experimental_get_query_params().get("access_token")[0]
        print(access_token)

    print(0)
    # PAGE CONFIG
    st.set_page_config(page_title="Portfolio Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide"
    )



    try: 

        categories_checkbox = chartsGenerator.generate_categories_checkbox(access_token)

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
                    chartsGenerator.generate_expenses_piechart(access_token)
                with mui.Box(key="second_item"):
                    chartsGenerator.generate_general_linechart(access_token)
                with mui.Box(key="third_item"):
                    chartsGenerator.generate_general_linechart(access_token)
        
        # PAGE CONFIG
        st.title("Main Page")
        st.subheader("Bienvenido")
        st.sidebar.success("Select a page")

    except:

        image = Image.open('images/access_denied.png')
        st.image(image)

                
# Run the app
if __name__ == "__main__":
   main()