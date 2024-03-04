#SpecMe: PRD - to - Backend Code Generation with human expert in the loop

"Are you a product manager, senior executive, or startup founder weary of the constant need to bother engineers for validating new product ideas? Or perhaps you're at the helm of a substantial product and engineering organization within a tech company, seeking to expedite the ideation-to-development cycle? Introducing SpecMe: SpecMe leverages RLHF concept to automate the process of transforming Product Requirement Documents (PRD) into actionable Backend Code, complete with UML diagrams and system design charts, streamlining the journey from concept to code."

The steps involved are as follows:

PRD Upload: Initiates the process by uploading a brief PRD or a product goal summary.
UML Diagram Generation: Utilizes LLM to analyze the PRD and generate a comprehensive UML diagram.
System Design Flow Charts: Produces three distinct system architecture design flowcharts based on the UML diagram with Pros and Cons explained.
Architect Select the Best Design Chart: Involves a human expert selecting the most suitable architecture based on project requirements.
Repo Structure Generation: Automatically generates a GitHub repository structure tailored to the selected design.
Sample Code Generation: Generates basic code templates for the defined architecture.
User Flow: Human 🙎 [PRD Upload] --> [UML Diagram Generation] --> [System Architecture Design Flowchart] (3 choices with Pros and Cons) --> Human 🙎 [Expert Selection] (RLHF (Futuristic))--> [GitHub Repository Structure Generation] --> [Basic Code Generation]

Installation Requirements
To set up and run this project, follow these steps:

Clone the Repository Clone this repository to your local machine using:
git clone https://github.com/sgovindgari/specme.git
Set Up a Virtual Environment (optional but recommended)
For Unix/macOS:
python3 -m venv venv
source venv/bin/activate
For Windows:
python -m venv venv
.\venv\Scripts\activate
Install Dependencies Navigate to the cloned repository's directory and install the required dependencies using:
pip install -r requirements.txt
Run the Application Start the application by running:
 streamlit run app.py
Feel free to use Sample PRD.pdf in this repo to try the product.
