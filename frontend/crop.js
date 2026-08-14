import sharp from 'sharp';

async function processImage() {
  try {
    const inputPath = "C:\\Users\\LENOVO\\.gemini\\antigravity\\brain\\8b1ace12-cd8f-4b85-b571-47bfdf268ed7\\.user_uploaded\\media_1786723432929.png";
    const outputPath = "e:\\TBD\\company wise dsa\\frontend\\public\\favicon.png";
    
    console.log("Processing image...");
    await sharp(inputPath)
      .trim() // removes white/transparent borders automatically
      .resize({
        width: 256,
        height: 256,
        fit: 'contain',
        background: { r: 0, g: 0, b: 0, alpha: 0 }
      })
      .toFile(outputPath);
      
    console.log("Saved cropped image to " + outputPath);
  } catch (err) {
    console.error("Error processing image:", err);
  }
}

processImage();
