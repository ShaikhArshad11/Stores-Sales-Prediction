from flask import Flask , request, render_template
import pickle
import numpy as np
from mongodb import db_ops
from src.logger import logging
from src.exception import CustomException
import sys

application =Flask(__name__)
app = application
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    logging.info("Initiated 'index.html'")
    try:
        return render_template('index.html')
    except Exception as e:
        raise CustomException(e,sys) from e

@app.route('/predict', methods = ['GET','POST'])
def predict():
    logging.info("Started '/predict' api")
    try:
        Item_Weight= float(request.form['Item_Weight'])
        Item_Fat_Content=int(request.form['Item_Fat_Content'])
        Item_Visibility= float(request.form['Item_Visibility'])
        Item_Type= int(request.form['Item_Type'])
        Item_MRP= float(request.form['Item_MRP'])
        Outlet_Location_Type= int(request.form['Outlet_Location_Type'])
        Outlet_Size= int(request.form['Outlet_Size'])
        Outlet_Type_Supermarket_Type1= int(request.form['Outlet_Type_Supermarket_Type1'])
        Outlet_Type_Supermarket_Type2= int(request.form['Outlet_Type_Supermarket_Type2'])
        Outlet_Type_Supermarket_Type3= int(request.form['Outlet_Type_Supermarket_Type3'])

        x = np.array([[ Item_Weight,Item_Fat_Content,Item_Visibility,Item_Type,Item_MRP,
        Outlet_Location_Type,Outlet_Size,Outlet_Type_Supermarket_Type1,
        Outlet_Type_Supermarket_Type2,Outlet_Type_Supermarket_Type3 ]])
    
        prediction = model.predict(x)
        output = prediction**3
        output = round(output[0], 2)
        #return jsonify({'Prediction': float(prediction)})

        return render_template('index.html', prediction_text='Predicted Sales $ {}'.format(output))
    
    except Exception as e:
            raise CustomException(e,sys) from e

@app.route('/predict_all', methods=['POST'])
def predict_all():
    logging.info("Started '/predict_all' api")
    try:
        data = [x for x in request.form.values()]
        #[np.array(data)]
        database=''.join(data[-2:-1])
        collection=''.join(data[-1:])
        print(database,collection)

        db_obj = db_ops(database, collection)
        df = db_obj.load_df()
        print(df)
        if type(df) == str:
            return render_template('index.html', Error=df)
        else:
            #Test transformation
            X=df[[x for x in df.columns if x != 'Classes']]
            print(X)
            my_prediction=model.predict(X.values)
            output = my_prediction**3
            output=output.tolist()
            return render_template('index.html',prediction = output)
        
    except Exception as e:
            raise CustomException(e,sys) from e

if __name__ == "__main__":
    app.run()