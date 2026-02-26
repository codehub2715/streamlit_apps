#AI Lifestyle & Energy Predictor

#Main sections of the app:
#1) Title and description
#2) Input section (columns layout for better design)
#3) Predict button and result display
#4) Suggestions based on input values
#5) Feature importance chart
#6) Display sample training data
#You will use col1, col2, col3 from st.columns for organizing inputs.


import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(page_title='AI Lifestyle & Energy Predictor', layout='wide')

st.title('AI Lifestyle & Energy Predictor')

@st.cache_data
def load_data_and_model():
    data = {
        'sleep_hours': [7, 5, 8, 6, 4, 9, 7],
        'steps': [8000, 3000, 10000, 6000, 2000, 12000, 7500],
        'workout_intensity': [2, 0, 3, 1, 0, 3, 2],
        'junk_food_level': [1, 3, 1, 2, 3, 1, 2],
        'screen_time': [4, 7, 3, 5, 8, 2, 4],
        'stress_level': [3, 8, 2, 5, 9, 2, 4],
        'energy_score': [80, 40, 90, 70, 30, 95, 75]
    }
    df = pd.DataFrame(data)
    X = df.drop('energy_score', axis=1)
    y = df['energy_score']
    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)
    return df, X, model

train_df, X, model = load_data_and_model()

st.subheader('Enter today\'s lifestyle details')

col1, col2, col3 = st.columns(3)

with col1:
    sleep_hours = st.slider('Sleep hours', 3.0, 10.0, 7.0, 0.5)
    steps = st.number_input('Steps walked', 0, 30000, 8000, 500)

with col2:
    workout_intensity = st.selectbox('Workout intensity', ['None', 'Light', 'Medium', 'Heavy'])
    junk_food_level = st.selectbox('Junk food intake', ['Low', 'Medium', 'High'])

with col3:
    screen_time = st.slider('Screen time (hours)', 1.0, 12.0, 5.0, 0.5)
    stress_level = st.slider('Stress level (1-10)', 1, 10, 4)

workout_map = {'None': 0, 'Light': 1, 'Medium': 2, 'Heavy': 3}
junk_map = {'Low': 1, 'Medium': 2, 'High': 3}

input_row = pd.DataFrame({
    'sleep_hours': [sleep_hours],
    'steps': [steps],
    'workout_intensity': [workout_map[workout_intensity]],
    'junk_food_level': [junk_map[junk_food_level]],
    'screen_time': [screen_time],
    'stress_level': [stress_level]
})

if st.button('Predict Energy'):
    pred = model.predict(input_row)[0]
    st.session_state.pred_int = int(pred)

    st.subheader(f'Predicted Energy Score Today: {st.session_state.pred_int}/100')
    suggestions = []
    if sleep_hours < 7:
        suggestions.append('Increase sleep towards 7–8 hours.')
    if steps < 6000:
        suggestions.append('Increase movement, target at least 6000–8000 steps.')
    if junk_food_level == 'High':
        suggestions.append('Reduce junk food intake to improve energy.')
    if screen_time > 7:
        suggestions.append('Try to reduce screen time, especially at night.')
    if stress_level > 6:
        suggestions.append('Use small breaks, breathing, or walking to reduce stress.')

    st.subheader('Suggestions to improve energy')
    if suggestions:
        for s in suggestions:
            st.write('- ' + s)
    else:
        st.write('Your habits look quite balanced. Maintain consistency.')

    feat_imp = model.feature_importances_
    imp_df = pd.DataFrame({'feature': X.columns, 'importance': feat_imp}).sort_values('importance', ascending=False)

    st.subheader('Which habits influence energy the most (model view)')
    fig = px.bar(imp_df, x='feature', y='importance')
    st.plotly_chart(fig, use_container_width=True)

st.subheader('Sample training data')
st.dataframe(train_df)

#mini task----
#Allow user to log data daily and store it in a CSV.

st.subheader("Log Today's Data")

if st.button("Save Today's Data"):

    if 'pred_int' not in st.session_state:
        st.warning("Please click 'Predict Energy' first.")
    else:
        log_df = input_row.copy()
        log_df['energy_score'] = st.session_state.pred_int
        log_df['date'] = datetime.now().strftime('%Y-%m-%d')

        if os.path.exists('lifestyle_log.csv'):
            log_df.to_csv('lifestyle_log.csv', mode='a', header=False, index=False)
        else:
            log_df.to_csv('lifestyle_log.csv', index=False)

        st.success("Data logged successfully!")

    st.subheader("Log History")
    hist_df = pd.read_csv('lifestyle_log.csv')
    st.dataframe(hist_df)

#Show last 7 or 30 days energy score trend with line chart.

st.subheader("Energy Score Trend")

if os.path.exists("lifestyle_log.csv"):

    hist_df = pd.read_csv("lifestyle_log.csv")

    if not hist_df.empty:

        hist_df["date"] = pd.to_datetime(hist_df["date"])
       
        hist_df = hist_df.sort_values("date")
    days_option = st.radio( "Select Trend Period",["Last 7 Days", "Last 30 Days"],horizontal=True)

    if days_option == "Last 7 Days":
        filtered_df = hist_df.tail(7)
    else:
        filtered_df = hist_df.tail(30)
    fig = px.line(filtered_df,x="date",y="energy_score",markers=True,title=f"{days_option} Energy Score Trend")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Log some data and predict energy to see the trend.")