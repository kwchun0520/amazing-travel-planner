import streamlit as st
import datetime
import asyncio
from src.graphs.runner import run_planner


@st.dialog("Travel Plan",width="large")
def travel_planner_output(interests: str,
                         country: str,
                         trip_length: int = 7,
                         budget: str = "moderate",
                         travel_style: str = "chilling",
                         travel_date: str = "2024-01-01"):
    """Run the travel planner with the given parameters."""
    
    st.markdown("### Final Travel Plan:")
    st.write("Your travel plan will be displayed here after submission.")
    
    with st.spinner("Generating your travel plan..."):
            # Run the planner with the provided inputs
            final = asyncio.run(run_planner(interests=interests, 
                                            country=country, 
                                            trip_length=trip_length, 
                                            budget=budget, 
                                            travel_style=travel_style, 
                                            travel_date=travel_date
            ))
    st.success("Travel plan generated successfully!")
    st.markdown("### Final Travel Plan:")
    st.markdown(final)
    
    st.download_button(
        label="Download Travel Plan",
        data=final,
        file_name=f"travel_plan_{country}_{travel_date}.txt",
        mime="text/plain"
    )
        
        
def main():
    st.title("Travel Planner")

    # Country Input
    country = st.text_input("Enter your desired country:")

    # Date Input
    travel_date = st.date_input("Select your travel date:", datetime.date.today())

    # Hobbies Input (String)
    interests = st.text_area("Tell us about your interests (comma-separated if multiple):",
                           help="e.g., hiking, photography, cooking")

    # Travel Style Input (Dropdown)
    travel_style_options = ["Adventure", "Relaxation", "Cultural Immersion", "Budget", "Luxury", "Family-friendly", "Romantic"]
    travel_style = st.selectbox("Choose your travel style:", travel_style_options)
    
    # Budget Input (Slider)
    budget = st.select_slider("Select your budget range:",
                              options=["Low", "Moderate", "High"],
                              value="Moderate",
                              help="Select your budget range for the trip.")
    
    # Trip Length Input (Number Input)
    st.subheader("Trip Length")
    trip_length = st.number_input("Enter the length of your trip (in days):", min_value=1, max_value=30, value=7)
    

    if st.button("Submit"):
        travel_planner_output(
            interests=interests,
            country=country,
            trip_length=trip_length,
            budget=budget,
            travel_style=travel_style,
            travel_date=str(travel_date)
        )

if __name__ == "__main__":
    main()