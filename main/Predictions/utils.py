import pandas as pd

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
