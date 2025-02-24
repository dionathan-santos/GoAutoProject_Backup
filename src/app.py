import streamlit as st
import pandas as pd
import altair as alt


class DealershipInsightsApp:
    def __init__(self):
        self.html_file_path = "app_files/Dealership-map.html"
        self.used_cars_file = "app_files/used_cars.csv"
        self.new_cars_file = "app_files/new_cars.csv"

    def render_map(self):
        st.subheader("🗺️ Dealership Locations")
        try:
            with open(self.html_file_path, "r", encoding="utf-8") as f:
                map_html = f.read()
            st.components.v1.html(map_html, height=600, scrolling=True)
        except FileNotFoundError:
            st.error("The HTML file containing the map was not found. Please check the file path.")

    def render_sales_comparison(self):
        df_used = pd.read_csv(self.used_cars_file)
        df_new = pd.read_csv(self.new_cars_file)

        df_used["car_type"] = "Used"
        df_new["car_type"] = "New"

        df_combined = pd.concat([df_used, df_new], ignore_index=True)
        sales_data = df_combined.groupby(["region_label", "car_type"]).size().reset_index(name="cars_sold")

        st.subheader("🚗 Used vs New Cars Sold in Edmonton Regions")
        chart = alt.Chart(sales_data).mark_bar().encode(
            x=alt.X('region_label:N', title='Region'),
            y=alt.Y('cars_sold:Q', title='Number of Cars Sold'),
            color=alt.Color('car_type:N', title='Car Type', scale=alt.Scale(domain=["Used", "New"], range=["#FF6F61", "#C0392B"])),
            tooltip=['region_label', 'car_type', 'cars_sold']
        ).properties(
            width=800,
            height=500
        )
        st.altair_chart(chart, use_container_width=True)

    def render_price_vs_year(self, df_combined):
        price_by_year = df_combined.groupby("model_year")["price"].mean().reset_index().sort_values(by="model_year")

        st.subheader("📈 Average Price vs Model Year")
        line_chart = alt.Chart(price_by_year).mark_line(color="#C0392B").encode(
            x=alt.X('model_year:Q', title='Model Year'),
            y=alt.Y('price:Q', title='Average Price'),
            tooltip=['model_year', 'price']
        ).properties(
            width=800,
            height=500
        )
        st.altair_chart(line_chart, use_container_width=True)

    def render_top_10_makes(self, df_combined):
        sales_data_makes = (
            df_combined.groupby(["make", "car_type"])["vin"]
            .count()
            .reset_index(name="cars_sold")
        )
        total_sales_per_make = (
            sales_data_makes.groupby("make")["cars_sold"]
            .sum()
            .reset_index(name="total_cars_sold")
        )
        top_10_makes = total_sales_per_make.sort_values(by="total_cars_sold", ascending=False).head(10)["make"]
        top_sales_data = sales_data_makes[sales_data_makes["make"].isin(top_10_makes)]

        st.subheader("📊 Top 10 Car Makes (Used vs New)")
        chart = alt.Chart(top_sales_data).mark_bar().encode(
            x=alt.X('make:N', sort=top_10_makes, title='Make'),
            y=alt.Y('cars_sold:Q', title='Number of Cars Sold'),
            color=alt.Color('car_type:N', title='Stock Type', scale=alt.Scale(domain=["Used", "New"], range=["#FF6F61", "#C0392B"])),
            tooltip=['make', 'car_type', 'cars_sold']
        ).properties(
            width=800,
            height=500
        )
        st.altair_chart(chart, use_container_width=True)

    def run(self):
        st.title("🚗 Dealership and Sales Insights in Edmonton")
        self.render_map()
        self.render_sales_comparison()
        df_combined = pd.concat(
            [pd.read_csv(self.used_cars_file).assign(car_type="Used"),
             pd.read_csv(self.new_cars_file).assign(car_type="New")],
            ignore_index=True
        )
        self.render_price_vs_year(df_combined)
        self.render_top_10_makes(df_combined)


# Run the app
if __name__ == "__main__":
    app = DealershipInsightsApp()
    app.run()
