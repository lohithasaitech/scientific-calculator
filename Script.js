// JS Logic created by Lohitha Sai
console.log("Calculator App loaded successfully - Lohitha");

// Screen element ni theeskuntunnam
let lohithaDisplay = document.getElementById("lohitha-screen");

function appendValue(val) {
    lohithaDisplay.value += val;
}

function clearScreen() {
    lohithaDisplay.value = "";
}

function calcSquareRoot() {
    try {
        let currentNum = eval(lohithaDisplay.value);
        if (currentNum >= 0) {
            lohithaDisplay.value = Math.sqrt(currentNum);
        } else {
            lohithaDisplay.value = "Error"; // minus values ki root undadu ga
        }
    } catch (err) {
        lohithaDisplay.value = "Error";
    }
}

function calculateResult() {
    try {
        // eval function use chesi string expression ni calculate chesthunnam
        let finalOutput = eval(lohithaDisplay.value);
        
        // Output format check chesthunnam (e.g., decimals ekkuva unte round off cheyadaniki)
        if (finalOutput === undefined) {
            lohithaDisplay.value = "";
        } else {
            lohithaDisplay.value = finalOutput;
        }
        
    } catch (error) {
        console.log("Lohitha, calculation lo edaina thappu undi: ", error);
        lohithaDisplay.value = "Error";
    }
}
