let display = document.getElementById("display");

function appendValue(value){
    display.value += value;
}

function clearDisplay(){
    display.value = "";
}

function deleteLast(){
    display.value = display.value.slice(0,-1);
}

function calculate(){

    try{
        display.value = eval(display.value);
    }

    catch{
        display.value = "Error";
    }
}

function squareRoot(){

    try{
        display.value = Math.sqrt(eval(display.value));
    }

    catch{
        display.value = "Error";
    }
}

function square(){

    try{
        display.value = Math.pow(eval(display.value),2);
    }

    catch{
        display.value = "Error";
    }
}
