import pandas as pd
from main.utils import get_rate

def convert_form_to_model_input(form, model_columns):

    new_car = dict.fromkeys(model_columns, 0)

    # numeric fields
    new_car['model_year'] = form.model_year.data
    new_car['milage'] = form.milage.data
    new_car['transmission'] = int(form.transmission.data)
    new_car['condition'] = int(form.condition.data)
    new_car['cc'] = form.cc.data
    new_car['age'] = form.age.data
    new_car['power_steering'] = int(form.power_steering.data)
    new_car['push_start'] = int(form.push_start.data)

    # one hot
    new_car[form.car_model.data] = 1
    new_car[form.fuel_type.data] = 1
    new_car[form.location.data] = 1
    new_car[form.vehicle_type.data] = 1
    new_car[form.color.data] = 1

    return new_car

def predict_price(input_dict, model,model_columns):

    input_df = pd.DataFrame([input_dict])
    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    print("\nFinal model input:")
    #print(input_df.T)

    prediction = model.predict(input_df)

    return round(prediction[0], 2)


def apply_dollar_adjustment():
    dollar_rate = get_rate()

    if 125 < dollar_rate <= 175:
        factor = 0.542
    elif 175 < dollar_rate <= 225:
        factor = 0.8275
    elif 225 < dollar_rate <= 275:
        factor = 0.9132
    elif 275 < dollar_rate <= 325:
        factor = 1
    else:  # > 325
        factor = 1.072

    return factor