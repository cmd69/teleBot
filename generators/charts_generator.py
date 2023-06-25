import os
import pandas as pd
import datetime
from streamlit_elements import elements, mui, html
from streamlit_elements import nivo



class ChartsGenerator:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    

    def _load_data(self, chatID=os.environ.get('ALTOKE_CHATID')):
    # def _load_data(self, chatID):
        return self.db_manager.get_all_expenses(chatID)
    
    
    def _get_chatID_from_token(self, token):
        return self.db_manager.get_chatID_from_token(token)


    # Extract expenses per category FOREACH CATEGORY
    # JSON ----> JSON
    def _expenses_to_categories(self, data):
        number_months = 0
        total_income_count = 0
        categories = {}
        for year in data['years']:

                for month in year['months']:
                    
                    expenses_list = month["expenses"]
                    income_list = month["income"]
                    if income_list:
                        total_income_count += month["totalIncome"]
                        
                    if income_list or expenses_list:
                        number_months += 1
                    for expense in month['expenses']:
                        category = expense['category']
                        price = expense['price']
                        if category in categories:
                            categories[category]['total'] += price
                        else:
                            categories[category] = {'total': price}

        # Create a pretty table

        if total_income_count > 0 and number_months > 0:
            average_income = total_income_count / number_months
        else:
            average_income = 0

        df_rows = []
        # Calculate average expense and percentage for each category
        for category, data in categories.items():
            average_expense = 0
            expense_percentage = 0
            if number_months != 0:
                average_expense = data['total'] / number_months
            if average_income != 0:
                expense_percentage = (average_expense / average_income) * 100
            df_rows.append([category, round(average_expense, 2), round(expense_percentage, 1)])
        
        return pd.DataFrame(df_rows, columns=['Category', 'Spent', '%'])


    # Extract expenses/incomes FOREACH YEAR
    # JSON ----> JSON
    def _expenses_to_general(self, data):
        df_rows = []
        for year_data in data['years']:
            year = int(year_data['year'])
            for month_data in year_data['months']:
                month = int(month_data['month'])
                total_expenses = month_data['totalExpenses']
                total_income = month_data['totalIncome']
                # Create a date with the year, month, and a default day of 1
                date = datetime.date(year, month, 1)
                df_rows.append([date, total_expenses, total_income])
        # Create the DataFrame
        df_expenses_incomes = pd.DataFrame(df_rows, columns=['Date', 'Total Expenses', 'Total Income'])
        df_expenses_incomes['Net Expenses'] = df_expenses_incomes['Total Income'] - df_expenses_incomes['Total Expenses']

        return df_expenses_incomes


    def df_to_piechart_json(self, df):
        json_list = []
        for index, row in df.iterrows():
            json_dict = {}
            json_dict["id"] = str(row["Category"]) + " " + str(row["%"]) + " %"
            json_dict["label"] = row["Category"]
            json_dict["value"] = row["Spent"]
            json_list.append(json_dict)
        return json_list


    def df_to_linechart_json(self, df):
        # Initialize an empty list for each line in the chart
        income_data = []
        expenses_data = []
        net_income_data = []

        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            # Append a dictionary for each data point in each line
            income_data.append({"x": row["Date"].strftime('%Y-%m-%d'), "y": row["Total Income"]})
            expenses_data.append({"x": row["Date"].strftime('%Y-%m-%d'), "y": row["Total Expenses"]})
            net_income_data.append({"x": row["Date"].strftime('%Y-%m-%d'), "y": row["Net Expenses"]})

        # Return a list of dictionaries, where each dictionary represents a line in the chart
        return [
            {"id": "Income", "data": income_data},
            {"id": "Expenses", "data": expenses_data},
            {"id": "Net Income", "data": net_income_data}
        ]


    def generate_expenses_piechart(self, token):
        if (token == None):
            data = self._load_data()
        else:
            chatID = self._get_chatID_from_token(token)
            data = self._load_data(chatID)

        piechart_df = self._expenses_to_categories(data)
        piechart_data = self.df_to_piechart_json(piechart_df)

        with elements("nivo_charts"):

            # Streamlit Elements includes 45 dataviz components powered by Nivo.        
            with mui.Box(sx={"height": 500}):
                nivo.Pie(
                    data=piechart_data,
                    margin={ "top": 40, "right": 80, "bottom": 80, "left": 80 },
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    borderWidth=1,
                    borderColor={
                        "from": 'color',
                        "modifiers": [
                            [
                                'darker',
                                0.2
                            ]
                        ]
                    },
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="#333333",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={ "from": 'color' },
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={
                        "from": 'color',
                        "modifiers": [
                            [
                                'darker',
                                2
                            ]
                        ]
                    },
                    defs=[
                        {
                            "id": 'dots',
                            "type": 'patternDots',
                            "background": 'inherit',
                            "color": 'rgba(255, 255, 255, 0.3)',
                            "size": 4,
                            "padding": 1,
                            "stagger": True
                        },
                        {
                            "id": 'lines',
                            "type": 'patternLines',
                            "background": 'inherit',
                            "color": 'rgba(255, 255, 255, 0.3)',
                            "rotation": -45,
                            "lineWidth": 6,
                            "spacing": 10
                        }
                    ],
                    fill=[
                        {
                            "match": {
                                "id": 'ruby'
                            },
                            "id": 'dots'
                        },
                        {
                            "match": {
                                "id": 'c'
                            },
                            "id": 'dots'
                        },
                        {
                            "match": {
                                "id": 'go'
                            },
                            "id": 'dots'
                        },
                        {
                            "match": {
                                "id": 'python'
                            },
                            "id": 'dots'
                        },
                        {
                            "match": {
                                "id": 'scala'
                            },
                            "id": 'lines'
                        },
                        {
                            "match": {
                                "id": 'lisp'
                            },
                            "id": 'lines'
                        },
                        {
                            "match": {
                                "id": 'elixir'
                            },
                            "id": 'lines'
                        },
                        {
                            "match": {
                                "id": 'javascript'
                            },
                            "id": 'lines'
                        }
                    ],
                    legends=[
                        {
                            "anchor": 'bottom',
                            "direction": 'row',
                            "justify": False,
                            "translateX": 0,
                            "translateY": 56,
                            "itemsSpacing": 0,
                            "itemWidth": 40,
                            "itemHeight": 20,
                            "itemTextColor": '#999',
                            "itemDirection": 'top-to-bottom',
                            "itemOpacity": 4,
                            "symbolSize": 18,
                            "symbolShape": 'circle',
                            "effects": [
                                {
                                    "on": 'hover',
                                    "style": {
                                        "itemTextColor": '#000'
                                    }
                                }
                            ]
                        }
                    ]
                )


    def generate_general_linechart(self, token):
        if (token == None):
            data = self._load_data()
        else:
            chatID = self._get_chatID_from_token(token)
            data = self._load_data(chatID)
        
        linechart_df = self._expenses_to_general(data)
        linechart_data = self.df_to_linechart_json(linechart_df)
        
        with elements("nivo_charts"):
            # Streamlit Elements includes 45 dataviz components powered by Nivo.        
            with mui.Box(sx={"height": 500}):
                nivo.Line(
                    data=linechart_data,
                    margin={ "top": 50, "right": 110, "bottom": 50, "left": 60 },
                    xScale={ "type": 'point' },
                    yScale={
                        "type": 'linear',
                        "min": 'auto',
                        "max": 'auto',
                        "stacked": False,
                        "reverse": False
                    },
                    yFormat=" >-.2f",
                    curve="catmullRom",
                    axisTop=None,
                    axisRight=None,
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 30,
                        "tickValues": 5,
                        "legend": '',
                        "legendOffset": 40,
                        "legendPosition": 'middle'
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": 'count',
                        "legendOffset": -40,
                        "legendPosition": 'middle'
                    },
                    enableGridX=False,
                    colors={ "scheme": 'category10' },
                    pointColor={ "from": 'color', "modifiers": [] },
                    pointBorderWidth=2,
                    pointBorderColor={ "from": 'serieColor', "modifiers": [] },
                    pointLabel="y",
                    pointLabelYOffset=-14,
                    useMesh=True,
                    legends=[
                        {
                            "anchor": 'bottom-right',
                            "direction": 'column',
                            "justify": False,
                            "translateX": 100,
                            "translateY": 0,
                            "itemsSpacing": 0,
                            "itemDirection": 'left-to-right',
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemOpacity": 0.75,
                            "symbolSize": 12,
                            "symbolShape": 'circle',
                            "symbolBorderColor": 'rgba(0, 0, 0, .5)',
                            "effects": [
                                {
                                    "on": 'hover',
                                    "style": {
                                        "itemBackground": 'rgba(0, 0, 0, .03)',
                                        "itemOpacity": 1
                                    }
                                }
                            ]
                        }
                    ],
                    motionConfig="wobbly"
            )


    def generate_categories_checkbox(self, token):
        if (token == None):
            data = self._load_data()
        else:
            chatID = self._get_chatID_from_token(token)
            print(chatID)
            data = self._load_data(chatID)
        
        df_categories = self._expenses_to_categories(data)
        categories = df_categories['Category'].tolist()

        categories_checkbox = pd.DataFrame(
            {
                "widgets": categories,
                "selected": [True for _ in range(len(categories))]
            }
        )
        return categories_checkbox