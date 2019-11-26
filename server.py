from flask import Flask, request , jsonify
import RPi.GPIO as GPIO

# Mapping appliances/modules to words identifying them (in commands)
words = {"cfan" : {"fan", "ceiling"},
         "tube" : {"light", "tube", "tubelight","on"},
         "bulb" : {"bulb", "dim"}
        }

# Mapping appliances/modules to their ports 
GPIO_ports = {"tube":3,
              "cfan":4,
              "bulb":3}

GPIO.setmode(GPIO.BOARD)

def init_switches(inds):
    
    for i in inds:
        GPIO.setup(i, GPIO.OUT, initial = 0)

def switch(ind,status):
   
    print("Switching :",ind,">>",status=='on')
    GPIO.output(ind, status=='on')

def trigger(command_string):
      
    
    command_words = set(command_string.lower().split(" "))
    
    status = 'on' if 'on' in command_words else 'off'

   
    for appliance in words:
        
        if command_words.intersection(words[appliance]):
            
            port_num = GPIO_ports[appliance]
            switch(port_num,status)
            return

app = Flask(__name__)

@app.route('/prime', methods=['POST'])
def prime():
   
    cont = request.get_json()
    if cont is not None:
        trigger(command_string=cont['obj'])
    return jsonify({"SUCCESS":True})

if __name__ == '__main__':  
    print('Starting Server')
    init_switches(GPIO_ports.values())	
    app.run(debug=True,
            use_reloader=False,
            host='0.0.0.0',
            port=5000
            ) 
