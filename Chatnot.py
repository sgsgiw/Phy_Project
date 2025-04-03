import easyocr
import cv2
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify English language

# Empty dictionary for elements
elements_dict = {
    "H": {"name": "Hydrogen", "atomic_number": 1, "symbol": "H"},
    "HE": {"name": "Helium", "atomic_number": 2, "symbol": "HE"},
    "LI": {"name": "Lithium", "atomic_number": 3, "symbol": "LI"},
    "BE": {"name": "Beryllium", "atomic_number": 4, "symbol": "BE"},
    "B": {"name": "Boron", "atomic_number": 5, "symbol": "B"},
    "C": {"name": "Carbon", "atomic_number": 6, "symbol": "C"},
    "N": {"name": "Nitrogen", "atomic_number": 7, "symbol": "N"},
    "O": {"name": "Oxygen", "atomic_number": 8, "symbol": "O"},
    "F": {"name": "Fluorine", "atomic_number": 9, "symbol": "F"},
    "NE": {"name": "Neon", "atomic_number": 10, "symbol": "NE"},
    "NA": {"name": "Sodium", "atomic_number": 11, "symbol": "NA"},
    "MG": {"name": "Magnesium", "atomic_number": 12, "symbol": "MG"},
    "AL": {"name": "Aluminum", "atomic_number": 13, "symbol": "AL"},
    "SI": {"name": "Silicon", "atomic_number": 14, "symbol": "SI"},
    "P": {"name": "Phosphorus", "atomic_number": 15, "symbol": "P"},
    "S": {"name": "Sulfur", "atomic_number": 16, "symbol": "S"},
    "CL": {"name": "Chlorine", "atomic_number": 17, "symbol": "CL"},
    "AR": {"name": "Argon", "atomic_number": 18, "symbol": "AR"},
    "K": {"name": "Potassium", "atomic_number": 19, "symbol": "K"},
    "CA": {"name": "Calcium", "atomic_number": 20, "symbol": "CA"},
    "SC": {"name": "Scandium", "atomic_number": 21, "symbol": "SC"},
    "TI": {"name": "Titanium", "atomic_number": 22, "symbol": "TI"},
    "V": {"name": "Vanadium", "atomic_number": 23, "symbol": "V"},
    "CR": {"name": "Chromium", "atomic_number": 24, "symbol": "CR"},
    "MN": {"name": "Manganese", "atomic_number": 25, "symbol": "MN"},
    "FE": {"name": "Iron", "atomic_number": 26, "symbol": "FE"},
    "CO": {"name": "Cobalt", "atomic_number": 27, "symbol": "CO"},
    "NI": {"name": "Nickel", "atomic_number": 28, "symbol": "NI"},
    "CU": {"name": "Copper", "atomic_number": 29, "symbol": "CU"},
    "ZN": {"name": "Zinc", "atomic_number": 30, "symbol": "ZN"},
    "GA": {"name": "Gallium", "atomic_number": 31, "symbol": "GA"},
    "GE": {"name": "Germanium", "atomic_number": 32, "symbol": "GE"},
    "AS": {"name": "Arsenic", "atomic_number": 33, "symbol": "AS"},
    "SE": {"name": "Selenium", "atomic_number": 34, "symbol": "SE"},
    "BR": {"name": "Bromine", "atomic_number": 35, "symbol": "BR"},
    "KR": {"name": "Krypton", "atomic_number": 36, "symbol": "KR"},
    "RB": {"name": "Rubidium", "atomic_number": 37, "symbol": "RB"},
    "SR": {"name": "Strontium", "atomic_number": 38, "symbol": "SR"},
    "Y": {"name": "Yttrium", "atomic_number": 39, "symbol": "Y"},
    "ZR": {"name": "Zirconium", "atomic_number": 40, "symbol": "ZR"},
    "NB": {"name": "Niobium", "atomic_number": 41, "symbol": "NB"},
    "MO": {"name": "Molybdenum", "atomic_number": 42, "symbol": "MO"},
    "TC": {"name": "Technetium", "atomic_number": 43, "symbol": "TC"},
    "RU": {"name": "Ruthenium", "atomic_number": 44, "symbol": "RU"},
    "RH": {"name": "Rhodium", "atomic_number": 45, "symbol": "RH"},
    "PD": {"name": "Palladium", "atomic_number": 46, "symbol": "PD"},
    "AG": {"name": "Silver", "atomic_number": 47, "symbol": "AG"},
    "CD": {"name": "Cadmium", "atomic_number": 48, "symbol": "CD"},
    "IN": {"name": "Indium", "atomic_number": 49, "symbol": "IN"},
    "SN": {"name": "Tin", "atomic_number": 50, "symbol": "SN"},
    "SB": {"name": "Antimony", "atomic_number": 51, "symbol": "SB"},
    "TE": {"name": "Tellurium", "atomic_number": 52, "symbol": "TE"},
    "I": {"name": "Iodine", "atomic_number": 53, "symbol": "I"},
    "XE": {"name": "Xenon", "atomic_number": 54, "symbol": "XE"},
    "CS": {"name": "Cesium", "atomic_number": 55, "symbol": "CS"},
    "BA": {"name": "Barium", "atomic_number": 56, "symbol": "BA"},
    "LA": {"name": "Lanthanum", "atomic_number": 57, "symbol": "LA"},
    "CE": {"name": "Cerium", "atomic_number": 58, "symbol": "CE"},
    "PR": {"name": "Praseodymium", "atomic_number": 59, "symbol": "PR"},
    "ND": {"name": "Neodymium", "atomic_number": 60, "symbol": "ND"},
    "PM": {"name": "Promethium", "atomic_number": 61, "symbol": "PM"},
    "SM": {"name": "Samarium", "atomic_number": 62, "symbol": "SM"},
    "EU": {"name": "Europium", "atomic_number": 63, "symbol": "EU"},
    "GD": {"name": "Gadolinium", "atomic_number": 64, "symbol": "GD"},
    "TB": {"name": "Terbium", "atomic_number": 65, "symbol": "TB"},
    "DY": {"name": "Dysprosium", "atomic_number": 66, "symbol": "DY"},
    "HO": {"name": "Holmium", "atomic_number": 67, "symbol": "HO"},
    "ER": {"name": "Erbium", "atomic_number": 68, "symbol": "ER"},
    "TM": {"name": "Thulium", "atomic_number": 69, "symbol": "TM"},
    "YB": {"name": "Ytterbium", "atomic_number": 70, "symbol": "YB"},
    "LU": {"name": "Lutetium", "atomic_number": 71, "symbol": "LU"},
    "HF": {"name": "Hafnium", "atomic_number": 72, "symbol": "HF"},
    "TA": {"name": "Tantalum", "atomic_number": 73, "symbol": "TA"},
    "W": {"name": "Tungsten", "atomic_number": 74, "symbol": "W"},
    "RE": {"name": "Rhenium", "atomic_number": 75, "symbol": "RE"},
    "OS": {"name": "Osmium", "atomic_number": 76, "symbol": "OS"},
    "IR": {"name": "Iridium", "atomic_number": 77, "symbol": "IR"},
    "PT": {"name": "Platinum", "atomic_number": 78, "symbol": "PT"},
    "AU": {"name": "Gold", "atomic_number": 79, "symbol": "AU"},
    "HG": {"name": "Mercury", "atomic_number": 80, "symbol": "HG"},
    "TL": {"name": "Thallium", "atomic_number": 81, "symbol": "TL"},
    "PB": {"name": "Lead", "atomic_number": 82, "symbol": "PB"},
    "BI": {"name": "Bismuth", "atomic_number": 83, "symbol": "BI"},
    "PO": {"name": "Polonium", "atomic_number": 84, "symbol": "PO"},
    "AT": {"name": "Astatine", "atomic_number": 85, "symbol": "AT"},
    "RN": {"name": "Radon", "atomic_number": 86, "symbol": "RN"},
    "FR": {"name": "Francium", "atomic_number": 87, "symbol": "FR"},
    "RA": {"name": "Radium", "atomic_number": 88, "symbol": "RA"},
    "AC": {"name": "Actinium", "atomic_number": 89, "symbol": "AC"},
    "TH": {"name": "Thorium", "atomic_number": 90, "symbol": "TH"},
    "PA": {"name": "Protactinium", "atomic_number": 91, "symbol": "PA"},
    "U": {"name": "Uranium", "atomic_number": 92, "symbol": "U"},
    "NP": {"name": "Neptunium", "atomic_number": 93, "symbol": "NP"},
    "PU": {"name": "Plutonium", "atomic_number": 94, "symbol": "PU"},
    "AM": {"name": "Americium", "atomic_number": 95, "symbol": "AM"},
    "CM": {"name": "Curium", "atomic_number": 96, "symbol": "CM"},
    "BK": {"name": "Berkelium", "atomic_number": 97, "symbol": "BK"},
    "CF": {"name": "Californium", "atomic_number": 98, "symbol": "CF"},
    "ES": {"name": "Einsteinium", "atomic_number": 99, "symbol": "ES"},
    "FM": {"name": "Fermium", "atomic_number": 100, "symbol": "FM"},
    "MD": {"name": "Mendelevium", "atomic_number": 101, "symbol": "MD"},
    "NO": {"name": "Nobelium", "atomic_number": 102, "symbol": "NO"},
    "LR": {"name": "Lawrencium", "atomic_number": 103, "symbol": "LR"},
    "RF": {"name": "Rutherfordium", "atomic_number": 104, "symbol": "RF"},
    "DB": {"name": "Dubnium", "atomic_number": 105, "symbol": "DB"},
    "SG": {"name": "Seaborgium", "atomic_number": 106, "symbol": "SG"},
    "BH": {"name": "Bohrium", "atomic_number": 107, "symbol": "BH"},
    "HS": {"name": "Hassium", "atomic_number": 108, "symbol": "HS"},
    "MT": {"name": "Meitnerium", "atomic_number": 109, "symbol": "MT"},
    "DS": {"name": "Darmstadtium", "atomic_number": 110, "symbol": "DS"},
    "RG": {"name": "Roentgenium", "atomic_number": 111, "symbol": "RG"},
    "CN": {"name": "Copernicium", "atomic_number": 112, "symbol": "CN"},
    "NH": {"name": "Nihonium", "atomic_number": 113, "symbol": "NH"},
    "FL": {"name": "Flerovium", "atomic_number": 114, "symbol": "FL"},
    "MC": {"name": "Moscovium", "atomic_number": 115, "symbol": "MC"},
    "LV": {"name": "Livermorium", "atomic_number": 116, "symbol": "LV"},
    "TS": {"name": "Tennessine", "atomic_number": 117, "symbol": "TS"},
    "OG": {"name": "Oganesson", "atomic_number": 118, "symbol": "OG"},
    "H2O": {"name": "Water", "atomic_number_if_available": 0, "symbol": "H2O"},
    "CO2": {"name": "Carbon Dioxide", "atomic_number_if_available": 0, "symbol": "CO2"},
    "NaCl": {"name": "Sodium Chloride", "atomic_number_if_available": 0, "symbol": "NaCl"},
    "CH4": {"name": "Methane", "atomic_number_if_available": 0, "symbol": "CH4"},
    "NH3": {"name": "Ammonia", "atomic_number_if_available": 0, "symbol": "NH3"},
    "H2SO4": {"name": "Sulfuric Acid", "atomic_number_if_available": 0, "symbol": "H2SO4"},
    "C6H12O6": {"name": "Glucose", "atomic_number_if_available": 0, "symbol": "C6H12O6"},
    "O2": {"name": "Oxygen Gas", "atomic_number_if_available": 0, "symbol": "O2"},
    "N2": {"name": "Nitrogen Gas", "atomic_number_if_available": 0, "symbol": "N2"},
    "HCl": {"name": "Hydrochloric Acid", "atomic_number_if_available": 0, "symbol": "HCl"},
    "CaCO3": {"name": "Calcium Carbonate", "atomic_number_if_available": 0, "symbol": "CaCO3"},
    "C2H5OH": {"name": "Ethanol", "atomic_number_if_available": 0, "symbol": "C2H5OH"},
    "HNO3": {"name": "Nitric Acid", "atomic_number_if_available": 0, "symbol": "HNO3"},
    "CaO": {"name": "Calcium Oxide", "atomic_number_if_available": 0, "symbol": "CaO"},
    "SO2": {"name": "Sulfur Dioxide", "atomic_number_if_available": 0, "symbol": "SO2"},
    "C12H22O11": {"name": "Sucrose", "atomic_number_if_available": 0, "symbol": "C12H22O11"},
    "CaCl2": {"name": "Calcium Chloride", "atomic_number_if_available": 0, "symbol": "CaCl2"},
    "KOH": {"name": "Potassium Hydroxide", "atomic_number_if_available": 0, "symbol": "KOH"},
    "Fe2O3": {"name": "Iron(III) Oxide", "atomic_number_if_available": 0, "symbol": "Fe2O3"},
    "Al2O3": {"name": "Aluminum Oxide", "atomic_number_if_available": 0, "symbol": "Al2O3"},
    "CuSO4": {"name": "Copper(II) Sulfate", "atomic_number_if_available": 0, "symbol": "CuSO4"},
    "AgNO3": {"name": "Silver Nitrate", "atomic_number_if_available": 0, "symbol": "AgNO3"},
    "H3PO4": {"name": "Phosphoric Acid", "atomic_number_if_available": 0, "symbol": "H3PO4"},
    "NaOH": {"name": "Sodium Hydroxide", "atomic_number_if_available": 0, "symbol": "NaOH"},
    "K2Cr2O7": {"name": "Potassium Dichromate", "atomic_number_if_available": 0, "symbol": "K2Cr2O7"},
    "Ca(OH)2": {"name": "Calcium Hydroxide", "atomic_number_if_available": 0, "symbol": "Ca(OH)2"},
    "MgSO4": {"name": "Magnesium Sulfate", "atomic_number_if_available": 0, "symbol": "MgSO4"},
    "NaHCO3": {"name": "Sodium Bicarbonate", "atomic_number_if_available": 0, "symbol": "NaHCO3"},
    "CH3COOH": {"name": "Acetic Acid", "atomic_number_if_available": 0, "symbol": "CH3COOH"},
    "Ca3(PO4)2": {"name": "Calcium Phosphate", "atomic_number_if_available": 0, "symbol": "Ca3(PO4)2"},
    "N2O": {"name": "Dinitrogen Monoxide", "atomic_number_if_available": 0, "symbol": "N2O"},
    "H2O2": {"name": "Hydrogen Peroxide", "atomic_number_if_available": 0, "symbol": "H2O2"},
    "C3H8": {"name": "Propane", "atomic_number_if_available": 0, "symbol": "C3H8"},
    "C4H10": {"name": "Butane", "atomic_number_if_available": 0, "symbol": "C4H10"},
    "CH3OH": {"name": "Methanol", "atomic_number_if_available": 0, "symbol": "CH3OH"},
    "C5H12": {"name": "Pentane", "atomic_number_if_available": 0, "symbol": "C5H12"},
    "C6H6": {"name": "Benzene", "atomic_number_if_available": 0, "symbol": "C6H6"},
    "C8H18": {"name": "Octane", "atomic_number_if_available": 0, "symbol": "C8H18"},
    "C10H8": {"name": "Naphthalene", "atomic_number_if_available": 0, "symbol": "C10H8"},
    "C16H34": {"name": "Hexadecane", "atomic_number_if_available": 0, "symbol": "C16H34"},
    "C18H36O2": {"name": "Stearic Acid", "atomic_number_if_available": 0, "symbol": "C18H36O2"},
    "C20H42": {"name": "Eicosane", "atomic_number_if_available": 0, "symbol": "C20H42"},
    "C2H4": {"name": "Ethylene", "atomic_number_if_available": 0, "symbol": "C2H4"},
    "C2H2": {"name": "Acetylene", "atomic_number_if_available": 0, "symbol": "C2H2"},
    "C2H6": {"name": "Ethane", "atomic_number_if_available": 0, "symbol": "C2H6"},
    "C3H6": {"name": "Cyclopropane", "atomic_number_if_available": 0, "symbol": "C3H6"},
    "C4H8": {"name": "Cyclobutane", "atomic_number_if_available": 0, "symbol": "C4H8"},
    "C5H10": {"name": "Cyclopentane", "atomic_number_if_available": 0, "symbol": "C5H10"},
    "C6H12": {"name": "Cyclohexane", "atomic_number_if_available": 0, "symbol": "C6H12"},
    "C7H14": {"name": "Heptane", "atomic_number_if_available": 0, "symbol": "C7H14"},
    "C9H8O4": {"name": "Aspirin", "atomic_number_if_available": 0, "symbol": "C9H8O4"},
    "C13H21NO2": {"name": "Ibuprofen", "atomic_number_if_available": 0, "symbol": "C13H21NO2"},
    "C17H19NO3": {"name": "Paracetamol", "atomic_number_if_available": 0, "symbol": "C17H19NO3"}
}

def capture_image_from_webcam(image_path):
    """Opens webcam, waits for user to press 'q', and captures an image."""
    cap = cv2.VideoCapture(0)  # Open default webcam

    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    print("Press 'q' to capture the image.")

    while True:
        ret, frame = cap.read()  # Read frame from webcam
        if not ret:
            print("Failed to capture frame.")
            break

        cv2.imshow("Press 'q' to Capture", frame)  # Show the live video feed

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Capture the image when 'q' is pressed
            cv2.imwrite(image_path, frame)  # Save the captured image
            print(f"Image captured and saved to {image_path}")
            break

    cap.release()
    cv2.destroyAllWindows()  # Close the webcam window
    return image_path

def extract_text_from_image(image_path):
    """Extracts text from an image using EasyOCR."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Read image with OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image at {image_path}. Check path and file integrity.")

        # Convert to grayscale for better OCR results
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use EasyOCR to extract text
        extracted_texts = reader.readtext(gray_image, detail=0)  # `detail=0` returns just the text

        if not extracted_texts:
            return "No text detected in the image."

        return " ".join(extracted_texts).strip()  # Combine all detected text
    except Exception as e:
        raise RuntimeError(f"Error during OCR processing: {e}") from e

def chat_with_gemini(prompt):
    """Chats with the Gemini AI model, handling API key and errors."""
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not found. Set it using a .env file or system settings.")

    try:
        # Configure Gemini API with the key
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')  # Best model
        response = model.generate_content(prompt)  # Request the response from Gemini AI
        return response.text.strip()  # Return the AI response without extra spaces
    except Exception as e:
        raise RuntimeError(f"Error communicating with Gemini API: {e}") from e

def get_element_details(image_path):
    """Extracts element symbol from an image and gets details from Gemini AI."""
    # Extract text (element symbol) from the image using OCR
    element_symbol = extract_text_from_image(image_path)

    if not element_symbol:
        return "No element symbol detected in the image."

    print(f"Detected Element Symbol: {element_symbol}")  # Debugging output

    # Clean up and process extracted symbol (e.g., remove extra spaces, ensure uppercase)
    element_symbol = element_symbol.strip().upper()

    # Check if the extracted symbol matches known elements
    if element_symbol in elements_dict:
        # Construct a prompt for the Gemini AI
        element_info = elements_dict[element_symbol]
        prompt = f"Please provide detailed information about: {element_info['name']}"
        try:
            # Get the detailed response from Gemini AI
            response = chat_with_gemini(prompt)
            return response
        except Exception as e:
            return f"Error while getting data from Gemini: {e}"
    else:
        return f"Element or Compound symbol '{element_symbol}' not found in the dictionary."

# Main execution block
if __name__ == "__main__":
    image_path = "captured_image.jpg"  # Default image path

    try:
        # Open webcam and wait for user to press 'q' to capture the image
        capture_image_from_webcam(image_path)

        # Get element details from the captured image
        response = get_element_details(image_path)
        print(response)  # Print the response from Gemini AI
    except Exception as e:
        print(f"Error: {e}")  # Handle any errors gracefully
