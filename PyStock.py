import base64
from io import BytesIO
from flask import Flask, request
from matplotlib.figure import Figure 
from compare_functions import compare_industry_pe

app = Flask(__name__)

@app.route("/pystock", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the word from the form submission
        word = request.form.get("word")

        # Display the word in the page
        return plot_lib(word)
    
    # Create the form input field
    text_input = """
        <form method="POST">
            <input type="text" name="word">
            <input type="submit" value="Enter">
        </form>
        """

    # Display the form input field in the page
    return text_input

def plot_lib(word):
    # Generate the figure
    fig = Figure()
    ax = fig.subplots()
    ax.bar(compare_industry_pe(word)['Ticker'], compare_industry_pe(word)['P/E'])

    # Save the figure to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Encode the figure as base64
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    # Return the figure as an image
    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == "__main__":
    app.run(port=8000)