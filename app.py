from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Define all possible options
all_options = {
    'maritalStatus': ['Current marital status_Living with partner', 'Current marital status_Married',
                      'Current marital status_Never in union', 'Current marital status_No longer living together/separated',
                      'Current marital status_Widowed'],
    'livingArrangement': ['Currently residing with husband/partner_Not Available (single)',
                          'Currently residing with husband/partner_Staying elsewhere'],
    'stateOfResidence': ['State of residence_Adamawa', 'State of residence_Akwa Ibom', 'State of residence_Anambra',
                         'State of residence_Bauchi', 'State of residence_Bayelsa', 'State of residence_Benue',
                         'State of residence_Borno', 'State of residence_Cross River', 'State of residence_Delta',
                         'State of residence_Ebonyi', 'State of residence_Edo', 'State of residence_Ekiti',
                         'State of residence_Enugu', 'State of residence_FCT Abuja', 'State of residence_Gombe',
                         'State of residence_Imo', 'State of residence_Jigawa', 'State of residence_Kaduna',
                         'State of residence_Kano', 'State of residence_Katsina', 'State of residence_Kebbi',
                         'State of residence_Kogi', 'State of residence_Kwara', 'State of residence_Lagos',
                         'State of residence_Nasarawa', 'State of residence_Niger', 'State of residence_Ogun',
                         'State of residence_Ondo', 'State of residence_Osun', 'State of residence_Oyo',
                         'State of residence_Plateau', 'State of residence_Rivers', 'State of residence_Sokoto',
                         'State of residence_Taraba', 'State of residence_Yobe', 'State of residence_Zamfara'],
    'religion': ['Religion_Islam', 'Religion_Other', 'Religion_Other Christian', 'Religion_Traditionalist'],
    'ethnicity': ['Ethnicity_Ekoi', 'Ethnicity_Fulani', 'Ethnicity_Hausa', 'Ethnicity_Ibibio', 'Ethnicity_Igala',
                  'Ethnicity_Igbo', 'Ethnicity_Ijaw/Izon', 'Ethnicity_Kanuri/Beriberi', 'Ethnicity_Other',
                  'Ethnicity_Tiv', 'Ethnicity_Yoruba']
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart/')
def chart():
    # Load the entire dataset from a CSV file
    dataset_path = 'selected1.csv'
    df = pd.read_csv(dataset_path)
    marital_status = df['Current marital status'].value_counts().index.tolist()
    marital_status_counts = df['Current marital status'].value_counts().values.tolist()
    religion_status = df['Religion'].value_counts().index.tolist()
    religion_status_counts = df['Religion'].value_counts().values.tolist()
    ethnicity_status = df['Ethnicity'].value_counts().index.tolist()
    ethnicity_status_counts = df['Ethnicity'].value_counts().values.tolist()
    smoke_status = df['Smoke_cigarate'].value_counts().index.tolist()
    smoke_status_counts = df['Smoke_cigarate'].value_counts().values.tolist()
    risk_status = df['risk_category'].value_counts().index.tolist()
    risk_status_counts = df['risk_category'].value_counts().values.tolist()
    age_status = df["Respondent's current age"].value_counts().index.tolist()
    age_status_counts = df["Respondent's current age"].value_counts().values.tolist()
    df_head = df.head()
    return render_template('chart.html', df_head=df_head,
                           marital_status=marital_status, marital_status_counts=marital_status_counts,
                           religion_status=religion_status, religion_status_counts=religion_status_counts,
                           ethnicity_status=ethnicity_status, ethnicity_status_counts=ethnicity_status_counts,
                           smoke_status=smoke_status, smoke_status_counts=smoke_status_counts,
                           risk_status=risk_status, risk_status_counts=risk_status_counts,
                           age_status=age_status, age_status_counts=age_status_counts)

@app.route('/predict/', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Load the machine learning model
        model_path = 'xgb_model_pkl.pkl'
        loaded_model = pickle.load(open(model_path, 'rb'))

        # Initialize input data dictionary with all options set to 0
        input_data = {option: 0 for option_list in all_options.values() for option in option_list}

        # Get form data and set the selected options to 1
        selected_options = {}
        for option_name, option_list in all_options.items():
            selected_option = request.form.get(option_name)
            selected_options[option_name] = selected_option
            if selected_option in option_list:
                input_data[selected_option] = 1

        # Get additional form data
        age = int(request.form['age'])
        education = int(request.form['education'])
        total_children = int(request.form['totalChildren'])
        smokes_cigarettes = 1 if request.form['smokesCigarettes'] == 'Yes' else 0

        # Set additional form data to input_data
        input_data['Respondent\'s Current Age'] = age
        input_data['Education in Single Years'] = education
        input_data['Total Children Ever Born'] = total_children
        input_data['Smokes Cigarettes_Yes'] = smokes_cigarettes

        # Prepare input data for prediction
        input_data = [list(input_data.values())]

        # Make prediction using the loaded model
        prediction = loaded_model.predict(input_data)

        # Render the result template with only the prediction value
        return render_template('result.html', prediction=prediction[0])

    return "Method not allowed"

if __name__ == '__main__':
    app.run(debug=True, port=(5100))
