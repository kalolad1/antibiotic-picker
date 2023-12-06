# Pillanti

## What is Pillanti?
Pillanti is a website that provides antibiotic regimen recommendations for a patient with an infection. It is simple to use——all you have to do is copy and paste a patient history and physical note into the textbox on the home page. Then, a recommended regimen will be returned to the user.

## Why does Pillanti exist?
Choosing the correct antibiotic for a patient can be a difficult task. There are several factors to consider, including a patient's sex, age, allergies, type of infection, and local resistance rates. Pillanti takes the guesswork out of choosing an antibiotic and provides a canonical answer, based on the latest clinical guidelines.

## How to run locally and set up
1. Initialize the repo in your local directory.
```
git init https://github.com/kalolad1/antibiotic-picker.git
```

2. Create a virtual environment, install necessary dependencies. There is a requirements.txt file in the backend folder for Python dependencies. There is a package.json file in the frontend directory for node modules. You may have to ```cd``` into the backend and frontend directory before running these commands.
```
pip install -r requirements.txt
npm install
```

3. Start the backend and frontend server.
To start the backend server, run this command (from the backend directory)
```
python manage.py runserver
```

To start the frontend server, run this command (from the frontend directory)
```
npm run dev
```

4. If everything worked successfully, you should be able to access the website at http://localhost:3000.

## Using and Testing
The website is pretty simple to use. You should see a textbox on the home screen. The typical workflow would require a physician copy and pasting a medical note that they have already written after seeing a patient into the textbox. I've attached one of these example notes here, generated from ChatGPT, as an example. This note is fake and does not contain any real patient data. This particular example is one I've tested and is sure to work. If you want another use case to check, add the sentence "The patient has a penicillin allergy" anywhere within the patient note. You should receive a different recommendation. I have implemented the logic for one other disease, pyelonephritis, but I have not thoroughly tested it at this time. To receive a response, several pieces of information must be present in the physician's note, such as age, sex, and type of infection. In the future, I would like to create a user workflow that prompts for additional information if needed.

```
Patient Information:

Name: Jane Smith
Age: 62
Gender: Female
Chief Complaint: Abdominal pain and fever
History of Present Illness:
Mrs. Jane Smith is a 62-year-old female who presents to the hospital with a chief complaint of diffuse abdominal pain and a fever of 101.2°F (38.4°C). She has a history of cirrhosis and ascites, for which she has been managed as an outpatient. She reports the sudden onset of abdominal discomfort, which has worsened over the past 24 hours. She also notes a fever and decreased appetite.

Past Medical History:
The patient has a history of:

Cirrhosis due to alcohol abuse, diagnosed five years ago.
Ascites managed with diuretics.
Hypertension controlled with lisinopril.
Social History:
Mrs. Smith is retired and lives alone. She admits to a history of heavy alcohol use in the past but reports abstinence for the last three years. She is a non-smoker. There is no history of intravenous drug use.

Family History:
There is no significant family history of liver disease or other relevant conditions.

Review of Systems:

Constitutional: Fever, fatigue.
Gastrointestinal: Abdominal pain, decreased appetite.
Cardiovascular: No chest pain or palpitations.
Respiratory: No shortness of breath or cough.
Musculoskeletal: No joint pain or swelling.
Physical Examination:

Vital Signs: Temperature 101.2°F, heart rate 90 bpm, blood pressure 140/85 mm Hg, respiratory rate 18 breaths/min, oxygen saturation 98% on room air.
General: The patient appears fatigued but not in acute distress.
Abdominal: Mild diffuse abdominal tenderness, shifting dullness suggestive of ascites.
Cardiovascular: Regular rate and rhythm, no murmurs.
Respiratory: Clear breath sounds.
Skin: No signs of jaundice or spider angiomata.
Extremities: No edema.
Laboratory and Diagnostic Findings:

Complete Blood Count (CBC): Elevated white blood cell count (WBC).
Liver Function Tests (LFTs): Elevated liver enzymes.
Ascitic Fluid Analysis: Elevated WBC count with a predominance of neutrophils.
Blood Cultures: Pending.
Imaging:

Abdominal ultrasound showing ascites.
Assessment and Plan:
Mrs. Smith presents with clinical symptoms and laboratory findings suggestive of Spontaneous Bacterial Peritonitis (SBP). The diagnosis is supported by the elevated ascitic fluid WBC count with a neutrophilic predominance.
```

After pasting this into the textbox, you can press the large button that says "Generate Recommendations." You should then be met with a loading screen. During this time, the software is parsing what you've inputted using OpenAI APIs. It will take some time to do this processing, upwards of 30 seconds (working on minimizing this), so please keep this in mind. In some cases, a request to OpenAI will timeout and you may have to go back to the homepage and try again. This may have happened if you find yourself waiting more than 30 seconds.

After this, you should see a box containing information on the recommended antibiotic regimen. You should be given the generic name of the drug, the dosage to be given (usually in grams or milligrams), the dosing frequency, the duration of the antibiotic course, and the route of access (IV means intravenous, which is through a needle in a vein). 
