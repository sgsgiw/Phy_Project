const fs = require('fs');
const dotenv = require('dotenv');
const cv = require('opencv4nodejs');
const Tesseract = require('tesseract.js');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Load environment variables from a .env file
dotenv.config();

// Empty dictionary for elements
const elementsDict = {
    "H": { "name": "Hydrogen", "atomic_number": 1, "symbol": "H" },
    "HE": { "name": "Helium", "atomic_number": 2, "symbol": "HE" },
    "LI": { "name": "Lithium", "atomic_number": 3, "symbol": "LI" },
    "BE": { "name": "Beryllium", "atomic_number": 4, "symbol": "BE" },
    "B": { "name": "Boron", "atomic_number": 5, "symbol": "B" },
    "C": { "name": "Carbon", "atomic_number": 6, "symbol": "C" },
    "N": { "name": "Nitrogen", "atomic_number": 7, "symbol": "N" },
    "O": { "name": "Oxygen", "atomic_number": 8, "symbol": "O" },
    "F": { "name": "Fluorine", "atomic_number": 9, "symbol": "F" },
    "NE": { "name": "Neon", "atomic_number": 10, "symbol": "NE" },
    "NA": { "name": "Sodium", "atomic_number": 11, "symbol": "NA" },
    "MG": { "name": "Magnesium", "atomic_number": 12, "symbol": "MG" },
    "AL": { "name": "Aluminum", "atomic_number": 13, "symbol": "AL" },
    "SI": { "name": "Silicon", "atomic_number": 14, "symbol": "SI" },
    "P": { "name": "Phosphorus", "atomic_number": 15, "symbol": "P" },
    "S": { "name": "Sulfur", "atomic_number": 16, "symbol": "S" },
    "CL": { "name": "Chlorine", "atomic_number": 17, "symbol": "CL" },
    "AR": { "name": "Argon", "atomic_number": 18, "symbol": "AR" },
    "K": { "name": "Potassium", "atomic_number": 19, "symbol": "K" },
    "CA": { "name": "Calcium", "atomic_number": 20, "symbol": "CA" },
    "SC": { "name": "Scandium", "atomic_number": 21, "symbol": "SC" },
    "TI": { "name": "Titanium", "atomic_number": 22, "symbol": "TI" },
    "V": { "name": "Vanadium", "atomic_number": 23, "symbol": "V" },
    "CR": { "name": "Chromium", "atomic_number": 24, "symbol": "CR" },
    "MN": { "name": "Manganese", "atomic_number": 25, "symbol": "MN" },
    "FE": { "name": "Iron", "atomic_number": 26, "symbol": "FE" },
    "CO": { "name": "Cobalt", "atomic_number": 27, "symbol": "CO" },
    "NI": { "name": "Nickel", "atomic_number": 28, "symbol": "NI" },
    "CU": { "name": "Copper", "atomic_number": 29, "symbol": "CU" },
    "ZN": { "name": "Zinc", "atomic_number": 30, "symbol": "ZN" },
    "GA": { "name": "Gallium", "atomic_number": 31, "symbol": "GA" },
    "GE": { "name": "Germanium", "atomic_number": 32, "symbol": "GE" },
    "AS": { "name": "Arsenic", "atomic_number": 33, "symbol": "AS" },
    "SE": { "name": "Selenium", "atomic_number": 34, "symbol": "SE" },
    "BR": { "name": "Bromine", "atomic_number": 35, "symbol": "BR" },
    "KR": { "name": "Krypton", "atomic_number": 36, "symbol": "KR" },
    "RB": { "name": "Rubidium", "atomic_number": 37, "symbol": "RB" },
    "SR": { "name": "Strontium", "atomic_number": 38, "symbol": "SR" },
    "Y": { "name": "Yttrium", "atomic_number": 39, "symbol": "Y" },
    "ZR": { "name": "Zirconium", "atomic_number": 40, "symbol": "ZR" },
    "NB": { "name": "Niobium", "atomic_number": 41, "symbol": "NB" },
    "MO": { "name": "Molybdenum", "atomic_number": 42, "symbol": "MO" },
    "TC": { "name": "Technetium", "atomic_number": 43, "symbol": "TC" },
    "RU": { "name": "Ruthenium", "atomic_number": 44, "symbol": "RU" },
    "RH": { "name": "Rhodium", "atomic_number": 45, "symbol": "RH" },
    "PD": { "name": "Palladium", "atomic_number": 46, "symbol": "PD" },
    "AG": { "name": "Silver", "atomic_number": 47, "symbol": "AG" },
    "CD": { "name": "Cadmium", "atomic_number": 48, "symbol": "CD" },
    "IN": { "name": "Indium", "atomic_number": 49, "symbol": "IN" },
    "SN": { "name": "Tin", "atomic_number": 50, "symbol": "SN" },
    "SB": { "name": "Antimony", "atomic_number": 51, "symbol": "SB" },
    "TE": { "name": "Tellurium", "atomic_number": 52, "symbol": "TE" },
    "I": { "name": "Iodine", "atomic_number": 53, "symbol": "I" },
    "XE": { "name": "Xenon", "atomic_number": 54, "symbol": "XE" },
    "CS": { "name": "Cesium", "atomic_number": 55, "symbol": "CS" },
    "BA": { "name": "Barium", "atomic_number": 56, "symbol": "BA" },
    "LA": { "name": "Lanthanum", "atomic_number": 57, "symbol": "LA" },
    "CE": { "name": "Cerium", "atomic_number": 58, "symbol": "CE" },
    "PR": { "name": "Praseodymium", "atomic_number": 59, "symbol": "PR" },
    "ND": { "name": "Neodymium", "atomic_number": 60, "symbol": "ND" },
    "PM": { "name": "Promethium", "atomic_number": 61, "symbol": "PM" },
    "SM": { "name": "Samarium", "atomic_number": 62, "symbol": "SM" },
    "EU": { "name": "Europium", "atomic_number": 63, "symbol": "EU" },
    "GD": { "name": "Gadolinium", "atomic_number": 64, "symbol": "GD" },
    "TB": { "name": "Terbium", "atomic_number": 65, "symbol": "TB" },
    "DY": { "name": "Dysprosium", "atomic_number": 66, "symbol": "DY" },
    "HO": { "name": "Holmium", "atomic_number": 67, "symbol": "HO" },
    "ER": { "name": "Erbium", "atomic_number": 68, "symbol": "ER" },
    "TM": { "name": "Thulium", "atomic_number": 69, "symbol": "TM" },
    "YB": { "name": "Ytterbium", "atomic_number": 70, "symbol": "YB" },
    "LU": { "name": "Lutetium", "atomic_number": 71, "symbol": "LU" },
    "HF": { "name": "Hafnium", "atomic_number": 72, "symbol": "HF" },
    "TA": { "name": "Tantalum", "atomic_number": 73, "symbol": "TA" },
    "W": { "name": "Tungsten", "atomic_number": 74, "symbol": "W" },
    "RE": { "name": "Rhenium", "atomic_number": 75, "symbol": "RE" },
    "OS": { "name": "Osmium", "atomic_number": 76, "symbol": "OS" },
    "IR": { "name": "Iridium", "atomic_number": 77, "symbol": "IR" },
    "PT": { "name": "Platinum", "atomic_number": 78, "symbol": "PT" },
    "AU": { "name": "Gold", "atomic_number": 79, "symbol": "AU" },
    "OG": { "name": "Oganesson", "atomic_number": 118, "symbol": "OG" }
};

async function captureImageFromWebcam(imagePath) {
    const cap = new cv.VideoCapture(0); // Open default webcam

    if (!cap.isOpened()) {
        throw new Error("Could not open webcam.");
    }

    console.log("Press 'q' to capture the image.");

    const frame = await new Promise((resolve) => {
        cap.readAsync((err, frame) => {
            if (err) throw new Error("Failed to capture frame.");
            resolve(frame);
        });
    });

    cv.imwriteAsync(imagePath, frame).then(() => {
        console.log(`Image captured and saved to ${imagePath}`);
    });

    cap.release();
    return imagePath;
}

async function extractTextFromImage(imagePath) {
    if (!fs.existsSync(imagePath)) {
        throw new Error(`Image file not found: ${imagePath}`);
    }

    const image = cv.imread(imagePath);
    if (image.empty) {
        throw new Error(`Could not load image at ${imagePath}. Check path and file integrity.`);
    }

    const grayImage = image.bgrToGray();
    const { data: { text } } = await Tesseract.recognize(grayImage.toString('base64'), 'eng');

    if (!text) {
        return "No text detected in the image.";
    }

    return text.trim();
}

async function chatWithGemini(prompt) {
    const apiKey = process.env.GOOGLE_API_KEY;

    if (!apiKey) {
        throw new Error("GOOGLE_API_KEY environment variable not found. Set it using a .env file or system settings.");
    }

    const genai = new GoogleGenerativeAI({ apiKey });
    const model = genai.getModel('models/gemini-1.5-pro-latest');

    try {
        const response = await model.generateContent(prompt);
        return response.text.trim();
    } catch (error) {
        throw new Error(`Error communicating with Gemini API: ${error.message}`);
    }
}

async function getElementDetails(imagePath) {
    const elementSymbol = await extractTextFromImage(imagePath);

    if (!elementSymbol) {
        return "No element symbol detected in the image.";
    }

    console.log(`Detected Element Symbol: ${elementSymbol}`);

    const cleanedSymbol = elementSymbol.trim().toUpperCase();

    if (elementsDict[cleanedSymbol]) {
        const elementInfo = elementsDict[cleanedSymbol];
        const prompt = `Please provide detailed information about the element: ${elementInfo.name}`;
        try {
            const response = await chatWithGemini(prompt);
            return response;
        } catch (error) {
            return `Error while getting data from Gemini: ${error.message}`;
        }
    } else {
        return `Element symbol '${cleanedSymbol}' not found in the dictionary.`;
    }
}

(async () => {
    const imagePath = "captured_image.jpg";

    try {
        await captureImageFromWebcam(imagePath);
        const response = await getElementDetails(imagePath);
        console.log(response);
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
})();
