from flask import * 
import predict


# Initialising flask
app = Flask(__name__) 



# Defining the route for the main() funtion
@app.route("/", methods=["POST", "GET"]) 
def main():
    past, future = predict.predict(model, target, past, future, std_path, data_path)
    dates = predict.getDate(data_path, past, future)

    past = past.tolist()
    past = past + [None, None, None, None, None]
    future = future.tolist()
    future = [None, None, None, None, None, None, None, None, None, past[9]] + future 
    # print("past >>>>> ", past, "future >>>>> ", future)
    temp = 0
    # data = {'past': [1,5,7,2,5,6,9,2,1,10]}
    data = {'past': past, 'future': future, 'dates': dates}
    # print(type(past))
    # print(type([1,2,3]))
    if (request.method == 'POST'):
        temp = 10
        data = {'temp': temp}

    return render_template("home.html", data = data) #rendering our home.html contained within /templates



if __name__ == "__main__": 
    
    # Running flask
    app.run(debug = True, port = 4445) 