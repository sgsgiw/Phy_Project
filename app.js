const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const { extractTextFromImage, chatWithGemini, elementsDict } = require('./Chatnot');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/analyze', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No image provided' });
        }

        const tempPath = req.file.path;

        try {
            const elementSymbol = await extractTextFromImage(tempPath);

            if (!elementSymbol) {
                return res.json({ error: 'No element symbol detected in the image' });
            }

            const cleanedSymbol = elementSymbol.trim().toUpperCase();

            if (elementsDict[cleanedSymbol]) {
                const elementInfo = elementsDict[cleanedSymbol];
                const prompt = `Please provide detailed information about the element: ${elementInfo.name}`;
                const response = await chatWithGemini(prompt);

                return res.json({
                    element: `${elementInfo.name} (${elementInfo.symbol})`,
                    details: response
                });
            } else {
                return res.json({ error: `Element symbol '${cleanedSymbol}' not found in our database` });
            }
        } catch (error) {
            return res.json({ error: `Error processing image: ${error.message}` });
        } finally {
            if (fs.existsSync(tempPath)) {
                fs.unlinkSync(tempPath);
            }
        }
    } catch (error) {
        return res.status(500).json({ error: `Server error: ${error.message}` });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
