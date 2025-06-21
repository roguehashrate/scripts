import strutils  # Import needed for parsing

var 
    height: float
    weight: float

echo "Please enter your height in inches: "
height = readLine(stdin).parseFloat()

echo "Please enter your weight in pounds (LBs): "
weight = readLine(stdin).parseFloat()

func calc_bmi(height: float, weight: float): float =
    return weight / (height * height) * 703.0

func bmiCat(bmi: float): string =
    if bmi < 18.5:
        "Underweight"
    elif bmi < 24.9:
        "Normal weight"
    elif bmi < 29.9:
        "Overweight"
    else:
        "Obese"

let bmi = calc_bmi(height, weight)

echo "Your BMI is: ", bmi
echo "Category: ", bmiCat(bmi)