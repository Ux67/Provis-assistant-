import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from threading import Thread
import speech_recognition as sr
import pyttsx3
import time
import datetime
import os
import sys
import wikipedia
from sympy import symbols, diff, integrate, sympify, sin

# Initialize the text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Create symbolic math objects
x = symbols('x')
y = sin(x)

# Function to convert symbolic to numerical
f = np.vectorize(lambda val: y.subs(x, val).evalf())

# Numerical values for plotting
x_vals = np.linspace(0, 2 * np.pi, 100)
y_vals = f(x_vals)

def SpeakText(command):  
        
    # Initialize the engine  
    engine = pyttsx3.init()  
    engine.say(command)   
    engine.runAndWait()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to handle speech input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except Exception as e:
            speak(f"An error occurred: {str(e)}")
            return ""

# Main assistant functions
def get_time():
    return time.strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

def search(query):
    try:
        summary = wikipedia.summary(query, sentences=3)
        speak(summary)
        return summary
    except wikipedia.exceptions.DisambiguationError:
        speak("Your query is ambiguous. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No page found for your query.")
    except Exception as e:
        speak(f"An error occurred: {str(e)}")

def math_assistant(expression):
    print("Welcome to the Math Assistant!")
    print("I can help you with:")
    print("1. Basic arithmetic operations: +, -, *, /")
    print("2. Derivatives: 'derivative(expression, variable)'")
    print("3. Integrals: 'integral(expression, variable)'")
    print("Type 'exit' to quit.")
    speak('i can solve basic maths problem and deraivaties')
    
    x, y = symbols('x y')  # Define symbols for advanced operations

    while True:
        speak('enter a math problem or command or type exit to exit')
        user_input = input("\nEnter a math problem or command: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            speak('goodbye')
            break
        try:
            if user_input.startswith("derivative"):
                # Parse the expression for derivative
                parts = user_input[len("derivative("):-1].split(',')
                expression = sympify(parts[0].strip())
                variable = symbols(parts[1].strip())
                result = diff(expression, variable)
            elif user_input.startswith("integral"):
                # Parse the expression for integral
                parts = user_input[len("integral("):-1].split(',')
                expression = sympify(parts[0].strip())
                variable = symbols(parts[1].strip())
                result = integrate(expression, variable)
            else:
                # Evaluate basic arithmetic operations
                result = eval(user_input)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}. Please enter a valid input.")
            speak('an error occured not a valid input')
    
def integrate_expression(query):
    """Integrate a mathematical expression."""
    try:
        x = symbols('x')
        # Example: "integrate x^3 + 2*x"
        expression = query.replace("integrate", "").strip()
        integral = integrate(eval(expression), x)
        return f"The integral of the expression is: {integral} + C"
    except Exception as e:
        return "I couldn't integrate the expression. Ensure the syntax is correct, e.g., 'integrate x^3 + 2*x'."


def open_application(app_name):
    try:
        if "notepad" in app_name:
            os.system("notepad")
        elif "calculator" in app_name:
            os.system("calc")
        elif "youtube" in app_name:
            os.system("start https://www.youtube.com")
        elif "gmail" in app_name:
            os.system("start https://www.gmail.com")
        elif "browser" in app_name:
            os.system("start https://www.google.com")
        else:
            speak("Sorry, I cannot open that application.")
    except Exception as e:
        speak(f"An error occurred: {str(e)}")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    os.system(f"start {url}")
    speak(f"Here are the results for {query}.")

# GUI and Animation Functions
def update_plot():
    global line, canvas
    y_vals_dynamic = np.sin(x_vals + update_plot.phase)
    line.set_ydata(y_vals_dynamic)
    canvas.draw()
    update_plot.phase += 0.1
    root.after(100, update_plot)
update_plot.phase = 0

def handle_command():
    speak("Hello! I am Provis. How can, I help you today?")
    while True:
        command = listen()
        if not command:
            continue

        if "time" in command:
            result = f"The current time is {get_time()}."
        elif "name" in command:
            speak("My name is Provis python recreated online virtual system .")
        elif "what can you do" in command:
            speak("I can tell the time, date, open applications, search the web, solve math problems, and more.")
        elif "good morning provis" in command:
            speak("good morning")
        elif "good afternoon provis" in command:
            speak("good afternoon")
        elif "good night provis" in command:
            speak("good night")
        elif "date" in command:
            result = f"Today's date is {get_date()}."
        elif "what is" in command:
            query = command.replace("search", "").strip()
            result = search(query)
        elif "solve" in command:
            expression = command.replace("solve", "").strip()
            result = math_assistant(expression)
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            open_application(app_name)
            result = f"Opened {app_name}."
        elif "search" in command:
            query = command.replace("search web", "").strip()
            search_web(query)
            result = f"Searching the web for {query}."
        elif "goodbye" in command or "exit" in command:
            speak("Goodbye! Have a great day!")
            root.destroy()
            sys.exit()
        else:
            result = "I'm not sure how to help with that."
        messagebox.showinfo("Assistant", result)
        speak(result)

def start_listening():
    Thread(target=handle_command).start()

# GUI Setup
root = tk.Tk()
root.title("Provis Assistant")

# Canvas for plotting
fig = Figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(111)
line, = ax.plot(x_vals, y_vals, label="")
ax.legend()
ax.set_title("Provis Assistant")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Buttons and Labels
tk.Label(root, text="Welcome to Provis Assistant", font=("Helvetica", 16)).pack(pady=10)
tk.Button(root, text="Start Listening", command=start_listening, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="exit", command=lambda: root.destroy(), bg="red", fg="white").pack(pady=10)

# Start animation
update_plot()

# Run the GUI
root.mainloop()
